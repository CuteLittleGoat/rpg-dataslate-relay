# Niebieska ramka — note for DataSlate Offline maintainers

This file documents the blue-frame asset family used by DataSlate Offline.

## Current offline workflow

- The active application is `DataSlate_Offline/index.html`.
- Background/frame metadata is consumed from `assets/data/data.json` and from the embedded fallback data in the synchronized HTML files.
- The source spreadsheet remains `assets/data/DataSlate_manifest.xlsx`.
- After data changes, refresh generated artifacts with `python3 DataSlate_Offline/tools/update_embedded_data.py` after regenerating `data.json` from the manifest in the project workflow.

## Checklist when adding or changing a background/frame

1. Add local image assets below `DataSlate_Offline/assets/`.
2. Update the source manifest.
3. Regenerate `assets/data/data.json` from the manifest.
4. Run `python3 DataSlate_Offline/tools/update_embedded_data.py` to refresh embedded data and synchronize `index_backup.html` plus `index_test.html`.
5. Verify `index.html` in a browser: background, frame alignment, logo, filler text, message text, colors, and generated tab.
