# ══════════════════════════════════════════════════════════════════════════════
# BuildSwift AI — Deployment Guide
# ══════════════════════════════════════════════════════════════════════════════

## File structure you need in your repo

```
your-repo/
├── app.py                          ← Streamlit front-end
├── requirements.txt
├── .github/
│   └── workflows/
│       └── main.yml                ← Buildozer CI pipeline
├── src/
│   └── main.py                     ← Default source drop-zone (auto-created on first build)
└── .streamlit/
    └── secrets.toml                ← LOCAL ONLY — never commit this file
```

---

## STEP 1 — Create the GitHub repository

1. Go to https://github.com/new
2. Create a **public** repo (name it e.g. `buildswift-studio`).
3. Clone it locally:
   ```bash
   git clone https://github.com/<YOUR_USERNAME>/buildswift-studio.git
   cd buildswift-studio
   ```
4. Copy `app.py`, `requirements.txt`, and the `.github/` folder into it.
5. Create an empty `src/` directory:
   ```bash
   mkdir -p src
   echo "# placeholder" > src/main.py
   ```
6. Commit and push:
   ```bash
   git add .
   git commit -m "Initial BuildSwift AI scaffold"
   git push origin main
   ```

---

## STEP 2 — Generate a GitHub Personal Access Token (PAT)

The app needs a token with **two scopes**:

| Scope        | Why |
|---|---|
| `repo`       | Read/write files, read Actions runs & artifacts |
| `workflow`   | Trigger `repository_dispatch` events            |

Steps:
1. Go to https://github.com/settings/tokens?type=beta  (Fine-grained tokens) **OR**
   https://github.com/settings/tokens (Classic tokens — easier for testing)
2. Click **Generate new token (classic)**
3. Set expiry → 90 days (or No expiry for permanent use)
4. Check ✅ `repo` and ✅ `workflow`
5. Click **Generate** — **copy the token now** (shown only once)

---

## STEP 3 — Local secrets file (for local testing)

Create `.streamlit/secrets.toml` in the project root:

```toml
# .streamlit/secrets.toml
# ⚠️  NEVER commit this file — add it to .gitignore

GITHUB_TOKEN       = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GITHUB_OWNER       = "your-github-username"
GITHUB_REPO        = "buildswift-studio"
GITHUB_WORKFLOW_ID = "main.yml"
```

Add to `.gitignore`:
```
.streamlit/secrets.toml
```

Test locally:
```bash
pip install streamlit requests
streamlit run app.py
```

---

## STEP 4 — Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io and sign in with GitHub.
2. Click **"New app"**.
3. Select:
   - **Repository** : `your-username/buildswift-studio`
   - **Branch**     : `main`
   - **Main file**  : `app.py`
4. Click **"Advanced settings"** → **Secrets** section.
5. Paste the following (replace values with your real credentials):

```toml
GITHUB_TOKEN       = "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
GITHUB_OWNER       = "your-github-username"
GITHUB_REPO        = "buildswift-studio"
GITHUB_WORKFLOW_ID = "main.yml"
```

6. Click **Deploy**. Streamlit Cloud will install `requirements.txt` and launch the app.
7. Your public URL will be: `https://your-app-name.streamlit.app`

---

## STEP 5 — Verify the GitHub Actions workflow

1. In your repo on GitHub, go to **Settings → Actions → General**
2. Under **Workflow permissions** → select **"Read and write permissions"** → Save.
3. Go to the **Actions** tab — you should see `BuildSwift AI — Build APK` listed.
4. To test manually: **Actions → BuildSwift AI — Build APK → Run workflow**.

---

## STEP 6 — First end-to-end build test

1. Open your Streamlit app URL.
2. Leave the default Kivy Hello-World code in the editor.
3. Click **"⚡ Build Production APK"**.
4. Watch the pipeline tracker: Queued → Pushing → Building → Packaging → Ready.
   - The first build takes **15–25 min** (Buildozer downloads Android SDK/NDK).
   - Subsequent builds use GitHub's cache and run in **5–8 min**.
5. When complete, a green **"⬇️ Download APK"** button appears.
6. Click it → GitHub will ask you to authenticate (normal for artifact downloads) → APK downloads.

---

## STEP 7 — Optional: Add a buildozer.spec to your repo

For fine-grained control (permissions, icons, orientation) add a `buildozer.spec`
to the repo root. If absent, the workflow auto-generates one from the app name.

Key fields to customise:
```ini
[app]
title         = My Awesome App
package.name  = myapp
package.domain= org.mycompany
version       = 1.0.0
requirements  = python3,kivy==2.3.0,requests
orientation   = portrait
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
```

---

## Architecture notes

```
┌─────────────────────┐     GitHub API (REST)      ┌──────────────────────┐
│   Streamlit App     │ ─── push file ──────────► │  GitHub Repository   │
│   (Streamlit Cloud) │ ─── repository_dispatch ─► │  main branch         │
│                     │                             └──────────┬───────────┘
│   Live status       │ ◄── poll /actions/runs ───────────────┘
│   tracker           │ ◄── poll /runs/{id}/artifacts
└─────────────────────┘

                                  GitHub Actions (Ubuntu 22.04)
                                  ┌───────────────────────────┐
                                  │ 1. checkout               │
                                  │ 2. install buildozer      │
                                  │ 3. buildozer android debug│
                                  │ 4. upload-artifact (APK)  │
                                  └───────────────────────────┘
```

## AI Linter plug-in (later)

To activate AI code linting, edit the `AICodeAssistant.lint()` method in `app.py`:

```python
import anthropic   # or openai / openrouter

def lint(self, code: str, language: str = "python") -> dict:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": (
                f"You are a strict {language} linter for Android/Kivy apps. "
                f"Return JSON: {{\"issues\": [...], \"fixed_code\": \"...\", \"summary\": \"...\"}}.\n\n"
                f"```{language}\n{code}\n```"
            )
        }]
    )
    return json.loads(msg.content[0].text)
```

Add `anthropic` to `requirements.txt` and `ANTHROPIC_API_KEY` to `st.secrets` — zero other changes needed.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| "GITHUB_TOKEN missing" | Check Streamlit Cloud secrets are saved and app is restarted |
| Dispatch returns 404 | Token needs `workflow` scope; repo name/owner typo |
| Run never detected | Workflow file must be on `main` branch before dispatch fires |
| Build fails at NDK step | First run — wait 25 min; NDK download is slow; cache kicks in on run 2+ |
| APK artifact not found | Workflow `upload-artifact` name must contain "apk" (it does by default) |
| Download link requires login | Normal — GitHub artifact downloads require authentication |
