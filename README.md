# RPG DataSlate Relay

`rpg-dataslate-relay` contains two DataSlate variants:

1. `DataSlate` — the online GM-to-player display module.
2. `DataSlate_Offline` — a simplified offline module for preparing and generating visual message images on one device.

The repository is intended for RPG session support: atmospheric transmissions, briefing screens, styled messages, and player-facing visual handouts.

---

## Modules

| Module | Purpose | Firebase |
| --- | --- | --- |
| `DataSlate` | GM panel sends messages to a player screen through Firestore. | Required |
| `DataSlate_Offline` | Offline single-device version used to compose and generate message images. | Not used |

---

## DataSlate

`DataSlate` is the online relay version.

It uses two screens:

| Screen | Entry point | Purpose |
| --- | --- | --- |
| GM panel | `DataSlate/GM.html` | The GM prepares text, style, background, logo, sound, and effects. |
| Player screen | `DataSlate/DataSlate.html` | Players see the published message on a separate display. |

The online module uses Cloud Firestore as the live communication layer between the GM panel and the player screen.

Firebase setup is documented in:

```text
DataSlate/config/FirebaseREADME.md
```

User and technical documentation:

```text
DataSlate/docs/README.md
DataSlate/docs/Documentation.md
```

---

## DataSlate_Offline

`DataSlate_Offline` is a simplified offline version.

It is intended for:

- composing styled DataSlate messages on one device,
- previewing the final visual output locally,
- generating image files or image-like outputs instead of sending messages to a second device,
- preparing visual handouts for later use in a VTT, chat, presentation, or session notes.

It does not use Firebase.

User and technical documentation:

```text
DataSlate_Offline/docs/README.md
DataSlate_Offline/docs/Documentation.md
```

---

## Documentation standard

Repository documentation should follow:

```text
docs-standard.md
```

General rules:

- documentation is English-only,
- do not maintain duplicated EN/PL sections in the same file,
- do not store private Firebase values, passwords, service account keys, tokens, or production URLs in documentation,
- describe DEMO/public placeholders as placeholders,
- document Firebase only for modules that actually use Firebase,
- keep online and offline DataSlate behavior clearly separated.

---

## Security notes

Do not commit:

- Firebase service account files,
- private keys,
- production tokens,
- private group URLs,
- real passwords,
- private session content.

Public Web SDK Firebase config values may be present in the app when required by Firebase Web SDK, but they must not be confused with private credentials.
