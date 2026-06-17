# User guide — DataSlate

DataSlate shows narrative messages to players on a dedicated display. The GM controls message text, visual style, logo, sound, and effects from a separate GM panel.

This is the online relay version of DataSlate. It uses Firebase Cloud Firestore to send the current GM message to the player screen.

For the offline single-device image generation version, see:

```text
DataSlate_Offline/docs/README.md
```

---

## What DataSlate is for

DataSlate is designed for table play where the GM wants to send atmospheric transmissions, alerts, briefings, or styled messages to players.

The online version uses two screens:

| Screen | Entry point | Purpose |
| --- | --- | --- |
| Player screen | `DataSlate/DataSlate.html` | Display shown to players. |
| GM screen | `DataSlate/GM.html` | Control panel used by the GM. |

Best setup: keep both pages open at the same time, either on separate devices or on a dual-monitor setup.

---

## Quick start

1. Open `DataSlate/DataSlate.html` on the player screen.
2. Open `DataSlate/GM.html` on the GM device.
3. In the GM panel, choose **Background** and **Logo**.
4. Choose **Font** and optional **Message audio**.
5. Configure visual toggles such as **Logo**, **Shadow rectangle**, **Flicker**, **Fillers**, and **Audio**.
6. Enter text in **Message content**.
7. Click **Send**.
8. Check the player screen. The message should appear immediately.

---

## Main GM panel actions

| Button / element | What it does |
| --- | --- |
| **Send** | Publishes the current message and settings to the player screen. |
| **Ping** | Plays the attention sound without changing message text. |
| **Clear message** | Clears the message input field only. |
| **Restore defaults** | Resets panel settings to default values. |
| **Update data from XLSX** | Refreshes selectable DataSlate data from the manifest workbook. |
| Preview mode: **Content** | Shows the text-layer preview. |
| Preview mode: **Background** | Shows a background-only preview. |

---

## Common settings

The GM commonly adjusts:

- background image,
- logo image,
- logo color,
- message font,
- message audio,
- message text color and size,
- prefix/suffix text color and size,
- filler line count,
- prefix/suffix area height,
- shadow rectangle,
- flicker,
- audio toggle.

In filler data, line separators are newline and pipe `|`. Semicolon stays inside the text and does not split one entry into multiple elements.

---

## In-session workflow

1. Prepare a visual style for the scene.
2. Send shorter messages more often instead of one very long block.
3. Use **Ping** when you need immediate player attention.
4. Use audio sparingly for impact.
5. If the layout becomes messy after experiments, click **Restore defaults**.
6. Test a scene style on the actual player display before using it in an important scene.

---

## Firebase requirement

DataSlate requires Firebase Cloud Firestore because the GM panel and player screen exchange live state through the database.

Firebase setup instructions:

```text
DataSlate/config/FirebaseREADME.md
```

Each group should use its own Firebase project or clearly separated Firestore paths to avoid mixing messages between groups.

---

## Difference from DataSlate_Offline

| Feature | `DataSlate` | `DataSlate_Offline` |
| --- | --- | --- |
| Second player device | Yes | No |
| Firebase | Required | Not used |
| Live relay | Yes | No |
| Image generation | Not the main purpose | Main purpose |
| Session use | Send live messages to player display | Prepare/export images locally |

---

## Common problems

| Symptom | Possible cause | Fix |
| --- | --- | --- |
| No message appears on the player screen. | GM and player pages are not connected to the same Firestore project/path, or one page is stale. | Refresh both pages and check Firebase config. |
| Ping does not play. | Audio toggle, browser autoplay policy, or system volume. | Enable audio, interact with the page once, and check volume. |
| Player screen looks different on projector/mobile. | Screen size, scaling, or background choice. | Test on the final display and use shorter text. |
| Logo color does not change. | Logo disabled or controls inactive. | Enable Logo and send again. |
| Data options are missing. | Local `data.json` is stale or missing. | Use **Update data from XLSX** and verify generated JSON. |
| Messages appear in another group's display. | Shared Firebase config/path. | Use a separate Firebase project or path. |

---

## Related documentation

| File | Purpose |
| --- | --- |
| `DataSlate/docs/Documentation.md` | Technical architecture and maintenance guide. |
| `DataSlate/config/FirebaseREADME.md` | Firebase setup guide. |
| `DataSlate_Offline/docs/README.md` | Offline DataSlate user guide. |
