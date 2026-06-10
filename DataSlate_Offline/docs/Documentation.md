# DataSlate Offline — current technical notes

## Current workflow

The active application is `DataSlate_Offline/index.html`. It contains the generator form, shared renderer, Working preview, local payload builder, and final-tab generator.

Current flow:

```text
index.html → local form state → local payload → shared renderer → new browser tab
```

`index_backup.html` and `index_test.html` are byte-synchronized copies of `index.html` used for recovery and test verification. They are not separate legacy applications.

## Language behavior

- Default language: English.
- Manual language option: Polski.
- Menu order: English, Polski.

## Runtime data

Data is loaded in a hybrid way:

1. `fetch('assets/data/data.json', { cache: 'no-store' })` for hosted/static-server usage.
2. Embedded fallback from the `embeddedDataSlateData` JSON script block for offline/local-file usage or fetch failure.

`assets/data/DataSlate_manifest.xlsx` remains the source of truth. `assets/data/data.json` and the embedded HTML data are generated browser-ready artifacts.

## Data update utility

After updating generated JSON data, run:

```bash
python3 DataSlate_Offline/tools/update_embedded_data.py
```

The utility updates the embedded data block in `index.html` and synchronizes `index_backup.html` plus `index_test.html` to the same content.

## Rendering notes

The Working preview writes `buildOfflineSlateHTML(payload)` into an iframe. The final tab uses the same `buildOfflineSlateHTML(payload)` output through `window.open()` and `document.write()`.

Small visual scale differences may occur between preview and final tab when their viewport sizes differ.

## Offline constraints

DataSlate Offline is a static generator. It does not depend on a network relay, receiver page, remote database, storage bridge, query/hash payload transfer, or audio playback. All required runtime assets are local to `DataSlate_Offline/`.

Google Fonts are optional. If the requested font family is not available in the browser, CSS fallback fonts are used.
