# Technical documentation — DataSlate_Offline

DataSlate_Offline is a simplified offline version of DataSlate. It is designed for single-device composition and image generation rather than live GM-to-player relay.

It does not use Firebase.

---

## 1. Module purpose

DataSlate_Offline is responsible for:

- rendering a local DataSlate-style editor/preview,
- letting the user compose a styled message,
- applying local backgrounds, logos, fonts, colors, and layout options,
- generating an image or image-like output from the composed message,
- working without Firestore, Realtime Database, Authentication, or a second display.

---

## 2. Difference from online DataSlate

| Area | Online `DataSlate` | `DataSlate_Offline` |
| --- | --- | --- |
| Main goal | Live message relay | Local image generation |
| Runtime | GM screen + player screen | Single screen |
| Firebase | Required | Not used |
| Firestore document | `dataslate/current` | None |
| Player screen listener | Yes | No |
| Output | Live browser rendering | Exported/generated image |
| Offline use | Limited | Primary purpose |

---

## 3. Expected entry points

The expected entry point is:

```text
DataSlate_Offline/index.html
```

If the implementation uses another file name, keep this documentation synchronized with the actual module entry point.

---

## 4. File responsibilities

Typical module files may include:

| File / folder | Purpose |
| --- | --- |
| `DataSlate_Offline/index.html` | Main offline editor/preview/export page. |
| `DataSlate_Offline/style.css` | Offline module layout and visual styles, if separated. |
| `DataSlate_Offline/script.js` | Offline editor logic and export logic, if separated. |
| `DataSlate_Offline/assets/` | Local backgrounds, logos, fonts, and decorative assets. |
| `DataSlate_Offline/docs/README.md` | User guide. |
| `DataSlate_Offline/docs/Documentation.md` | This technical guide. |

If CSS/JS are embedded in HTML, document that in this section when the file is updated.

---

## 5. Runtime model

The offline runtime should work without network services.

Expected flow:

1. User opens the offline page.
2. The page loads local assets.
3. User chooses a layout/background/preset.
4. User enters message text.
5. User adjusts visual options.
6. The preview updates locally.
7. User triggers image generation/export.
8. The browser creates a downloadable or copyable image output.

No Firestore listener is involved.

No external player screen is involved.

---

## 6. Firebase behavior

DataSlate_Offline does not use Firebase.

It must not require:

- Firebase Authentication,
- Cloud Firestore,
- Realtime Database,
- Firebase Storage,
- Web Push,
- service account files,
- Firebase Web SDK config.

Do not add `FirebaseREADME.md` for this module unless Firebase is intentionally added later.

If Firebase is added later, update this documentation and clearly explain why the module is no longer offline-only.

---

## 7. Image generation behavior

The offline module should generate a visual output from the current preview state.

Depending on implementation, this may use:

- an HTML canvas,
- SVG export,
- DOM-to-image rendering,
- browser download API,
- clipboard image API,
- a print/screenshot workflow.

Document the actual export mechanism when implementation details are finalized.

Expected output behavior:

- generated output should match the visible preview as closely as possible,
- local backgrounds and logos should be included,
- text should remain readable,
- output size/resolution should be documented,
- missing assets should produce readable errors or visible fallbacks.

---

## 8. Asset handling

The offline module should use local assets.

Important asset types:

- backgrounds,
- logos,
- fonts,
- frame overlays,
- decorative UI elements.

Rules:

- keep asset paths relative to the module,
- avoid external URLs for offline-critical assets,
- test from local file hosting and from the final deployed environment,
- verify that exported images include loaded assets.

---

## 9. Layout and safe areas

The offline module should keep message text inside the intended safe area.

If it reuses DataSlate background layouts, document:

- how the safe area is selected,
- whether blue-frame mapping is used,
- where background-to-rectangle mapping is stored,
- how to update mappings when adding new backgrounds.

If it does not use blue-frame mapping, document the alternative positioning method.

---

## 10. Suggested state model

The current preview state may include:

```text
messageText
backgroundId
backgroundFile
logoId
logoFile
fontId
fontPreset
messageColor
prefixColor
suffixColor
msgFontSize
prefixFontSize
suffixFontSize
showLogo
showShadow
flicker
fillersEnabled
prefixLines
suffixLines
fillerLineCount
exportScale
```

Use only the fields actually supported by the implementation. Keep this list synchronized with code.

---

## 11. Relationship to online DataSlate

DataSlate_Offline may reuse:

- backgrounds,
- logos,
- styles,
- layout concepts,
- message composition ideas.

It should not reuse the online relay requirement.

Do not copy these online-only concepts into the offline module unless they are actually implemented:

- Firestore path `dataslate/current`,
- GM-to-player live listener,
- Firebase config,
- second device workflow,
- live ping relay.

---

## 12. Adding new backgrounds

When adding a new background:

1. Add the background asset to the offline module.
2. Add any matching frame/overlay asset if required.
3. Add the selectable entry in the offline UI data.
4. Configure safe text area if the module supports it.
5. Test short and long text.
6. Test export.
7. Verify the generated image matches the preview.
8. Update documentation if the workflow changes.

---

## 13. Control tests

| Test | Steps | Expected result |
| --- | --- | --- |
| Open module | Open the offline entry point. | Editor/preview appears without Firebase. |
| Basic message | Enter short text and preview. | Text appears in the preview. |
| Long message | Enter long text. | Text remains readable or user receives clear layout feedback. |
| Background selection | Change background. | Preview updates. |
| Logo toggle | Enable/disable logo if supported. | Preview updates. |
| Font options | Change font/size/color if supported. | Preview updates. |
| Export image | Generate/export output. | Image is produced. |
| Export accuracy | Compare output to preview. | Output matches preview closely. |
| Missing asset | Temporarily remove an asset in a test copy. | Module handles the error clearly. |
| Offline mode | Test without network access. | Core composition/export still works. |

---

## 14. Rebuild checklist

To rebuild or copy DataSlate_Offline:

1. Restore the offline entry point.
2. Restore CSS and JS if separated.
3. Restore local assets.
4. Verify asset paths.
5. Verify preview rendering.
6. Verify export/generation.
7. Test without Firebase.
8. Test without network access if the module is meant to be fully offline.
9. Test output in the intended VTT/session workflow.
10. Update user and technical documentation.

---

## 15. Known release notes

- DataSlate_Offline is not a live relay.
- DataSlate_Offline does not use Firebase.
- DataSlate_Offline does not require a second device.
- The main deliverable is a local generated visual/image output.
- If live player-screen synchronization is needed, use the online `DataSlate` module.
