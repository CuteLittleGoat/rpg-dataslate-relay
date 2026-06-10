# DataSlate Offline — user guide

DataSlate Offline is a static screen generator for tabletop RPG sessions. It runs from local files, builds a local payload from the form, and opens a ready-to-capture DataSlate screen in a new browser tab.

## Active application file

- Open `DataSlate_Offline/index.html` to use the application.
- `index_backup.html` and `index_test.html` are synchronized copies kept for recovery and verification.
- Legacy GM/player receiver files are not part of the current workflow.

## Language

- The default language is **English**.
- **Polski** is available manually from the language menu.
- The language menu order is **English**, then **Polski**.

## How it works

1. Open `index.html`.
2. Choose a background, logo, font, colors, filler options, and message text.
3. Use **Working preview** to check the composition.
4. Click **Generate** / **Generuj**.
5. The browser opens a new tab containing the final DataSlate screen.
6. Capture the new tab as a screenshot or show it directly during your session.

The Working preview uses the same renderer as the generated tab. Minor scale differences can still appear because the preview iframe and the final browser tab may have different viewport sizes.

Your browser may block the generated tab as a pop-up. If that happens, allow pop-ups for the local file or hosting domain and click **Generate** / **Generuj** again.

## Running online from static hosting

You can publish the `DataSlate_Offline/` folder on any static hosting service or static web server.

Minimum requirements:

- Serve the folder as static files.
- Keep the folder structure unchanged.
- Ensure `index.html` can load `assets/data/data.json` and local assets below `assets/`.

Then open the hosted URL for `DataSlate_Offline/index.html` in a browser.

## Running offline from disk

1. Download or clone the repository.
2. Keep the `DataSlate_Offline/` folder structure unchanged.
3. Open `DataSlate_Offline/index.html` in a browser.
4. If the browser restricts local `fetch()` from `file://`, the application uses embedded fallback data stored inside the HTML file.

No network connection is required for normal use after the files are present on disk.

## No online relay, receiver, or audio

DataSlate Offline does not use Firebase or Firestore. It does not send messages to another device and it does not require a receiver screen or an online connection. The application does not use legacy **Send** / **Wyślij**, **Ping**, or audio playback controls.

## Data loading model

The application uses hybrid local data loading:

1. It first tries to fetch `assets/data/data.json`.
2. If that is unavailable, it falls back to the embedded `embeddedDataSlateData` block inside the HTML.

`assets/data/DataSlate_manifest.xlsx` remains the source of truth for the module data. The following files are generated artifacts:

- `assets/data/data.json`
- the embedded data block in `index.html`
- synchronized copies in `index_backup.html` and `index_test.html`

## Updating offline data

After changing `assets/data/DataSlate_manifest.xlsx`, regenerate the offline data artifacts used by the browser. The current synchronization utility is:

```bash
python3 DataSlate_Offline/tools/update_embedded_data.py
```

This utility refreshes the embedded data and synchronizes:

- `index.html`
- `index_backup.html`
- `index_test.html`

If your workflow also regenerates `assets/data/data.json` from the manifest, run that import step first, then run the synchronization utility above.

## Fonts

Google Fonts are not required for the application to work. Font names from the data are used as CSS font-family values; if a chosen font is not installed or available in the browser, DataSlate Offline falls back to system fonts.

## Basic troubleshooting

- **Generate does not open a new tab** — allow pop-ups for this file or site, then click **Generate** / **Generuj** again.
- **The online-hosted page has no data** — confirm that `assets/data/data.json` is served next to `index.html`; the embedded fallback still protects basic operation.
- **The offline file cannot fetch JSON** — this is expected in some browsers opened from `file://`; the embedded fallback is used.
- **Preview scale differs from the final tab** — resize the browser or final tab; the renderer is shared, but viewport size affects scaling.
- **A selected font looks different** — install the font locally or use an available fallback font.
