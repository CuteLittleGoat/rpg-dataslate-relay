# DataSlate Offline — ustalenia dotyczące modyfikacji

## Cel modułu

`DataSlate_Offline` ma być wersją modułu DataSlate działającą w pełni offline, bez integracji z Firebase. Moduł ma służyć Mistrzowi Gry do przygotowywania statycznych ekranów DataSlate przed sesją, przede wszystkim w celu wykonania screenshotów.

Wersja offline nie ma pełnić funkcji ekranu odbiorczego działającego na drugim urządzeniu. Zamiast komunikacji `GM → Firebase → DataSlate`, aplikacja ma działać lokalnie według schematu:

    DataSlate_Offline/index.html → klik „Generuj” → nowa karta przeglądarki z gotowym DataSlate

## Założenie startowe

Folder `DataSlate_Offline` jest wierną kopią obecnej wersji modułu DataSlate wymagającej integracji z Firebase. Modyfikacja powinna polegać na usunięciu zależności od Firebase i połączeniu funkcjonalności panelu GM oraz ekranu DataSlate w jednym trybie offline.

## Docelowe działanie

1. Użytkownik otwiera lokalnie `DataSlate_Offline/index.html`.
2. Wybiera tło, logo, font, filler, kolory, efekty wizualne i treść wiadomości.
3. Zamiast przycisków `Wyślij` i `Ping` dostępny jest przycisk `Generuj`.
4. Kliknięcie `Generuj` tworzy payload wiadomości lokalnie, bez zapisu do Firebase.
5. Aplikacja otwiera nową kartę przeglądarki.
6. W nowej karcie renderowany jest gotowy ekran DataSlate z wybranym tłem, logiem, tekstem, fillerami i ustawieniami wizualnymi.
7. Mistrz Gry może wykonać screenshot wygenerowanego ekranu.

## Firebase — elementy do usunięcia lub wyłączenia

W wersji offline nie są potrzebne:

- `firebase-config.js`,
- inicjalizacja Firebase,
- Firestore,
- dokument `dataslate/current`,
- `currentRef.set(...)`,
- `onSnapshot(...)`,
- logika typu `send`, `ping`, `clear` oparta o Firebase,
- komunikaty o połączeniu z Firebase,
- instrukcje konfiguracyjne Firebase w interfejsie offline.

Wersja offline nie powinna wykonywać żadnych zewnętrznych zapytań sieciowych. Wszystkie zasoby muszą być ładowane lokalnie z folderu `DataSlate_Offline`.

## Dźwięki

W wersji offline dźwięki są zbędne.

Do usunięcia albo zignorowania:

- przycisk `Ping`,
- `Ping.mp3`,
- `audioEnabled`,
- `messageAudioId`,
- `messageAudioFile`,
- odtwarzanie dźwięku przy wiadomości,
- wymóg kliknięcia ekranu w celu odblokowania audio.

Jeżeli dla zgodności z istniejącym payloadem część pól audio zostanie tymczasowo pozostawiona, renderer offline powinien je ignorować.

## Dane i manifest

Rekomendacja: wersja offline powinna korzystać z gotowego pliku:

    assets/data/data.json

Nie zaleca się opierania wersji offline na runtime’owym parsowaniu `DataSlate_manifest.xlsx`, ponieważ wymagałoby to utrzymania parsera XLSX w przeglądarce i zwiększałoby złożoność. Offline generator screenshotów powinien działać z gotowego, statycznego JSON-a.

Jeżeli obecna kopia zawiera `DataSlate_manifest.xlsx`, można go zostawić jako plik źródłowy/deweloperski, ale główna aplikacja offline powinna czytać `data.json`.

## Logika do wykorzystania z obecnego `GM.html`

Z obecnego panelu GM warto zachować:

- listy wyboru tła, logo, fontu i fillerów,
- edycję treści wiadomości,
- ustawienia kolorów,
- ustawienia widoczności loga,
- ustawienia overlay/flicker/moving overlay,
- ustawienia liczby linii fillerów,
- logikę budowania payloadu, szczególnie odpowiednik funkcji `getPayload(...)`,
- generowanie `prefixLines` i `suffixLines`,
- wybór `backgroundId`, `backgroundFile`, `logoId`, `logoFile`, `fontId`, `fontPreset`, `fillerId`, `fillerSet`.

Zamiast wysyłki do Firebase funkcja obsługi przycisku powinna wywołać lokalną funkcję generującą nową kartę, np.:

    const payload = getPayload("message");
    openOfflineSlate(payload);

## Logika do wykorzystania z obecnego `DataSlate.html`

Z obecnego ekranu DataSlate warto zachować:

- renderowanie tła,
- renderowanie loga,
- maskowanie/kolorowanie loga,
- ustawianie fontu,
- ustawianie kolorów tekstu i akcentów,
- układ treści w ramce,
- obsługę fillerów jako linii prefix/suffix,
- layout zależny od wybranego tła,
- efekty wizualne, jeśli mają sens w statycznej karcie,
- mechanizm dopasowania ekranu do rozmiaru okna.

Do usunięcia z tej części:

- nasłuchiwanie `onSnapshot`,
- reakcje na typy wiadomości `ping` i `clear`,
- audio,
- zależność od Firebase.

Renderer offline powinien przyjąć payload od razu po otwarciu nowej karty i natychmiast wyrenderować gotowy ekran.

## Proponowana architektura plików

Docelowo najprostszy wariant:

    DataSlate_Offline/
    ├── index.html
    ├── Offline.md
    ├── assets/
    │   ├── backgrounds/
    │   ├── logos/
    │   ├── data/
    │   │   └── data.json
    │   └── ...

`index.html` pełni rolę panelu generatora. Po kliknięciu `Generuj` otwiera nową kartę z wygenerowanym dokumentem HTML.

Alternatywny wariant, jeżeli łatwiej zachować podział kodu:

    DataSlate_Offline/
    ├── GM.html
    ├── DataSlate.html
    ├── Offline.md
    ├── assets/
    │   └── ...

W takim wariancie `GM.html` nie wysyła danych do Firebase, tylko otwiera `DataSlate.html` z payloadem przekazanym przez `sessionStorage`, `localStorage`, `postMessage` albo query/hash. Preferowane jest jednak generowanie kompletnego HTML-a bezpośrednio w nowej karcie, podobnie jak robi to `GeneratorNPC` przy generowaniu karty NPC.

## Preferowany sposób otwierania nowej karty

Najprostszy i najbardziej zbliżony do `GeneratorNPC`:

    function openOfflineSlate(payload) {
      const html = buildOfflineSlateHTML(payload);
      const slateWindow = window.open("", "_blank");
      if (!slateWindow) {
        alert("Nie udało się otworzyć nowej karty. Sprawdź blokadę pop-upów.");
        return;
      }
      slateWindow.document.open();
      slateWindow.document.write(html);
      slateWindow.document.close();
    }

`buildOfflineSlateHTML(payload)` powinno wygenerować kompletny dokument HTML zawierający style i skrypt potrzebny do wyrenderowania statycznego DataSlate.

## Tryb w pełni offline

Aby moduł rzeczywiście działał offline:

- nie używać Firebase,
- nie importować skryptów z CDN,
- nie polegać na zewnętrznych fontach,
- nie pobierać danych z sieci,
- używać lokalnego `assets/data/data.json`,
- używać lokalnych grafik tła i logotypów,
- zachować ścieżki względne działające po otwarciu pliku lokalnie lub przez prosty lokalny serwer statyczny.

## Elementy interfejsu do zmiany

Minimalny zakres zmian w UI:

- zmienić tytuł/etykietę modułu na wariant offline, np. `DataSlate Offline` albo `DataSlate — generator offline`,
- usunąć lub ukryć status Firebase,
- usunąć przycisk `Wyślij`,
- usunąć przycisk `Ping`,
- dodać przycisk `Generuj`,
- usunąć opcje audio albo zostawić je ukryte,
- dodać krótką informację, że moduł generuje statyczny ekran w nowej karcie i nie wysyła danych do Firebase.

## Oczekiwany efekt końcowy

Po zakończeniu modyfikacji `DataSlate_Offline` powinien być samodzielnym narzędziem offline dla Mistrza Gry:

- otwieranym lokalnie,
- niewymagającym konfiguracji Firebase,
- niewymagającym internetu,
- generującym gotowy ekran DataSlate w nowej karcie,
- nadającym się do robienia screenshotów przed sesją.

## Uwagi implementacyjne

1. Warto zachować zgodność struktury payloadu z obecną wersją online, nawet jeśli część pól będzie ignorowana. Ułatwi to późniejsze utrzymanie obu wariantów.
2. Największą wartość ma ponowne użycie obecnych funkcji renderujących z `DataSlate.html` oraz obecnej logiki budowania payloadu z `GM.html`.
3. Najważniejsza różnica architektoniczna: offline nie ma warstwy transportu. Payload nie jest wysyłany, tylko natychmiast renderowany.
4. Przy testach należy sprawdzić, czy wygenerowana karta wygląda tak samo jak karta otrzymana w normalnym DataSlate po wysłaniu tej samej wiadomości przez Firebase.
