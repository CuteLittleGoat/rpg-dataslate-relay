# User guide — DataSlate_Offline

DataSlate_Offline is a simplified single-device version of DataSlate.

It is used to compose styled DataSlate messages locally and generate image outputs instead of sending messages to a second player display.

This module does not use Firebase.

---

## What DataSlate_Offline is for

Use DataSlate_Offline when you want to:

- prepare a styled transmission or briefing screen on one device,
- preview a message without a player display,
- generate an image for later use,
- create visual handouts,
- export a message to a VTT, chat, notes, or presentation,
- work without internet access or Firebase.

---

## Difference from online DataSlate

| Feature | `DataSlate` | `DataSlate_Offline` |
| --- | --- | --- |
| Runtime model | GM panel + player display | Single local screen |
| Firebase | Required | Not used |
| Firestore relay | Yes | No |
| Second device | Recommended/expected | Not needed |
| Output | Live rendered player screen | Generated image/export |
| Best use | Live session display | Preparing handouts or static visuals |

---

## How to open

Open the offline module entry point, for example:

```text
DataSlate_Offline/index.html
```

If the actual entry point has a different name, use the file provided in the module folder.

---

## Basic workflow

1. Open DataSlate_Offline.
2. Choose a background or visual preset.
3. Enter the message text.
4. Adjust font, size, color, logo, and other available style options.
5. Preview the message locally.
6. Generate/export the image.
7. Save the image or use it in your VTT/session tools.

---

## Typical use cases

### Session handout

1. Prepare a message before the session.
2. Generate the image.
3. Upload it to a VTT or share it as a handout.

### Emergency message during play

1. Open the offline tool.
2. Type the message.
3. Use a known preset.
4. Generate image quickly.
5. Share or show the result locally.

### No internet / no Firebase

1. Open the module from local files.
2. Compose the message.
3. Generate output locally.
4. No online relay is required.

---

## Firebase behavior

DataSlate_Offline does not use Firebase.

It does not require:

- Firebase Authentication,
- Cloud Firestore,
- Realtime Database,
- Firebase Storage,
- Web Push.

If you need live GM-to-player synchronization, use the online `DataSlate` module instead.

---

## Assets

DataSlate_Offline may use local assets such as:

- backgrounds,
- logos,
- fonts,
- frame overlays,
- decorative elements.

Keep assets in the module folder so the offline page can load them without external services.

---

## Common problems

| Symptom | Possible cause | Fix |
| --- | --- | --- |
| Image does not generate. | Browser blocked export, canvas issue, or missing asset. | Check browser console and verify local assets. |
| Background is missing. | Asset path is wrong or file is missing. | Verify the background file exists. |
| Text is cropped. | Message is too long or font size is too large. | Reduce text, reduce font size, or use another layout. |
| Font looks different. | Font file is missing or browser fallback was used. | Verify font assets and CSS. |
| Output is blurry. | Export resolution is too low. | Use a larger canvas/export scale if available. |
| Need live player screen. | Offline module does not relay messages. | Use online `DataSlate`. |

---

## Related documentation

| File | Purpose |
| --- | --- |
| `DataSlate_Offline/docs/Documentation.md` | Technical architecture and maintenance guide. |
| `DataSlate/docs/README.md` | Online DataSlate user guide. |
| `DataSlate/config/FirebaseREADME.md` | Firebase setup for online DataSlate. |
| `docs-standard.md` | Repository documentation standard. |# DataSlate Offline docs

The current user guide is `DataSlate_Offline/README.md`.

Use `DataSlate_Offline/index.html` as the active application. The module is an offline/static DataSlate screen generator: it builds a local payload, renders the Working preview with the same renderer used by the final tab, and opens the final screen after **Generate** / **Generuj**.

There is no Firebase/Firestore setup, no online receiver screen, no legacy Send/Wyślij or Ping workflow, and no audio playback requirement.
