# Snippets folder overview

## Purpose
This folder stores reusable **Brave/Chrome DevTools snippets** that enable quick export of AI‑conversation data without leaving the browser.

## How to load a snippet in Brave DevTools
1. Open Brave and press **F12**.
2. Select the **Sources** tab.
3. In the left pane, click **Snippets**.
4. Click **+ New snippet**.
5. Paste the contents of `brave_leo_export.js` (or any other snippet).
6. Press **Ctrl + Enter** to run.

## Available snippets
- `brave_leo_export.js` – extracts Leo conversation data to JSON.

## Usage notes
- Requires Brave ≥ 145.1.87.190 (the version used in Sprint 2).
- Run the snippet on a page where Leo is active; the script writes a JSON file to the `exports/` directory.
