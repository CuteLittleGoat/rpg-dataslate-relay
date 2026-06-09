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

## Aktualizacja — 2026-06-09 — plan wdrożenia i pytania biznesowe

### Oryginalny pełny prompt użytkownika

Przeczytaj analizę DataSlate_Offline/Offline.md
Dopisz do niej plan wdrożenia oraz pytania dotyczące ewentualnych decyzji biznesowych.

### Zakres prac

- Przeczytano aktualną analizę i ustalenia w `DataSlate_Offline/Offline.md`.
- Dopisano plan wdrożenia dla przejścia z kopii modułu online do samodzielnego generatora offline.
- Dopisano listę pytań biznesowych i produktowych, które warto rozstrzygnąć przed lub w trakcie implementacji.
- Nie zmieniono kodu aplikacji, assetów, konfiguracji Firebase ani plików w chronionym folderze `DataSlate/`.

### Plan wdrożenia

#### Etap 0 — inwentaryzacja i zabezpieczenie zakresu

1. Sprawdzić aktualny stan folderu `DataSlate_Offline/` oraz listę plików pochodzących z kopii wersji online.
2. Potwierdzić, które pliki są faktycznie używane jako wejście aplikacji offline: `index.html`, `GM.html`, `DataSlate.html`, pliki testowe, backupy, dokumentacja oraz `assets/data/data.json`.
3. Oznaczyć folder `DataSlate/` jako wyłącznie referencyjny i nie modyfikować go w ramach wdrożenia offline.
4. Zidentyfikować wszystkie miejsca w `DataSlate_Offline/`, które importują Firebase, odwołują się do Firestore, wykonują `onSnapshot(...)`, `currentRef.set(...)`, obsługują `ping`, `clear` albo audio.
5. Zidentyfikować wszystkie zewnętrzne zależności sieciowe: CDN, zdalne fonty, zdalne skrypty, zdalne grafiki, zdalne pliki JSON.

#### Etap 1 — decyzja o strukturze aplikacji

1. Wybrać wariant docelowy:
   - preferowany: jeden główny plik `index.html`, który zawiera panel generatora i funkcję budującą nową kartę;
   - alternatywny: zachowany podział `GM.html` + `DataSlate.html`, ale bez Firebase i z lokalnym przekazaniem payloadu.
2. Jeżeli zostanie wybrany wariant z jednym `index.html`, zaplanować migrację użytecznej logiki z `GM.html` i `DataSlate.html` do jednej ścieżki wykonania.
3. Jeżeli zostanie zachowany wariant wieloplikowy, ustalić, czy payload ma być przekazywany przez `sessionStorage`, `localStorage`, `postMessage`, hash/query string, czy generowanie kompletnego dokumentu przez `document.write(...)`.
4. Uporządkować role plików testowych i backupowych: zdecydować, czy zostają jako materiały referencyjne, czy po wdrożeniu będą usunięte z modułu offline.

#### Etap 2 — przygotowanie lokalnych danych i assetów

1. Zweryfikować strukturę `assets/data/data.json` jako podstawowe źródło danych dla generatora.
2. Sprawdzić, czy JSON zawiera komplet wymaganych list i mapowań:
   - tła,
   - logotypy,
   - fonty,
   - fillery,
   - ścieżki assetów,
   - ustawienia ramek i layoutu zależne od tła,
   - dane potrzebne do prefixów i suffixów.
3. Potwierdzić, że wszystkie ścieżki w danych wskazują na lokalne pliki w `DataSlate_Offline/`.
4. Odłączyć aplikację od runtime’owego parsowania `DataSlate_manifest.xlsx`; plik może zostać wyłącznie jako materiał źródłowy/deweloperski, jeśli jest nadal potrzebny.
5. Ustalić minimalny zestaw danych testowych pozwalający sprawdzić każdy typ tła, logotypu, fontu i fillera.

#### Etap 3 — przebudowa panelu generatora

1. Dostosować UI do trybu offline:
   - zmienić nazwę modułu na wariant offline,
   - usunąć lub ukryć status Firebase,
   - usunąć przyciski `Wyślij` i `Ping`,
   - dodać przycisk `Generuj`,
   - usunąć lub ukryć opcje audio,
   - dodać komunikat, że aplikacja generuje statyczny ekran w nowej karcie i niczego nie wysyła do sieci.
2. Zachować kontrolki potrzebne Mistrzowi Gry:
   - wybór tła,
   - wybór logotypu,
   - przełącznik widoczności loga,
   - wybór fontu,
   - wybór fillera,
   - ustawienia kolorów,
   - ustawienia efektów wizualnych,
   - treść wiadomości,
   - liczba linii fillerów.
3. Zbudować lokalną funkcję tworzenia payloadu na podstawie obecnej logiki `getPayload(...)`, bez zapisu do Firebase.
4. Zachować strukturę payloadu możliwie zgodną z wersją online, ale pola Firebase/audio/ping traktować jako nieaktywne albo ignorowane.

#### Etap 4 — lokalne generowanie nowej karty

1. Dodać funkcję w stylu `openOfflineSlate(payload)`, która:
   - pobiera lokalnie zbudowany payload,
   - generuje kompletny dokument HTML dla statycznego widoku,
   - otwiera nową kartę przez `window.open("", "_blank")`,
   - zapisuje dokument przez `document.open()`, `document.write(html)`, `document.close()`,
   - pokazuje czytelny komunikat, jeśli przeglądarka zablokuje popup.
2. Dodać funkcję `buildOfflineSlateHTML(payload)`, która tworzy samowystarczalny dokument nowej karty z lokalnymi ścieżkami do assetów.
3. Zadbać, aby wygenerowana karta była gotowa do screenshotu od razu po otwarciu, bez oczekiwania na Firebase, kliknięcie odblokowujące audio albo komunikację z inną kartą.
4. Nie dodawać żadnej zewnętrznej zależności sieciowej.

#### Etap 5 — adaptacja renderera DataSlate

1. Przenieść lub zaadaptować z obecnego `DataSlate.html` logikę odpowiedzialną za:
   - tło,
   - logo,
   - kolorowanie/maskowanie loga,
   - font,
   - kolory tekstu i akcentów,
   - ramkę/obszar treści,
   - fillery prefix/suffix,
   - dopasowanie do rozmiaru okna,
   - efekty wizualne, które mają sens w statycznym widoku.
2. Usunąć z renderera:
   - `onSnapshot(...)`,
   - typy wiadomości `ping` i `clear`,
   - audio,
   - inicjalizację Firebase,
   - komunikaty połączenia z Firebase.
3. Renderer powinien otrzymywać payload bezpośrednio z generatora i natychmiast wywoływać renderowanie widoku.
4. Jeżeli jakieś efekty wizualne są dynamiczne, ale nadal przydatne do screenshotu, pozostawić je tylko wtedy, gdy nie wymagają sieci ani audio.

#### Etap 6 — porządki po Firebase i audio

1. Usunąć lub odłączyć importy Firebase z aktywnej ścieżki aplikacji offline.
2. Upewnić się, że brak pliku konfiguracyjnego Firebase nie powoduje błędów w konsoli.
3. Usunąć lub ukryć dokumentację Firebase z interfejsu użytkownika offline; jeżeli pliki dokumentacyjne zostają w repozytorium, oznaczyć je jako historyczne albo nieużywane przez tryb offline.
4. Usunąć z aktywnej ścieżki aplikacji odtwarzanie `Ping.mp3` i dźwięku wiadomości.
5. Jeżeli pola audio zostają w payloadzie dla zgodności, opisać je jako ignorowane przez renderer offline.

#### Etap 7 — testy funkcjonalne i regresyjne

1. Uruchomić moduł lokalnie bez konfiguracji Firebase.
2. Sprawdzić, czy panel generatora otwiera się bez błędów Firebase.
3. Kliknąć `Generuj` i potwierdzić, że powstaje nowa karta.
4. Zweryfikować w nowej karcie:
   - wybrane tło,
   - logo włączone i wyłączone,
   - wybrany font,
   - kolory tekstu i akcentów,
   - treść wiadomości,
   - fillery prefix/suffix,
   - layout zależny od tła,
   - efekty wizualne.
5. Sprawdzić, że aplikacja nie próbuje odtwarzać audio.
6. Sprawdzić w narzędziach developerskich albo automatycznym teście, że aplikacja nie wykonuje zewnętrznych żądań sieciowych.
7. Porównać wizualnie wygenerowaną kartę offline z analogicznym ekranem normalnego DataSlate dla tego samego payloadu, o ile wersja online jest dostępna jako referencja.
8. Udokumentować wyniki testów w `Offline.md` po każdej zmianie implementacyjnej.

#### Etap 8 — dokumentacja i finalizacja

1. Zaktualizować `Offline.md` po każdej zmianie, zgodnie z przyjętym formatem dziennika.
2. Zaktualizować widoczne instrukcje w UI, aby użytkownik wiedział, że moduł działa lokalnie i generuje ekran do screenshotu.
3. Jeżeli zostaną zachowane pliki backupowe/testowe, opisać ich rolę albo ryzyko utrzymaniowe.
4. Przygotować krótką instrukcję użycia:
   - otwórz `index.html`,
   - ustaw parametry,
   - kliknij `Generuj`,
   - wykonaj screenshot nowej karty.
5. Po wdrożeniu rozważyć osobny krok porządkowy usuwający martwe pliki i dokumentację online, ale tylko po potwierdzeniu decyzji biznesowej.

### Pytania dotyczące ewentualnych decyzji biznesowych

#### Zakres produktu

1. Czy `DataSlate_Offline` ma być wyłącznie narzędziem do screenshotów przed sesją, czy ma również obsługiwać użycie na żywo przy stole bez internetu?
2. Czy moduł offline ma zastąpić w praktyce część zastosowań wersji online, czy ma być tylko narzędziem pomocniczym dla Mistrza Gry?
3. Czy priorytetem jest maksymalna zgodność wizualna z obecnym DataSlate, czy dopuszczalne są uproszczenia, jeśli znacząco skrócą wdrożenie?
4. Czy wymagany jest tryb porównawczy online/offline dla testów, czy wystarczy ręczne porównanie z wersją referencyjną?

#### UX i nazewnictwo

1. Jaka ma być finalna nazwa widoczna w interfejsie: `DataSlate Offline`, `DataSlate — generator offline`, czy inna?
2. Czy użytkownik ma widzieć informację, że moduł nie używa Firebase i nie wysyła danych do sieci?
3. Czy w interfejsie mają pozostać jakiekolwiek ślady terminologii z wersji online, np. `Wyślij`, `Ping`, `połączenie`, `odbiornik`, czy należy je całkowicie usunąć?
4. Czy generator ma ostrzegać przy próbie otwarcia wielu kart, czy każde kliknięcie `Generuj` powinno po prostu tworzyć nową kartę?

#### Zakres funkcjonalny

1. Czy wszystkie efekty wizualne z wersji online są wymagane w wersji offline, czy część można pominąć jako nieistotną dla statycznego screenshotu?
2. Czy audio ma zostać całkowicie usunięte z UI i kodu aktywnego, czy tylko ignorowane dla zgodności payloadu?
3. Czy akcje typu `clear` i `ping` mają zostać całkowicie usunięte, czy zachowane wyłącznie jako nieaktywne pola kompatybilności?
4. Czy generator powinien pozwalać zapisać/pobrać wygenerowany payload jako JSON do późniejszego użycia?
5. Czy potrzebny jest przycisk resetowania formularza do ustawień domyślnych?
6. Czy potrzebny jest przycisk kopiowania payloadu albo eksportu gotowego HTML-a?

#### Dane i assety

1. Czy `DataSlate_manifest.xlsx` ma pozostać w repozytorium jako źródło danych, czy po wygenerowaniu `assets/data/data.json` powinien zostać usunięty z modułu offline?
2. Kto będzie właścicielem procesu aktualizacji `assets/data/data.json`, gdy zmienią się tła, logotypy, fonty albo fillery?
3. Czy wszystkie assety z wersji online mają zostać skopiowane do offline, czy tylko wybrany zestaw potrzebny do screenshotów?
4. Czy istnieją assety, których nie wolno dystrybuować w pakiecie offline ze względów licencyjnych?
5. Czy offline ma wspierać własne assety użytkownika dodawane lokalnie, czy tylko assety dostarczone w repozytorium?

#### Dystrybucja i środowisko użycia

1. Czy moduł ma działać po bezpośrednim otwarciu pliku `index.html` z dysku, czy dopuszczalne jest wymaganie prostego lokalnego serwera statycznego?
2. Jakie przeglądarki mają być wspierane jako minimalny zakres testów?
3. Czy użytkownicy będą korzystać z modułu na desktopie, tablecie, czy także na urządzeniach mobilnych?
4. Czy docelowy screenshot ma mieć konkretną rozdzielczość albo proporcje ekranu?
5. Czy nowa karta ma być zoptymalizowana pod pełny ekran, okno przeglądarki, czy konkretny rozmiar capture’u?

#### Utrzymanie i kompatybilność

1. Czy struktura payloadu offline ma być formalnie kompatybilna z wersją online, nawet jeżeli część pól jest ignorowana?
2. Czy po zmianach w wersji online należy każdorazowo synchronizować renderer offline, czy offline ma rozwijać się niezależnie?
3. Czy pliki `GM_backup.html`, `DataSlate_backup.html`, `GM_test.html` i `DataSlate_test.html` mają pozostać w module, czy powinny zostać usunięte po zakończeniu migracji?
4. Czy dokumentacja Firebase w `DataSlate_Offline/config/` ma zostać zachowana jako historyczna, czy usunięta, aby nie sugerowała zależności online?
5. Czy wymagany jest automatyczny test wykrywający zewnętrzne żądania sieciowe albo importy Firebase w aktywnej ścieżce aplikacji?

#### Kryteria akceptacji

1. Czy akceptacja ma wymagać pełnej zgodności wizualnej z normalnym DataSlate, czy wystarczy zgodność funkcjonalna i ogólna zgodność stylu?
2. Jaki minimalny zestaw kombinacji tło/logo/font/filler powinien zostać przetestowany przed uznaniem wdrożenia za zakończone?
3. Czy test screenshotowy ma być wykonywany ręcznie, czy warto dodać automatyczny test wizualny?
4. Czy brak jakichkolwiek zewnętrznych żądań sieciowych ma być formalnym kryterium blokującym odbiór?
5. Czy brak Firebase w aktywnej ścieżce działania ma być weryfikowany ręcznie, czy automatycznie przez wyszukiwanie/import scan?

### Ustalenia i decyzje

- Na tym etapie dopisano plan i pytania, ale nie podjęto jeszcze decyzji implementacyjnych zmieniających kod.
- Plan utrzymuje założenie, że `DataSlate_Offline` ma działać lokalnie, bez Firebase, bez sieci i bez audio.
- Rekomendowany kierunek wdrożenia pozostaje zgodny z wcześniejszą analizą: lokalny formularz buduje payload, a następnie lokalny renderer generuje gotową kartę do screenshotu.
- Pytania biznesowe powinny zostać rozstrzygnięte przed większym refaktorem, szczególnie w obszarach: zgodność wizualna, dystrybucja, zakres assetów, rola plików backup/test oraz kryteria akceptacji.

### Zmienione pliki

- `DataSlate_Offline/Offline.md` — dopisano pełny prompt użytkownika, plan wdrożenia, pytania biznesowe, ustalenia, informację o braku zmian w kodzie oraz test dokumentacyjny.

### Szczegóły zmian

- Stan przed zmianą: `Offline.md` zawierał analizę docelowego działania modułu offline, rekomendowaną architekturę, listę elementów Firebase/audio do usunięcia oraz ogólne uwagi implementacyjne.
- Stan po zmianie: dokument zawiera dodatkowo etapowy plan wdrożenia oraz listę pytań biznesowych i produktowych potrzebnych do domknięcia zakresu.
- Powód zmiany: użytkownik poprosił o przeczytanie analizy i dopisanie planu wdrożenia oraz pytań dotyczących decyzji biznesowych.
- Kod aplikacji nie został zmieniony.

### Testy

- Sprawdzono, że zmiana dotyczy wyłącznie dokumentacji w `DataSlate_Offline/Offline.md`.
- Nie wykonywano testów funkcjonalnych aplikacji, ponieważ zadanie miało charakter dokumentacyjny i nie obejmowało zmian kodu.

### Ryzyka i następne kroki

- Przed implementacją należy rozstrzygnąć pytania biznesowe dotyczące zakresu zgodności wizualnej, sposobu dystrybucji, wsparcia przeglądarek oraz utrzymania danych i assetów.
- Należy szczególnie uważać, aby podczas kolejnych etapów nie modyfikować chronionego folderu `DataSlate/`.
- Następny rekomendowany krok techniczny to inwentaryzacja aktywnych zależności Firebase, audio i sieciowych w `DataSlate_Offline/` oraz wskazanie najmniejszego bezpiecznego zakresu pierwszego refaktoru.
