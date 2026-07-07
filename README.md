# 🧰 Devbox — Developer Utilities

A fast, zero-build, offline-friendly toolkit that bundles four everyday developer tools into a single polished single-page app. Everything lives in one static [`index.html`](index.html) — open it in a browser and it just works.

<br>

## Table of contents

- [Overview](#overview)
- [Quick start](#quick-start)
- [Tools](#tools)
  - [1. JSON Unescape & Formatter](#1-json-unescape--formatter)
  - [2. AES Encryption](#2-aes-encryption)
  - [3. cURL Formatter](#3-curl-formatter)
  - [4. HTML Previewer](#4-html-previewer)
- [App features](#app-features)
- [Project structure](#project-structure)
- [Deployment](#deployment)
- [Tech & dependencies](#tech--dependencies)

<br>

## Overview

Devbox is a collection of small, self-contained utilities that developers reach for constantly — cleaning up escaped JSON, encrypting/decrypting values, un-mangling copied cURL commands, and previewing HTML. They are combined into a single responsive interface with a sidebar, dark/light theming, deep-linkable tabs, and one-click copy.

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

> ⚠️ The default key/IV are baked into the client for convenience. This tool is meant for interoperating with existing internal payloads — it is **not** a substitute for proper key management. Don't treat client-side values as secret.

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

## App features

- 🎬 **Load Sample everywhere** — every tool ships a **Load Sample** button that fills in a working example and runs it, so anyone can see the functionality instantly.
- 🌗 **Dark / light theme** — toggled from the sidebar, remembered across visits via `localStorage`.
- 📋 **One-click copy** — every output has a copy button with toast confirmation.
- 🔗 **Deep-linkable tabs** — `#json`, `#aes`, `#curl`, `#html`.
- 📱 **Responsive** — collapsible sidebar with a hamburger menu on mobile.
- ⚡ **Zero build** — a single static HTML file, works offline (except the AES tool's CDN dependency).

<br>

## Project structure

```
.
├── index.html      # The entire single-page app (markup, styles, logic)
├── README.md       # This file
└── .gitignore
```

<br>

## Deployment

This is a static site, so hosting is trivial.

**Vercel**
1. Push the repo to GitHub.
2. In Vercel, **Import** the repo.
3. Framework preset: **Other** · Build command: *none* · Output directory: *root*.
4. Deploy. That's it.

Any static host (GitHub Pages, Netlify, S3, Cloudflare Pages) works the same way — just serve `index.html`.

<br>

## Tech & dependencies

- **Vanilla HTML / CSS / JavaScript** — no framework, no bundler.
- **[CryptoJS 4.0.0](https://cdnjs.com/libraries/crypto-js)** (via CDN) — the only external dependency, used solely by the AES tool.

All other functionality — JSON parsing/highlighting, cURL unescaping, HTML preview, theming, clipboard — is self-contained with no third-party code.
