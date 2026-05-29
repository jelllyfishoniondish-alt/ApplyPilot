const state = {
  inputMode: "url",
  lastJob: null,
  lastPlan: null,
};

const presetCatalog = {
  targetRoles: {
    label: "Target roles",
    groups: [
      ["Engineering", ["Software Engineer", "Frontend Engineer", "Backend Engineer", "Full Stack Developer", "Mobile Developer", "QA Engineer", "DevOps Engineer", "Cloud Engineer", "Site Reliability Engineer", "Security Engineer", "Embedded Software Engineer", "Solutions Engineer"]],
      ["Data & AI", ["Data Engineer", "Data Analyst", "Business Intelligence Analyst", "Machine Learning Engineer", "AI Engineer", "Research Assistant", "Analytics Engineer", "MLOps Engineer", "Data Scientist", "Quantitative Analyst", "NLP Engineer", "Computer Vision Engineer"]],
      ["Product & Design", ["Product Manager", "Associate Product Manager", "Product Analyst", "UX Researcher", "UX/UI Designer", "Product Designer", "Product Marketing Manager", "Growth Product Manager", "Technical Product Manager"]],
      ["Business", ["Business Analyst", "Strategy Analyst", "Consultant", "Operations Associate", "Project Coordinator", "Program Manager", "Supply Chain Analyst", "Procurement Analyst", "Customer Success Manager", "Partnerships Associate"]],
      ["Marketing & Sales", ["Marketing Associate", "Growth Marketing Associate", "Content Marketing Specialist", "CRM Specialist", "Sales Development Representative", "Account Executive", "Brand Strategist", "Community Manager", "Performance Marketing Analyst"]],
      ["Finance & Admin", ["Finance Analyst", "Accounting Analyst", "Investment Analyst", "Risk Analyst", "HR Associate", "Recruiting Coordinator", "Legal Assistant", "Administrative Assistant", "Compliance Analyst"]],
    ],
  },
  coreSkills: {
    label: "Core skills",
    groups: [
      ["Technical", ["Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript", "Go", "Rust", "SQL", "APIs", "REST APIs", "GraphQL", "Data Structures", "Algorithms", "System Design", "Testing", "Debugging", "Object-oriented programming", "Microservices"]],
      ["Data & AI", ["Data Analysis", "Machine Learning", "Deep Learning", "Data Visualization", "ETL", "ELT", "Data Modeling", "Statistics", "A/B Testing", "Prompt Engineering", "RAG", "NLP", "Computer Vision", "Feature Engineering", "Model Evaluation", "Time Series Analysis", "Data Cleaning"]],
      ["Business", ["Market Research", "Competitive Analysis", "Financial Modeling", "Business Strategy", "Process Improvement", "Requirements Gathering", "KPI Reporting", "Market Sizing", "Benchmarking", "Cost Analysis", "Forecasting", "Business Case Development"]],
      ["Product", ["User Research", "Roadmapping", "PRD Writing", "Prioritization", "Stakeholder Communication", "Product Analytics", "Experiment Design", "User Journey Mapping", "Backlog Management", "Go-to-market Strategy"]],
      ["Marketing", ["Campaign Planning", "Copywriting", "SEO", "SEM", "CRM", "Social Media", "Email Marketing", "Brand Positioning", "Lead Generation", "Content Strategy", "Community Management", "Influencer Marketing"]],
      ["General", ["Project Coordination", "Presentation", "Problem Solving", "Cross-functional Collaboration", "Customer Communication", "Documentation", "Research Synthesis", "Public Speaking", "Negotiation", "Event Organization", "Team Leadership"]],
    ],
  },
  tools: {
    label: "Tools",
    groups: [
      ["Engineering", ["Git", "GitHub", "GitLab", "Docker", "Kubernetes", "Postman", "Linux", "Bash", "CI/CD", "Jenkins", "GitHub Actions", "Jira", "VS Code", "IntelliJ IDEA", "PyCharm", "Terraform", "Ansible"]],
      ["Data", ["Excel", "Google Sheets", "Tableau", "Power BI", "Looker", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch", "Spark", "Airflow", "dbt", "Databricks", "Jupyter Notebook"]],
      ["Cloud & DB", ["Google Cloud", "Vertex AI", "Azure", "AWS", "MongoDB", "PostgreSQL", "MySQL", "SQLite", "Redis", "BigQuery", "Snowflake", "Oracle", "SQL Server", "Firebase"]],
      ["Product & Design", ["Figma", "Miro", "Notion", "Confluence", "Amplitude", "Mixpanel", "Google Analytics", "Hotjar", "Linear", "Trello", "Asana"]],
      ["Business & Marketing", ["PowerPoint", "Canva", "Salesforce", "HubSpot", "Mailchimp", "Google Ads", "Meta Ads", "LinkedIn Ads", "Shopify", "WordPress", "Hootsuite", "SEMrush"]],
    ],
  },
  domains: {
    label: "Domain interests",
    groups: [
      ["Technology", ["AI", "Generative AI", "B2B SaaS", "Cloud Computing", "Cybersecurity", "Developer Tools", "Data Platforms", "FinTech", "HealthTech", "EdTech", "Robotics", "IoT", "Telecommunications"]],
      ["Business", ["Finance", "Consulting", "E-commerce", "Retail", "Luxury", "Supply Chain", "Marketplace", "Insurance", "Banking", "Real Estate", "Mobility", "Logistics"]],
      ["Impact", ["Healthcare", "Education", "Sustainability", "Climate Tech", "Public Sector", "Nonprofit", "Energy", "Smart Cities", "Social Impact"]],
      ["Media & Consumer", ["Gaming", "Social Media", "Content", "Travel", "Hospitality", "Sports", "Entertainment", "Fashion", "Beauty", "Food & Beverage"]],
    ],
  },
  evidence: {
    label: "Evidence / achievements",
    groups: [
      ["Technical", ["Built a backend API", "Created a data pipeline", "Deployed a cloud service", "Implemented authentication", "Improved system performance", "Built an ML prediction model", "Created automated tests", "Integrated third-party APIs", "Designed a database schema", "Built a responsive web app", "Containerized an application"]],
      ["Data & Research", ["Built a dashboard", "Analyzed customer data", "Designed an A/B test", "Cleaned and modeled datasets", "Presented insights to stakeholders", "Conducted user interviews", "Created a survey", "Synthesized research findings", "Automated reporting", "Built a forecasting model"]],
      ["Business", ["Built a market research deck", "Performed competitive analysis", "Created a financial model", "Coordinated a team project", "Managed weekly reporting", "Improved an operational workflow", "Prepared executive slides", "Analyzed sales performance", "Mapped business processes", "Supported vendor coordination"]],
      ["Marketing & Product", ["Planned a marketing campaign", "Wrote user-facing copy", "Managed social media content", "Drafted product requirements", "Synthesized customer feedback", "Supported a product launch", "Created content calendar", "Optimized landing page copy", "Tracked campaign KPIs", "Prepared go-to-market materials"]],
    ],
  },
  degreeLevels: {
    label: "Degree level",
    groups: [
      ["Level", ["High school diploma", "Associate degree", "Bachelor's student", "Bachelor's degree", "Master's student", "Master's degree", "Engineering degree", "MBA", "PhD student", "PhD"]],
      ["School type", ["University", "Engineering school", "Business school", "Grande ecole", "IUT", "BTS", "Preparatory classes"]],
    ],
  },
  studyFields: {
    label: "Study field",
    groups: [
      ["Technology", ["Computer Science", "Informatique", "Software Engineering", "Data Science", "Artificial Intelligence", "Cybersecurity", "Information Systems", "Telecommunications", "Electrical Engineering"]],
      ["Business", ["Finance", "Accounting", "Management", "Marketing", "International Business", "Business Analytics", "Economics", "Strategy", "Supply Chain"]],
      ["Other fields", ["Mathematics", "Statistics", "Physics", "Design", "Communication", "Law", "Political Science", "Psychology", "Sustainability"]],
    ],
  },
  certifications: {
    label: "Certifications",
    groups: [
      ["Cloud & Tech", ["Google Cloud certification", "AWS certification", "Microsoft Azure certification", "MongoDB certification", "Cisco certification", "Kubernetes certification", "Databricks certification"]],
      ["Data & Business", ["Tableau certification", "Power BI certification", "Google Analytics certification", "HubSpot certification", "Salesforce certification", "Bloomberg Market Concepts"]],
      ["Project & Language", ["Scrum certification", "PMP certification", "TOEIC", "TOEFL", "IELTS", "DELF", "DALF", "HSK"]],
    ],
  },
  constraints: {
    label: "Constraints",
    groups: [
      ["Work type", ["Internship", "Apprenticeship", "Full-time", "Part-time", "Remote", "Hybrid", "On-site"]],
      ["Availability", ["Available immediately", "Summer internship", "6-month internship", "End-of-study internship", "Start date flexible"]],
      ["Language & authorization", ["English", "French", "Chinese", "Visa-aware", "Requires sponsorship", "EU work authorization"]],
    ],
  },
  // locations is handled by the cascading locationTree picker below
};

// ---------------------------------------------------------------------------
// Location tree — Country → Province/Region → City
// ---------------------------------------------------------------------------
const locationTree = {
  France: {
    "Ile-de-France":              ["Paris", "La Défense", "Boulogne-Billancourt", "Nanterre", "Saint-Denis", "Versailles"],
    "Auvergne-Rhône-Alpes":       ["Lyon", "Grenoble"],
    "Occitanie":                  ["Toulouse", "Montpellier"],
    "Nouvelle-Aquitaine":         ["Bordeaux"],
    "Hauts-de-France":            ["Lille"],
    "Provence-Alpes-Côte d'Azur": ["Marseille", "Nice", "Sophia Antipolis"],
    "Bretagne":                   ["Rennes"],
    "Pays de la Loire":           ["Nantes"],
    "Grand Est":                  ["Strasbourg"],
    "Normandie":                  ["Caen", "Rouen"],
  },
  China: {
    "Beijing":   ["Beijing"],
    "Shanghai":  ["Shanghai"],
    "Guangdong": ["Shenzhen", "Guangzhou"],
    "Zhejiang":  ["Hangzhou", "Ningbo"],
    "Jiangsu":   ["Suzhou", "Nanjing"],
    "Sichuan":   ["Chengdu"],
    "Hubei":     ["Wuhan"],
    "Fujian":    ["Xiamen", "Fuzhou"],
    "Shaanxi":   ["Xi'an"],
    "Shandong":  ["Qingdao", "Jinan"],
    "Chongqing": ["Chongqing"],
    "Tianjin":   ["Tianjin"],
    "Hong Kong": ["Hong Kong"],
    "Macau":     ["Macau"],
  },
};

const knownSkills = [
  "Python",
  "MongoDB",
  "FastAPI",
  "Google Cloud",
  "Gemini",
  "Vertex AI",
  "MCP",
  "SQL",
  "PostgreSQL",
  "JavaScript",
  "TypeScript",
  "React",
  "Docker",
  "Kubernetes",
  "Machine Learning",
  "LLM",
  "API",
];

const elements = {};

document.addEventListener("DOMContentLoaded", () => {
  cacheElements();
  renderRoute();
  bindEvents();          // initialises preset fields first
  loadProfileFromStorage(); // then restores saved values + refreshes tag strips
});

function cacheElements() {
  elements.analyzeView = document.querySelector("#analyze-view");
  elements.dashboardView = document.querySelector("#dashboard-view");
  elements.urlModeButton = document.querySelector("#url-mode-button");
  elements.textModeButton = document.querySelector("#text-mode-button");
  elements.targetRolesInput = document.querySelector("#target-roles-input");
  elements.coreSkillsInput = document.querySelector("#core-skills-input");
  elements.toolsInput = document.querySelector("#tools-input");
  elements.domainsInput = document.querySelector("#domains-input");
  elements.evidenceInput = document.querySelector("#evidence-input");
  elements.degreeInput = document.querySelector("#degree-input");
  elements.studyFieldInput = document.querySelector("#study-field-input");
  elements.certificationsInput = document.querySelector("#certifications-input");
  elements.locationsInput = document.querySelector("#locations-input");
  elements.constraintsInput = document.querySelector("#constraints-input");
  elements.urlPanel = document.querySelector("#url-panel");
  elements.textPanel = document.querySelector("#text-panel");
  elements.urlInput = document.querySelector("#url-input");
  elements.jdInput = document.querySelector("#jd-input");
  elements.analyzeButton = document.querySelector("#analyze-button");
  elements.saveButton = document.querySelector("#save-button");
  elements.statusText = document.querySelector("#status-text");
  elements.emptyState = document.querySelector("#empty-state");
  elements.resultContent = document.querySelector("#result-content");
  elements.resultCompany = document.querySelector("#result-company");
  elements.resultTitle = document.querySelector("#result-title");
  elements.analysisSource = document.querySelector("#analysis-source");
  elements.fitScore = document.querySelector("#fit-score");
  elements.matchedCount = document.querySelector("#matched-count");
  elements.missingCount = document.querySelector("#missing-count");
  elements.matchedSkills = document.querySelector("#matched-skills");
  elements.missingSkills = document.querySelector("#missing-skills");
  elements.stepsList = document.querySelector("#steps-list");
  elements.jobsList           = document.querySelector("#jobs-list");
  elements.profileSaveStatus  = document.querySelector("#profile-save-status");
  elements.clearProfileBtn    = document.querySelector("#clear-profile-btn");
}

function bindEvents() {
  elements.urlModeButton.addEventListener("click", () => setInputMode("url"));
  elements.textModeButton.addEventListener("click", () => setInputMode("text"));
  document.querySelectorAll(".preset-input").forEach(initPresetField);

  // Auto-save profile whenever the user types directly into a preset input
  document.querySelectorAll(".preset-input").forEach((input) => {
    input.addEventListener("input", scheduleProfileSave);
  });

  elements.clearProfileBtn?.addEventListener("click", () => {
    if (confirm("Clear your saved profile? This cannot be undone.")) clearProfile();
  });

  elements.analyzeButton.addEventListener("click", analyzeJob);
  elements.saveButton.addEventListener("click", saveJob);
}

// ---------------------------------------------------------------------------
// Inline preset picker — each field has its own independent collapsible panel
// ---------------------------------------------------------------------------

function initPresetField(input) {
  const presetKey = input.dataset.preset;
  const isLocations = presetKey === "locations";
  const catalog = presetCatalog[presetKey];
  // Skip if no catalog and not the special locations field
  if (!isLocations && !catalog) return;
  if (input.dataset.presetInited) return;
  input.dataset.presetInited = "1";

  const label = input.closest("label");
  if (!label) return;

  // 1. Selected-tags strip
  const tagsDiv = document.createElement("div");
  tagsDiv.className = "selected-tags";
  input.insertAdjacentElement("afterend", tagsDiv);

  // 2. Toggle button
  const browseBtn = document.createElement("button");
  browseBtn.type = "button";
  browseBtn.className = "preset-browse-btn";
  browseBtn.setAttribute("aria-expanded", "false");
  browseBtn.innerHTML =
    '<span>Browse presets</span><span class="preset-arrow" aria-hidden="true">▾</span>';
  tagsDiv.insertAdjacentElement("afterend", browseBtn);

  // 3. Inline panel (position: static — multiple can be open simultaneously)
  const panel = document.createElement("div");
  panel.className = "preset-panel";
  browseBtn.insertAdjacentElement("afterend", panel);

  const openPanel = () => {
    if (isLocations) renderLocationPanel(input, panel);
    else renderPresetPanel(input);
  };

  // Toggle open / close
  browseBtn.addEventListener("click", () => {
    const isOpen = panel.classList.toggle("open");
    browseBtn.setAttribute("aria-expanded", String(isOpen));
    browseBtn.querySelector(".preset-arrow").textContent = isOpen ? "▴" : "▾";
    if (isOpen) openPanel();
  });

  // Re-filter panel chips as the user types (locations panel doesn't filter by typing)
  input.addEventListener("input", () => {
    renderSelectedTags(input);
    if (panel.classList.contains("open") && !isLocations) renderPresetPanel(input);
  });

  // Render initial selected tags
  renderSelectedTags(input);
}

/**
 * Render (or re-render) the chip grid inside the panel for `input`.
 * Called on open and on every input/selection change while the panel is open.
 */
function renderPresetPanel(input) {
  const catalog = presetCatalog[input.dataset.preset];
  if (!catalog) return;

  const panel = input.closest("label")?.querySelector(".preset-panel");
  if (!panel) return;

  // Use the last token as a filter query so typing narrows the chip list
  const query = currentToken(input.value).toLowerCase();
  const selectedSet = new Set(splitKeywords(input.value).map((v) => v.toLowerCase()));

  const groupsHtml = catalog.groups
    .map(([groupName, options]) => {
      const filtered = query
        ? options.filter((o) => o.toLowerCase().includes(query))
        : options;
      if (!filtered.length) return "";

      const chips = filtered
        .map((option) => {
          const sel = selectedSet.has(option.toLowerCase());
          return `<button type="button" class="preset-chip${sel ? " selected" : ""}" data-value="${escapeHtml(option)}">${escapeHtml(option)}</button>`;
        })
        .join("");

      return `<div class="preset-group"><h3>${escapeHtml(groupName)}</h3><div class="preset-options">${chips}</div></div>`;
    })
    .filter(Boolean)
    .join("");

  panel.innerHTML = groupsHtml || '<p class="preset-empty">No matching presets.</p>';

  // Bind chip click: toggle selected / unselected
  panel.querySelectorAll(".preset-chip").forEach((chip) => {
    chip.addEventListener("mousedown", (e) => e.preventDefault()); // keep input focus
    chip.addEventListener("click", (e) => {
      e.stopPropagation();
      const val = chip.dataset.value;
      if (chip.classList.contains("selected")) {
        removePresetValue(input, val);
      } else {
        appendPresetValue(input, val);
      }
      renderPresetPanel(input); // refresh chip states in-place
    });
  });
}

// ---------------------------------------------------------------------------
// Location cascading picker (Country → Province/Region → City)
// ---------------------------------------------------------------------------

/**
 * Renders the location panel at the correct drill level.
 * Drill state is stored on the panel element as data attributes:
 *   panel.dataset.locCountry — "" = top / "France" = inside France
 *   panel.dataset.locRegion  — "" = country level / "Ile-de-France" = inside that region
 */
function renderLocationPanel(input, panel) {
  const country = panel.dataset.locCountry || "";
  const region  = panel.dataset.locRegion  || "";
  const selectedSet = new Set(splitKeywords(input.value).map((v) => v.toLowerCase()));

  let html = "";

  if (!country) {
    // ── Level 0: choose country ──────────────────────────────────────────────
    const chips = Object.keys(locationTree)
      .map((c) => {
        const sel = selectedSet.has(c.toLowerCase());
        return `
          <div class="loc-chip-wrap">
            <button type="button" class="preset-chip loc-select${sel ? " selected" : ""}"
                    data-value="${escapeHtml(c)}">${escapeHtml(c)}</button>
            <button type="button" class="loc-drill" data-country="${escapeHtml(c)}"
                    title="Browse regions in ${escapeHtml(c)}">▸</button>
          </div>`;
      })
      .join("");
    html = `<div class="preset-group">
              <h3>Country</h3>
              <div class="preset-options">${chips}</div>
            </div>`;

  } else if (!region) {
    // ── Level 1: choose province / region ────────────────────────────────────
    const regions = locationTree[country] || {};
    const chips = Object.entries(regions)
      .map(([r, cities]) => {
        const sel = selectedSet.has(r.toLowerCase());
        const drillBtn = cities.length
          ? `<button type="button" class="loc-drill"
                     data-country="${escapeHtml(country)}" data-region="${escapeHtml(r)}"
                     title="Browse cities in ${escapeHtml(r)}">▸</button>`
          : "";
        return `
          <div class="loc-chip-wrap">
            <button type="button" class="preset-chip loc-select${sel ? " selected" : ""}${!drillBtn ? " loc-no-drill" : ""}"
                    data-value="${escapeHtml(r)}">${escapeHtml(r)}</button>
            ${drillBtn}
          </div>`;
      })
      .join("");
    html = `<div class="loc-breadcrumb">
              <button type="button" class="loc-back">← Back</button>
              <span>${escapeHtml(country)}</span>
            </div>
            <div class="preset-group">
              <h3>Province / Region</h3>
              <div class="preset-options">${chips}</div>
            </div>`;

  } else {
    // ── Level 2: choose city ─────────────────────────────────────────────────
    const cities = (locationTree[country] || {})[region] || [];
    const chips = cities
      .map((c) => {
        const sel = selectedSet.has(c.toLowerCase());
        return `<button type="button" class="preset-chip loc-select${sel ? " selected" : ""}"
                        data-value="${escapeHtml(c)}">${escapeHtml(c)}</button>`;
      })
      .join("");
    html = `<div class="loc-breadcrumb">
              <button type="button" class="loc-back" data-back="region">← ${escapeHtml(country)}</button>
              <span>/ ${escapeHtml(region)}</span>
            </div>
            <div class="preset-group">
              <h3>City</h3>
              <div class="preset-options">${chips || '<em style="color:var(--muted);font-size:12px">No cities listed</em>'}</div>
            </div>`;
  }

  panel.innerHTML = html;

  // Select chip (add / remove value)
  panel.querySelectorAll(".loc-select").forEach((chip) => {
    chip.addEventListener("mousedown", (e) => e.preventDefault());
    chip.addEventListener("click", (e) => {
      e.stopPropagation();
      const val = chip.dataset.value;
      if (chip.classList.contains("selected")) {
        removePresetValue(input, val);
      } else {
        appendPresetValue(input, val);
      }
      renderLocationPanel(input, panel); // refresh selected states
    });
  });

  // Drill down into a country or region
  panel.querySelectorAll(".loc-drill").forEach((btn) => {
    btn.addEventListener("mousedown", (e) => e.preventDefault());
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      panel.dataset.locCountry = btn.dataset.country || "";
      panel.dataset.locRegion  = btn.dataset.region  || "";
      renderLocationPanel(input, panel);
    });
  });

  // Back navigation
  const backBtn = panel.querySelector(".loc-back");
  if (backBtn) {
    backBtn.addEventListener("mousedown", (e) => e.preventDefault());
    backBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (backBtn.dataset.back === "region") {
        // City → Region level (keep country)
        panel.dataset.locRegion = "";
      } else {
        // Region → Country level
        panel.dataset.locCountry = "";
        panel.dataset.locRegion  = "";
      }
      renderLocationPanel(input, panel);
    });
  }
}

// ---------------------------------------------------------------------------
// Tag strip
// ---------------------------------------------------------------------------

function renderSelectedTags(input) {
  const tags = input.closest("label")?.querySelector(".selected-tags");
  if (!tags) return;

  const values = splitKeywords(input.value);
  tags.innerHTML = values
    .map(
      (value) =>
        `<button type="button" class="selected-tag" data-value="${escapeHtml(value)}">` +
        `<span>${escapeHtml(value)}</span><span aria-hidden="true">×</span></button>`,
    )
    .join("");

  tags.querySelectorAll(".selected-tag").forEach((tag) => {
    tag.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      removePresetValue(input, tag.dataset.value);
      // Keep panel in sync if it is open
      const panel = input.closest("label")?.querySelector(".preset-panel");
      if (panel?.classList.contains("open")) renderPresetPanel(input);
    });
  });
}

// ---------------------------------------------------------------------------
// Value helpers
// ---------------------------------------------------------------------------

function appendPresetValue(target, value) {
  if (!target || !value) return;
  const separator = target.tagName === "TEXTAREA" ? "\n" : ", ";
  const existing = splitKeywords(target.value);
  if (existing.some((item) => item.toLowerCase() === value.toLowerCase())) return;
  target.value = existing.length
    ? `${existing.join(separator)}${separator}${value}${separator}`
    : `${value}${separator}`;
  renderSelectedTags(target);
  scheduleProfileSave(); // chip click also auto-saves
}

function removePresetValue(input, value) {
  const separator = input.tagName === "TEXTAREA" ? "\n" : ", ";
  const nextValues = splitKeywords(input.value).filter(
    (item) => item.toLowerCase() !== String(value).toLowerCase(),
  );
  input.value = nextValues.length ? `${nextValues.join(separator)}${separator}` : "";
  renderSelectedTags(input);
  scheduleProfileSave(); // tag removal also auto-saves
}

function currentToken(value) {
  const parts = value.split(/[\n,;]+/);
  return parts[parts.length - 1]?.trim() || "";
}

// ---------------------------------------------------------------------------
// Profile persistence — localStorage, no server required
// ---------------------------------------------------------------------------

const PROFILE_KEY = "applypilot_profile_v1";

/** Ordered list of [elementsKey, storageKey] for all profile fields. */
const PROFILE_FIELDS = [
  ["targetRolesInput",    "targetRoles"],
  ["coreSkillsInput",     "coreSkills"],
  ["toolsInput",          "tools"],
  ["domainsInput",        "domains"],
  ["evidenceInput",       "evidence"],
  ["degreeInput",         "degree"],
  ["studyFieldInput",     "studyField"],
  ["certificationsInput", "certifications"],
  ["locationsInput",      "locations"],
  ["constraintsInput",    "constraints"],
];

let _profileSaveTimer = null;

/** Schedule a debounced localStorage save (fires 700 ms after last change). */
function scheduleProfileSave() {
  clearTimeout(_profileSaveTimer);
  _profileSaveTimer = setTimeout(() => {
    saveProfileToStorage();
    _flashProfileSaved();
  }, 700);
}

function saveProfileToStorage() {
  const data = {};
  for (const [key, storeKey] of PROFILE_FIELDS) {
    if (elements[key]) data[storeKey] = elements[key].value;
  }
  try {
    localStorage.setItem(PROFILE_KEY, JSON.stringify(data));
  } catch {}
}

function loadProfileFromStorage() {
  let data;
  try {
    const raw = localStorage.getItem(PROFILE_KEY);
    if (!raw) return;
    data = JSON.parse(raw);
  } catch { return; }

  for (const [key, storeKey] of PROFILE_FIELDS) {
    const el = elements[key];
    if (el && data[storeKey] != null) el.value = data[storeKey];
  }
  // Refresh tag strips so selected chips appear immediately
  document.querySelectorAll(".preset-input").forEach((input) => {
    renderSelectedTags(input);
  });
}

function clearProfile() {
  for (const [key] of PROFILE_FIELDS) {
    if (elements[key]) elements[key].value = "";
  }
  document.querySelectorAll(".preset-input").forEach((input) => {
    renderSelectedTags(input);
    // Close and reset any open preset panels
    const panel = input.closest("label")?.querySelector(".preset-panel");
    if (panel?.classList.contains("open")) {
      if (input.dataset.preset === "locations") renderLocationPanel(input, panel);
      else renderPresetPanel(input);
    }
  });
  try { localStorage.removeItem(PROFILE_KEY); } catch {}
}

let _flashTimer = null;
function _flashProfileSaved() {
  if (!elements.profileSaveStatus) return;
  elements.profileSaveStatus.textContent = "Saved";
  clearTimeout(_flashTimer);
  _flashTimer = setTimeout(() => {
    if (elements.profileSaveStatus) elements.profileSaveStatus.textContent = "";
  }, 2000);
}

// ---------------------------------------------------------------------------
// Input mode (URL / text)
// ---------------------------------------------------------------------------

function setInputMode(mode) {
  state.inputMode = mode;
  elements.urlModeButton.classList.toggle("active", mode === "url");
  elements.textModeButton.classList.toggle("active", mode === "text");
  elements.urlPanel.classList.toggle("hidden", mode !== "url");
  elements.textPanel.classList.toggle("hidden", mode !== "text");
  elements.saveButton.disabled = true;
  state.lastJob = null;
  setStatus("");
}

// ---------------------------------------------------------------------------
// Routing
// ---------------------------------------------------------------------------

function renderRoute() {
  const isDashboard = window.location.pathname === "/dashboard";
  elements.analyzeView.classList.toggle("hidden", isDashboard);
  elements.dashboardView.classList.toggle("hidden", !isDashboard);

  document.querySelectorAll("[data-nav]").forEach((link) => {
    link.classList.toggle("active", link.dataset.nav === (isDashboard ? "dashboard" : "analyze"));
  });

  if (isDashboard) {
    loadJobs();
  }
}

// ---------------------------------------------------------------------------
// API calls
// ---------------------------------------------------------------------------

async function analyzeJob() {
  const profile = buildCandidateProfile();
  if (!profile) return;

  const job = buildJobInput();
  if (!job) return;

  setBusy(true, state.inputMode === "url" ? "Fetching job page…" : "Analyzing…");

  try {
    const response = await fetch("/analyze-job", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile, job }),
    });

    if (!response.ok) throw new Error(`Analyze failed with ${response.status}`);

    // The endpoint returns Server-Sent Events: status events then the final result.
    const reader  = response.body.getReader();
    const decoder = new TextDecoder();
    let buf  = "";
    let plan = null;

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });

      // Split on the SSE double-newline separator
      const blocks = buf.split("\n\n");
      buf = blocks.pop() ?? ""; // keep any incomplete trailing chunk

      for (const block of blocks) {
        const line = block.trim();
        if (!line.startsWith("data: ")) continue;
        let data;
        try { data = JSON.parse(line.slice(6)); } catch { continue; }

        if (data.status === "fetching")  setStatus("Fetching job page…");
        if (data.status === "analyzing") setStatus("Sending to Gemini…");
        if (data.status === "done")      plan = data.result;
        if (data.status === "error")     throw new Error(data.message || "Server error");
      }
    }

    if (!plan) throw new Error("No result received from server.");

    state.lastJob = jobFromPlan(job, plan);
    state.lastPlan = plan;
    renderAnalysis(plan);
    elements.saveButton.disabled = false;
    setStatus(
      plan.cache_hit
        ? `Cached · ${formatSource(plan.analysis_source)}`
        : `Done · ${formatSource(plan.analysis_source)}`,
    );
  } catch (error) {
    setStatus(error.message);
  } finally {
    setBusy(false);
  }
}

const jobsCache = new Map();

async function handleStatusChange(id, newStatus) {
  const job = jobsCache.get(id) || {};
  const today = new Date().toISOString().split("T")[0];
  const updates = { status: newStatus };
  const autoDateMap = {
    applied:      "applied_date",
    interview_1:  "interview_1_date",
    interview_2:  "interview_2_date",
    offer:        "offer_date",
    rejected:     "rejected_date",
  };
  const field = autoDateMap[newStatus];
  if (field && !job[field]) updates[field] = today;
  await updateJob(id, updates);
}

async function deleteJob(id) {
  if (!confirm("Delete this job?")) return;
  try {
    const res = await fetch(`/jobs/${id}`, { method: "DELETE" });
    if (!res.ok) throw new Error(`Delete failed (${res.status})`);
    await loadJobs();
  } catch (err) {
    alert(err.message);
  }
}

async function updateJob(id, updates) {
  try {
    const res = await fetch(`/jobs/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(updates),
    });
    if (!res.ok) throw new Error(`Update failed (${res.status})`);
    await loadJobs();
  } catch (err) {
    alert(err.message);
  }
}

async function saveJob() {
  if (!state.lastJob) {
    setStatus("Analyze a JD before saving.");
    return;
  }

  setBusy(true, "Saving…");

  try {
    // Include the full analysis result so the dashboard can show fit scores.
    const payload = { ...state.lastJob, analysis: state.lastPlan || {} };
    const response = await fetch("/jobs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error(`Save failed with ${response.status}`);

    const saved = await response.json();
    elements.saveButton.disabled = true;
    const where = { mcp: "MongoDB MCP", mongodb: "MongoDB", file: "local file", memory: "memory" }[saved.storage] ?? "local";
    setStatus(`Saved to ${where}. Open Dashboard to view it.`);
  } catch (error) {
    setStatus(error.message);
  } finally {
    setBusy(false);
  }
}

async function loadJobs() {
  elements.jobsList.innerHTML = '<div class="empty-list">Loading saved jobs…</div>';

  try {
    const response = await fetch("/jobs");
    if (!response.ok) throw new Error(`Load failed with ${response.status}`);

    const body = await response.json();
    const storageLabel = { mcp: "MongoDB MCP", mongodb: "MongoDB", file: "Local file", memory: "Memory" }[body.storage] ?? body.storage;
    const heading = document.querySelector(".dashboard-heading h1");
    if (heading) heading.textContent = `Saved jobs · ${storageLabel}`;
    renderJobs(body.jobs || []);
  } catch (error) {
    elements.jobsList.innerHTML = `<div class="empty-list">${escapeHtml(error.message)}</div>`;
  }
}

// ---------------------------------------------------------------------------
// Profile / job builders
// ---------------------------------------------------------------------------

function parseJobDescription(text) {
  const lines = text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean);

  const title = findTitle(lines);
  const company = findCompany(lines);
  const requiredSkills = knownSkills.filter((skill) =>
    text.toLowerCase().includes(skill.toLowerCase()),
  );

  return {
    company,
    title,
    source_url: "",
    description: text,
    required_skills: requiredSkills.length ? requiredSkills : ["Communication", "Problem Solving"],
    nice_to_have_skills: [],
  };
}

function buildJobInput() {
  if (state.inputMode === "url") {
    const url = elements.urlInput.value.trim();
    if (!url) { setStatus("Paste a job URL first."); return null; }
    if (!/^https?:\/\/\S+$/i.test(url)) { setStatus("Use a full http:// or https:// URL."); return null; }
    return {
      company: "Unknown company",
      title: "Job posting from URL",
      source_url: url,
      description: "",
      required_skills: [],
      nice_to_have_skills: [],
    };
  }

  const jdText = elements.jdInput.value.trim();
  if (!jdText) { setStatus("Paste a JD first."); return null; }
  return parseJobDescription(jdText);
}

function buildCandidateProfile() {
  const targetRoles = splitKeywords(elements.targetRolesInput.value);
  const coreSkills = splitKeywords(elements.coreSkillsInput.value);
  const tools = splitKeywords(elements.toolsInput.value);
  const domains = splitKeywords(elements.domainsInput.value);
  const evidence = splitKeywords(elements.evidenceInput.value);
  const degreeLevels = splitKeywords(elements.degreeInput.value);
  const studyFields = splitKeywords(elements.studyFieldInput.value);
  const certifications = splitKeywords(elements.certificationsInput.value);
  const locations = splitKeywords(elements.locationsInput.value);
  const constraints = splitKeywords(elements.constraintsInput.value);

  const hasProfile = [
    targetRoles, coreSkills, tools, domains, evidence,
    degreeLevels, studyFields, certifications, locations, constraints,
  ].some((items) => items.length);

  if (!hasProfile) {
    setStatus("Add candidate profile keywords first.");
    return null;
  }

  return {
    user_id: "local-user",
    headline: targetRoles.length ? targetRoles.join(", ") : "Candidate",
    target_roles: targetRoles,
    core_skills: coreSkills,
    tools,
    evidence,
    domain_interests: domains,
    degree_levels: degreeLevels,
    study_fields: studyFields,
    certifications,
    locations,
    constraints: [...constraints, ...locations],
  };
}

// ---------------------------------------------------------------------------
// Utilities
// ---------------------------------------------------------------------------

function splitKeywords(value) {
  return value
    .split(/[\n,;]+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function findTitle(lines) {
  const labeled = lines.find((line) => /^(role|title|position)\s*:/i.test(line));
  if (labeled) return labeled.split(":").slice(1).join(":").trim() || "Untitled role";
  return lines[0]?.slice(0, 90) || "Untitled role";
}

function findCompany(lines) {
  const labeled = lines.find((line) => /^(company|organization)\s*:/i.test(line));
  if (labeled) return labeled.split(":").slice(1).join(":").trim() || "Unknown company";
  const atLine = lines.find((line) => /\s(at|@)\s/i.test(line));
  if (atLine) {
    const match = atLine.match(/\s(?:at|@)\s+(.+)$/i);
    return match?.[1]?.trim().slice(0, 70) || "Unknown company";
  }
  return "Unknown company";
}

// ---------------------------------------------------------------------------
// Render helpers
// ---------------------------------------------------------------------------

function renderAnalysis(plan) {
  elements.emptyState.classList.add("hidden");
  elements.resultContent.classList.remove("hidden");
  elements.resultCompany.textContent = plan.company;
  elements.resultTitle.textContent = plan.title;
  elements.analysisSource.textContent = formatSource(plan.analysis_source);
  elements.fitScore.textContent = plan.fit.score;
  elements.matchedCount.textContent = plan.fit.matched_skills.length;
  elements.missingCount.textContent = plan.fit.missing_skills.length;
  renderChips(elements.matchedSkills, plan.fit.matched_skills, "Matched");
  renderChips(elements.missingSkills, plan.fit.missing_skills, "Missing", "missing");
  elements.stepsList.innerHTML = plan.steps.map((step) => `<li>${escapeHtml(step)}</li>`).join("");
}

function jobFromPlan(originalJob, plan) {
  const analyzedJob = plan.job || {};
  const analyzedSkills = [
    ...(plan.fit?.matched_skills || []),
    ...(plan.fit?.missing_skills || []),
  ];
  return {
    ...originalJob,
    ...analyzedJob,
    company: plan.company || originalJob.company,
    title: plan.title || originalJob.title,
    description: analyzedJob.description || originalJob.description,
    required_skills: analyzedSkills.length
      ? Array.from(new Set(analyzedSkills))
      : analyzedJob.required_skills || originalJob.required_skills,
  };
}

function renderChips(container, items, fallback, variant = "") {
  const values = items.length ? items : [fallback];
  container.innerHTML = values
    .map((item) => `<span class="chip ${variant}">${escapeHtml(item)}</span>`)
    .join("");
}

const STATUS_OPTIONS = [
  { value: "planned",     label: "Saved" },
  { value: "applied",     label: "Applied" },
  { value: "interview_1", label: "1st Interview" },
  { value: "interview_2", label: "2nd Interview" },
  { value: "offer",       label: "Offer" },
  { value: "rejected",    label: "Rejected" },
];

const MILESTONES = [
  { field: "applied_date",     label: "Applied",       triggerStatus: "applied",     exclusive: false },
  { field: "interview_1_date", label: "1st Interview", triggerStatus: "interview_1", exclusive: false },
  { field: "interview_2_date", label: "2nd Interview", triggerStatus: "interview_2", exclusive: false },
  { field: "offer_date",       label: "Offer",         triggerStatus: "offer",       exclusive: true  },
  { field: "rejected_date",    label: "Rejected",      triggerStatus: "rejected",    exclusive: true  },
];

const STATUS_RANK = { planned: 0, applied: 1, interview_1: 2, interview_2: 3, offer: 4, rejected: 4 };

function renderTimeline(job) {
  const status     = job.status || "planned";
  const statusRank = STATUS_RANK[status] ?? 0;

  const visible = MILESTONES.filter((m) => {
    if (m.triggerStatus === "offer" || m.triggerStatus === "rejected") {
      // These two are mutually exclusive — only show the one matching current status.
      // If status is still mid-process, show whichever has a date (at most one).
      if (status === "offer" || status === "rejected") return m.triggerStatus === status;
      return !!job[m.field];
    }
    return statusRank >= (STATUS_RANK[m.triggerStatus] ?? 99) || !!job[m.field];
  });

  if (!visible.length) return "";

  return visible.map((m, i) => {
    const date    = job[m.field] || "";
    const isLast  = i === visible.length - 1;
    const nextHasDate = !isLast && !!job[visible[i + 1]?.field];

    let dotState = "pending";
    if (date)                        dotState = "done";
    else if (m.triggerStatus === status) dotState = "current";

    const isNegative = m.triggerStatus === "rejected";
    const dotClass   = `tl-dot ${dotState}${isNegative && dotState !== "pending" ? " negative" : ""}`;
    const labelClass = `tl-label${dotState === "pending" ? " pending" : ""}${isNegative ? " negative" : ""}`;
    const dateClass  = `tl-date${date ? " filled" : ""}`;

    return `
      <div class="tl-item">
        <div class="tl-col">
          <div class="${dotClass}"></div>
          ${isLast ? "" : `<div class="tl-line${nextHasDate ? " done" : ""}"></div>`}
        </div>
        <div class="tl-body${isLast ? " last" : ""}">
          <span class="${labelClass}">${m.label}</span>
          <input class="${dateClass}" type="date" value="${escapeHtml(date)}"
            onchange="updateJob('${job.id}', {'${m.field}': this.value})">
        </div>
      </div>`;
  }).join("");
}

function renderJobs(jobs) {
  if (!jobs.length) {
    elements.jobsList.innerHTML = '<div class="empty-list">No saved jobs yet.</div>';
    return;
  }

  jobsCache.clear();
  jobs.forEach((j) => jobsCache.set(j.id, j));

  elements.jobsList.innerHTML = jobs.map((job) => {
    const id       = job.id || "";
    const analysis = job.analysis || {};
    const fit      = analysis.fit || {};
    const score    = fit.score != null ? fit.score : null;
    const matched  = (fit.matched_skills || []).slice(0, 4);
    const missing  = (fit.missing_skills || []).slice(0, 3);
    const source   = analysis.analysis_source || "";
    const status   = job.status || "planned";
    const savedAt  = job.saved_at
      ? new Date(job.saved_at).toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" })
      : "";

    const scoreHtml = score !== null
      ? `<div class="score-ring score-ring-sm"><span>${score}</span><small>fit</small></div>`
      : "";

    const matchedHtml = matched.length
      ? `<div class="chip-row chip-row-sm">${matched.map((s) => `<span class="chip">${escapeHtml(s)}</span>`).join("")}</div>`
      : "";

    const missingHtml = missing.length
      ? `<div class="chip-row chip-row-sm">${missing.map((s) => `<span class="chip missing">${escapeHtml(s)}</span>`).join("")}</div>`
      : "";

    const sourceBadge = source
      ? `<span class="source-badge">${escapeHtml(formatSource(source))}</span>`
      : "";

    const statusOptions = STATUS_OPTIONS.map((opt) =>
      `<option value="${opt.value}"${status === opt.value ? " selected" : ""}>${opt.label}</option>`
    ).join("");

    const timelineHtml = renderTimeline(job);

    return `
      <article class="job-card">
        <div class="job-card-header">
          <div class="job-card-meta">
            <p class="eyebrow">${escapeHtml(job.company)}</p>
            <h2>${escapeHtml(job.title)}</h2>
            <div class="job-card-badges">
              ${sourceBadge}
              ${savedAt ? `<span class="job-date">${escapeHtml(savedAt)}</span>` : ""}
            </div>
          </div>
          ${scoreHtml}
        </div>
        ${matchedHtml}
        ${missingHtml}
        ${job.source_url
          ? `<a class="job-link" href="${escapeHtml(job.source_url)}" target="_blank" rel="noreferrer">Open posting ↗</a>`
          : ""}
        <div class="job-card-footer">
          <div class="status-row">
            <span class="status-label">Status</span>
            <select class="status-select s-${status}"
              onchange="this.className='status-select s-'+this.value; handleStatusChange('${id}', this.value)">
              ${statusOptions}
            </select>
            <button class="delete-btn" onclick="deleteJob('${id}')">Delete</button>
          </div>
          ${timelineHtml ? `<div class="timeline">${timelineHtml}</div>` : ""}
        </div>
      </article>`;
  }).join("");
}

function summary(text) {
  if (!text) return "No description saved.";
  return text.length > 140 ? `${text.slice(0, 137)}...` : text;
}

function setBusy(isBusy, label = "") {
  elements.analyzeButton.disabled = isBusy;
  if (state.lastJob) elements.saveButton.disabled = isBusy || elements.saveButton.disabled;
  if (label) setStatus(label);
}

function setStatus(message) {
  elements.statusText.textContent = message;
}

function formatSource(source) {
  return source === "gemini" ? "Gemini" : "local fallback";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
