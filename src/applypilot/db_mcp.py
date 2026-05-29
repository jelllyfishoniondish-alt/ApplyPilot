"""MongoDB MCP server client for ApplyPilot.

Wraps the mongodb-mcp-server npm package via stdio MCP protocol.
Falls back gracefully when MDB_MCP_CONNECTION_STRING is not set.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
from typing import Any

DB_NAME = "applypilot"

# Matches the security wrapper added by mongodb-mcp-server around query results.
_UNTRUSTED_RE = re.compile(
    r"<untrusted-user-data-[^>]+>\s*(.*?)\s*</untrusted-user-data-[^>]+>",
    re.DOTALL,
)


class MongoMCPClient:
    """Async wrapper around the mongodb-mcp-server subprocess."""

    def __init__(self) -> None:
        self._session: Any = None
        self._stdio_ctx: Any = None
        self._session_ctx: Any = None
        self.is_connected: bool = False

    async def start(self) -> bool:
        """Start the MCP subprocess and initialise the session. Returns True on success."""
        conn_str = os.getenv("MDB_MCP_CONNECTION_STRING", "").strip()
        if not conn_str:
            print("[ApplyPilot] MDB_MCP_CONNECTION_STRING not set; MCP disabled.")
            return False
        try:
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client

            server_params = StdioServerParameters(
                command="npx",
                args=["-y", "mongodb-mcp-server@latest"],
                env={**os.environ, "MDB_MCP_CONNECTION_STRING": conn_str},
            )
            self._stdio_ctx = stdio_client(server_params)
            read, write = await self._stdio_ctx.__aenter__()

            self._session_ctx = ClientSession(read, write)
            self._session = await self._session_ctx.__aenter__()

            await asyncio.wait_for(self._session.initialize(), timeout=15.0)
            self.is_connected = True
            print("[ApplyPilot] MongoDB MCP server connected.")
            return True
        except Exception as exc:
            print(f"[ApplyPilot] MongoDB MCP failed to start ({exc}); falling back.")
            await self.stop()
            return False

    async def stop(self) -> None:
        for ctx in (self._session_ctx, self._stdio_ctx):
            if ctx:
                try:
                    await ctx.__aexit__(None, None, None)
                except Exception:
                    pass
        self.is_connected = False
        self._session = None
        self._stdio_ctx = None
        self._session_ctx = None

    # ── internal ──────────────────────────────────────────────────────────────

    async def _call(self, tool: str, args: dict[str, Any]) -> Any:
        if not self._session:
            raise RuntimeError("MCP session not active")
        result = await self._session.call_tool(tool, args)
        if result.isError:
            msg = result.content[0].text if result.content else "MCP error"
            raise RuntimeError(msg)
        if not result.content:
            return None

        # mongodb-mcp-server wraps results in <untrusted-user-data-*> tags. The tag
        # name also appears in warning/footer text, so we iterate all matches and
        # return the first one that parses as valid JSON.
        for item in result.content:
            for m in _UNTRUSTED_RE.finditer(item.text):
                try:
                    return json.loads(m.group(1))
                except json.JSONDecodeError:
                    pass

        # Fall back to parsing the first content item as plain text / JSON.
        raw = result.content[0].text
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, AttributeError):
            return raw

    @staticmethod
    def _clean(docs: list[dict]) -> list[dict]:
        """Remove MongoDB internal _id from each document."""
        for d in docs:
            d.pop("_id", None)
        return docs

    # ── public operations ─────────────────────────────────────────────────────

    async def insert_one(self, collection: str, document: dict) -> dict:
        await self._call("insert-many", {
            "collection": collection,
            "database": DB_NAME,
            "documents": [document],
        })
        document.pop("_id", None)
        return document

    async def find(
        self,
        collection: str,
        filter: dict | None = None,
        sort: dict | None = None,
        limit: int = 500,
    ) -> list[dict]:
        args: dict[str, Any] = {
            "collection": collection,
            "database": DB_NAME,
            "limit": limit,
        }
        if filter:
            args["filter"] = filter
        if sort:
            args["sort"] = sort
        result = await self._call("find", args)
        if not isinstance(result, list):
            return []
        return self._clean(result)

    async def delete_one(self, collection: str, filter: dict) -> bool:
        result = await self._call("delete-many", {
            "collection": collection,
            "database": DB_NAME,
            "filter": filter,
        })
        if isinstance(result, str):
            m = re.search(r"Deleted\s+`?(\d+)`?", result)
            return int(m.group(1)) > 0 if m else False
        if isinstance(result, dict):
            return result.get("deletedCount", 0) > 0
        return False

    async def update_one(self, collection: str, filter: dict, update: dict) -> dict | None:
        await self._call("update-many", {
            "collection": collection,
            "database": DB_NAME,
            "filter": filter,
            "update": update,
        })
        docs = await self.find(collection, filter=filter, limit=1)
        return docs[0] if docs else None
