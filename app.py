"""
BuildSwift AI — Mobile Studio
A professional Code-to-APK Web Engine built with Streamlit + GitHub API.
Author: Senior Full-Stack Cloud Architect
"""

import streamlit as st
import requests
import base64
import time
import json
import re
from datetime import datetime, timezone
from typing import Optional

# ──────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="BuildSwift AI · Mobile Studio",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# CUSTOM CSS  — White Professional / Mobile-first
# ──────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Google Font ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

  /* ── Root tokens ── */
  :root {
    --bg:        #F7F8FC;
    --surface:   #FFFFFF;
    --border:    #E8EAF0;
    --text:      #0D0F1A;
    --muted:     #6B7280;
    --accent:    #2563EB;
    --accent-lt: #EFF4FF;
    --success:   #16A34A;
    --warn:      #D97706;
    --danger:    #DC2626;
    --radius:    16px;
    --shadow:    0 2px 16px rgba(13,15,26,.07);
    --shadow-lg: 0 8px 40px rgba(13,15,26,.12);
  }

  /* ── Base reset ── */
  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding: 1rem 1rem 3rem !important; max-width: 680px !important; }

  /* ── Cards ── */
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
  }

  /* ── Logo / Wordmark ── */
  .wordmark {
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: var(--text);
  }
  .wordmark span { color: var(--accent); }
  .tagline {
    font-size: 0.78rem;
    color: var(--muted);
    font-weight: 500;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-top: 2px;
  }

  /* ── Section headers ── */
  .section-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.5rem;
  }

  /* ── Code editor area ── */
  .stTextArea textarea {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    line-height: 1.6 !important;
    background: #0D1117 !important;
    color: #E6EDF3 !important;
    border: 1px solid #30363D !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    caret-color: var(--accent) !important;
  }
  .stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,.15) !important;
  }

  /* ── Primary CTA button ── */
  .stButton > button {
    width: 100%;
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 1.5rem !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    transition: all .18s ease !important;
    box-shadow: 0 4px 14px rgba(37,99,235,.35) !important;
  }
  .stButton > button:hover {
    background: #1D4ED8 !important;
    box-shadow: 0 6px 20px rgba(37,99,235,.45) !important;
    transform: translateY(-1px) !important;
  }
  .stButton > button:active { transform: translateY(0) !important; }

  /* ── Download APK button ── */
  .download-btn a {
    display: block;
    width: 100%;
    background: var(--success);
    color: #fff !important;
    text-decoration: none !important;
    border-radius: 12px;
    padding: 0.85rem 1.5rem;
    font-size: 0.95rem;
    font-weight: 600;
    text-align: center;
    box-shadow: 0 4px 14px rgba(22,163,74,.35);
    transition: all .18s ease;
  }
  .download-btn a:hover {
    background: #15803D;
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(22,163,74,.45);
  }

  /* ── Status pipeline ── */
  .pipeline {
    display: flex;
    align-items: center;
    gap: 0;
    margin: 0.75rem 0;
    overflow-x: auto;
    padding-bottom: 4px;
  }
  .step {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    flex: 1;
    min-width: 72px;
  }
  .step-dot {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    transition: all .3s ease;
  }
  .step-dot.idle     { background: var(--border); color: var(--muted); }
  .step-dot.active   { background: var(--accent); color: #fff; animation: pulse 1.2s infinite; }
  .step-dot.done     { background: var(--success); color: #fff; }
  .step-dot.failed   { background: var(--danger); color: #fff; }
  .step-label {
    font-size: 0.62rem;
    font-weight: 500;
    color: var(--muted);
    text-align: center;
    white-space: nowrap;
  }
  .step-connector {
    flex: 0.4;
    height: 2px;
    background: var(--border);
    margin-bottom: 20px;
  }
  .step-connector.done { background: var(--success); }
  @keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(37,99,235,.4); }
    50%       { box-shadow: 0 0 0 8px rgba(37,99,235,.0); }
  }

  /* ── Log box ── */
  .log-box {
    background: #0D1117;
    border: 1px solid #30363D;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    color: #8B949E;
    line-height: 1.65;
    max-height: 200px;
    overflow-y: auto;
  }
  .log-box .log-ok   { color: #3FB950; }
  .log-box .log-info { color: #79C0FF; }
  .log-box .log-warn { color: #D29922; }
  .log-box .log-err  { color: #F85149; }

  /* ── Meta badge ── */
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: var(--accent-lt);
    color: var(--accent);
    border-radius: 999px;
    padding: 3px 10px;
    font-size: 0.72rem;
    font-weight: 600;
  }

  /* ── Selectboxes / inputs ── */
  .stSelectbox > div > div,
  .stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 1px solid var(--border) !important;
    font-size: 0.875rem !important;
  }

  /* ── Divider ── */
  hr { border: none; border-top: 1px solid var(--border); margin: 1rem 0; }

  /* ── Alert boxes ── */
  .stAlert { border-radius: 12px !important; }

  /* ── Expandable ── */
  .streamlit-expanderHeader { font-size: 0.85rem !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# CONSTANTS & PIPELINE STAGES
# ══════════════════════════════════════════════

PIPELINE_STAGES = [
    ("📋", "Queued"),
    ("📤", "Pushing"),
    ("⚙️", "Building"),
    ("📦", "Packaging"),
    ("✅", "Ready"),
]

POLL_INTERVAL   = 12   # seconds between GitHub API polls
MAX_POLL_CYCLES = 40   # ~8 minutes max wait


# ══════════════════════════════════════════════
# ── AI LINTER / FIXER  (plug-in interface) ──
# Swap this stub with OpenRouter / Anthropic SDK
# without touching any core build logic.
# ══════════════════════════════════════════════

class AICodeAssistant:
    """
    Plug-in interface for AI linting / auto-fixing.

    To activate:
      1. Set st.secrets["OPENROUTER_API_KEY"]
      2. Replace `lint()` body with real API call.
      3. The rest of the app calls this transparently.
    """

    def lint(self, code: str, language: str = "python") -> dict:
        """
        Analyse code and return issues + a fixed version.

        Returns:
          { "issues": [...], "fixed_code": str, "summary": str }
        """
        # ── STUB ── replace with LLM call
        return {
            "issues":     [],
            "fixed_code": code,
            "summary":    "AI linter not yet configured. Proceeding with original code.",
        }

    def explain_error(self, log_text: str) -> str:
        """Given raw build logs, return a human-readable diagnosis."""
        # ── STUB ──
        return ""


ai_assistant = AICodeAssistant()


# ══════════════════════════════════════════════
# GITHUB API HELPERS
# ══════════════════════════════════════════════

def _gh_headers() -> dict:
    token = st.secrets.get("GITHUB_TOKEN", "")
    return {
        "Authorization": f"Bearer {token}",
        "Accept":        "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def push_file_to_github(
    owner: str,
    repo:  str,
    path:  str,
    content: str,
    commit_msg: str = "BuildSwift AI: update source",
    branch: str = "main",
) -> tuple[bool, str]:
    """
    Create-or-update a single file in a GitHub repo.
    Returns (success, sha_or_error).
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    # Check if file exists (need its SHA for updates)
    existing_sha: Optional[str] = None
    r = requests.get(url, headers=_gh_headers(), params={"ref": branch})
    if r.status_code == 200:
        existing_sha = r.json().get("sha")

    encoded = base64.b64encode(content.encode()).decode()
    payload: dict = {
        "message": commit_msg,
        "content": encoded,
        "branch":  branch,
    }
    if existing_sha:
        payload["sha"] = existing_sha

    r2 = requests.put(url, headers=_gh_headers(), json=payload)
    if r2.status_code in (200, 201):
        return True, r2.json()["content"]["sha"]
    return False, r2.text


def trigger_repository_dispatch(
    owner:      str,
    repo:       str,
    event_type: str = "build-apk",
    payload:    Optional[dict] = None,
) -> bool:
    """Fire a repository_dispatch event to kick off GitHub Actions."""
    url = f"https://api.github.com/repos/{owner}/{repo}/dispatches"
    body = {"event_type": event_type, "client_payload": payload or {}}
    r = requests.post(url, headers=_gh_headers(), json=body)
    return r.status_code == 204


def get_latest_workflow_run(
    owner:       str,
    repo:        str,
    workflow_id: str = "main.yml",
    branch:      str = "main",
) -> Optional[dict]:
    """Return the most recent run object for the given workflow."""
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
    params = {"workflow_id": workflow_id, "branch": branch, "per_page": 1}
    r = requests.get(url, headers=_gh_headers(), params=params)
    if r.status_code != 200:
        return None
    runs = r.json().get("workflow_runs", [])
    return runs[0] if runs else None


def get_run_status(
    owner: str,
    repo:  str,
    run_id: int,
) -> tuple[str, str]:
    """
    Return (status, conclusion) for a run.
    status:     queued | in_progress | completed
    conclusion: success | failure | cancelled | None
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}"
    r = requests.get(url, headers=_gh_headers())
    if r.status_code != 200:
        return "unknown", "unknown"
    data = r.json()
    return data.get("status", "unknown"), data.get("conclusion") or ""


def get_artifact_download_url(
    owner:  str,
    repo:   str,
    run_id: int,
    name_filter: str = "apk",
) -> Optional[str]:
    """
    Return the archive_download_url for the first artifact whose name
    contains `name_filter`.  The user must be authenticated to use this URL.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts"
    r = requests.get(url, headers=_gh_headers())
    if r.status_code != 200:
        return None
    for art in r.json().get("artifacts", []):
        if name_filter.lower() in art["name"].lower():
            return art["archive_download_url"]
    return None


# ══════════════════════════════════════════════
# UI COMPONENTS
# ══════════════════════════════════════════════

def render_header():
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;padding:0.5rem 0 1rem;">
      <div style="width:42px;height:42px;background:#2563EB;border-radius:12px;
                  display:flex;align-items:center;justify-content:center;
                  font-size:1.3rem;box-shadow:0 4px 14px rgba(37,99,235,.35);">⚡</div>
      <div>
        <div class="wordmark">Build<span>Swift</span> AI</div>
        <div class="tagline">Mobile Studio · Code → APK Engine</div>
      </div>
    </div>
    """, unsafe_allow_html=True)


def render_pipeline(stage_idx: int, failed: bool = False):
    """
    Render the 5-step visual pipeline.
    stage_idx: index of the CURRENTLY ACTIVE step (0-based).
    """
    dots_html = ""
    for i, (icon, label) in enumerate(PIPELINE_STAGES):
        if failed and i == stage_idx:
            cls = "failed"
        elif i < stage_idx:
            cls = "done"
        elif i == stage_idx:
            cls = "active"
        else:
            cls = "idle"
        dots_html += f'<div class="step"><div class="step-dot {cls}">{icon}</div><div class="step-label">{label}</div></div>'
        if i < len(PIPELINE_STAGES) - 1:
            conn_cls = "done" if i < stage_idx else ""
            dots_html += f'<div class="step-connector {conn_cls}"></div>'

    st.markdown(f'<div class="pipeline">{dots_html}</div>', unsafe_allow_html=True)


def render_log(lines: list[str]):
    """Render a dark terminal-style log box."""
    html_lines = []
    for line in lines[-30:]:  # keep last 30 lines
        if line.startswith("✅") or "success" in line.lower() or "done" in line.lower():
            cls = "log-ok"
        elif line.startswith("ℹ") or line.startswith("→"):
            cls = "log-info"
        elif "warn" in line.lower():
            cls = "log-warn"
        elif line.startswith("✗") or "error" in line.lower() or "fail" in line.lower():
            cls = "log-err"
        else:
            cls = ""
        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        html_lines.append(f'<div class="{cls}">{safe}</div>')

    st.markdown(
        f'<div class="log-box">{"".join(html_lines)}</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════
# SESSION STATE BOOTSTRAP
# ══════════════════════════════════════════════

def _init_state():
    defaults = {
        "build_running":  False,
        "build_complete": False,
        "build_failed":   False,
        "stage_idx":      0,
        "run_id":         None,
        "apk_url":        None,
        "log_lines":      [],
        "error_msg":      "",
        "commit_sha":     "",
        "build_triggered_at": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


_init_state()


# ══════════════════════════════════════════════
# CORE BUILD ORCHESTRATOR
# ══════════════════════════════════════════════

def run_build_pipeline(
    code:         str,
    owner:        str,
    repo:         str,
    source_path:  str,
    branch:       str,
    workflow_id:  str,
    app_name:     str,
):
    """
    Full end-to-end pipeline.
    Each logical stage updates session_state so the UI re-renders live.
    """
    ss = st.session_state
    ss["log_lines"] = []
    ss["build_running"]  = True
    ss["build_complete"] = False
    ss["build_failed"]   = False
    ss["apk_url"]        = None

    def log(msg: str):
        ts = datetime.now().strftime("%H:%M:%S")
        ss["log_lines"].append(f"[{ts}] {msg}")

    # ── STAGE 0: Queued ──────────────────────
    ss["stage_idx"] = 0
    log("ℹ Build queued. Validating credentials…")

    if not st.secrets.get("GITHUB_TOKEN"):
        ss["build_failed"] = True
        ss["build_running"] = False
        ss["error_msg"] = "GITHUB_TOKEN missing from st.secrets."
        log("✗ GITHUB_TOKEN not found in secrets.")
        return

    # Optional AI lint pass
    lint_result = ai_assistant.lint(code)
    if lint_result["issues"]:
        log(f"ℹ AI Linter found {len(lint_result['issues'])} issue(s) — applying fixes.")
        code = lint_result["fixed_code"]
    else:
        log("✅ AI Linter: code looks clean.")

    # ── STAGE 1: Pushing to GitHub ───────────
    ss["stage_idx"] = 1
    log(f"→ Pushing source to {owner}/{repo}/{source_path} …")

    commit_msg = f"BuildSwift AI [{app_name}] — {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}"
    ok, result = push_file_to_github(owner, repo, source_path, code, commit_msg, branch)
    if not ok:
        ss["build_failed"]  = True
        ss["build_running"] = False
        ss["error_msg"]     = f"GitHub push failed: {result[:300]}"
        log(f"✗ Push failed: {result[:200]}")
        return

    ss["commit_sha"] = str(result)[:7]
    log(f"✅ Pushed. Commit SHA: {ss['commit_sha']}")

    # ── Fire dispatch ─────────────────────────
    log(f"→ Triggering workflow dispatch (event: build-apk) …")
    ss["build_triggered_at"] = time.time()

    fired = trigger_repository_dispatch(
        owner, repo,
        event_type="build-apk",
        payload={"app_name": app_name, "source_path": source_path, "branch": branch},
    )
    if not fired:
        ss["build_failed"]  = True
        ss["build_running"] = False
        ss["error_msg"]     = "Repository dispatch failed. Check GITHUB_TOKEN permissions (needs repo + workflow scope)."
        log("✗ Dispatch failed.")
        return

    log("✅ Dispatch event sent. Waiting for runner to pick up…")
    time.sleep(5)  # let GitHub queue the run

    # ── STAGE 2: Building ────────────────────
    ss["stage_idx"] = 2

    run_id: Optional[int] = None
    for attempt in range(12):          # up to 60 s to find the run
        run = get_latest_workflow_run(owner, repo, workflow_id, branch)
        if run and run.get("created_at"):
            triggered_at = ss["build_triggered_at"]
            run_created = datetime.fromisoformat(
                run["created_at"].replace("Z", "+00:00")
            ).timestamp()
            if run_created >= triggered_at - 15:
                run_id = run["id"]
                log(f"ℹ Workflow run #{run_id} detected.")
                break
        log(f"ℹ Waiting for run… (attempt {attempt + 1}/12)")
        time.sleep(6)

    if run_id is None:
        ss["build_failed"]  = True
        ss["build_running"] = False
        ss["error_msg"]     = "Could not locate the triggered GitHub Actions run. Check that the workflow file is on the correct branch and accepts repository_dispatch events."
        log("✗ Run not found after 72 s timeout.")
        return

    ss["run_id"] = run_id

    # ── Poll until completion ─────────────────
    for cycle in range(MAX_POLL_CYCLES):
        status, conclusion = get_run_status(owner, repo, run_id)
        log(f"ℹ Cycle {cycle + 1}: status={status}  conclusion={conclusion or '—'}")

        if status == "completed":
            if conclusion == "success":
                ss["stage_idx"] = 3   # Packaging
                log("✅ Build succeeded. Fetching artifact…")
                break
            else:
                ss["build_failed"]  = True
                ss["build_running"] = False
                ss["error_msg"]     = f"Build {conclusion}. Check the Actions tab for logs."
                log(f"✗ Build ended: {conclusion}")
                return

        # Update sub-stage label based on status
        if status == "in_progress" and ss["stage_idx"] < 3:
            ss["stage_idx"] = 2

        time.sleep(POLL_INTERVAL)

    else:
        ss["build_failed"]  = True
        ss["build_running"] = False
        ss["error_msg"]     = "Build timed out after ~8 minutes."
        log("✗ Timed out.")
        return

    # ── STAGE 3: Fetch Artifact ──────────────
    ss["stage_idx"] = 3
    apk_url = get_artifact_downlo
