# 🇵🇱 Instrukcja Firebase dla modułu `DataSlate` (PL)

## Cel
Ten plik zawiera kompletny skrypt Node.js do utworzenia dokumentu `dataslate/current` z pełną strukturą wiadomości.

## 1) Konfiguracja `config/firebase-config.js`
Utwórz własny projekt Firebase i bazę Firestore dla grupy. Skopiuj dane z Firebase Console (aplikacja Web) i zastąp nimi angielskie placeholdery w `DataSlate/config/firebase-config.js` jako `window.firebaseConfig`. Nie zapisuj haseł, tokenów ani plików kont usługowych w repozytorium.

Firestore DataSlate zachowuje komunikację panel GM → ekran gracza przez dokument `dataslate/current`.

Wersja Release nie zawiera Web Push i nie wymaga żadnej dodatkowej konfiguracji powiadomień push. Zwykły ping i audio DataSlate są obsługiwane przez komunikację Firestore oraz lokalne assety modułu, a nie przez Web Push.

## 2) Struktura Firestore (drzewko + typy)
```text
dataslate (kolekcja)
└── current (dokument)
    ├── type (string)
    ├── faction (string)
    ├── color (string, np. "#222222")
    ├── fontColor (string, np. "#f5f5f5")
    ├── text (string)
    ├── ts (number, znacznik czasu Unix w ms)
    ├── nonce (number)
    ├── msgUrl (string, opcjonalne)
    └── pingUrl (string, opcjonalne)
```

## 3) Pełny skrypt Node.js (do skopiowania)
Zapisz jako `DataSlate/config/init-firestore-structure.js`:

```js
const admin = require("firebase-admin");

if (!process.env.GOOGLE_APPLICATION_CREDENTIALS) {
  console.error("[ERR] Ustaw GOOGLE_APPLICATION_CREDENTIALS na ścieżkę do pliku JSON konta serwisowego.");
  process.exit(1);
}

admin.initializeApp({
  credential: admin.credential.applicationDefault()
});

const db = admin.firestore();

const payload = {
  type: "status",
  faction: "neutral",
  color: "#222222",
  fontColor: "#f5f5f5",
  text: "",
  ts: Date.now(),
  nonce: 0,
  msgUrl: "",
  pingUrl: ""
};

async function main() {
  await db.collection("dataslate").doc("current").set(payload, { merge: true });
  console.log("[OK] Utworzono / zaktualizowano dokument dataslate/current");
}

main().catch((err) => {
  console.error("[ERR] Błąd inicjalizacji:", err);
  process.exit(1);
});
```

## 4) Uruchomienie
```bash
npm i firebase-admin
export GOOGLE_APPLICATION_CREDENTIALS="/pełna/ścieżka/do/service-account.json"
node DataSlate/config/init-firestore-structure.js
```

---

# 🇬🇧 Firebase guide for `DataSlate` module (EN)

## Purpose
This file provides a full Node.js script to create `dataslate/current` with the complete message payload structure.

## 1) `config/firebase-config.js`
Create your own Firebase project and Firestore database for the group. Copy Firebase Web config values and replace the English placeholders in `DataSlate/config/firebase-config.js` as `window.firebaseConfig`. Do not store passwords, tokens, or service-account files in the repository.

DataSlate Firestore preserves GM panel → player screen communication through the `dataslate/current` document.

The Release version does not include Web Push and does not require any additional push-notification configuration. Standard DataSlate ping and audio are handled through Firestore communication and local module assets, not Web Push.

## 2) Firestore structure (tree + types)
```text
dataslate (collection)
└── current (document)
    ├── type (string)
    ├── faction (string)
    ├── color (string, e.g. "#222222")
    ├── fontColor (string, e.g. "#f5f5f5")
    ├── text (string)
    ├── ts (number, Unix timestamp in ms)
    ├── nonce (number)
    ├── msgUrl (string, optional)
    └── pingUrl (string, optional)
```

## 3) Full Node.js script (copy-paste)
Save as `DataSlate/config/init-firestore-structure.js`:

```js
const admin = require("firebase-admin");

if (!process.env.GOOGLE_APPLICATION_CREDENTIALS) {
  console.error("[ERR] Set GOOGLE_APPLICATION_CREDENTIALS to your service account JSON path.");
  process.exit(1);
}

admin.initializeApp({
  credential: admin.credential.applicationDefault()
});

const db = admin.firestore();

const payload = {
  type: "status",
  faction: "neutral",
  color: "#222222",
  fontColor: "#f5f5f5",
  text: "",
  ts: Date.now(),
  nonce: 0,
  msgUrl: "",
  pingUrl: ""
};

async function main() {
  await db.collection("dataslate").doc("current").set(payload, { merge: true });
  console.log("[OK] Created / updated dataslate/current");
}

main().catch((err) => {
  console.error("[ERR] Initialization failed:", err);
  process.exit(1);
});
```

## 4) Run
```bash
npm i firebase-admin
export GOOGLE_APPLICATION_CREDENTIALS="/full/path/to/service-account.json"
node DataSlate/config/init-firestore-structure.js
```
