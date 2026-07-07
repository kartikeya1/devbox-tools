# 🧰 Devbox — Developer Utilities

A fast, zero-build, offline-friendly toolkit that bundles five everyday developer tools into a
single polished single-page app. Everything lives in one static [`index.html`](index.html) —
open it in a browser and it just works. A companion command-line JWT generator lives in
[`cli/`](cli/).

<br>

## Table of contents

- [Overview](#overview)
- [Quick start](#quick-start)
- [Tools](#tools)
  - [1. JSON Unescape & Formatter](#1-json-unescape--formatter)
  - [2. AES Encryption](#2-aes-encryption)
  - [3. cURL Formatter](#3-curl-formatter)
  - [4. HTML Previewer](#4-html-previewer)
  - [5. JWT Maker](#5-jwt-maker)
- [App features](#app-features)
- [Command-line JWT tool (`cli/`)](#command-line-jwt-tool-cli)
- [Project structure](#project-structure)
- [Architecture](#architecture)
- [Deployment](#deployment)
- [Adding a future tool](#adding-a-future-tool)
- [Tech & dependencies](#tech--dependencies)

<br>

## Overview

Devbox is a collection of small, self-contained utilities that developers reach for constantly —
cleaning up escaped JSON, encrypting/decrypting values, un-mangling copied cURL commands,
previewing HTML, and minting signed JWTs. They are combined into a single responsive interface
with a sidebar, dark/light theming, deep-linkable tabs, and one-click copy.

There is **no build step** and **no backend** — all processing happens locally in your browser.

<br>

## Quick start

Open the file directly:

```bash
open index.html          # macOS
```

Or serve it (recommended, so relative paths and the clipboard API behave consistently):

```bash
python3 -m http.server 4321
# visit http://localhost:4321
```

Each tool is deep-linkable — jump straight to one with a URL hash:

| Tool | URL |
|------|-----|
| JSON Formatter | `index.html#json` |
| AES Encryption | `index.html#aes` |
| cURL Formatter | `index.html#curl` |
| HTML Previewer | `index.html#html` |
| JWT Maker | `index.html#jwt` |

<br>

## Tools

### 1. JSON Unescape & Formatter

Turns an escaped/stringified JSON blob into clean, structured, syntax-highlighted JSON.

**What it does**
- Removes all backslashes (`\`) from the input string.
- Parses the result with `JSON.parse`.
- Pretty-prints it with 2-space indentation and colour-codes keys, strings, numbers, booleans and `null`.

**How to use**
1. Paste an escaped JSON string (e.g. `{\"name\":\"value\"}`).
2. Click **Format JSON**.
3. Use **Copy** to grab the formatted output, **Load Sample** for a demo payload, or **Clear** to reset.

Invalid JSON surfaces an inline error and a toast rather than failing silently.

<br>

### 2. AES Encryption

Encrypt and decrypt text with **AES (CBC mode, PKCS7 padding)** using a configurable key and IV.

**What it does**
- **Encrypt:** takes plain text and returns the Base64 cipher text.
- **Decrypt:** strips any stray backslashes from the cipher text, then decrypts it back to plain text.
- The **Secret Key** and **Secret IV** are editable and default to preset values; changing them updates the cipher immediately.

**How to use**
1. (Optional) Adjust the **Secret Key** / **Secret IV**.
2. Under **Encrypt**, enter plain text → **Encrypt** → copy the cipher.
3. Under **Decrypt**, paste cipher text → **Decrypt** → read the plain text.

> ⚠️ The default key/IV are baked into the client for convenience. This tool is meant for
> interoperating with existing internal payloads — it is **not** a substitute for proper key
> management. Don't treat client-side values as secret.

<br>

### 3. cURL Formatter

Un-escapes a cURL command that got mangled when copied out of logs, JSON, or a shell.

**What it does**

Converts escape sequences back into readable characters:

| Input | Output |
|-------|--------|
| `\"`  | `"`    |
| `\'`  | `'`    |
| `\\`  | `\`    |

**How to use**
1. Paste the escaped cURL command.
2. Click **Format cURL**.
3. Copy the cleaned-up command, or **Clear** to reset.

<br>

### 4. HTML Previewer

A live, side-by-side HTML editor and renderer.

**What it does**
- Renders whatever you type into a sandboxed `<iframe>` in real time — no button needed.

**How to use**
- Type or paste HTML on the left; the preview updates on the right as you type.

<br>

### 5. JWT Maker

Generate and sign **JSON Web Tokens** (HS256 / HS384 / HS512) entirely in the browser using the
**Web Crypto API** — no dependency, no network call, nothing leaves the page.

**What it does**
- **Header:** choose the signing algorithm (HS256/384/512) and token type (`typ`, default `JWT`).
- **Payload:** set the `broker` claim, an optional `iat` (issued-at; defaults to *now*) and an
  `exp` (expiration). Both `iat` and `exp` accept human-readable dates or Unix timestamps —
  see the [supported formats](#supported-date-formats).
- **Secret:** the HMAC key used to sign the token.
- **Generate** produces the token, shows its three colour-coded segments
  (`header.payload.signature`), the decoded header and payload, and the expiration in local time.
- **Run Tests** executes a built-in 12-case self-check (date parsing, HS256/384/512 signing,
  verify round-trip, invalid-signature detection, Unicode/emoji payloads) and reports pass/fail.

**How to use**
1. Pick the algorithm and fill in the payload + secret (or click **Load Sample**).
2. Click **Generate JWT** → **Copy** the token.
3. Optionally click **Run Tests** to confirm the crypto path end-to-end.

> ⚠️ The secret is used only client-side for signing. Use a key of at least 32 characters for
> HS256, never share it, and set reasonable expirations.

<br>

## App features

- 🎬 **Load Sample everywhere** — every tool ships a **Load Sample** button that fills in a working example and runs it, so anyone can see the functionality instantly.
- 🌗 **Dark / light theme** — toggled from the sidebar, remembered across visits via `localStorage`.
- 📋 **One-click copy** — every output has a copy button with toast confirmation.
- 🔗 **Deep-linkable tabs** — `#json`, `#aes`, `#curl`, `#html`, `#jwt`.
- 📱 **Responsive** — collapsible sidebar with a hamburger menu on mobile.
- ⚡ **Zero build** — a single static HTML file, works offline (except the AES tool's CDN dependency).

<br>

## Command-line JWT tool (`cli/`)

The browser JWT Maker has a sibling Python CLI in [`cli/create_jwt.py`](cli/create_jwt.py) — handy
for scripting or terminal-only workflows. It produces the same kind of token the web tool does.

### Installation

```bash
cd cli
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt   # PyJWT>=2.8.0
```

### Usage

```bash
python create_jwt.py
```

The script interactively prompts you for:

**Header** — Algorithm (`HS256`/`HS384`/`HS512`, default `HS256`) and Type (default `JWT`).
**Payload** — Broker name (required), Issued At (`iat`, defaults to current time), Expiration (`exp`, required).
**Secret** — the signing key.

### Supported date formats

Both the CLI and the web tool accept these expiration/`iat` formats:

| Format | Example |
|--------|---------|
| `YYYY-MM-DD HH:MM:SS` | `2026-12-31 23:59:59` |
| `YYYY-MM-DD` | `2026-12-31` |
| `DD/MM/YYYY HH:MM:SS` | `31/12/2026 23:59:59` |
| `DD/MM/YYYY` | `31/12/2026` |
| `YYYY/MM/DD HH:MM:SS` | `2026/12/31 23:59:59` |
| `YYYY/MM/DD` | `2026/12/31` |
| Unix timestamp | `1798741799` |

### Example session

```
==================================================
         JWT Token Generator
==================================================

[Header Configuration]
Algorithm (default: HS256):
Type (default: JWT):

[Payload Configuration]
Broker name: my-broker

Expiration date formats: YYYY-MM-DD HH:MM:SS, YYYY-MM-DD, DD/MM/YYYY, or Unix timestamp
Issued At (iat) - press Enter for current time, or provide timestamp:
Expiration (exp): 2026-12-31

[Secret]
Enter your secret key: my-super-secret-key-32chars!!!

==================================================
         Generated JWT Token
==================================================

Header: { "alg": "HS256", "typ": "JWT" }
Payload: { "broker": "my-broker", "iat": 1770820804, "exp": 1798655400 }
Expiration: 2026-12-31 00:00:00

🔑 JWT Token:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
==================================================
```

### Token structure

A JWT has three dot-separated parts: `header.payload.signature`.
- **Header** — the algorithm and token type.
- **Payload** — your claims (`broker`, `iat`, `exp`).
- **Signature** — cryptographic signature using your secret.

### Security notes

- Use a secret key of at least 32 characters for HS256.
- Never share your secret key.
- Set reasonable expiration times, and store tokens securely.

<br>

## Project structure

```
.
├── index.html          # The entire single-page app (markup, styles, logic for all 5 tools)
├── cli/
│   ├── create_jwt.py   # Command-line JWT generator (Python)
│   └── requirements.txt
├── vercel.json         # Static-hosting config
├── README.md           # This file
├── MIGRATION.md        # jwt-maker → devbox merge record + validation
└── .gitignore
```

<br>

## Architecture

The web app is a single static file organised as a small SPA:

- **Sidebar navigation** toggles one `.view` section per tool; the active view is reflected in the
  URL hash so tabs are deep-linkable and shareable.
- **Shared primitives** — `.card`, `.field`, `.btn`, `pre.output`, the `toast()` notifier and the
  `copyText()`/`highlightJSON()` helpers — are reused by every tool, so tools stay consistent and
  new ones are cheap to add.
- **Theming** is driven by CSS custom properties on `[data-theme]`, persisted in `localStorage`.
- Each tool's logic is an isolated block of vanilla JS. The JWT tool uses the browser-native
  **Web Crypto API** (`crypto.subtle`) for HMAC signing — no library required.

<br>

## Deployment

This is a static site, so hosting is trivial.

**Vercel**
1. Push the repo to GitHub.
2. In Vercel, **Import** the repo.
3. Framework preset: **Other** · Build command: *none* · Output directory: *root*.
4. Deploy. That's it.

`vercel.json` already pins `framework: null` and `outputDirectory: "."`. The Python `cli/` folder
is not part of the deployed site — it's a local developer tool.

Any static host (GitHub Pages, Netlify, S3, Cloudflare Pages) works the same way — just serve `index.html`.

<br>

## Adding a future tool

Because every tool reuses the same primitives, adding one is a four-step pattern (mirror any
existing tool, e.g. the JWT Maker):

1. **Sidebar** — add a `<button class="nav-item" data-view="mytool">` with an inline SVG icon.
2. **View** — add a `<section class="view" id="view-mytool">` built from `.card`/`.field`/`.btn`/
   `pre.output`. Give buttons `onclick` handlers and a **Load Sample** button.
3. **Logic** — add your functions in the `<script>`; reuse `toast()`, `copyText()` and
   `highlightJSON()` rather than re-implementing them.
4. **Deep link** — add `'mytool'` to the whitelist array in the deep-link check near the top of
   the script.

No build config changes are needed.

<br>

## Tech & dependencies

- **Vanilla HTML / CSS / JavaScript** — no framework, no bundler.
- **[CryptoJS 4.0.0](https://cdnjs.com/libraries/crypto-js)** (via CDN) — used solely by the AES tool.
- **Web Crypto API** (browser-native) — used by the JWT Maker; no dependency.
- **Python + [PyJWT](https://pyjwt.readthedocs.io/)** — only for the optional `cli/` tool.

All other functionality — JSON parsing/highlighting, cURL unescaping, HTML preview, theming,
clipboard — is self-contained with no third-party code.
