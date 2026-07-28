# Roadmap & Pending Work — devbox-tools

What this repo is: a zero-build static developer toolkit — one 1,074-line `index.html` with all CSS
and JS inline, plus `favicon.svg` and a `vercel.json` with no build step. Five tools, all
implemented and wired: JSON formatter, AES encryption, cURL unescaper, live HTML previewer, JWT
maker (`data-view="json|aes|curl|html|jwt"`, `index.html:365-381`). A small Python CLI lives in
`cli/create_jwt.py` (130 lines, PyJWT).

This is the most *complete* repo in the portfolio relative to its scope — small, finished and
honestly documented. The items below are genuinely optional except Phase 0.

Phases are meant to be executed in order — P0 → P5. Within a phase, items are independent.
The numbering is shared across all of Kartikeya's repos: **P0** stop the bleeding · **P1** tests/CI ·
**P2** truth in docs · **P3** polish · **P4** features · **P5** decision-gated.

_Last verified against the tree: 2026-07-29 · working tree clean, level with `origin/main` · 4 commits._

---

## Phase 0 — Stop the bleeding

### 0.1 — Finish the jwt-maker retirement

`MIGRATION.md:60-66` lists two manual steps and notes "Nothing is deleted automatically". Current
state, verified today:

- [x] **The GitHub repo is gone.** `kartikeya1/jwt-maker` no longer resolves — so this step is further along than `MIGRATION.md` records (it was deleted or renamed, not merely archived). Update `MIGRATION.md` so the next reader isn't hunting for it.
- [ ] **The standalone jwt-maker Vercel project** — status unknown from here; needs a dashboard check. If it's still live it serves a superseded copy of the JWT tool at a URL you may still have shared.
- [ ] **A stale local clone remains** at `~/workspace/jwt-maker`, with `origin` still pointing at the now-deleted `github.com/kartikeya1/jwt-maker.git`. It can never push or fetch again. Delete it — it is dead weight that will confuse a future search for "where is the JWT code".

---

## Phase 1 — Safety net (tests + CI)

The repo has real tests. They just never run unless a human clicks a button.

- [ ] **Make the 12 JWT self-tests run automatically.** `jwtTestCases` (`index.html:1012`) holds 12 cases, executed by `runJWTTests()` (`:1051`) only via the **Run Tests** button (`:596`). Cheapest high-value win here: a CI workflow that loads the page in headless Chrome, calls `runJWTTests()`, and fails the build on a non-zero fail count. The assertions already exist — only the trigger is missing.
- [ ] **The other four tools have no tests at all.** `MIGRATION.md` records them as hand-verified via "Load Sample". Worth adding cases in the same `jwtTestCases` shape, ordered by how silently each can break:
  1. **AES** — depends on a CDN library and a key/IV pair; an encrypt→decrypt round-trip test would catch both the CDN vanishing and a key-handling regression.
  2. **cURL unescaper** — pure string transformation, trivially testable, easy to break on an unusual quoting form.
  3. **JSON formatter** — needs malformed-input cases more than happy-path ones.
  4. **HTML previewer** — hardest to assert meaningfully; lowest priority.
- [ ] There is no `.github/` directory at all today.

---

## Phase 2 — Truth in docs

- [ ] **Two JWT implementations, one set of tests.** `cli/create_jwt.py` reimplements the JWT logic in Python via PyJWT alongside the browser's Web Crypto path — two sources of truth for expiry parsing and claim defaults, with the 12 tests covering only the browser side. Either test the Python path too, or document in the README that the CLI is a convenience copy that can drift.
- [ ] **The README's "offline-friendly" framing is not quite true** — see Phase 3's CDN item. One line of qualification fixes it.
- [ ] Update `MIGRATION.md` per 0.1 above, so its manual-steps list reflects what's actually done.

---

## Phase 3 — Polish

- [ ] **CryptoJS 4.0.0 loads from cdnjs** (`index.html:9`) with **no SRI hash**. Two consequences: the AES tool silently breaks offline (contradicting the README's offline-friendly claim), and a compromised CDN would execute arbitrary script on a page where users paste data they want encrypted. Vendoring the file locally fixes both and costs nothing — this is the highest-value item in this phase.
- [ ] **Accessibility is one attribute deep.** `index.html` has exactly **1** `aria-` attribute in 1,074 lines (`aria-label="Menu"`, `:349`). The five tool tabs are plain `<button data-view=…>` with no `role="tab"` / `aria-selected` / `aria-controls`, results areas have no `aria-live`, and nothing manages focus when the view switches — so a screen-reader or keyboard user gets no signal that the page changed.
- [ ] **No global error handler.** Five `try`/`catch` blocks surface toasts (`:670`, `:675`, `:701`, `:736`, `:993`); anything failing outside them fails silently. A `window.onerror` + `unhandledrejection` pair routed into the existing `toast()` would cover the rest for a few lines.
- [ ] No meta description, no Open Graph tags, no `robots.txt`. Reasonable for a private-use utility; a gap only if you want it discoverable.

---

## Phase 4 — Features

`README.md:315` documents a clean 4-step recipe for adding a tool (sidebar button → view section →
logic reusing `toast()` / `copyText()` / `highlightJSON()` → add the slug to the deep-link whitelist
at `index.html:662`) but names **no candidates**, so the recipe has no subject. Candidates — all
genuinely optional, pick by what you actually reach for:

- [ ] **Timestamp / epoch converter** — the most common companion to a JWT tool (`iat`/`exp` are epochs, and you currently have to leave the page to read them). Best fit by a distance.
- [ ] **Base64 encode/decode** — already half-present inside the JWT logic; exposing it is nearly free.
- [ ] **UUID / ULID generator** — trivial, and pairs with the existing key/IV fields.
- [ ] **Diff viewer** (text or JSON) — the one tool here that would need real UI work rather than a text box.
- [ ] **URL parser / query-string editor** — natural sibling to the cURL unescaper.
- [ ] **Hash generator** (MD5/SHA-1/SHA-256) — CryptoJS is already loaded, so this is a thin wrapper; do it after the vendoring in Phase 3, not before.

---

## Phase 5 — Decision-gated

- [ ] **The hardcoded AES key and IV.** `index.html:438` ships `value="7fb9cd483db64577c28e17da1e74d20d"` and `:442` ships `value="66542e0ca20dbbdf"` as prefilled defaults on a publicly deployed page. The README **does** disclose this ("the default key/IV are baked into the client… not a substitute for proper key management"), so it's a documented tradeoff rather than a silent bug. The question is whether these are arbitrary demo values or real internal-shaped ones. Options:
  - **Keep** — if they're throwaway values and the convenience of a prefilled field is the point.
  - **Blank the fields with a "generate random" button** — keeps the tool usable, removes the shipped constants. Recommended if there's any doubt about their origin.
  - **Keep but relabel** the fields as demo values, so nobody assumes they're safe.
- [ ] **Is the Python CLI worth keeping?** It duplicates the browser JWT logic (Phase 2) and adds a `requirements.txt`/venv surface to an otherwise zero-dependency repo. Keeping it is fine — but it should be a decision, not an inheritance from the jwt-maker merge.

---

## Verified non-issues (do not re-investigate)

- **No TODO / FIXME / HACK / XXX / "coming soon" markers** anywhere in `index.html`, `README.md` or `cli/create_jwt.py`. The only "future" string is the README's own §"Adding a future tool" heading.
- **All five tools are implemented and reachable** — the deep-link whitelist at `index.html:662` matches the five `data-view` buttons exactly, with no orphans in either direction.
- **`.gitignore` correctly blocks `.env`, `.env.*`, `venv/` and `__pycache__`.** `MIGRATION.md` records that a Vercel OIDC token leak was avoided during the merge. No secrets are committed.
- `MIGRATION.md` is a **sealed historical record** of the jwt-maker merge, not a backlog — its only live content is the manual-steps list now tracked in Phase 0. Don't add new items to it.
