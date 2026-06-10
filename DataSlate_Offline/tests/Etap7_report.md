# Etap 7 — raport testów automatycznych i regresyjnych DataSlate Offline

Data wykonania: 2026-06-10  
Repozytorium: `CuteLittleGoat/rpg-dataslate-relay`  
Zakres aktywnej ścieżki: `DataSlate_Offline/index.html`, `index_backup.html`, `index_test.html`, `tools/update_embedded_data.py`, `assets/data/data.json`.

## Środowisko testowe

- System wykonania: środowisko Codex w kontenerze Linux.
- Python: `Python 3.12.13`.
- Node: `v20.20.2`.
- npm: `11.4.2`.
- Headless browser: **NOT AVAILABLE** — w środowisku nie znaleziono `chromium`, `chromium-browser`, `google-chrome`, `playwright` ani bibliotek Python `playwright`/`selenium`. Z tego powodu test przeglądarkowy został zastąpiony testem statycznym i testem Node VM generującym finalny HTML przez `buildOfflineSlateHTML(payload)`.
- Nie instalowano ciężkich zależności testowych.

## Komendy wykonane ręcznie przez agenta

- `git status --short`
- `python3 -m json.tool DataSlate_Offline/assets/data/data.json >/tmp/dataslate-data-json-ok`
- `python3 -m py_compile DataSlate_Offline/tools/update_embedded_data.py`
- `cmp -s DataSlate_Offline/index.html DataSlate_Offline/index_backup.html`
- `cmp -s DataSlate_Offline/index.html DataSlate_Offline/index_test.html`
- `rg -n -i "Firebase|Firestore|firebase-config\.js|config/firebase-config\.js|initializeApp|getFirestore|dataslate/current|currentRef\.set|onSnapshot|\bSend\b|Wyślij|Wyslij|\bPing\b|new Audio|\.play\(|audioEnabled|messageAudioId|messageAudioFile|odblok|localStorage|sessionStorage|postMessage|location\.hash|location\.search|URLSearchParams|SheetJS|xlsx" DataSlate_Offline/index.html DataSlate_Offline/index_backup.html DataSlate_Offline/index_test.html DataSlate_Offline/tools/update_embedded_data.py DataSlate_Offline/assets/data/data.json || true`
- `python3 DataSlate_Offline/tests/etap7_regression.py`
- `python3 DataSlate_Offline/tests/etap7_regression.py --markdown`
- `git diff --name-only -- DataSlate`

## Automatyczny runner dodany w Etapie 7

Dodano lekki runner bez zewnętrznych zależności:

```bash
python3 DataSlate_Offline/tests/etap7_regression.py
```

Runner wykonuje walidacje statyczne, porównania embedded JSON, skan zakazanych mechanizmów, kontrolę assetów, `node --check`, `python3 -m py_compile`, test Node VM dla `buildOfflineSlateHTML(payload)` oraz kontrolę braku zmian w chronionym folderze `DataSlate/`.

## Wyniki runnera

| Check | Result | Details |
| --- | --- | --- |
| git status snapshot | PASS | `?? DataSlate_Offline/tests/` podczas pierwszego uruchomienia po dodaniu testów; po commitowaniu testy staną się śledzone. |
| data.json parses as JSON | PASS | top-level keys=`backgrounds`, `logos`, `audios`, `fonts`, `fillers`, `importLog` |
| embedded data parses and matches data.json | PASS | `embeddedDataSlateData` w `index.html`, `index_backup.html` i `index_test.html` jest zgodne z `assets/data/data.json`. |
| index backup/test synchronized | PASS | `index_backup.html` i `index_test.html` są binarnie zgodne z `index.html`. |
| static HTML parser validation | PASS | `html.parser` zaakceptował `index.html`, `index_backup.html`, `index_test.html`. |
| index JavaScript syntax | PASS | `node --check` zaakceptował wyodrębniony skrypt JavaScript z `index.html`. |
| update_embedded_data.py compiles | PASS | `python3 -m py_compile` zaakceptował `DataSlate_Offline/tools/update_embedded_data.py`. |
| forbidden active mechanisms scan | PASS | Nie znaleziono aktywnych mechanizmów Firebase/Firestore/Send/Ping/audio/storage/postMessage/query/hash/SheetJS w aktywnej ścieżce. |
| index structure and generator function scan | PASS | Potwierdzono strukturę EN/PL, `DATA_URL`, fetch no-store, fallback embedded, funkcje generatora i markery finalnego dokumentu. |
| data and local asset integrity | PASS | `backgrounds=10`, `logos=14`, `audios=1`, `fonts=16`, `fillers=14`; wszystkie tła mają jawny `contentRect`; wszystkie wskazane assety istnieją lokalnie. |
| external dependency scan | PASS | Aktywny `index.html` używa lokalnych skryptów/stylów/assetów/danych; nazwy fontów Google pozostają tylko nieblokującymi wartościami danych. |
| Node VM generated HTML and fallback behavior | PASS | Node VM wygenerował HTML dla wariantów payloadu: `showLogo=true/false`, `fillersEnabled=true/false`, pusta wiadomość, wiadomość wieloliniowa, różne kolory i rozmiary fontów, brakujący font preset, niepoprawny `contentRect`, dwa różne tła. Potwierdzono też parsowanie embedded fallbacku. |
| protected DataSlate folder unchanged | PASS | Brak zmian w chronionym folderze `DataSlate/`. |

## Testy zakazanych mechanizmów

PASS. Aktywna ścieżka offline nie zawiera aktywnych mechanizmów:

- Firebase / Firestore / `firebase-config.js` / `config/firebase-config.js` / `initializeApp` / `getFirestore` / `dataslate/current` / `currentRef.set` / `onSnapshot`,
- przycisku lub mechanizmu Send/Wyślij,
- przycisku lub mechanizmu Ping,
- `new Audio`, `.play()`, `audioEnabled`, `messageAudioId`, `messageAudioFile`, odblokowania audio,
- `localStorage`, `sessionStorage`, `postMessage`, `location.hash`, `location.search`, `URLSearchParams`,
- SheetJS ani runtime'owego parsowania XLSX.

Uwaga: `assets/data/data.json` nadal zawiera listę `audios`, a embedded fallback zawiera te same dane. To nie jest błąd, bo runner potwierdza brak aktywnego odtwarzania i brak użycia danych audio przez renderer offline.

## Testy danych i assetów

PASS.

- `backgrounds`: 10 wpisów, każdy wskazuje istniejący lokalny plik.
- `logos`: 14 wpisów, każdy wskazuje istniejący lokalny plik.
- `audios`: 1 wpis, wskazuje istniejący lokalny plik, mimo że renderer offline go ignoruje.
- `fonts`: 16 wpisów, każdy ma wymagane pola `id`, `name`, `font`.
- `fillers`: 14 wpisów, każdy ma `prefixes` i `suffixes` jako tablice.
- Wszystkie ścieżki assetów są względne i lokalne.
- Wszystkie id teł mają jawny wpis w `CONTENT_RECTS_BY_BACKGROUND_ID`; `DEFAULT_CONTENT_RECT` także istnieje jako bezpieczny fallback.

## Test funkcjonalny bez ręcznej interakcji

PASS w wariancie automatycznym Node VM; SKIPPED/NOT AVAILABLE w wariancie prawdziwej przeglądarki headless.

Co przetestowano automatycznie:

- wyodrębniono główny skrypt z `index.html`,
- uruchomiono go w kontrolowanym kontekście Node VM z minimalnym stubem DOM,
- wywołano `buildOfflineSlateHTML(payload)` dla kilku wariantów payloadu,
- potwierdzono pełny dokument `<!doctype html>`, tło, overlay, `PAYLOAD_CONTENT_RECT`, wiadomość, logo opcjonalne, fillery opcjonalne, fallback fontu i brak mechanizmów Firebase/audio/storage/postMessage w finalnym HTML,
- potwierdzono `parseEmbeddedManifest()` dla embedded fallbacku.

Czego nie wykonano:

- nie uruchomiono realnego Chromium/Playwright/Selenium,
- nie przechwycono realnego popupu `window.open` w przeglądarce,
- nie wykonano automatycznego testu wizualnego renderingu pikselowego.

Powód: środowisko nie zawiera przeglądarki headless ani bibliotek automatyzacji przeglądarki. Nie jest to blocker Etapu 7, bo test statyczny i Node VM pokrywają logikę generowania HTML; pozostaje ryzyko środowiskowe związane z realnym renderingiem przeglądarki i blokowaniem popupów.

## Test fetch + embedded fallback

PASS w zakresie automatycznym/statycznym i Node VM.

- Potwierdzono `DATA_URL = 'assets/data/data.json'`.
- Potwierdzono `fetch(DATA_URL, { cache: 'no-store' })` w `loadManifest()`.
- Potwierdzono `try/catch` i wywołanie `parseEmbeddedManifest()` w ścieżce fallback.
- Potwierdzono, że embedded JSON jest poprawny i zgodny z `assets/data/data.json`.
- W Node VM potwierdzono, że `parseEmbeddedManifest()` zwraca dane z expected listami.

Nie wykonano realnego testu fetch w przeglądarce przez lokalny serwer, bo brak headless browsera uniemożliwił automatyczne sprawdzenie zachowania DOM w Chromium/Playwright.

## Problemy znalezione i poprawki

- Nie znaleziono błędów w aktywnym generatorze wymagających zmiany `index.html`.
- Nie zmieniono `index.html`, `index_backup.html`, `index_test.html`, `assets/data/data.json` ani `tools/update_embedded_data.py`.
- Dodano wyłącznie test runner, raport i dokumentację Etapu 7.

## Decyzja o blockerach

Brak blockerów kodowych dla Etapu 8.

Pozostające ryzyka są ograniczeniami środowiskowymi:

- brak automatycznego testu w prawdziwej przeglądarce headless,
- brak automatycznego testu `file://` na Windows,
- brak porównania wizualnego/screenshotowego.

Te ryzyka nie blokują PR, ponieważ użytkownik wyraźnie nie wymaga ręcznych testów i polecił nie blokować PR wyłącznie z powodu technicznie niemożliwych testów środowiskowych.

## Rekomendacje dla Etapu 8

1. Jeżeli w przyszłym środowisku będzie dostępny Chromium/Playwright, dodać opcjonalny test E2E przechwytujący `window.open` i sprawdzający wygenerowaną kartę w realnym DOM.
2. Rozważyć automatyczny screenshot/regresję wizualną dopiero po świadomym dodaniu lekkiej i akceptowalnej infrastruktury headless.
3. Utrzymać obecny lekki runner jako szybki test regresyjny po każdej zmianie w `DataSlate_Offline/index.html`, danych lub narzędziu synchronizacji.

## Wniosek

Etap 7 został zakończony w zakresie możliwym automatycznie w środowisku Codex. Aktywny generator pozostaje wolny od Firebase/audio/Ping/Send/storage/postMessage/query/hash, pliki `index.html`, `index_backup.html` i `index_test.html` są zsynchronizowane, embedded fallback jest zgodny z `assets/data/data.json`, domyślny angielski i ręczny polski pozostają zachowane. Można przejść do Etapu 8.
