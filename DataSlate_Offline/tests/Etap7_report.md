# Etap 7 — raport regresji DataSlate Offline

Data aktualizacji raportu: 2026-06-10.

## Zakres raportu

Raport obejmuje aktualny runner `DataSlate_Offline/tests/etap7_regression.py` po poprawce obsługi kolorów oraz przebudowie Working preview tak, aby korzystał z tego samego renderera co finalna karta generowana przez `buildOfflineSlateHTML(payload)`.

Runner wykonuje walidacje statyczne, porównania embedded JSON, skan zakazanych mechanizmów, kontrolę assetów, `node --check`, `python3 -m py_compile`, test Node VM dla `buildOfflineSlateHTML(payload)`, test architektury pól kolorów i preview oraz kontrolę braku zmian w chronionym folderze `DataSlate/`.

## Wynik ostatniego uruchomienia

Komenda:

```bash
python3 DataSlate_Offline/tests/etap7_regression.py --markdown
```

| Check | Result | Details |
| --- | --- | --- |
| git status snapshot | PASS | M DataSlate_Offline/Offline.md<br> M DataSlate_Offline/index.html<br> M DataSlate_Offline/index_backup.html<br> M DataSlate_Offline/index_test.html<br> M DataSlate_Offline/tests/Etap7_report.md<br> M DataSlate_Offline/tests/etap7_regression.py |
| data.json parses as JSON | PASS | top-level keys=backgrounds, logos, audios, fonts, fillers, importLog |
| embedded data parses and matches data.json | PASS | embeddedDataSlateData in all index files matches assets/data/data.json |
| index backup/test synchronized | PASS | index_backup.html and index_test.html are byte-identical to index.html |
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


## Nowe pokrycie po poprawce

- Test statyczny potwierdza, że stary mutujący helper `applyColorPair(...)` nie występuje w aktywnym `index.html`.
- Test statyczny potwierdza istnienie `iframe#previewFrame` oraz przypisanie `previewFrame.srcdoc = buildOfflineSlateHTML(payload)`.
- Test statyczny sprawdza, że `renderPreview()` nie nadpisuje wartości inputów przez `.value = ...` i używa payloadu oraz wspólnego finalnego renderera.
- Test statyczny sprawdza obecność stanu ostatnich poprawnych kolorów (`validColors` / `dataset.lastValidColor`) oraz osobnych listenerów dla pickerów i pól tekstowych.
- Test Node VM potwierdza, że finalny HTML zawiera tekst wiadomości, fillery, logo przy `showLogo: true`, brak logo przy `showLogo: false`, tytuł `DataSlate` z timestampem oraz różne kolory wiadomości/fillerów/logo.

## Uwagi środowiskowe

- Runner pozostaje testem statycznym i Node VM; nie instaluje zależności przeglądarkowych.
- Weryfikacja wizualna w realnej przeglądarce nadal jest zalecana jako końcowy test UX, szczególnie dla różnic skalowania preview względem nowej karty przy innym rozmiarze viewportu.
