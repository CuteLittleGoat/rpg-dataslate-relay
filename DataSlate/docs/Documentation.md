# Technical documentation — DataSlate

DataSlate publishes GM-prepared messages to a player-facing screen. The GM panel writes the current display payload to Firestore, and the player screen listens for changes and renders the message immediately.

This is the online relay version. The offline image-generation version is documented separately in:

```text
DataSlate_Offline/docs/Documentation.md
```

---

## 1. Module purpose

DataSlate is responsible for:

- displaying narrative messages to players,
- letting the GM configure message text and visual style,
- synchronizing GM panel state to the player screen through Firestore,
- playing ping and message audio from local assets,
- rendering backgrounds, logos, text, fillers, shadow rectangles, flicker, and overlays,
- importing selectable asset data from an XLSX manifest into local JSON,
- supporting helper/test views for users who modify the module.

---

## 2. Entry points

| File | Role |
| --- | --- |
| `DataSlate/index.html` | Launcher for production and helper views, if present. |
| `DataSlate/GM.html` | Production GM control panel. |
| `DataSlate/DataSlate.html` | Production player-facing display. |
| `DataSlate/GM_test.html` | Helper GM view for testing modifications, if present. |
| `DataSlate/DataSlate_test.html` | Helper player view for testing modifications, if present. |
| `DataSlate/GM_backup.html` | Reference backup for experiments, if present. |
| `DataSlate/DataSlate_backup.html` | Reference backup for experiments, if present. |

The `_test.html` and `_backup.html` files are helper/reference files. They are not the normal production route during play.

---

## 3. Main files and assets

| Path | Purpose |
| --- | --- |
| `DataSlate/config/firebase-config.js` | Firebase Web SDK config for Firestore communication. |
| `DataSlate/assets/data/data.json` | Local selectable DataSlate data snapshot. |
| `DataSlate/assets/data/DataSlate_manifest.xlsx` | Source workbook for updating selectable data, if present. |
| `DataSlate/assets/backgrounds/` | Final background images displayed to players. |
| `DataSlate/assets/ramki/` | Technical blue-frame background variants used for safe text-area calculation, if present. |
| `DataSlate/assets/logos/` | Logo assets. |
| `DataSlate/assets/audios/` | Message and ping audio assets. |

---

## 4. Firestore communication

DataSlate uses Cloud Firestore for live communication between the GM panel and the player screen.

Current working document:

```text
dataslate/current
```

Model:

```text
dataslate (collection)
└── current (document)
```

The GM panel writes a full current-state payload. The player screen listens to the same document and rerenders when it changes.

Important implementation rule:

```text
The current document should be treated as a complete snapshot of the display state.
```

When publishing a message, the GM side should overwrite the current payload with the full state rather than relying on partial updates.

---

## 5. Firebase services

| Service | Used | Purpose |
| --- | --- | --- |
| Cloud Firestore | yes | Live GM-to-player synchronization. |
| Firebase Authentication | optional | Only needed if deployment rules require authenticated users. |
| Realtime Database | no | Not used by DataSlate. |
| Storage | no | DataSlate uses local assets, not Firebase Storage. |

Firebase setup belongs in:

```text
DataSlate/config/FirebaseREADME.md
```

---

## 6. Payload structure

The GM panel publishes a payload describing the complete player-screen state.

Typical fields include:

```text
type
text
backgroundId
backgroundFile
logoId
logoFile
fillerId
fillerSet
fontId
fontPreset
messageAudioId
messageAudioFile
fillersEnabled
audioEnabled
showLogo
movingOverlay
flicker
prefixLines
suffixLines
fillerLineCount
fillerBandLines
messageColor
prefixColor
suffixColor
msgFontSize
prefixFontSize
suffixFontSize
pingUrl
nonce
ts
```

Expected `type` values include:

| Type | Meaning |
| --- | --- |
| `message` | Render a normal message. |
| `ping` | Play attention sound without changing message text. |
| `clear` | Clear visible message text. |

A `nonce` or timestamp-like field helps force listeners to react even when values are otherwise similar.

---

## 7. GM panel responsibilities

The GM panel is responsible for:

- loading local selectable data from `assets/data/data.json`,
- rendering selectors for backgrounds, logos, fonts, fillers, and audio,
- maintaining current UI state,
- previewing message content and background layout,
- publishing the current payload to Firestore,
- playing or triggering ping behavior,
- importing manifest data into refreshed local JSON,
- restoring default settings,
- handling missing assets and invalid selections.

---

## 8. Player screen responsibilities

The player screen is responsible for:

- subscribing to `dataslate/current`,
- reading the full current payload,
- applying background and visual settings,
- applying selected font and color values,
- rendering prefix, message, suffix, and filler layers,
- applying shadow rectangle / overlay / flicker settings,
- showing or hiding logos,
- playing audio if enabled and allowed by the browser,
- using safe fallback behavior when assets are missing.

---

## 9. Data import from XLSX

If the module includes manifest import, the source workbook is typically:

```text
DataSlate/assets/data/DataSlate_manifest.xlsx
```

Generated data target:

```text
DataSlate/assets/data/data.json
```

Expected workflow:

1. Open the GM panel.
2. Use **Update data from XLSX**.
3. Select/read the DataSlate manifest workbook.
4. Generate refreshed JSON data.
5. Save or place the generated output as `assets/data/data.json`.
6. Reload the GM panel and verify options.

---

## 10. Blue-frame maintenance workflow

If the module includes blue-frame technical backgrounds, these files may exist:

```text
DataSlate/assets/ramki/
DataSlate/assets/data/NiebieskaRamka.md
DataSlate/assets/data/Mapowanie.xlsx
```

Purpose:

- `assets/backgrounds/` contains final backgrounds displayed to players.
- `assets/ramki/` contains matching technical images with blue rectangles/frames.
- `Mapowanie.xlsx` maps each blue-frame image to the matching final background.
- `NiebieskaRamka.md` explains how to calculate a normalized safe text rectangle.

The blue-frame files are not final player backgrounds. They are maintenance/reference files used to calculate the safe area where message text should appear.

---

## 11. Audio behavior

DataSlate audio uses local files.

Important behavior:

- Ping uses a local ping audio file.
- Message audio uses the selected message audio file from local assets/data.
- Browsers may block audio until the user interacts with the page.
- The Audio toggle controls whether message audio should play.
- The player screen should degrade gracefully if audio cannot play.

---

## 12. Styling and layout

The player screen renders:

- full-screen background image,
- optional frame/overlay layers,
- optional logo,
- prefix lines,
- message text,
- suffix lines,
- filler lines,
- optional shadow rectangle,
- flicker/moving effects where enabled.

The GM preview should help validate readability before publication.

When changing layout:

1. Test on the target projector/display.
2. Test narrow/mobile dimensions.
3. Test long and short messages.
4. Test backgrounds with different safe text rectangles.
5. Test with logo enabled and disabled.
6. Test with fillers enabled and disabled.

---

## 13. Difference from DataSlate_Offline

| Feature | `DataSlate` | `DataSlate_Offline` |
| --- | --- | --- |
| Runtime model | Two-screen live relay | Single-device composition/export |
| Firebase | Required | Not used |
| Firestore path | `dataslate/current` | None |
| Player display | Separate browser/device | Local preview only |
| Output | Live rendered message | Generated image or visual export |

Do not copy Firebase documentation into `DataSlate_Offline`.

---

## 14. Control tests

| Test | Steps | Expected result |
| --- | --- | --- |
| Firestore sync | Open GM and player screens, send a message. | Player screen updates immediately. |
| Clear message | Send text, then clear. | Player screen clears message text. |
| Ping | Click Ping. | Ping sound plays if browser audio policy allows it. |
| Background selection | Select different backgrounds and send. | Player screen changes background. |
| Logo selection | Enable logo, select logo/color, send. | Player screen shows selected logo/color. |
| Logo disabled | Disable logo and send. | Player screen hides logo. |
| Fillers | Enable fillers and send. | Filler lines render around the message. |
| Audio toggle | Enable/disable audio and send audio message. | Audio behavior follows toggle/browser policy. |
| Restore defaults | Change many controls, restore defaults, send. | GM panel and player output return to default style. |
| Data import | Update data from XLSX and reload. | New selectable options appear. |

---

## 15. Rebuild checklist

To rebuild or copy DataSlate:

1. Keep production files: `GM.html` and `DataSlate.html`.
2. Keep helper/reference files if users need them.
3. Keep local assets under `assets/`.
4. Keep `assets/data/data.json`.
5. Keep manifest files if data import is required.
6. Keep blue-frame maintenance files if background maintenance is required.
7. Configure `DataSlate/config/firebase-config.js`.
8. Enable Firestore.
9. Verify rules for the intended group.
10. Open GM and player screens.
11. Send a test message.
12. Test ping, audio, background, logo, fillers, and clear behavior.

---

## 16. Known release notes

- DataSlate uses Firestore, not Realtime Database.
- DataSlate uses local assets, not Firebase Storage.
- The online version is a two-screen relay module.
- The offline version is documented separately.
- Each group should use isolated Firebase configuration to avoid cross-group message leaks.
