# Migration Record — jwt-maker → devbox-tools

## Summary

`jwt-maker` was merged into `devbox-tools` so that JWT generation is a **native tab** in the
Devbox single-page app rather than a separate deployment. The standalone repo is now redundant.

- **Source:** `kartikeya1/jwt-maker` @ `9cace35` ("Initial commit: JWT Maker")
- **Target:** `kartikeya1/devbox-tools` (this repo)
- **Approach:** the JWT web tool's logic was ported **verbatim** (Web Crypto API — `parseExpiration`,
  `base64urlEncode`, `getHashAlgorithm`, `createJWT`, `verifyJWT`, and all 12 self-tests) into
  `index.html` as a 5th tool. Presentation was re-skinned to Devbox's design system and its
  `toast()` / `copyText()` / `highlightJSON()` helpers (behaviour preserved, `alert()`s replaced
  with toasts). The Python CLI (`create_jwt.py`) was preserved verbatim under `cli/`.
- **History:** fresh — the commit hash above is recorded here for provenance (the original repo
  had a single "Initial commit").

### What was intentionally **not** migrated
- `jwt-maker.html` (a byte-for-byte duplicate of the deployed `index.html`) — folded into the tab.
- `.env.local` — an auto-generated **Vercel OIDC token** (a secret; gitignored). Never migrated.
- `venv/`, `__pycache__/`, `.vercel/` — local/build artifacts.

## Documentation mapping

Proof that no documentation was lost. Every section of both original READMEs now has a home.

| Original repo → section | New location in devbox-tools |
|---|---|
| **devbox README** — Overview | README → Overview (updated: 4 → 5 tools) |
| devbox README — Quick start + deep-link table | README → Quick start (added `#jwt` row) |
| devbox README — Tools 1–4 (JSON, AES, cURL, HTML) | README → Tools §1–§4 (verbatim) |
| devbox README — App features | README → App features (added `#jwt`) |
| devbox README — Project structure | README → Project structure (updated for `cli/`, `vercel.json`) |
| devbox README — Deployment | README → Deployment |
| devbox README — Tech & dependencies | README → Tech & dependencies (added Web Crypto + PyJWT) |
| **jwt-maker README** — Tool description | README → Tools §5 (JWT Maker) |
| jwt-maker README — Installation | README → Command-line JWT tool → Installation |
| jwt-maker README — Usage | README → Command-line JWT tool → Usage |
| jwt-maker README — Header/Payload/Secret config tables | README → Tools §5 + CLI Usage |
| jwt-maker README — Supported Date Formats | README → CLI → Supported date formats (table verbatim) |
| jwt-maker README — Example Session | README → CLI → Example session |
| jwt-maker README — Token Structure | README → CLI → Token structure |
| jwt-maker README — Security Notes | README → CLI → Security notes + Tools §5 callout |

**Nothing dropped.** New material added: Architecture section and an "Adding a future tool" guide.

## Validation report

| Check | Result |
|---|---|
| Build | Static site, no build step. Serves cleanly on `python3 -m http.server`. |
| All 5 tools functional | ✅ JSON, AES (encrypt+decrypt round-trip), cURL, HTML preview, JWT — each *Load Sample* verified |
| JWT self-test suite | ✅ **12 passed / 0 failed** (run in-browser via `runJWTTests()`) |
| JWT deep link (`#jwt`) | ✅ activates the JWT view on load; 5 nav items present |
| Theme toggle + persistence | ✅ unchanged |
| CLI preserved | ✅ `cli/create_jwt.py` byte-identical to source |
| Console errors | ✅ none |
| Secrets | ✅ no `.env.local`/tokens committed (gitignored) |

## Manual steps for you

1. **Deploy:** push to `origin` (existing `kartikeya1/devbox-tools`); Vercel redeploys automatically
   if the project is connected, or import once (preset **Other**, no build, output = root).
2. **Retire the old project:** delete/rename the standalone **jwt-maker** Vercel project, and
   archive the `kartikeya1/jwt-maker` GitHub repo. Exact commands are in the top-level
   consolidation report. Nothing is deleted automatically.
