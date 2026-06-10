# Etap 8 — raport regresji DataSlate Offline

Data aktualizacji raportu: 2026-06-10.

## Zakres raportu

Raport obejmuje aktualny runner `DataSlate_Offline/tests/etap7_regression.py` po finalizacji Etapu 8. Runner zachowuje nazwę pliku z poprzedniego etapu dla ciągłości, ale waliduje także nowy oczekiwany stan po cleanupie: brak legacy plików GM/DataSlate oraz brak dawnej konfiguracji Firebase w `DataSlate_Offline/config/`.

Runner wykonuje walidacje statyczne, porównania embedded JSON, kontrolę synchronizacji `index.html` / `index_backup.html` / `index_test.html`, skan zakazanych aktywnych mechanizmów, kontrolę assetów, `node --check`, `python3 -m py_compile`, test Node VM dla `buildOfflineSlateHTML(payload)`, test architektury pól kolorów i preview oraz kontrolę braku zmian w chronionym folderze `DataSlate/`.

## Wynik ostatniego uruchomienia

Komenda:

```bash
python3 DataSlate_Offline/tests/etap7_regression.py --markdown
```

| Check | Result | Details |
| --- | --- | --- |
| git status snapshot | PASS | D DataSlate_Offline/DataSlate.html<br> D DataSlate_Offline/DataSlate_backup.html<br> D DataSlate_Offline/DataSlate_test.html<br> M DataSlate_Offline/Disclaimer.md<br> D DataSlate_Offline/GM.html<br> D DataSlate_Offline/GM_backup.html<br> D DataSlate_Offline/GM_test.html<br> M DataSlate_Offline/Offline.md<br> M DataSlate_Offline/assets/data/NiebieskaRamka.md<br> D DataSlate_Offline/config/FirebaseREADME.md<br> D DataSlate_Offline/config/firebase-config.js<br> M DataSlate_Offline/docs/Documentation.md<br> M DataSlate_Offline/docs/README.md<br> M DataSlate_Offline/tests/Etap7_report.md<br> M DataSlate_Offline/tests/etap7_regression.py<br>?? DataSlate_Offline/README.md |
| data.json parses as JSON | PASS | top-level keys=backgrounds, logos, audios, fonts, fillers, importLog |
| embedded data parses and matches data.json | PASS | embeddedDataSlateData in all index files matches assets/data/data.json |
| index backup/test synchronized | PASS | index_backup.html and index_test.html are byte-identical to index.html |
| legacy GM/DataSlate cleanup | PASS | legacy GM/DataSlate/Firebase files are absent from DataSlate_Offline |
| static HTML parser validation | PASS | Python html.parser accepted index.html/index_backup.html/index_test.html |
| index JavaScript syntax | PASS | node --check accepted extracted index.html script |
| update_embedded_data.py compiles | PASS | python3 -m py_compile accepted update_embedded_data.py |
| forbidden active mechanisms scan | PASS | no active Firebase/Firestore/Send/Ping/audio/storage/postMessage/query/hash/SheetJS mechanisms found |
| index structure and generator function scan | PASS | index structure, language defaults, fetch path, embedded fallback, generator functions and generated document markers verified |
| color controls and shared preview renderer scan | PASS | color controls keep last valid hex without renderPreview mutations; preview iframe uses buildOfflineSlateHTML(payload) |
| data and local asset integrity | PASS | backgrounds=10, logos=14, audios=1, fonts=16, fillers=14; all backgrounds have explicit content rects |
| external dependency scan | PASS | active index uses local scripts/styles/assets/data only; Google font names remain non-blocking data values |
| Node VM generated HTML and fallback behavior | PASS | Node VM generated HTML test passed for fractional contentRect, user-reported overlay variant, timestamp title, logo/filler/message/color variants and embedded fallback parsing |
| protected DataSlate folder unchanged | PASS | no git diff under protected DataSlate/ folder |

## Pokrycie po Etapie 8

- Test statyczny potwierdza, że `index_backup.html` i `index_test.html` są bajtowo zgodne z aktywnym `index.html`.
- Test statyczny potwierdza nieobecność plików `GM.html`, `DataSlate.html`, wariantów backup/test oraz dawnej konfiguracji Firebase w katalogu `config/`.
- Test statyczny potwierdza, że aktywna ścieżka nie używa Firebase/Firestore, storage, `postMessage`, hash/query string, runtime XLSX, audio playback, Ping ani Send/Wyślij.
- Test Node VM potwierdza, że finalny HTML zawiera tekst wiadomości, fillery, logo przy `showLogo: true`, brak logo przy `showLogo: false`, tytuł `DataSlate` z timestampem oraz różne kolory wiadomości/fillerów/logo.

## Uwagi środowiskowe

- Runner pozostaje testem statycznym i Node VM; nie instaluje zależności przeglądarkowych.
- Weryfikacja wizualna w realnej przeglądarce nadal jest zalecana jako końcowy test UX, szczególnie dla różnic skalowania preview względem nowej karty przy innym rozmiarze viewportu.
