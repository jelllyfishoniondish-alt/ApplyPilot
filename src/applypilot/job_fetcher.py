"""Fetch and normalize public job posting pages."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from urllib.parse import urlparse

import httpx


class JobFetchError(RuntimeError):
    """Raised when a job posting URL cannot be fetched."""


_FETCH_CACHE: dict[str, str] = {}


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
        if tag in {"p", "br", "li", "div", "section", "article", "h1", "h2", "h3"}:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1
        if tag in {"p", "li", "div", "section", "article"}:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            text = data.strip()
            if text:
                self._chunks.append(text)

    def text(self) -> str:
        return _normalize_text(" ".join(self._chunks))


def fetch_job_description(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise JobFetchError("Job URL must start with http:// or https://.")

    cache_key = url.strip()
    if cache_key in _FETCH_CACHE:
        return _FETCH_CACHE[cache_key]

    try:
        response = httpx.get(
            url,
            follow_redirects=True,
            timeout=4,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 ApplyPilot/0.1 "
                    "(job application analysis; +https://localhost)"
                )
            },
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise JobFetchError(f"Could not fetch job URL: {exc}") from exc

    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type and "text/plain" not in content_type:
        raise JobFetchError("Job URL did not return a readable HTML or text page.")

    if "text/plain" in content_type:
        text = _normalize_text(response.text)
    else:
        parser = _TextExtractor()
        parser.feed(response.text)
        text = parser.text()

    if len(text) < 80:
        raise JobFetchError("Job URL did not contain enough readable job text.")

    normalized = text[:5000]
    _FETCH_CACHE[cache_key] = normalized
    return normalized


def _normalize_text(text: str) -> str:
    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)
