# Firebase setup — DataSlate

This guide explains how to configure Firebase for the online DataSlate module.

DataSlate uses Cloud Firestore for live GM panel → player screen communication. It does not use Realtime Database, Firebase Storage, or Web Push in the release version.

---

## Firebase services used

| Service | Used | Purpose |
| --- | --- | --- |
| Cloud Firestore | yes | Stores the current DataSlate payload at `dataslate/current`. |
| Firebase Authentication | optional | Only needed if your Firestore rules require signed-in users. |
| Realtime Database | no | Not used by DataSlate. |
| Storage | no | DataSlate uses local assets. |
| Web Push / Cloud Messaging | no | Release DataSlate does not use push notifications. |

Standard ping and audio are handled through Firestore communication plus local module assets.

---

## Required repository files

| File | Purpose |
| --- | --- |
| `DataSlate/config/firebase-config.js` | Firebase Web SDK config for this module. |
| `DataSlate/GM.html` | Production GM panel that writes the current payload. |
| `DataSlate/DataSlate.html` | Production player screen that listens for payload changes. |

Do not commit passwords, private keys, service account files, tokens, or production secrets.

---

## Firestore path

Current document:

```text
dataslate/current
```

Structure:

```text
dataslate (collection)
└── current (document)
```

The GM panel writes the current full display payload to this document. The player screen listens to the same document.

Firestore creates the `dataslate` collection and `current` document automatically on the first successful write. You do not need to manually create them first.

The Firestore service itself must still be enabled manually in Firebase Console, and rules must allow the intended read/write access.

---

## Step 1 — Create or open a Firebase project

1. Open Firebase Console.
2. Click **Add project** or open an existing project.
3. Enter the project name.
4. Continue through the project wizard.
5. Configure Analytics according to your group's needs.
6. Finish project creation.
7. Open the project overview.

---

## Step 2 — Add a Web App

1. In the Firebase project overview, click the Web icon (`</>`).
2. Enter an app nickname, for example `RPG DataSlate Relay`.
3. Register the app.
4. Copy the `firebaseConfig` object.
5. Paste the public Web SDK values into `DataSlate/config/firebase-config.js`.

Example shape:

```js
window.firebaseConfig = {
  apiKey: "INSERT_YOUR_API_KEY",
  authDomain: "INSERT_YOUR_AUTH_DOMAIN",
  projectId: "INSERT_YOUR_PROJECT_ID",
  storageBucket: "INSERT_YOUR_STORAGE_BUCKET",
  messagingSenderId: "INSERT_YOUR_MESSAGING_SENDER_ID",
  appId: "INSERT_YOUR_APP_ID",
};
```

`databaseURL` is not required for DataSlate because it does not use Realtime Database.

---

## Step 3 — Enable Cloud Firestore

1. In Firebase Console, open **Build**.
2. Click **Firestore Database**.
3. Click **Create database**.
4. Choose production mode unless you are deliberately creating a temporary demo environment.
5. Select the region.
6. Click **Enable**.
7. Wait until Firestore is ready.

---

## Step 4 — Configure Firestore rules

For a local/demo setup, rules must allow the GM panel to write and the player screen to read `dataslate/current`.

A safer authenticated example looks like this:

```js
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /dataslate/current {
      allow read, write: if request.auth != null;
    }
  }
}
```

If you use unauthenticated screens for a private local table setup, document that choice and restrict deployment access by hosting/project controls.

Do not use open public write rules in a real public deployment.

---

## Step 5 — First write creates the document

After Firestore is enabled and rules are set:

1. Open `DataSlate/GM.html`.
2. Open `DataSlate/DataSlate.html` on the player display.
3. In the GM panel, enter a short test message.
4. Click **Send**.
5. Open Firebase Console.
6. Open **Firestore Database**.
7. Verify that collection `dataslate` exists.
8. Verify that document `current` exists.
9. Verify that the player screen shows the message.

No Node.js initialization script is required for the normal release flow. The first successful GM-panel write can create the Firestore document.

---

## Expected document fields

The current payload may include fields such as:

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

The payload is a full current-state snapshot. The player screen should be able to render from the current document alone.

---

## Test with helper files

If helper files exist, they are useful for configuration tests:

```text
DataSlate/GM_test.html
DataSlate/DataSlate_test.html
```

Test steps:

1. Open the GM helper page.
2. Open the player helper page.
3. Send a short message.
4. Verify that it appears on the test player screen.
5. Test **Ping**.
6. Test **Clear message**.
7. Test background/logo selections.

After the helper pair works, test the production pair:

```text
DataSlate/GM.html
DataSlate/DataSlate.html
```

---

## Copying DataSlate for another group

If another group uses the module:

1. Create or select a separate Firebase project, or use a clearly separate Firestore path.
2. Replace `DataSlate/config/firebase-config.js` with that group's Web SDK config.
3. Verify rules.
4. Run the helper pair if present.
5. Run the production pair.
6. Send a test message.

This prevents one group's GM panel from sending messages to another group's player screen.

---

## Common errors

| Symptom | Possible cause | Fix |
| --- | --- | --- |
| Player screen does not update. | GM and player screens use different Firebase projects or rules block access. | Verify `DataSlate/config/firebase-config.js` and Firestore rules. |
| Firestore document is missing. | No successful GM write has happened yet. | Send a message from the GM panel. |
| Permission denied. | Firestore rules block read/write. | Adjust rules for the intended access model. |
| Ping does not play. | Browser audio policy or missing local audio file. | Interact with the page and verify the local audio file. |
| Audio does not play. | Audio disabled, browser blocked playback, or asset missing. | Enable audio, interact with the page, and check local assets. |
| Messages appear on the wrong display. | Shared Firebase config/path between groups. | Use a separate project or path. |
| Web Push setup is missing. | Release DataSlate does not use Web Push. | No push setup is required. |

---

## Security notes

- Do not commit service account files.
- Do not commit private keys.
- Do not commit production tokens.
- Do not use open Firestore rules for public deployments.
- DataSlate does not require Realtime Database.
- DataSlate does not require Firebase Storage.
- DataSlate does not require Web Push.
