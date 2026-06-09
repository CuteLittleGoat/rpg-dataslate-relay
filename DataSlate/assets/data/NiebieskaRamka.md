# NiebieskaRamka — wyliczanie pola roboczego (`CONTENT_RECTS_BY_BACKGROUND_ID`)

Ten plik opisuje dokładnie, jak liczę prostokąt treści (`x, y, w, h`) dla każdego tła na podstawie pliku `*_ramka.png` z niebieską ramką.

## 1) Pliki źródłowe
- Mapa przypisań tło -> ramka: `DataSlate/assets/data/Mapowanie.xlsx`.
- Grafiki ramek: `DataSlate/assets/ramki/*_ramka.png`.
- Miejsce użycia wyników: `DataSlate/DataSlate_test.html` -> `CONTENT_RECTS_BY_BACKGROUND_ID`.

## 2) Definicja współczynników
Dla każdej ramki liczę pikselowy bounding box niebieskiego obszaru:
- `minX`, `minY` — lewa/górna krawędź ramki,
- `maxX`, `maxY` — prawa/dolna krawędź ramki,
- `imgW`, `imgH` — szerokość i wysokość pliku PNG.

Następnie normalizuję do zakresu 0..1:
- `x = minX / imgW`
- `y = minY / imgH`
- `w = (maxX - minX + 1) / imgW`
- `h = (maxY - minY + 1) / imgH`

Finalnie wartości zapisuję do 4 miejsc po przecinku (tak jak w kodzie).

## 3) Reguła wykrywania niebieskiej ramki
Piksel należy do ramki, gdy:
- alfa `a > 0` (piksel widoczny),
- kanał niebieski dominuje:
  - `b > 140`,
  - `b > r + 30`,
  - `b > g + 15`.

Ta reguła odtwarza dotychczasowe współrzędne 1:1 dla istniejących teł (DataSlate_01..Pergamin) i daje spójny wynik dla nowych ramek.

## 4) Wynik dla nowego tła WnG
Plik: `DataSlate/assets/ramki/WnG_ramka.png`
- Wymiary PNG: `1549 x 2048`
- Bounding box: `minX=188`, `minY=197`, `maxX=1331`, `maxY=1851`
- Współczynniki:
  - `x = 0.1214`
  - `y = 0.0962`
  - `w = 0.7385`
  - `h = 0.8081`

Wpis do `CONTENT_RECTS_BY_BACKGROUND_ID`:
```js
10:{ x:0.1214, y:0.0962, w:0.7385, h:0.8081 } // WnG
```


## 4a) Wynik po podmianie pliku `Pergamin_ramka.png` (2026-04-22)
Plik: `DataSlate/assets/ramki/Pergamin_ramka.png`
- Wymiary PNG: `1024 x 1536`
- Bounding box: `minX=79`, `minY=200`, `maxX=966`, `maxY=1270`
- Współczynniki:
  - `x = 0.0771`
  - `y = 0.1302`
  - `w = 0.8672`
  - `h = 0.6973`

Wpis do `CONTENT_RECTS_BY_BACKGROUND_ID`:
```js
9:{ x:0.0771, y:0.1302, w:0.8672, h:0.6973 } // Pergamin
```

## 5) Procedura przy dodawaniu kolejnego tła
1. Dodaj plik tła do `assets/backgrounds/`.
2. Dodaj odpowiadającą ramkę do `assets/ramki/`.
3. Dopisz mapowanie w `assets/data/Mapowanie.xlsx` (ID, nazwa, link tła, link ramki).
4. Wylicz `x,y,w,h` metodą z tego pliku i dopisz wpis w `CONTENT_RECTS_BY_BACKGROUND_ID`.
5. Upewnij się, że `backgroundId` w payloadzie (GM) odpowiada temu samemu ID.
6. Jeżeli nowe tło ma być domyślne, ustaw `DEFAULT_FORM_STATE.backgroundId` w `GM_test.html`.
7. Zaktualizuj dokumentację (`docs/README.md`, `docs/Documentation.md`).

## 6) Notatki praktyczne
- `Mapowanie.xlsx` służy jako źródło przypisania, ale URL może zawierać literówkę — traktuj nazwę pliku ramki jako źródło prawdy i zawsze sprawdzaj fizyczną obecność pliku w `assets/ramki/`.
- Jeśli kolor ramki będzie inny niż niebieski, trzeba zmienić progi detekcji koloru.
- Jeżeli ramka ma antyaliasing, powyższe progi nadal działają, bo używają dominacji kanału `b`, a nie pojedynczej wartości RGB.
