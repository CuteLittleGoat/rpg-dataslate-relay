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
- Each group should use isolated Firebase configuration to avoid cross-group message leaks.# 🇬🇧 Technical documentation (EN)

## 1. Purpose and production entry points
`DataSlate` publishes GM-prepared messages to a player-facing screen. The production launcher is `index.html`, the production GM panel is `GM.html`, and the production player screen is `DataSlate.html`. Firestore communication uses the `dataslate/current` document or the equivalent path documented in the configured deployment.

## 2. Supported helper files
`GM_test.html` and `DataSlate_test.html` are helper views for users testing their own modifications. `GM_backup.html` and `DataSlate_backup.html` are reference backups for experiments. These four files are intentionally distributed, but they are not the normal production route.

## 3. Files, assets, and data
- `index.html` links production and helper entry points.
- `GM.html` writes the current payload; `DataSlate.html` listens and renders it.
- The `_test.html` pair supports modification testing; the `_backup.html` pair is retained as reference material.
- `config/firebase-config.js` contains the administrator-supplied Firebase Web SDK configuration template.
- `assets/backgrounds/`, `assets/ramki/`, `assets/logos/`, and `assets/audios/` contain local presentation assets.
- `assets/data/data.json`, spreadsheets, and mapping notes support selectable content and maintenance.

## 4. Runtime mechanics
The GM panel assembles a payload from message type, content, background, frame, logo, filler, ping, and audio controls, then writes a full current-state snapshot to Firestore. The player screen listens for the current document and updates presentation immediately. Local assets provide visuals and typing/audio effects; Firestore provides synchronization.

## 5. Styling and reconstruction
The presentation uses full-screen themed backgrounds, overlay frames, logos, text layers, and responsive scaling for player displays. To rebuild the module, restore every production, helper, backup, config, and asset file; configure a separate Firebase project; open `GM.html` and `DataSlate.html`; publish each content type; then verify visuals, fillers, ping, audio, and Firestore synchronization. Use the helper pair separately when testing modifications.

# 🇵🇱 Dokumentacja techniczna (PL)

# DataSlate — dokumentacja techniczna (odtworzenie 1:1)

## Zakres komunikacji

DataSlate używa Firestore do komunikacji panel GM → ekran gracza przez dokument `dataslate/current`. Zwykły ping i audio DataSlate korzystają z komunikacji Firestore oraz lokalnych assetów modułu.

## 1. Zakres modułu
Główną ścieżkę produkcyjnego uruchamiania DataSlate tworzą dwa ekrany:
- `GM.html` — panel przygotowania i publikacji komunikatów.
- `DataSlate.html` — ekran odczytu komunikatów dla graczy.

Pliki testowe (`GM_test.html`, `DataSlate_test.html`) oraz backupowe (`GM_backup.html`, `DataSlate_backup.html`) celowo są dostępne. Służą użytkownikom jako narzędzia pomocnicze do testowania własnych modyfikacji i jako punkt odniesienia podczas eksperymentów. Nie są główną ścieżką produkcyjną modułu. Funkcjonalnie punktem rozwoju pozostają pliki `_test`.

## 2. Struktura katalogów i odpowiedzialność plików
- `index.html` — launcher modułu z linkami do widoków produkcyjnych i pomocniczych widoków testowych.
- `GM.html` — produkcyjny panel GM.
- `DataSlate.html` — produkcyjny ekran odczytu dla graczy.
- `GM_test.html` — pomocnicza logika GM: edycja treści, import danych, podgląd tła, publikacja.
- `DataSlate_test.html` — pomocniczy ekran odczytu publikowanych treści.
- `GM_backup.html` i `DataSlate_backup.html` — zachowane pliki referencyjne dla użytkowników eksperymentujących z własnymi zmianami.
- `assets/data/data.json` — lokalny snapshot treści (źródło dla importów/odczytu lokalnego).
- `assets/data/DataSlate_manifest.xlsx` — arkusz źródłowy dla importu treści i układów.
- `assets/backgrounds/*` — tła ekranów (DataSlate, Pergamin, WnG, Notatnik, Litannie itp.).
- `assets/ramki/*` — ramki odpowiadające tłom.
- `assets/logos/*` — logotypy warstw UI.
- `config/firebase-config.js` — konfiguracja klienta Firebase.

## 3. Renderowanie UI i warstwa stylów
### 3.1. Fonty i typografia
- Moduł obsługuje wybór fontu z panelu GM oraz przekazanie fontu w payloadzie danych.
- Fonty są preloadowane dla stabilnego pierwszego renderu i mniejszego „skakania” tekstu.
- Dla środowisk bez załadowania wybranego fontu działa fallback do bezpiecznego font-stacku.

### 3.2. Motyw i tła
- Ekran gracza renderuje tekst na wybranym tle (`backgroundKey`) + dedykowanej ramce (`frameKey`).
- Obsługiwane są tryby podglądu tła: wycinek i całość (zależnie od wybranej opcji GM).
- Wdrożono dodatkowe pole robocze dla tła **Pergamin** (warianty kompozycji tekstu na tym tle).

### 3.3. Podgląd „Treść / Tło”
- Panel GM ma równoległy podgląd:
  - samej treści,
  - treści osadzonej na tle.
- Dzięki temu operator przed publikacją kontroluje czytelność, kontrast i finalny układ.

## 4. Model danych (payload komunikatu)

Panel `GM_test.html` zapisuje do Firestore pełny snapshot bieżącego komunikatu. Zapis jest wykonywany przez `currentRef.set(getPayload(type), { merge: false })`.

Aktualny payload zawiera następujące pola:

```text
type: string
text: string
backgroundId: string albo null
backgroundFile: string
logoId: string albo null
logoFile: string
fillerId: string albo null
fillerSet: string
fontId: string albo null
fontPreset: string
messageAudioId: string albo null
messageAudioFile: string
fillersEnabled: boolean
audioEnabled: boolean
showLogo: boolean
movingOverlay: boolean
flicker: boolean
prefixLines: tablica stringów
suffixLines: tablica stringów
fillerLineCount: number
fillerBandLines: number
messageColor: string HEX
prefixColor: string HEX
suffixColor: string HEX
msgFontSize: number
prefixFontSize: number
suffixFontSize: number
pingUrl: string
nonce: string
ts: Firestore serverTimestamp
```

Dla `type: "message"` pole `text` zawiera treść wiadomości wpisaną przez GM. Dla `type: "ping"` i `type: "clear"` pole `text` jest pustym stringiem.


## 5. Integracja Firebase
### 5.1. Warstwa klienta
- Konfiguracja znajduje się w `config/firebase-config.js`.
- Ekran GM publikuje payload do dokumentu bieżącego komunikatu.
- Ekran DataSlate nasłuchuje zmian i renderuje aktualny snapshot.

### 5.2. Model dokumentu
- Dokument roboczy: `dataslate/current`.
- Zapis powinien być pełnym snapshotem stanu wiadomości (single source of truth).

### 5.3. Uwaga implementacyjna (krytyczna)
**Uwaga implementacyjna:** dokument jest zapisywany jako pełny snapshot stanu wiadomości (bez merge), aby zawsze nadpisywać kompletny payload publikacji.

Ta zasada jest obowiązkowa przy odtwarzaniu modułu 1:1.

## 6. Import danych XLSX → JSON
### 6.1. Wejście
- Plik źródłowy: `assets/data/DataSlate_manifest.xlsx`.
- Import uruchamiany z panelu GM (przycisk aktualizacji danych z XLSX).

### 6.2. Przetwarzanie
- Dane z arkusza są mapowane do pól używanych przez payload UI.
- Obsługiwane jest autoformatowanie tokenu `+++` podczas importu do JSON.
- Wynik importu generuje plik JSON do pobrania. Po wygenerowaniu należy umieścić pobrany `data.json` w `DataSlate/assets/data/data.json`, jeżeli ma zastąpić lokalny snapshot używany przez moduł.

### 6.3. Oczekiwany efekt
- Po imporcie nowa struktura jest od razu dostępna do podglądu i publikacji.
- Zmiany w treści, tle, logo i stylu tekstu mają być widoczne bez ręcznej edycji JSON.

## 7. Logika GM (`GM_test.html`)
Kluczowe grupy funkcji:
1. Inicjalizacja UI i domyślnych ustawień panelu.
2. Obsługa wyboru fontu, tła, ramki i logo.
3. Podgląd treści i podgląd tła (w tym tryb wycinek/całość).
4. Import `DataSlate_manifest.xlsx` i odświeżanie danych roboczych.
5. Publikacja payloadu do `dataslate/current`.
6. Obsługa błędów (walidacja, brak danych, problemy sieciowe).

## 8. Logika ekranu gracza (`DataSlate_test.html`)
Kluczowe grupy funkcji:
1. Odbiór i render aktualnego snapshotu danych.
2. Budowa warstwy wizualnej (tło + ramka + logo + tekst).
3. Stosowanie fontu otrzymanego z payloadu.
4. Bezpieczne fallbacki przy brakujących zasobach.
5. Utrzymanie czytelności i responsywności w różnych proporcjach ekranu.

## 9. Struktura Firestore do odtworzenia

Minimalna struktura Firestore używana przez moduł:

```text
dataslate (kolekcja)
└── current (dokument)
    ├── type
    ├── text
    ├── backgroundId
    ├── backgroundFile
    ├── logoId
    ├── logoFile
    ├── fillerId
    ├── fillerSet
    ├── fontId
    ├── fontPreset
    ├── messageAudioId
    ├── messageAudioFile
    ├── fillersEnabled
    ├── audioEnabled
    ├── showLogo
    ├── movingOverlay
    ├── flicker
    ├── prefixLines
    ├── suffixLines
    ├── fillerLineCount
    ├── fillerBandLines
    ├── messageColor
    ├── prefixColor
    ├── suffixColor
    ├── msgFontSize
    ├── prefixFontSize
    ├── suffixFontSize
    ├── pingUrl
    ├── nonce
    └── ts
```


## 10. Skrypt Node.js do bootstrapu dokumentu `dataslate/current`
Poniższy przykład pokazuje minimalny bootstrap dokumentu `dataslate/current` zgodny z aktualnym modelem payloadu modułu DataSlate.

Przykład służy wyłącznie do przygotowania struktury dokumentu w Firestore. Panel GM zapisuje później pełny snapshot przez `currentRef.set(getPayload(type), { merge: false })`.

```js
// node scripts/bootstrap-dataslate.js
import { initializeApp, cert } from 'firebase-admin/app';
import { getFirestore, FieldValue } from 'firebase-admin/firestore';
import serviceAccount from './serviceAccountKey.json' assert { type: 'json' };

initializeApp({ credential: cert(serviceAccount) });

const db = getFirestore();

await db.doc('dataslate/current').set({
  type: 'clear',
  text: '',
  backgroundId: null,
  backgroundFile: '',
  logoId: null,
  logoFile: '',
  fillerId: null,
  fillerSet: '',
  fontId: null,
  fontPreset: '',
  messageAudioId: null,
  messageAudioFile: '',
  fillersEnabled: true,
  audioEnabled: true,
  showLogo: true,
  movingOverlay: true,
  flicker: true,
  prefixLines: [],
  suffixLines: [],
  fillerLineCount: 3,
  fillerBandLines: 2,
  messageColor: '#00ff66',
  prefixColor: '#ffffff',
  suffixColor: '#ffffff',
  msgFontSize: 20,
  prefixFontSize: 12,
  suffixFontSize: 12,
  pingUrl: '',
  nonce: '',
  ts: FieldValue.serverTimestamp(),
});

console.log('Bootstrap complete');
```

## 11. Testy kontrolne po wdrożeniu
1. Otwórz `GM_test.html` i opublikuj testowy komunikat.
2. Otwórz `DataSlate_test.html` i sprawdź natychmiastowy render.
3. Zmień font i tło — potwierdź poprawne odświeżenie.
4. Wykonaj import XLSX i sprawdź poprawność mapowania.
5. Zweryfikuj tryb podglądu oraz poprawność renderu po zmianach ustawień.

## 12. Ograniczenia i zasady utrzymania
- Nie edytować automatycznie: `GM.html`, `DataSlate.html`, `GM_backup.html`, `DataSlate_backup.html`.
- Zmiany funkcjonalne wykonywać w plikach `_test`.
- Po każdej zmianie kodu aktualizować `docs/README.md` i `docs/Documentation.md`.
- Przy zmianach `GM_test.html`/`DataSlate_test.html` podnosić `INF_VERSION` w formacie czasu lokalnego PL.

## 13. Szczegółowa mapa funkcji (`GM_test.html`)
Poniżej lista funkcji wymaganych do odtworzenia zachowania 1:1:

### 14.1. Wersjonowanie i status UI
- `autoCacheBust()` — wymusza parametr `?v=<INF_VERSION>` w URL, aby uniknąć cache po deployu.
- `setStatus(...)` — centralny renderer komunikatów statusu (sukces/błąd/info) w panelu GM.

### 14.2. Walidacja i narzędzia pomocnicze
- `clamp(value, min, max)` — ograniczenie zakresu numerycznego.
- `safeGet(obj, path, fallback)` — bezpieczne pobieranie zagnieżdżonych pól.
- `toInt`, `toStr`, `toStringArray` — normalizacja typów rekordów importu.
- `toStringArray` rozdziela wartości fillerów po separatorach: `\n` oraz `|`, a następnie trimuje i odrzuca puste elementy. Średnik jest pozostawiany w treści pojedynczego fillera, aby nie rozbijać gotowych litanii na sztuczne fragmenty.
- `normalizeHexColor`, `isFullHexColor`, `resolveHexColor` — sanityzacja kolorów z manifestu.

### 14.3. Fonty, selecty i etykiety
- `getSelectedFont()` — zwraca aktywnie wybrany font do payloadu.
- `buildOptionLabel(...)` — buduje czytelny label opcji wyboru.
- `fillSelect(...)` — zasilenie `<select>` danymi manifestu.
- `preloadManifestFonts(...)` — preload fontów wykrytych w danych.
- `applySelectedFontToPreview(...)` — natychmiastowe zastosowanie fontu do podglądu.

### 14.4. Import XLSX i transformacja danych
- `normalizeHeader`, `normalizeRecordKeys` — unifikacja nazw kolumn.
- `pickValue(...)` — fallbackowe mapowanie wartości między aliasami kolumn.
- `parseSheetRows(...)` — parsowanie pojedynczego arkusza do rekordów domenowych.
- `buildManifestFromWorkbook(...)` — składanie finalnego manifestu z wielu arkuszy.
- `updateDataFromXlsx(...)` — pełen pipeline importu i odświeżenia danych.
- `writeImportLog(...)` — raport importu (błędy, pominięcia, ostrzeżenia).
- `downloadJson(...)` — eksport wygenerowanego JSON do pliku.

### 14.5. Podgląd i render
- `getPreviewMode`, `setPreviewMode`, `loadSavedPreviewMode` — zarządzanie trybem podglądu.
- `syncFlickerDependency(...)` — synchronizacja zależności opcji migotania/efektu.
- `renderPreview(...)` — render warstwy treści + dekoracji.
- `draw(...)` — finalny etap rysowania widoku.
- `mapBasic(...)` — mapowanie ustawień panelu do modelu renderowania.

### 14.6. Payload i publikacja
- `getPayload()` — serializacja bieżącego stanu panelu do modelu Firestore.
- `send()` — zapis snapshotu wiadomości do `dataslate/current`.
- `ping()` — szybki test łączności warstwy publikacji; zapisuje pełny snapshot `getPayload('ping')` bez pól `undefined`, bo Firestore odrzuca `undefined` (błąd `Function DocumentReference.set() called with invalid data`).
- `restoreDefaults()` — przywrócenie ustawień domyślnych panelu.
- `rerollFillers()` i `pick()` — odświeżanie oraz wybór elementów dynamicznych (`fillers`).

## 14. Szczegółowa mapa funkcji (`DataSlate_test.html`)
- `autoCacheBust()` — ten sam mechanizm wersjonowania URL co po stronie GM.
- `preloadKnownFonts()` — preload typowych rodzin fontów dla szybszego first paint.
- `clamp()` — pomocnicze ograniczenia numeryczne.
- `play()` — bootstrap renderera po otrzymaniu danych.
- `getViewportSize()` — metryki viewportu używane do skalowania overlay.
- `updateOverlayMetrics()` — przeliczenie geometrii warstw tekstowych.
- `applyStyles(payload)` — zastosowanie stylów (font, kolor, spacing) z payloadu.
- `applyLayout(payload)` — zastosowanie pozycji i rozmiarów kontenerów.
- `applyMessage(payload)` — render treści komunikatu.
- `clearMessage()` — bezpieczne czyszczenie widoku przy błędzie/braku danych.
- `fitOverlayToBackground()` — dopasowanie skali overlay do tła.
- `scheduleFitOverlay()` — debouncing/odroczenie dopasowania przy zmianie rozmiaru.

## 15. Specyfikacja wersjonowania testowego (`INF_VERSION`)
- Pole `INF_VERSION` występuje równolegle w `GM_test.html` i `DataSlate_test.html`.
- Format obowiązkowy: `rrrr-MM-dd_gg-hh-ss` (czas lokalny Polski).
- Każda zmiana kodu w którymkolwiek z plików testowych wymaga podniesienia tej wartości w obu plikach.
- Funkcja `autoCacheBust()` wymusza spójność `?v=INF_VERSION`, co gwarantuje odświeżenie zasobów na kliencie.
- Aktualna wersja testowa: `2026-04-30_12-00-51`.

## 16. Macierz kompletności technicznej
- **Style, kolory, fonty i warstwy:** sekcje 3, 14.3, 15.
- **Funkcje i mechaniki UI:** sekcje 7, 8, 14, 15.
- **Model danych i logika publikacji:** sekcje 4, 5, 14.6.
- **Firebase/Firestore:** sekcje 5, 10 (dokument `dataslate/current`).
- **Wersjonowanie i cache-busting:** sekcja 18.

## 17. Wymagalność Firebase w instrukcji użytkownika
Instrukcja użytkownika (`docs/README.md`) powinna jednoznacznie wskazywać, że moduł Infoczytnik wymaga integracji z Firebase/Firestore do komunikacji GM↔gracze.

Procedura użytkowa powinna obejmować:
- utworzenie projektu Firebase,
- rejestrację aplikacji web,
- konfigurację `config/firebase-config.js`,
- utworzenie Firestore Database,
- ustawienie reguł,
- test dwuekranowy GM↔DataSlate.

## 18. Wdrożenia dla wielu grup
Każda grupa wymaga osobnego projektu Firebase, aby dokument `dataslate/current` nie był współdzielony między niezależnymi instancjami.

W plikach `GM_test.html` i `DataSlate_test.html` komentarze `WAŻNE/IMPORTANT` oznaczają istotne miejsca wdrożeniowe:
- `INF_VERSION` jako cache-busting testowej wersji,
- `config/firebase-config.js`,
- walidację `window.firebaseConfig`.

Po każdej zmianie testowych plików wartość `INF_VERSION` powinna być taka sama w `GM_test.html` i `DataSlate_test.html`.

## 19. Linki względne
Moduł używa ścieżek względnych do nawigacji i ładowania zasobów. Dzięki temu kopia modułu może działać po przeniesieniu na inny serwer lub do innej instancji wdrożeniowej, o ile zachowana jest struktura katalogów.

Przy wdrożeniu dla osobnej grupy należy sprawdzić:
- ścieżkę do `config/firebase-config.js`,
- ścieżki do assetów,
- ścieżki używane przez panel GM i ekran DataSlate,
- zgodność konfiguracji Firebase z docelowym projektem.

## 14. Panel koloru logo
- Domyślna wartość `DEFAULT_FORM_STATE.logoColor` to `#d4af37`.
- Payload publikowany do Firestore zawiera pole `logoColor` (HEX), aby ekran odbiorcy renderował identyczny kolor co panel GM.
- W `renderPreview()` logo podglądu jest kolorowane przez CSS mask (`mask-image`/`-webkit-mask-image`) i zmienną koloru, dzięki czemu podgląd reaguje natychmiast.
- Gdy `showLogo=false`, funkcja `updateLogoColorPanelState()` wyszarza panel i blokuje interakcję (`opacity` + `pointer-events`).
- Zdarzenia `.chip[data-target]` rozdzielają trzy cele (`msg`, `logo`, `ps`), aby presety koloru logo nie nadpisywały koloru prefix/suffix.
- `updateLogoColorPanelState()` jest wywoływana wewnątrz `renderPreview()`, dzięki czemu stan aktywności panelu koloru logo jest zawsze zsynchronizowany z checkboxem `showLogo`.
- W `DataSlate_test.html` logo odbiorcy również renderowane jest jako maska PNG z jednolitym kolorem (`--logoColor`), pobieranym z payloadu (`d.logoColor`).


- Kolor logo w szybkich presetach obejmuje wariant **Czarny (#000000)**, a logo renderowane jest na elementach dekoracyjnych bez fallbacku tekstowego IMG, co eliminuje artefakty podczas zoomu.

## 20. Dane manifestu DataSlate
- `assets/data/data.json` odpowiada zestawowi assetów logo w `assets/logos/`.
- Tablica `logos` zawiera 14 wpisów wskazujących pliki PNG z `assets/logos/`.
- W `GM_test.html` wartość `DEFAULT_FORM_STATE.logoId` wynosi `3`, co wybiera logo `Aquila` (`assets/logos/Aquila.png`).
- Wartość `INF_VERSION` powinna być zgodna w `GM_test.html` i `DataSlate_test.html`, aby cache-busting obu pomocniczych punktów wejścia działał spójnie.
