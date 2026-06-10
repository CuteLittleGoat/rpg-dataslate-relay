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

## Aktualizacja — 2026-06-10 — odpowiedzi na pytania biznesowe i produktowe

### Oryginalny pełny prompt użytkownika

Poniżej moje odpowiedzi na zadane pytania. Dodaj je do pliku DataSlate_Offline/Offline.md

1. Czy DataSlate_Offline ma być wyłącznie narzędziem do screenshotów przed sesją, czy ma również obsługiwać użycie na żywo przy stole bez internetu?
- DataSlate Offline generuje samodzielne statyczne ekrany w nowych kartach. Nie pełni funkcji aktywnego odbiornika aktualizowanego na żywo.

2. Czy moduł offline ma zastąpić w praktyce część zastosowań wersji online, czy ma być tylko narzędziem pomocniczym dla Mistrza Gry?
- Moduł Offline ma być alternatywą dla zwykłego modułu DataSlate

3. Czy priorytetem jest maksymalna zgodność wizualna z obecnym DataSlate, czy dopuszczalne są uproszczenia, jeśli znacząco skrócą wdrożenie?
- Maksymalna zgodność wizualna

4. Czy wymagany jest tryb porównawczy online/offline dla testów, czy wystarczy ręczne porównanie z wersją referencyjną?
- Ręczne porównanie

1. Jaka ma być finalna nazwa widoczna w interfejsie: DataSlate Offline, DataSlate — generator offline, czy inna?
- DataSlate Offline

2. Czy użytkownik ma widzieć informację, że moduł nie używa Firebase i nie wysyła danych do sieci?
- Nie

3. Czy w interfejsie mają pozostać jakiekolwiek ślady terminologii z wersji online, np. Wyślij, Ping, połączenie, odbiornik, czy należy je całkowicie usunąć?
- Całkowicie usuwamy

4. Czy generator ma ostrzegać przy próbie otwarcia wielu kart, czy każde kliknięcie Generuj powinno po prostu tworzyć nową kartę?
- Bez ostrzeżeń. Każde kliknięcie to nowa karta.

1. Czy wszystkie efekty wizualne z wersji online są wymagane w wersji offline, czy część można pominąć jako nieistotną dla statycznego screenshotu?
- Prostokąt cienia i Flicker kasujemy z wersji Offline.

2. Czy audio ma zostać całkowicie usunięte z UI i kodu aktywnego, czy tylko ignorowane dla zgodności payloadu?
- Ignorowane. W UI ma nie być śladu po audio, ale plik wsadowy DataSlate_manifest.xlsx i utworzony data.json będą identyczne dla wersji Online i Offline.

3. Czy akcje typu clear i ping mają zostać całkowicie usunięte, czy zachowane wyłącznie jako nieaktywne pola kompatybilności?
- Ping jest zbędny. Clear może zostać, żeby wyczyścić tekst.

4. Czy generator powinien pozwalać zapisać/pobrać wygenerowany payload jako JSON do późniejszego użycia?
- Nie dodajemy eksportu/importu payloadu JSON. Payload istnieje tylko wewnętrznie w kodzie podczas generowania karty.

5. Czy potrzebny jest przycisk resetowania formularza do ustawień domyślnych?
- Tak

6. Czy potrzebny jest przycisk kopiowania payloadu albo eksportu gotowego HTML-a?
- Nie dodajemy przycisku kopiowania payloadu ani eksportu gotowego HTML-a. Jedyną główną akcją generującą wynik pozostaje Generuj.

1. Czy DataSlate_manifest.xlsx ma pozostać w repozytorium jako źródło danych, czy po wygenerowaniu assets/data/data.json powinien zostać usunięty z modułu offline?
- Pozostaje

2. Kto będzie właścicielem procesu aktualizacji assets/data/data.json, gdy zmienią się tła, logotypy, fonty albo fillery?
- Aktualizacja danych odbywa się przez aktualizację DataSlate_manifest.xlsx, wygenerowanie nowego assets/data/data.json oraz aktualizację odpowiednich folderów z plikami.

3. Czy wszystkie assety z wersji online mają zostać skopiowane do offline, czy tylko wybrany zestaw potrzebny do screenshotów?
- Wszystkie

4. Czy istnieją assety, których nie wolno dystrybuować w pakiecie offline ze względów licencyjnych?
- Nie

5. Czy offline ma wspierać własne assety użytkownika dodawane lokalnie, czy tylko assety dostarczone w repozytorium?
- Wersja Offline wspiera assety dostarczone w repozytorium i opisane w data.json. Nie dodajemy UI do wgrywania własnych assetów. Ewentualne nowe assety dodaje się przez aktualizację manifestu/data.json i folderów z plikami.

1. Czy moduł ma działać po bezpośrednim otwarciu pliku index.html z dysku, czy dopuszczalne jest wymaganie prostego lokalnego serwera statycznego?
- Moduł ma działać offline lokalnie z dysku c:\ oraz online poprzez host na github

2. Jakie przeglądarki mają być wspierane jako minimalny zakres testów?
- Te same co w wersji Online

3. Czy użytkownicy będą korzystać z modułu na desktopie, tablecie, czy także na urządzeniach mobilnych?
- Domyślnie na PC

4. Czy docelowy screenshot ma mieć konkretną rozdzielczość albo proporcje ekranu?
- Nie

5. Czy nowa karta ma być zoptymalizowana pod pełny ekran, okno przeglądarki, czy konkretny rozmiar capture’u?
- Nie

1. Czy struktura payloadu offline ma być formalnie kompatybilna z wersją online, nawet jeżeli część pól jest ignorowana?
- Payload Offline powinien być możliwie kompatybilny z Online, ale renderer Offline ignoruje pola audio, ping i Firebase.

2. Czy po zmianach w wersji online należy każdorazowo synchronizować renderer offline, czy offline ma rozwijać się niezależnie?
- Rozwój niezależnie

3. Czy pliki GM_backup.html, DataSlate_backup.html, GM_test.html i DataSlate_test.html mają pozostać w module, czy powinny zostać usunięte po zakończeniu migracji?
- Pliki "backup" i "test" będą potrzebne również w wersji Offline. Po zakończeniu projektu wszystkie będą zawierać dokładnie ten sam kod.

4. Czy dokumentacja Firebase w DataSlate_Offline/config/ ma zostać zachowana jako historyczna, czy usunięta, aby nie sugerowała zależności online?
- Dokumentacja oraz Readme będą do przepisania

5. Czy wymagany jest automatyczny test wykrywający zewnętrzne żądania sieciowe albo importy Firebase w aktywnej ścieżce aplikacji?
- Nie dodajemy automatycznego testu. Weryfikacja braku Firebase i zewnętrznych żądań będzie ręczna podczas odbioru.

1. Czy akceptacja ma wymagać pełnej zgodności wizualnej z normalnym DataSlate, czy wystarczy zgodność funkcjonalna i ogólna zgodność stylu?
- Offline ma być możliwie jaknajbardziej zbliżony do wersji Online.

2. Jaki minimalny zestaw kombinacji tło/logo/font/filler powinien zostać przetestowany przed uznaniem wdrożenia za zakończone?
- Wdrożenie będzie zakończone jak uznam, że wszystko działa jak oczekuję.

3. Czy test screenshotowy ma być wykonywany ręcznie, czy warto dodać automatyczny test wizualny?
- Testy wizualne robimy ręcznie. Nie dodajemy automatycznego porównywania screenshotów.

4. Czy brak jakichkolwiek zewnętrznych żądań sieciowych ma być formalnym kryterium blokującym odbiór?
- Nie rozumiem pytania

5. Czy brak Firebase w aktywnej ścieżce działania ma być weryfikowany ręcznie, czy automatycznie przez wyszukiwanie/import scan?
- Brak Firebase, CDN i zewnętrznych usług jest wymaganiem. Sprawdzamy to ręcznie, nie automatycznym testem.

### Zakres prac

- Przeczytano aktualną treść `DataSlate_Offline/Offline.md` przed zmianą dokumentacji.
- Dopisano pełny prompt użytkownika zawierający odpowiedzi na wcześniej zapisane pytania biznesowe i produktowe.
- Dopisano syntetyczne ustalenia wynikające z odpowiedzi, aby kolejne prace implementacyjne mogły korzystać z nich jako z decyzji projektowych.
- Nie zmieniono kodu aplikacji, assetów, danych JSON, manifestu XLSX ani chronionego folderu `DataSlate/`.

### Ustalenia i decyzje

- `DataSlate Offline` generuje samodzielne statyczne ekrany w nowych kartach i nie jest aktywnym odbiornikiem aktualizowanym na żywo.
- Moduł offline ma być alternatywą dla zwykłego DataSlate, a nie jedynie pobocznym narzędziem pomocniczym.
- Priorytetem jest maksymalna możliwa zgodność wizualna z wersją online; porównanie będzie wykonywane ręcznie.
- Finalna nazwa w interfejsie to `DataSlate Offline`.
- Interfejs nie powinien pokazywać komunikatu o braku Firebase ani o niewysyłaniu danych do sieci.
- Z interfejsu należy całkowicie usunąć ślady terminologii online: `Wyślij`, `Ping`, `połączenie`, `odbiornik`.
- Każde kliknięcie `Generuj` ma tworzyć nową kartę bez ostrzeżeń o wielu kartach.
- Z wersji offline należy usunąć prostokąt cienia i efekt Flicker.
- Audio ma być ignorowane w aktywnym działaniu; UI nie może zawierać śladów audio, ale `DataSlate_manifest.xlsx` i `assets/data/data.json` mają pozostać zgodne między wersją Online i Offline.
- `Ping` jest zbędny, natomiast `Clear` może zostać jako akcja czyszcząca tekst.
- Nie dodajemy eksportu/importu payloadu JSON, kopiowania payloadu ani eksportu gotowego HTML-a; payload istnieje tylko wewnętrznie podczas generowania karty.
- Należy dodać przycisk resetowania formularza do ustawień domyślnych.
- `DataSlate_manifest.xlsx` pozostaje w repozytorium jako źródło danych, a aktualizacja danych odbywa się przez aktualizację manifestu, wygenerowanie nowego `assets/data/data.json` i aktualizację folderów z plikami.
- Wersja offline ma zawierać wszystkie assety z wersji online; nie ma wskazanych ograniczeń licencyjnych dla dystrybucji pakietu offline.
- Własne assety użytkownika nie dostają osobnego UI; nowe assety dodaje się przez manifest, `data.json` i foldery z plikami.
- Moduł ma działać lokalnie z dysku `c:\` oraz online przez host na GitHub.
- Minimalny zakres przeglądarek jest taki sam jak w wersji online, a domyślnym środowiskiem użycia jest PC.
- Screenshot nie ma narzuconej konkretnej rozdzielczości, proporcji ani zoptymalizowanego rozmiaru capture’u.
- Payload offline powinien być możliwie kompatybilny z payloadem online, ale renderer offline ignoruje pola audio, ping i Firebase.
- Wersja offline ma rozwijać się niezależnie od wersji online.
- Pliki `GM_backup.html`, `DataSlate_backup.html`, `GM_test.html` i `DataSlate_test.html` mają pozostać w module; po zakończeniu projektu wszystkie mają zawierać dokładnie ten sam kod.
- Dokumentacja oraz README w module offline będą do przepisania, aby nie sugerować zależności online.
- Nie dodajemy automatycznych testów wykrywających zewnętrzne żądania, Firebase/CDN ani automatycznego porównywania screenshotów; weryfikacja pozostaje ręczna.
- Brak Firebase, CDN i zewnętrznych usług pozostaje wymaganiem modułu offline, mimo że nie będzie sprawdzany automatycznym testem.
- Akceptacja wdrożenia nastąpi wtedy, gdy użytkownik uzna, że wszystko działa zgodnie z oczekiwaniami.

### Zmienione pliki

- `DataSlate_Offline/Offline.md` — dopisano pełny prompt użytkownika oraz decyzje projektowe wynikające z odpowiedzi na pytania biznesowe i produktowe.

### Szczegóły zmian

- Stan przed zmianą: `Offline.md` zawierał plan wdrożenia i listę pytań biznesowych bez odpowiedzi.
- Stan po zmianie: dokument zawiera pełne odpowiedzi użytkownika oraz uporządkowaną listę decyzji dotyczących roli modułu, UI, efektów, audio, danych, assetów, środowiska, kompatybilności, dokumentacji i testów.
- Powód zmiany: użytkownik poprosił o dodanie odpowiedzi do `DataSlate_Offline/Offline.md`.
- Kod aplikacji nie został zmieniony.

### Testy

- Sprawdzono status repozytorium przed zmianą.
- Sprawdzono aktualną treść `DataSlate_Offline/Offline.md` przed dopisaniem nowej sekcji.
- Sprawdzono różnicę w Git po zmianie dokumentacji.
- Nie wykonywano testów funkcjonalnych aplikacji, ponieważ zadanie dotyczyło wyłącznie aktualizacji dokumentacji i nie zmieniało aktywnej ścieżki działania modułu.

### Ryzyka i następne kroki

- W kolejnych etapach implementacji należy pamiętać, że część wcześniejszych rekomendacji została doprecyzowana: w UI nie ma być informacji o braku Firebase, efekt Flicker i prostokąt cienia mają zostać usunięte, a przycisk resetowania formularza jest wymagany.
- Odpowiedź „Nie rozumiem pytania” przy formalnym kryterium blokującym brak zewnętrznych żądań oznacza, że wymaganie braku Firebase/CDN/zewnętrznych usług pozostaje ważne, ale sposób odbioru i kryterium blokujące należy w razie potrzeby doprecyzować w rozmowie.
- Następny rekomendowany krok to przełożenie decyzji z tej sekcji na minimalny zakres zmian w interfejsie i aktywnej ścieżce `DataSlate_Offline`.

## Aktualizacja — 2026-06-10 — Etap 0: inwentaryzacja i zabezpieczenie zakresu

### Oryginalny pełny prompt użytkownika

Przeczytaj plik DataSlate_Offline/Offline.md a następnie zrealizuj:
Etap 0 — inwentaryzacja i zabezpieczenie zakresu

### Zakres prac

- Przeczytano aktualną treść `DataSlate_Offline/Offline.md` przed rozpoczęciem inwentaryzacji.
- Sprawdzono aktualny stan repozytorium przed zmianą dokumentacji; drzewo robocze było czyste.
- Zinwentaryzowano pliki i podfoldery w `DataSlate_Offline/` bez modyfikowania chronionego folderu `DataSlate/`.
- Sprawdzono aktywne i pomocnicze pliki HTML pod kątem ról wejściowych, zależności Firebase, Firestore, audio, ping oraz zewnętrznych URL/CDN.
- Sprawdzono podstawową strukturę `DataSlate_Offline/assets/data/data.json` jako obecnego lokalnego źródła danych.
- Nie zmieniano kodu aplikacji, assetów, konfiguracji Firebase, dokumentacji poza tym dziennikiem ani folderu `DataSlate/`.

### Ustalenia i decyzje

- Zakres edycji pozostaje ograniczony do `DataSlate_Offline/`; folder `DataSlate/` jest w tym etapie wyłącznie materiałem referencyjnym i nie został zmodyfikowany.
- Bieżący `DataSlate_Offline/index.html` jest launcherem, a nie docelowym generatorem offline: linkuje do `GM.html`, `DataSlate.html`, `GM_test.html` i `DataSlate_test.html` oraz nadal zawiera widoczną wzmiankę o audio.
- Obecna aktywna ścieżka produkcyjna nadal wygląda jak wersja online: `GM.html` publikuje payload do Firestore, a `DataSlate.html` nasłuchuje dokumentu Firestore.
- Pliki `GM_backup.html`, `DataSlate_backup.html`, `GM_test.html` i `DataSlate_test.html` są obecnie technicznie zbliżone do wariantów online i również zawierają zależności Firebase/CDN/audio/ping; zgodnie z wcześniejszą decyzją użytkownika mają pozostać w module i docelowo zawierać ten sam kod co główne pliki offline.
- Dokumentacja `config/FirebaseREADME.md`, `docs/Documentation.md` i `docs/README.md` nadal opisuje model online/Firebase i wymaga późniejszego przepisania, aby nie sugerować zależności online w module offline.
- `assets/data/data.json` istnieje i zawiera klucze `backgrounds`, `logos`, `audios`, `fonts`, `fillers` oraz `importLog`; obecnie obejmuje 10 teł, 14 logotypów, 1 audio, 16 fontów, 14 zestawów fillerów i pusty `importLog`.
- `assets/data/DataSlate_manifest.xlsx` i `assets/data/Mapowanie.xlsx` pozostają w module jako pliki źródłowe/deweloperskie, ale aktywne działanie offline powinno docelowo bazować na gotowym `assets/data/data.json`.
- Inwentaryzacja potwierdza, że Etap 1 powinien rozpocząć się od decyzji/implementacji docelowej struktury `index.html` jako generatora albo wariantu wieloplikowego bez Firebase.

### Zmienione pliki

- `DataSlate_Offline/Offline.md` — dopisano pełny prompt użytkownika oraz wynik Etapu 0: inwentaryzację plików, aktywnych wejść, zależności online, ryzyk i kolejnych kroków.

### Szczegóły zmian

#### Stan folderu i plików

- Stan przed zmianą: `Offline.md` zawierał plan wdrożenia, odpowiedzi biznesowe i wskazanie, że kolejnym krokiem jest Etap 0, ale nie zawierał wykonanej inwentaryzacji aktualnego drzewa plików.
- Stan po zmianie: dokument zawiera wynik inwentaryzacji obecnego folderu `DataSlate_Offline/`.
- W folderze znajdują się główne pliki HTML: `index.html`, `GM.html`, `DataSlate.html`, ich warianty `GM_backup.html`, `DataSlate_backup.html`, `GM_test.html`, `DataSlate_test.html`, dokumenty `Offline.md`, `Disclaimer.md`, `docs/Documentation.md`, `docs/README.md`, konfiguracja `config/firebase-config.js`, dokumentacja `config/FirebaseREADME.md`, lokalne assety graficzne, lokalne audio oraz dane w `assets/data/`.

#### Potwierdzenie plików wejściowych

- `index.html` obecnie pełni rolę launchera i prowadzi do produkcyjnych oraz testowych widoków, ale nie jest jeszcze właściwym generatorem offline.
- `GM.html` jest obecnie panelem GM opartym o Firebase/Firestore; ładuje `assets/data/data.json`, potrafi pobrać `DataSlate_manifest.xlsx` i wygenerować pobierany plik `data.json`, ale zapisuje payload przez `currentRef.set(...)`.
- `DataSlate.html` jest obecnie ekranem odbiorczym opartym o Firebase/Firestore; renderuje tło, overlay, logo, tekst i fillery, ale robi to po `onSnapshot(...)` dokumentu Firestore.
- `GM_backup.html`, `DataSlate_backup.html`, `GM_test.html` i `DataSlate_test.html` pozostają w module i obecnie również wymagają oczyszczenia z architektury online.
- `assets/data/data.json` jest obecnym lokalnym manifestem danych dla list teł, logotypów, audio, fontów i fillerów.

#### Firebase, Firestore i komunikacja online

- Importy lub odniesienia Firebase/Firestore wykryto w plikach HTML produkcyjnych, backupowych i testowych: `GM.html`, `GM_backup.html`, `GM_test.html`, `DataSlate.html`, `DataSlate_backup.html`, `DataSlate_test.html`.
- `GM*.html` zawierają import `config/firebase-config.js`, importy Firebase z `https://www.gstatic.com/firebasejs/9.6.8/...`, inicjalizację `firebase.initializeApp(...)`, `firebase.firestore()`, `firebase.firestore.FieldValue.serverTimestamp()` oraz zapisy `currentRef.set(...)`.
- `DataSlate*.html` zawierają import `config/firebase-config.js`, importy Firebase z `https://www.gstatic.com/firebasejs/9.6.8/...`, inicjalizację Firebase/Firestore oraz `ref.onSnapshot(...)`.
- `config/firebase-config.js` nadal zawiera realną konfigurację klienta Firebase dla projektu `rpg-dataslate-relay` i powinien zostać usunięty z aktywnej ścieżki offline w późniejszym etapie.
- `config/FirebaseREADME.md`, `docs/Documentation.md` i `docs/README.md` nadal opisują model Firestore i wymagają przepisania w późniejszych etapach.

#### Audio, ping, clear i efekty

- `GM*.html` zawierają UI i payload dla `audioSelect`, `audioEnabled`, `messageAudioId`, `messageAudioFile`, `pingUrl` oraz przycisk `Ping`.
- `DataSlate*.html` zawierają `PING_URL`, `new Audio(...)`, obsługę `type === 'ping'` i odtwarzanie audio dla wiadomości.
- W `assets/audios/` znajdują się lokalne pliki `KeyboardTyping.mp3` i `ping/Ping.mp3`; zgodnie z decyzją użytkownika audio może pozostać w danych/assetach dla zgodności, ale UI i aktywny renderer offline mają je ignorować.
- `Clear` jest obecnie częścią logiki panelu i zgodnie z decyzją użytkownika może pozostać jako akcja czyszczenia tekstu, ale nie powinien wymagać zapisu do Firestore.
- Efekty `flicker` i prostokąt cienia są nadal obecne w HTML/CSS i będą wymagały usunięcia z wersji offline zgodnie z decyzjami biznesowymi.

#### Zewnętrzne zależności sieciowe

- Zewnętrzne fonty Google wykryto w `GM.html`, `GM_backup.html`, `GM_test.html`, `DataSlate.html`, `DataSlate_backup.html` i `DataSlate_test.html` przez `fonts.googleapis.com` oraz `fonts.gstatic.com`.
- Zewnętrzne skrypty Firebase z `www.gstatic.com` wykryto w plikach `GM*.html` i `DataSlate*.html`.
- Zewnętrzny CDN SheetJS `https://cdn.sheetjs.com/xlsx-0.20.3/package/dist/xlsx.full.min.js` wykryto w `GM.html`, `GM_backup.html` i `GM_test.html`.
- `Disclaimer.md` i `docs/README.md` zawierają zewnętrzne adresy URL w dokumentacji; nie są one aktywną ścieżką działania, ale powinny zostać przejrzane przy przepisywaniu dokumentacji offline.
- Docelowy generator offline nie może zależeć od żadnego z powyższych zewnętrznych zasobów.

#### Dane i assety

- Lokalne tła znajdują się w `assets/backgrounds/`, ramki w `assets/ramki/`, logotypy w `assets/logos/`, audio w `assets/audios/`, a dane w `assets/data/`.
- `data.json` zawiera listy wymagane przez formularz i renderer: tła, logotypy, fonty, fillery oraz wpis audio dla zgodności z manifestem.
- Na tym etapie nie zmieniano struktury `data.json`, więc nie wykonywano pełnej walidacji mapowania ścieżek assetów, prefixów/suffixów ani wyboru tła/logo/fontu poza potwierdzeniem obecności głównych kluczy i liczebności list.

### Testy

- Sprawdzono status repozytorium przed zmianą: drzewo robocze było czyste.
- Wypisano pliki i podfoldery `DataSlate_Offline/` poleceniem `find`, bez używania `ls -R`.
- Przeskanowano `DataSlate_Offline/` poleceniem `rg` pod kątem `firebase`, `firestore`, `onSnapshot`, `currentRef.set`, `dataslate/current`, `ping`, `audio`, `mp3`, zewnętrznych URL, Google Fonts, Firebase CDN i SheetJS CDN.
- Sprawdzono strukturę `assets/data/data.json` krótkim skryptem Python odczytującym JSON i raportującym klucze oraz liczebność list.
- Nie wykonywano testu otwierania modułu w przeglądarce ani kliknięcia `Generuj`, ponieważ w obecnym stanie Etap 0 był inwentaryzacją, a aplikacja nie ma jeszcze docelowego przycisku `Generuj` ani lokalnego renderera offline.
- Nie wykonywano testu braku zewnętrznych żądań sieciowych w narzędziach przeglądarki; statyczne skanowanie wykazało istniejące zależności online, które muszą zostać usunięte w kolejnych etapach.

### Ryzyka i następne kroki

- Największe ryzyko techniczne to nadal silne sprzężenie głównych plików HTML i wariantów test/backup z Firebase, Firestore, Google Fonts i CDN SheetJS.
- Przed wdrażaniem właściwego generatora należy zdecydować, czy `index.html` przejmie rolę jedynego głównego generatora, czy utrzymany zostanie podział wieloplikowy z lokalnym przekazaniem payloadu.
- Następny rekomendowany krok to Etap 1: wybór i opis docelowej struktury aplikacji, a następnie rozpoczęcie minimalnych zmian w aktywnej ścieżce tylko w `DataSlate_Offline/`.
- Przy kolejnych etapach trzeba pamiętać, że folder `DataSlate/` pozostaje nietykalny, a wszelkie porównania z wersją online mogą mieć wyłącznie charakter odczytowy.

## Aktualizacja — 2026-06-10 — formalne zamknięcie Etapu 1: decyzja o strukturze aplikacji

### Oryginalny pełny prompt użytkownika

Repozytorium: CuteLittleGoat/rpg-dataslate-relay

Przeczytaj aktualny plik DataSlate_Offline/Offline.md i pracuj zgodnie z dotychczasowym stylem dokumentowania zmian w tym pliku.

Zadanie składa się z dwóch części:

1. Zaktualizuj DataSlate_Offline/Offline.md o moje decyzje zamykające „Etap 1 — decyzja o strukturze aplikacji”.
2. Następnie zrealizuj „Etap 2 — przygotowanie lokalnych danych i assetów” zgodnie z planem zapisanym w Offline.md.

Moje decyzje dotyczące „Etap 1 — decyzja o strukturze aplikacji”:

Wybieramy wariant jednego głównego pliku DataSlate_Offline/index.html.

index.html ma przejąć rolę generatora offline, z formularzem i funkcją tworzącą nową kartę. Payload jest tworzony lokalnie i istnieje tylko wewnętrznie w czasie generowania. Nie używamy sessionStorage, localStorage, postMessage, query/hash ani eksportu JSON/HTML jako podstawowego mechanizmu.

Ponieważ docelowym wariantem jest jeden główny index.html, pliki GM.html, DataSlate.html, GM_backup.html, DataSlate_backup.html, GM_test.html i DataSlate_test.html są zbędne w finalnej strukturze modułu offline.

Docelowa struktura powinna opierać się na:
- index.html — główna wersja generatora offline,
- index_backup.html — kopia/backup głównej wersji offline,
- index_test.html — wersja testowa generatora offline.

Pliki GM.html, DataSlate.html, GM_backup.html, DataSlate_backup.html, GM_test.html i DataSlate_test.html mogą pozostać tymczasowo jako materiał referencyjny w trakcie migracji, ale po zakończeniu przebudowy powinny zostać usunięte albo wyłączone z aktywnej/docelowej struktury DataSlate_Offline.

Zapisz powyższe decyzje w DataSlate_Offline/Offline.md jako formalne zamknięcie Etapu 1. W sekcji tej uwzględnij:
- pełny prompt użytkownika,
- zakres prac,
- ustalenia i decyzje,
- zmienione pliki,
- testy/sprawdzenia,
- ryzyka i następne kroki.

Następnie zrealizuj „Etap 2 — przygotowanie lokalnych danych i assetów”.

Zakres Etapu 2:

1. Zweryfikuj strukturę DataSlate_Offline/assets/data/data.json jako podstawowego źródła danych dla generatora offline.
2. Sprawdź, czy JSON zawiera komplet wymaganych list i mapowań:
   - tła,
   - logotypy,
   - fonty,
   - fillery,
   - ścieżki assetów,
   - ustawienia ramek i layoutu zależne od tła,
   - dane potrzebne do prefixów i suffixów.
3. Sprawdź, czy wszystkie ścieżki w data.json prowadzą do lokalnych plików w DataSlate_Offline/.
4. Sprawdź rolę DataSlate_Offline/assets/data/DataSlate_manifest.xlsx jako pliku źródłowego/deweloperskiego. Plik ma pozostać w repozytorium.
5. Ustal minimalny zestaw danych testowych pozwalający sprawdzić każdy typ tła, logotypu, fontu i fillera.
6. Sprawdź, czy w DataSlate_Offline/ znajdują się assety wymagane przez data.json:
   - backgrounds,
   - logos,
   - fonts albo lokalnie dostępne fonty, jeśli takie są,
   - fillery jako dane w JSON,
   - ramki/layouty/mapowania, jeżeli są wymagane przez renderer.
7. Sprawdź, czy data.json nie odwołuje się do plików spoza DataSlate_Offline/ ani do zewnętrznych URL.
8. Sprawdź, czy istnieją potencjalne braki, niespójności nazw, literówki w ścieżkach, puste listy, nieużywane sekcje albo zależności, które utrudnią Etap 3 i Etap 4.

Ważne ograniczenia:

- Nie modyfikuj folderu DataSlate/. Folder DataSlate/ jest tylko referencyjny.
- Nie przebudowuj jeszcze generatora offline ani UI index.html w ramach tego zadania, chyba że zmiana jest absolutnie konieczna dla przygotowania danych i assetów.
- Nie usuwaj jeszcze plików GM.html, DataSlate.html, GM_backup.html, DataSlate_backup.html, GM_test.html i DataSlate_test.html. Na tym etapie tylko zapisz decyzję, że są zbędne w finalnej strukturze i że docelowo zastąpią je index_backup.html oraz index_test.html.
- Nie usuwaj DataSlate_manifest.xlsx.
- Nie dodawaj sessionStorage, localStorage, postMessage, query/hash ani eksportu JSON/HTML jako mechanizmu działania.
- Nie dodawaj automatycznych testów wizualnych.
- Jeżeli Etap 2 ujawni konieczność zmian w kodzie aplikacji, których bezpiecznie nie da się wykonać bez rozpoczęcia Etapu 3 lub Etapu 4, opisz je jako rekomendację/bloker w Offline.md, ale nie wykonuj przedwczesnej przebudowy generatora.

Po wykonaniu Etapu 2 dopisz do DataSlate_Offline/Offline.md nową sekcję dokumentującą wynik Etapu 2. Sekcja powinna zawierać:
- pełny prompt użytkownika,
- zakres prac,
- ustalenia i decyzje,
- wynik weryfikacji data.json,
- wynik weryfikacji ścieżek assetów,
- informację o DataSlate_manifest.xlsx,
- minimalny zestaw danych testowych,
- zmienione pliki,
- testy/sprawdzenia,
- ryzyka i następne kroki.

W testach/sprawdzeniach użyj statycznej weryfikacji repozytorium, np.:
- sprawdzenie statusu repozytorium przed i po zmianach,
- odczyt i walidacja JSON,
- sprawdzenie kluczy i liczebności list w data.json,
- sprawdzenie ścieżek plików z data.json,
- wyszukanie zewnętrznych URL w data.json,
- sprawdzenie obecności lokalnych assetów, do których odwołuje się data.json.

Na końcu przygotuj krótkie podsumowanie:
- czy Etap 1 został formalnie zamknięty,
- czy Etap 2 został zakończony,
- czy można przejść do Etapu 3,
- jakie są ewentualne blokery lub ryzyka przed Etapem 3.

Utwórz PR z tymi zmianami.

### Zakres prac

- Przeczytano aktualną treść `DataSlate_Offline/Offline.md` przed dopisaniem nowych ustaleń.
- Sprawdzono status repozytorium przed zmianami dokumentacji.
- Dopisano formalne zamknięcie Etapu 1 zgodnie z decyzjami użytkownika.
- Nie przebudowywano `index.html`, nie dodawano mechanizmu przekazywania payloadu i nie usuwano plików referencyjnych `GM*.html` ani `DataSlate*.html`.
- Nie modyfikowano chronionego folderu `DataSlate/`.

### Ustalenia i decyzje

- Etap 1 zostaje formalnie zamknięty decyzją o jednym głównym pliku `DataSlate_Offline/index.html`.
- `index.html` ma przejąć rolę generatora offline: formularz, lokalne zbudowanie payloadu i utworzenie nowej karty z gotowym ekranem DataSlate.
- Payload ma istnieć tylko wewnętrznie w czasie generowania i nie może opierać podstawowego działania o `sessionStorage`, `localStorage`, `postMessage`, query/hash ani eksport JSON/HTML.
- Docelowa struktura aktywna modułu offline ma opierać się na plikach:
  - `index.html` — główna wersja generatora offline,
  - `index_backup.html` — kopia/backup głównej wersji offline,
  - `index_test.html` — wersja testowa generatora offline.
- Pliki `GM.html`, `DataSlate.html`, `GM_backup.html`, `DataSlate_backup.html`, `GM_test.html` i `DataSlate_test.html` są zbędne w finalnej strukturze aktywnej, ale na tym etapie pozostają tymczasowo jako materiał referencyjny do migracji.
- Decyzja z tej sekcji aktualizuje wcześniejsze ustalenie, że pliki backup/test miałyby docelowo zawierać ten sam kod co wersja offline: aktualny wariant docelowy wskazuje odpowiednio `index_backup.html` i `index_test.html` zamiast par `GM_*`/`DataSlate_*`.

### Zmienione pliki

- `DataSlate_Offline/Offline.md` — dopisano formalne zamknięcie Etapu 1 i decyzję o docelowej strukturze opartej o `index.html`, `index_backup.html` oraz `index_test.html`.

### Szczegóły zmian

- Stan przed zmianą: `Offline.md` zawierał plan Etapu 1 oraz wcześniejsze odpowiedzi biznesowe, ale nie zawierał formalnego zamknięcia decyzji strukturalnej.
- Stan po zmianie: dokument wskazuje jeden aktywny plik główny `index.html` jako wariant docelowy oraz oznacza pary `GM*.html`/`DataSlate*.html` jako tymczasowy materiał referencyjny do usunięcia albo wyłączenia po migracji.
- Powód zmiany: użytkownik podjął decyzję kończącą Etap 1 i poprosił o jej zapisanie przed rozpoczęciem Etapu 2.

### Testy/sprawdzenia

- Sprawdzono status repozytorium przed zmianami: drzewo robocze było czyste na gałęzi `work`.
- Przeczytano aktualny plik `DataSlate_Offline/Offline.md` przed dopisaniem sekcji.
- Sprawdzono listę plików `AGENTS.md`, `Offline.md`, `data.json` i manifestów XLSX poleceniem `rg --files`, bez modyfikowania folderu `DataSlate/`.
- Nie wykonywano testów funkcjonalnych aplikacji, ponieważ zamknięcie Etapu 1 jest zmianą dokumentacyjną i nie uruchamia jeszcze docelowego generatora.

### Ryzyka i następne kroki

- Etap 3 będzie musiał przenieść użyteczną logikę formularza i renderera do `index.html` bez wprowadzania niedozwolonych mechanizmów transportu payloadu.
- Po zakończeniu przebudowy trzeba utworzyć albo zsynchronizować `index_backup.html` i `index_test.html`, a pliki `GM*.html` oraz `DataSlate*.html` usunąć albo wyłączyć z aktywnej/docelowej struktury.
- Do czasu migracji istnieje ryzyko utrzymaniowe: folder zawiera nadal stare pliki online oparte o Firebase, CDN i Google Fonts, ale nie zostały one usunięte zgodnie z ograniczeniem tego zadania.

## Aktualizacja — 2026-06-10 — Etap 2: przygotowanie lokalnych danych i assetów

### Oryginalny pełny prompt użytkownika

Repozytorium: CuteLittleGoat/rpg-dataslate-relay

Przeczytaj aktualny plik DataSlate_Offline/Offline.md i pracuj zgodnie z dotychczasowym stylem dokumentowania zmian w tym pliku.

Zadanie składa się z dwóch części:

1. Zaktualizuj DataSlate_Offline/Offline.md o moje decyzje zamykające „Etap 1 — decyzja o strukturze aplikacji”.
2. Następnie zrealizuj „Etap 2 — przygotowanie lokalnych danych i assetów” zgodnie z planem zapisanym w Offline.md.

Moje decyzje dotyczące „Etap 1 — decyzja o strukturze aplikacji”:

Wybieramy wariant jednego głównego pliku DataSlate_Offline/index.html.

index.html ma przejąć rolę generatora offline, z formularzem i funkcją tworzącą nową kartę. Payload jest tworzony lokalnie i istnieje tylko wewnętrznie w czasie generowania. Nie używamy sessionStorage, localStorage, postMessage, query/hash ani eksportu JSON/HTML jako podstawowego mechanizmu.

Ponieważ docelowym wariantem jest jeden główny index.html, pliki GM.html, DataSlate.html, GM_backup.html, DataSlate_backup.html, GM_test.html i DataSlate_test.html są zbędne w finalnej strukturze modułu offline.

Docelowa struktura powinna opierać się na:
- index.html — główna wersja generatora offline,
- index_backup.html — kopia/backup głównej wersji offline,
- index_test.html — wersja testowa generatora offline.

Pliki GM.html, DataSlate.html, GM_backup.html, DataSlate_backup.html, GM_test.html i DataSlate_test.html mogą pozostać tymczasowo jako materiał referencyjny w trakcie migracji, ale po zakończeniu przebudowy powinny zostać usunięte albo wyłączone z aktywnej/docelowej struktury DataSlate_Offline.

Zapisz powyższe decyzje w DataSlate_Offline/Offline.md jako formalne zamknięcie Etapu 1. W sekcji tej uwzględnij:
- pełny prompt użytkownika,
- zakres prac,
- ustalenia i decyzje,
- zmienione pliki,
- testy/sprawdzenia,
- ryzyka i następne kroki.

Następnie zrealizuj „Etap 2 — przygotowanie lokalnych danych i assetów”.

Zakres Etapu 2:

1. Zweryfikuj strukturę DataSlate_Offline/assets/data/data.json jako podstawowego źródła danych dla generatora offline.
2. Sprawdź, czy JSON zawiera komplet wymaganych list i mapowań:
   - tła,
   - logotypy,
   - fonty,
   - fillery,
   - ścieżki assetów,
   - ustawienia ramek i layoutu zależne od tła,
   - dane potrzebne do prefixów i suffixów.
3. Sprawdź, czy wszystkie ścieżki w data.json prowadzą do lokalnych plików w DataSlate_Offline/.
4. Sprawdź rolę DataSlate_Offline/assets/data/DataSlate_manifest.xlsx jako pliku źródłowego/deweloperskiego. Plik ma pozostać w repozytorium.
5. Ustal minimalny zestaw danych testowych pozwalający sprawdzić każdy typ tła, logotypu, fontu i fillera.
6. Sprawdź, czy w DataSlate_Offline/ znajdują się assety wymagane przez data.json:
   - backgrounds,
   - logos,
   - fonts albo lokalnie dostępne fonty, jeśli takie są,
   - fillery jako dane w JSON,
   - ramki/layouty/mapowania, jeżeli są wymagane przez renderer.
7. Sprawdź, czy data.json nie odwołuje się do plików spoza DataSlate_Offline/ ani do zewnętrznych URL.
8. Sprawdź, czy istnieją potencjalne braki, niespójności nazw, literówki w ścieżkach, puste listy, nieużywane sekcje albo zależności, które utrudnią Etap 3 i Etap 4.

Ważne ograniczenia:

- Nie modyfikuj folderu DataSlate/. Folder DataSlate/ jest tylko referencyjny.
- Nie przebudowuj jeszcze generatora offline ani UI index.html w ramach tego zadania, chyba że zmiana jest absolutnie konieczna dla przygotowania danych i assetów.
- Nie usuwaj jeszcze plików GM.html, DataSlate.html, GM_backup.html, DataSlate_backup.html, GM_test.html i DataSlate_test.html. Na tym etapie tylko zapisz decyzję, że są zbędne w finalnej strukturze i że docelowo zastąpią je index_backup.html oraz index_test.html.
- Nie usuwaj DataSlate_manifest.xlsx.
- Nie dodawaj sessionStorage, localStorage, postMessage, query/hash ani eksportu JSON/HTML jako mechanizmu działania.
- Nie dodawaj automatycznych testów wizualnych.
- Jeżeli Etap 2 ujawni konieczność zmian w kodzie aplikacji, których bezpiecznie nie da się wykonać bez rozpoczęcia Etapu 3 lub Etapu 4, opisz je jako rekomendację/bloker w Offline.md, ale nie wykonuj przedwczesnej przebudowy generatora.

Po wykonaniu Etapu 2 dopisz do DataSlate_Offline/Offline.md nową sekcję dokumentującą wynik Etapu 2. Sekcja powinna zawierać:
- pełny prompt użytkownika,
- zakres prac,
- ustalenia i decyzje,
- wynik weryfikacji data.json,
- wynik weryfikacji ścieżek assetów,
- informację o DataSlate_manifest.xlsx,
- minimalny zestaw danych testowych,
- zmienione pliki,
- testy/sprawdzenia,
- ryzyka i następne kroki.

W testach/sprawdzeniach użyj statycznej weryfikacji repozytorium, np.:
- sprawdzenie statusu repozytorium przed i po zmianach,
- odczyt i walidacja JSON,
- sprawdzenie kluczy i liczebności list w data.json,
- sprawdzenie ścieżek plików z data.json,
- wyszukanie zewnętrznych URL w data.json,
- sprawdzenie obecności lokalnych assetów, do których odwołuje się data.json.

Na końcu przygotuj krótkie podsumowanie:
- czy Etap 1 został formalnie zamknięty,
- czy Etap 2 został zakończony,
- czy można przejść do Etapu 3,
- jakie są ewentualne blokery lub ryzyka przed Etapem 3.

Utwórz PR z tymi zmianami.

### Zakres prac

- Przeczytano aktualny `DataSlate_Offline/Offline.md` i wykonano Etap 2 jako statyczną weryfikację danych oraz assetów.
- Zweryfikowano `DataSlate_Offline/assets/data/data.json` jako obecne podstawowe źródło danych dla generatora offline.
- Sprawdzono klucze, typy i liczebność list w JSON-ie.
- Sprawdzono ścieżki plików deklarowane w `backgrounds`, `logos` i `audios`.
- Sprawdzono obecność lokalnych katalogów assetów i plików ramek w `assets/ramki/` odpowiadających tłom.
- Sprawdzono brak zewnętrznych URL w `data.json`.
- Sprawdzono obecność `DataSlate_Offline/assets/data/DataSlate_manifest.xlsx` i pozostawiono go bez zmian jako plik źródłowy/deweloperski.
- Nie przebudowywano generatora, nie zmieniano UI `index.html`, nie dodawano mechanizmu transportu payloadu, nie usuwano starych plików HTML i nie dodawano automatycznych testów wizualnych.
- Nie modyfikowano chronionego folderu `DataSlate/`.

### Ustalenia i decyzje

- `assets/data/data.json` może pozostać podstawowym źródłem danych dla Etapu 3 i Etapu 4, ale wymaga świadomego uzupełnienia albo przeniesienia niektórych mapowań z kodu przy przebudowie renderera.
- JSON zawiera komplet podstawowych list dla formularza: tła, logotypy, fonty, fillery oraz audio zachowane dla zgodności z manifestem.
- JSON zawiera ścieżki assetów dla teł, logotypów i audio; wszystkie sprawdzone ścieżki są lokalne i istnieją w `DataSlate_Offline/`.
- JSON nie zawiera obecnie jawnych ustawień ramek i layoutu zależnych od tła. Te ustawienia istnieją w aktywnym rendererze jako stała `CONTENT_RECTS_BY_BACKGROUND_ID` w plikach `DataSlate*.html`, więc Etap 3/4 musi zdecydować, czy przenieść je do `index.html`, czy rozszerzyć `data.json`.
- Pliki ramek `assets/ramki/*_ramka.png` istnieją lokalnie dla każdego tła, ale nie są jawnie wskazane w `data.json`; ich powiązanie jest inferowane po nazwach plików.
- Lokalnego katalogu `assets/fonts/` nie ma. Lista `fonts` zawiera nazwy rodzin fontów, nie ścieżki do lokalnych plików fontów. To jest najważniejsze ryzyko dla wymogu pełnego działania offline bez Google Fonts.
- Fillery są przechowywane jako dane w JSON-ie, a każdy sprawdzony wpis ma listę `prefixes` i `suffixes`.
- `importLog` jest pustą listą; nie blokuje Etapu 3, ale jest sekcją pomocniczą generowaną z manifestu i prawdopodobnie nie będzie potrzebna w aktywnym runtime generatora.
- `DataSlate_manifest.xlsx` pozostaje w repozytorium jako plik źródłowy/deweloperski. Aplikacja offline nie powinna opierać podstawowego runtime na parsowaniu XLSX.

### Wynik weryfikacji `data.json`

- Plik `DataSlate_Offline/assets/data/data.json` jest poprawnym JSON-em.
- Klucze najwyższego poziomu: `backgrounds`, `logos`, `audios`, `fonts`, `fillers`, `importLog`.
- Liczebność list:
  - `backgrounds`: 10,
  - `logos`: 14,
  - `audios`: 1,
  - `fonts`: 16,
  - `fillers`: 14,
  - `importLog`: 0.
- Identyfikatory i nazwy w listach `backgrounds`, `logos`, `audios`, `fonts` i `fillers` są unikalne według statycznego sprawdzenia.
- Nie wykryto pustych list wymaganych do formularza i renderera: tła, logotypy, fonty oraz fillery są niepuste.
- Nie wykryto fillerów bez prefixów albo bez suffixów.
- Dane potrzebne do prefixów i suffixów są obecne w każdym wpisie `fillers`.
- Brak jawnych pól layoutu/ramki w `backgrounds` oznacza, że mapowanie obszaru treści musi zostać przeniesione z obecnego kodu renderera albo dodane do danych w jednym z następnych etapów.

### Wynik weryfikacji ścieżek assetów

- Sprawdzono 25 ścieżek plików z sekcji `backgrounds`, `logos` i `audios`.
- Wszystkie 25 ścieżek jest ścieżkami względnymi do zasobów lokalnych w `DataSlate_Offline/`.
- Nie wykryto ścieżek wychodzących poza `DataSlate_Offline/`.
- Nie wykryto brakujących plików dla ścieżek zadeklarowanych w `data.json`.
- Nie wykryto zewnętrznych URL w `data.json`.
- Katalogi lokalnych assetów istnieją:
  - `DataSlate_Offline/assets/backgrounds`,
  - `DataSlate_Offline/assets/logos`,
  - `DataSlate_Offline/assets/audios`,
  - `DataSlate_Offline/assets/audios/ping`,
  - `DataSlate_Offline/assets/ramki`,
  - `DataSlate_Offline/assets/data`.
- Dla każdego tła znaleziono odpowiadający plik ramki w `assets/ramki/` przy założeniu konwencji nazwy `<nazwa_tła>_ramka.png`.
- Lokalny katalog `DataSlate_Offline/assets/fonts/` nie istnieje, więc fonty nie są obecnie dostarczone jako lokalne pliki fontów. W obecnych plikach HTML fonty są ładowane z Google Fonts, co musi zostać rozwiązane w Etapie 3/4, jeżeli pełny tryb offline ma zachować wybrane fonty.

### Informacja o `DataSlate_manifest.xlsx`

- `DataSlate_Offline/assets/data/DataSlate_manifest.xlsx` istnieje i nie został zmieniony.
- Rola pliku pozostaje źródłowa/deweloperska: aktualizacje danych mają wynikać z aktualizacji manifestu, wygenerowania nowego `assets/data/data.json` i aktualizacji odpowiednich folderów assetów.
- Etap 2 nie usuwa manifestu i nie wprowadza runtime’owego parsowania XLSX jako podstawowego mechanizmu działania aplikacji offline.

### Minimalny zestaw danych testowych

Minimalny zestaw testowy przed Etapem 3/4 powinien zapewnić pokrycie każdej pozycji z głównych list, ponieważ listy są krótkie i każda pozycja odpowiada odrębnemu assetowi albo stylowi:

- Tła: po jednym teście dla każdego z 10 wpisów `backgrounds`, aby sprawdzić obraz tła oraz odpowiadającą mu ramkę/layout: `Green with a narrow frame`, `Gray-blue frame`, `Silver with Aquilla`, `Retro with a thick frame`, `Silver with a narrow frame`, `Inquisition`, `Litanies of the Lost`, `Notebook`, `Parchment`, `WrathAndGlory`.
- Logotypy: po jednym teście z włączonym logo dla każdego z 14 wpisów `logos`: `Administratum`, `Apothecary`, `Aquila`, `Astra Militarum`, `Chaos Undivided`, `Inquisition`, `Khorne`, `Mechanicus`, `Medicae`, `Navigator`, `Nurgle`, `Slaanesh`, `Sororitas`, `Tzeentch`; dodatkowo jeden test z logo wyłączonym.
- Fonty: po jednym teście dla każdego z 16 wpisów `fonts`: `Share Tech Mono`, `Cinzel`, `Rajdhani`, `IBM Plex Serif`, `Open Sans`, `Noto Serif`, `DM Serif Display`, `IBM Plex Sans Condensed`, `Exo 2`, `Black Ops One`, `Staatliches`, `Orbitron`, `Questrial`, `Russo One`, `Caveat`, `Great Vibes`.
- Fillery: po jednym teście dla każdego z 14 wpisów `fillers`, z włączonymi prefixami i suffixami oraz co najmniej jedną linią z każdej strony; dodatkowo jeden test z fillerami wyłączonymi.
- Minimalna praktyczna matryca może być sekwencyjna zamiast pełnego iloczynu kartezjańskiego: 10 testów teł, 14 testów logo, 16 testów fontów i 14 testów fillerów, przy stałej przykładowej wiadomości oraz domyślnych kolorach, plus testy wyłączenia logo i fillerów.

### Zmienione pliki

- `DataSlate_Offline/Offline.md` — dopisano wynik Etapu 2, weryfikację `data.json`, weryfikację ścieżek assetów, informację o `DataSlate_manifest.xlsx`, minimalny zestaw danych testowych oraz ryzyka przed Etapem 3.

### Szczegóły zmian

- Stan przed zmianą: `Offline.md` zawierał plan Etapu 2, ale nie zawierał wyniku walidacji danych i assetów.
- Stan po zmianie: dokument zawiera statyczny raport z walidacji `data.json`, lokalnych ścieżek assetów, ramek, manifestu XLSX i minimalnej matrycy testowej.
- Powód zmiany: użytkownik poprosił o realizację Etapu 2 bez przedwczesnej przebudowy generatora i z opisaniem potencjalnych blokerów w dokumentacji.
- Kod aplikacji, dane JSON, assety i pliki XLSX nie zostały zmienione.

### Testy/sprawdzenia

- Sprawdzono status repozytorium przed zmianami: `git status --short --branch` zwrócił czystą gałąź `work`.
- Sprawdzono status repozytorium po zmianach dokumentacji: `git status --short --branch` pokazał jedynie zmodyfikowany plik `DataSlate_Offline/Offline.md` przed commitem.
- Odczytano i sprawdzono `DataSlate_Offline/Offline.md` przed dopisaniem nowych sekcji.
- Odczytano oraz zwalidowano `DataSlate_Offline/assets/data/data.json` skryptem Python z modułem `json`; wynik: JSON poprawny.
- Sprawdzono klucze i liczebność list w `data.json`; wynik: `backgrounds=10`, `logos=14`, `audios=1`, `fonts=16`, `fillers=14`, `importLog=0`.
- Sprawdzono 25 ścieżek z `backgrounds`, `logos` i `audios`; wynik: `path_issues=0`.
- Sprawdzono pliki ramek inferowane z nazw teł; wynik: `inferred_frame_issues=0`.
- Wyszukano zewnętrzne URL w `data.json` poleceniem `rg -n "https?://|//" DataSlate_Offline/assets/data/data.json`; wynik: brak dopasowań.
- Sprawdzono obecność lokalnych katalogów assetów poleceniem `find DataSlate_Offline/assets -maxdepth 2 -type d -print | sort`.
- Sprawdzono obecność `DataSlate_Offline/assets/data/DataSlate_manifest.xlsx`; wynik: plik istnieje.
- Nie wykonywano testów w przeglądarce ani automatycznych testów wizualnych, ponieważ zadanie dotyczyło statycznej weryfikacji danych i assetów przed przebudową generatora.

### Ryzyka i następne kroki

- Najważniejszy bloker przed pełnym offline w Etapie 3/4: brak lokalnych plików fontów przy jednoczesnej obecności nazw fontów Google w `data.json` i obecnym ładowaniu Google Fonts w starych plikach HTML.
- Drugi istotny punkt do decyzji implementacyjnej: ustawienia layoutu zależne od tła nie są zapisane w `data.json`, tylko w obecnym rendererze jako mapa `CONTENT_RECTS_BY_BACKGROUND_ID`; trzeba je przenieść do nowej aktywnej ścieżki `index.html` albo rozszerzyć `data.json`.
- Pliki ramek istnieją lokalnie, ale nie są jawnie mapowane w `data.json`; jeśli renderer Etapu 3/4 będzie potrzebował tych plików bez inferencji nazw, warto dodać jawne pola w danych albo utrzymać jednoznaczną konwencję nazewniczą.
- Sekcja `audios` oraz katalog `assets/audios/` pozostają dla zgodności z manifestem, ale UI i renderer offline powinny ignorować audio.
- Etap 2 został zakończony statycznie; można przejść do Etapu 3 pod warunkiem świadomego rozwiązania lokalnych fontów i przeniesienia mapy layoutów do docelowego `index.html` albo danych.

## Aktualizacja — 2026-06-10 — dodatkowe ustalenia przed Etapem 3: fonty, komunikaty i layouty

### Oryginalny pełny prompt użytkownika

Przeczytaj plik DataSlate_Offline/Offline.md a następnie dopisz do niego nowe wymagania:

Dodatkowe ustalenia przed Etapem 3 — fonty, komunikaty językowe i layouty zależne od tła

### Fonty i fallback offline

Wersja `DataSlate Offline` może nadal korzystać z nazw fontów zapisanych w `assets/data/data.json`, zgodnych z wersją online. Jeżeli aplikacja ma dostęp do internetu i Google Fonts zostaną poprawnie załadowane, wybrany font powinien być używany normalnie.

Jeżeli aplikacja działa bez internetu albo Google Fonts nie zostaną załadowane, generator i wygenerowany ekran DataSlate mają użyć fallbacku do fontu systemowego. Brak Google Fonts nie może blokować działania generatora, renderowania wiadomości ani tworzenia nowej karty.

W panelu generatora, najlepiej w pobliżu menu wyboru fontu, musi pojawić się czytelna informacja, że z powodu braku połączenia z internetem nie można załadować Google Fonts i dlatego używany jest font systemowy.

Ponieważ aplikacja obsługuje wybór języka, komunikat o niedostępności Google Fonts musi być przygotowany w obsługiwanych językach interfejsu. Nie powinien być wpisany wyłącznie na sztywno po polsku ani wyłącznie po angielsku.

Przykładowe komunikaty:

PL:
Google Fonts są niedostępne. Generator użyje fontu systemowego.

EN:
Google Fonts are unavailable. The generator will use a system font.

Komunikat powinien pojawiać się tylko wtedy, gdy Google Fonts faktycznie nie są dostępne albo nie udało się ich załadować. W normalnym trybie online nie powinien niepotrzebnie ostrzegać użytkownika.

### Layouty zależne od tła

„Layout zależny od tła” oznacza pozycję i rozmiar obszaru tekstowego na konkretnym tle DataSlate. Każde tło ma inną ramkę, marginesy i miejsce przeznaczone na wiadomość, więc renderer musi wiedzieć, gdzie wstawić tekst, logo, prefixy i suffixy.

W obecnej wersji informacje te znajdują się w kodzie `DataSlate.html` jako mapa `CONTENT_RECTS_BY_BACKGROUND_ID`. Mapa określa dla każdego `backgroundId` wartości `x`, `y`, `w`, `h`, czyli pozycję i rozmiar prostokąta treści względem tła.

Na tym etapie nie rozszerzamy `assets/data/data.json` o layouty zależne od tła. W Etapie 3/4 należy przenieść istniejącą mapę `CONTENT_RECTS_BY_BACKGROUND_ID` z obecnego `DataSlate.html` do docelowego `index.html`, aby zachować zgodność wizualną z wersją online.

Mapa layoutów nie jest decyzją biznesową, tylko technicznym elementem renderera potrzebnym do zachowania poprawnego położenia tekstu na różnych tłach.

### Wpływ na Etap 3

Etap 3 powinien uwzględniać następujące decyzje:

- menu wyboru fontu zostaje,
- nazwy fontów z `data.json` zostają zgodne z wersją online,
- Google Fonts mogą być użyte, jeżeli są dostępne,
- przy braku internetu aplikacja używa fontu systemowego,
- użytkownik widzi wielojęzyczny komunikat o fallbacku fontów,
- brak Google Fonts nie jest błędem krytycznym,
- mapa `CONTENT_RECTS_BY_BACKGROUND_ID` ma zostać przeniesiona do nowego `index.html`,
- `data.json` na razie nie musi być rozszerzany o dane layoutów.

### Zakres prac

- Przeczytano aktualną treść `DataSlate_Offline/Offline.md` przed dopisaniem nowych wymagań.
- Dopisano nowe wymagania przed Etapem 3 dotyczące obsługi Google Fonts, fallbacku do fontu systemowego, wielojęzycznego komunikatu ostrzegawczego oraz layoutów zależnych od tła.
- Nie przebudowywano generatora, nie zmieniano UI `index.html`, nie modyfikowano `assets/data/data.json`, nie przenoszono jeszcze mapy `CONTENT_RECTS_BY_BACKGROUND_ID` i nie zmieniano chronionego folderu `DataSlate/`.

### Ustalenia i decyzje

- Menu wyboru fontu pozostaje elementem panelu generatora offline.
- Nazwy fontów w `assets/data/data.json` pozostają zgodne z wersją online i mogą być używane do próby załadowania Google Fonts, jeżeli aplikacja ma dostęp do internetu.
- Brak internetu albo nieudane załadowanie Google Fonts nie może blokować działania generatora, renderowania wiadomości ani tworzenia nowej karty.
- W przypadku niedostępności Google Fonts generator oraz wygenerowany ekran DataSlate mają używać fontu systemowego jako fallbacku.
- Panel generatora ma pokazywać czytelny komunikat o fallbacku fontów tylko wtedy, gdy Google Fonts faktycznie nie są dostępne albo nie udało się ich załadować.
- Komunikat o fallbacku fontów musi być przygotowany w obsługiwanych językach interfejsu, co najmniej w wariantach PL i EN, zamiast być wpisany na sztywno w jednym języku.
- Przykładowy komunikat PL: `Google Fonts są niedostępne. Generator użyje fontu systemowego.`
- Przykładowy komunikat EN: `Google Fonts are unavailable. The generator will use a system font.`
- Layout zależny od tła oznacza pozycję i rozmiar obszaru tekstowego oraz powiązane rozmieszczenie tekstu, logo, prefixów i suffixów dla konkretnego tła DataSlate.
- Na tym etapie `assets/data/data.json` nie jest rozszerzany o layouty zależne od tła.
- W Etapie 3/4 należy przenieść mapę `CONTENT_RECTS_BY_BACKGROUND_ID` z obecnego `DataSlate_Offline/DataSlate.html` do docelowego `DataSlate_Offline/index.html`, aby zachować zgodność wizualną z wersją online.
- Mapa layoutów jest technicznym elementem renderera, a nie decyzją biznesową.

### Zmienione pliki

- `DataSlate_Offline/Offline.md` — dopisano nowe wymagania przed Etapem 3 dotyczące fontów, wielojęzycznego komunikatu fallbacku oraz przeniesienia mapy layoutów zależnych od tła do `index.html`.

### Szczegóły zmian

- Stan przed zmianą: `Offline.md` wskazywał brak lokalnych plików fontów jako najważniejszy bloker przed pełnym offline i wskazywał konieczność decyzji, czy layouty zależne od tła przenieść do `index.html`, czy rozszerzyć `data.json`.
- Stan po zmianie: dokument doprecyzowuje, że nazwy fontów z `data.json` zostają, Google Fonts mogą być użyte w trybie online, brak Google Fonts uruchamia fallback systemowy i wielojęzyczny komunikat w UI, a mapa `CONTENT_RECTS_BY_BACKGROUND_ID` ma zostać przeniesiona do `index.html` bez rozszerzania `data.json` na tym etapie.
- Powód zmiany: użytkownik doprecyzował wymagania przed rozpoczęciem Etapu 3, aby usunąć niejednoznaczność dotyczącą fontów i miejsca przechowywania layoutów zależnych od tła.
- Kod aplikacji, dane JSON, assety i pliki XLSX nie zostały zmienione.

### Testy/sprawdzenia

- Sprawdzono status repozytorium przed zmianą: `git status --short --branch` pokazał czystą gałąź `work`.
- Przeczytano aktualną treść `DataSlate_Offline/Offline.md` przed dopisaniem nowych wymagań.
- Po zmianie sprawdzono różnicę w Git dla `DataSlate_Offline/Offline.md`.
- Nie wykonywano testów funkcjonalnych aplikacji ani testów w przeglądarce, ponieważ zadanie dotyczyło wyłącznie aktualizacji dokumentacji wymagań przed Etapem 3.

### Ryzyka i następne kroki

- Etap 3 musi zaimplementować detekcję niedostępności Google Fonts w sposób, który nie generuje fałszywego ostrzeżenia w normalnym trybie online.
- Etap 3 musi zintegrować komunikat fallbacku fontów z istniejącym albo docelowym mechanizmem wyboru języka interfejsu.
- Etap 3/4 musi przenieść `CONTENT_RECTS_BY_BACKGROUND_ID` do aktywnej ścieżki `index.html` bez modyfikowania chronionego folderu `DataSlate/` i bez rozszerzania `data.json` o layouty na tym etapie.
- Po implementacji należy ręcznie sprawdzić działanie fontów w trybie online i offline oraz poprawne położenie tekstu na wszystkich tłach.

## Aktualizacja — 2026-06-10 — Etap 3: przebudowa panelu generatora

### Oryginalny pełny prompt użytkownika

Przeczytaj aktualny plik DataSlate_Offline/Offline.md i pracuj zgodnie z zapisanym tam planem, decyzjami i stylem dokumentowania zmian.

Zrealizuj:

Etap 3 — przebudowa panelu generatora

Celem Etapu 3 jest przebudowanie aktywnego panelu generatora offline w DataSlate_Offline/index.html. Ten etap ma przygotować lokalny formularz i lokalne budowanie payloadu, ale nie musi jeszcze w pełni generować gotowej karty w nowej karcie — to należy do Etapu 4.

Najważniejsze decyzje obowiązujące przed Etapem 3:

- Docelowym głównym plikiem modułu offline jest DataSlate_Offline/index.html.
- index.html ma przejąć rolę generatora offline.
- Payload jest tworzony lokalnie i istnieje tylko wewnętrznie w czasie generowania.
- Nie używamy sessionStorage, localStorage, postMessage, query/hash ani eksportu JSON/HTML jako podstawowego mechanizmu działania.
- Docelowa struktura modułu ma opierać się na:
  - index.html — główna wersja generatora offline,
  - index_backup.html — kopia/backup głównej wersji offline,
  - index_test.html — wersja testowa generatora offline.
- Pliki GM.html, DataSlate.html, GM_backup.html, DataSlate_backup.html, GM_test.html i DataSlate_test.html są tylko tymczasowym materiałem referencyjnym. Nie usuwaj ich jeszcze w Etapie 3, ale nie traktuj ich jako aktywnej docelowej struktury.
- Folder DataSlate/ jest chroniony i wolno go używać wyłącznie referencyjnie. Nie modyfikuj go.

Zakres Etapu 3:

1. Przebuduj DataSlate_Offline/index.html z obecnego launchera w panel generatora offline.

2. Panel generatora ma zawierać kontrolki potrzebne Mistrzowi Gry:
   - wybór tła,
   - wybór logotypu,
   - przełącznik widoczności loga,
   - wybór fontu,
   - wybór fillera,
   - ustawienia kolorów,
   - treść wiadomości,
   - liczba linii fillerów,
   - reset formularza do ustawień domyślnych,
   - czyszczenie treści wiadomości, jeżeli łatwo zachować tę funkcję lokalnie.

3. Dostosuj UI do trybu offline:
   - nazwa widoczna w interfejsie: DataSlate Offline,
   - usuń/nie pokazuj statusu Firebase,
   - usuń przyciski i terminologię: Wyślij, Ping, połączenie, odbiornik,
   - usuń ślady audio z UI,
   - usuń prostokąt cienia i efekt Flicker z UI,
   - dodaj przycisk Generuj jako główną akcję użytkownika,
   - nie pokazuj komunikatu typu „aplikacja nie używa Firebase” albo „nie wysyła danych do sieci”, bo wcześniejsza decyzja mówi, że użytkownik nie ma widzieć takiej informacji.

4. Zaimplementuj lokalne ładowanie danych:
   - index.html ma korzystać z DataSlate_Offline/assets/data/data.json,
   - nie używaj runtime’owego parsowania DataSlate_manifest.xlsx,
   - nie używaj SheetJS ani CDN SheetJS,
   - nie wymagaj Firebase ani config/firebase-config.js,
   - brak Firebase configu nie może generować błędu.

5. Zaimplementuj lokalne budowanie payloadu:
   - wykorzystaj logikę z obecnego GM.html jako materiał referencyjny,
   - zachowaj możliwie zgodną strukturę payloadu z wersją online,
   - pola audio/ping/Firebase mogą zostać pominięte albo ignorowane w aktywnej ścieżce,
   - payload ma powstawać lokalnie w pamięci,
   - nie zapisuj payloadu do Firestore,
   - nie zapisuj payloadu do localStorage/sessionStorage,
   - nie eksportuj payloadu jako JSON,
   - nie dodawaj kopiowania payloadu,
   - nie dodawaj eksportu gotowego HTML-a.

6. Przycisk Generuj w Etapie 3:
   - powinien co najmniej budować lokalny payload bez błędów,
   - nie musi jeszcze otwierać finalnej nowej karty z wyrenderowanym DataSlate, jeśli to wymagałoby realizacji Etapu 4,
   - jeżeli implementujesz tymczasową reakcję na kliknięcie, niech będzie bezpieczna i lokalna, np. aktualizacja statusu „Payload gotowy” / „Payload ready” albo zapis do zmiennej w pamięci,
   - nie implementuj jeszcze pełnej funkcji openOfflineSlate(payload), buildOfflineSlateHTML(payload) ani document.write(...), chyba że uznasz to za absolutnie konieczne i wyraźnie opiszesz w Offline.md, że zahaczyłeś o Etap 4.

7. Obsługa fontów:
   - menu wyboru fontu zostaje,
   - nazwy fontów z data.json zostają zgodne z wersją online,
   - Google Fonts mogą być użyte, jeżeli aplikacja działa online i fonty są dostępne,
   - brak internetu albo nieudane załadowanie Google Fonts nie może blokować działania generatora,
   - przy niedostępności Google Fonts generator ma używać fontu systemowego,
   - w panelu generatora, najlepiej przy wyborze fontu, pokaż komunikat tylko wtedy, gdy Google Fonts faktycznie nie są dostępne albo nie udało się ich załadować,
   - komunikat musi być przygotowany w obsługiwanych językach interfejsu, co najmniej PL i EN.

Przykładowe komunikaty:

PL:
Google Fonts są niedostępne. Generator użyje fontu systemowego.

EN:
Google Fonts are unavailable. The generator will use a system font.

8. Obsługa języka:
   - jeżeli obecny moduł ma mechanizm wyboru języka, zachowaj go albo odtwórz w index.html,
   - komunikat o fallbacku fontów musi korzystać z tego mechanizmu,
   - nie wpisuj komunikatu wyłącznie na sztywno po polsku ani wyłącznie po angielsku.

9. Layouty zależne od tła:
   - nie rozszerzaj w Etapie 3 pliku assets/data/data.json o layouty zależne od tła,
   - przenieś albo przygotuj do przeniesienia mapę CONTENT_RECTS_BY_BACKGROUND_ID z DataSlate_Offline/DataSlate.html do docelowej aktywnej ścieżki index.html,
   - mapa layoutów jest technicznym elementem renderera potrzebnym do zachowania pozycji tekstu na różnych tłach,
   - jeżeli pełne użycie tej mapy należy dopiero do Etapu 4/5, zachowaj ją w kodzie index.html jako przygotowanie i opisz to w Offline.md.

10. Pliki backup/test:
   - utwórz index_backup.html i index_test.html tylko wtedy, jeżeli bezpiecznie da się je zsynchronizować z index.html w ramach Etapu 3,
   - jeżeli uznasz, że tworzenie index_backup.html i index_test.html powinno nastąpić po stabilizacji index.html, opisz to w Offline.md jako następny krok,
   - nie usuwaj jeszcze GM.html, DataSlate.html, GM_backup.html, DataSlate_backup.html, GM_test.html ani DataSlate_test.html.

11. Nie wykonuj w Etapie 3:
   - pełnego renderowania gotowego DataSlate w nowej karcie, jeżeli wymaga to Etapu 4,
   - przebudowy renderera finalnego ekranu, jeżeli należy to do Etapu 5,
   - usuwania starych plików GM/DataSlate,
   - modyfikacji folderu DataSlate/,
   - zmian w DataSlate_manifest.xlsx,
   - automatycznych testów wizualnych,
   - eksportu/importu payloadu,
   - mechanizmu localStorage/sessionStorage/postMessage/query/hash.

Po zmianach zaktualizuj DataSlate_Offline/Offline.md.

Dopisz nową sekcję dokumentującą wykonanie Etapu 3. Sekcja powinna zawierać:
- pełny prompt użytkownika,
- zakres prac,
- ustalenia i decyzje,
- opis zmian w index.html,
- opis lokalnego ładowania data.json,
- opis lokalnego budowania payloadu,
- opis usunięcia/wyłączenia Firebase, Firestore, Ping, Wyślij i audio z aktywnego UI,
- opis obsługi fontów i fallbacku systemowego,
- opis obsługi komunikatu wielojęzycznego,
- informację, czy CONTENT_RECTS_BY_BACKGROUND_ID został przeniesiony do index.html albo przygotowany do dalszego etapu,
- informację, czy utworzono index_backup.html i index_test.html,
- zmienione pliki,
- testy/sprawdzenia,
- ryzyka i następne kroki.

W testach/sprawdzeniach wykonaj przynajmniej:
- sprawdzenie statusu repozytorium przed i po zmianach,
- walidację składni/struktury HTML na tyle, na ile jest to możliwe statycznie,
- sprawdzenie, że index.html nie importuje Firebase ani config/firebase-config.js,
- sprawdzenie, że index.html nie zawiera Firestore, onSnapshot, currentRef.set ani dataslate/current,
- sprawdzenie, że index.html nie zawiera przycisków Ping/Wyślij ani widocznych śladów audio w UI,
- sprawdzenie, że index.html ładuje assets/data/data.json,
- sprawdzenie, że data.json nadal jest poprawnym JSON-em,
- sprawdzenie, że nie zmodyfikowano folderu DataSlate/,
- jeżeli możliwe, prosty test lokalny w przeglądarce albo statyczny test potwierdzający, że formularz i funkcje JS nie mają oczywistych błędów składniowych.

### Zakres prac

- Przeczytano aktualny `DataSlate_Offline/Offline.md` przed zmianami i wykonano Etap 3 zgodnie z zapisanym planem oraz najnowszymi decyzjami użytkownika.
- Przebudowano aktywny `DataSlate_Offline/index.html` z launchera odsyłającego do `GM.html` i `DataSlate.html` w samodzielny panel generatora offline.
- Przygotowano lokalne ładowanie manifestu z `assets/data/data.json` oraz lokalne budowanie payloadu w pamięci po kliknięciu `Generuj`.
- Nie wdrożono pełnego otwierania nowej karty, `openOfflineSlate(payload)`, `buildOfflineSlateHTML(payload)` ani `document.write(...)`; zakres ten pozostaje dla Etapu 4.
- Nie modyfikowano folderu `DataSlate/`, pliku `DataSlate_manifest.xlsx` ani tymczasowych plików referencyjnych `GM.html`, `DataSlate.html`, `GM_backup.html`, `DataSlate_backup.html`, `GM_test.html`, `DataSlate_test.html`.

### Ustalenia i decyzje

- `index.html` jest od tego etapu aktywnym panelem generatora offline, a dawne pliki GM/DataSlate pozostają wyłącznie materiałem referencyjnym do kolejnych etapów.
- Payload jest budowany wyłącznie lokalnie w zmiennej `lastPayload` oraz pokazywany w roboczym podsumowaniu na ekranie; nie jest zapisywany do Firestore, `localStorage`, `sessionStorage`, query/hash, `postMessage` ani eksportowany do pliku.
- Tymczasowa reakcja przycisku `Generuj` to zbudowanie payloadu, zapis w pamięci i status `Payload gotowy` / `Payload ready`; finalna karta w nowej karcie pozostaje zakresem Etapu 4.
- Pola i mechanizmy Firebase, Firestore, Ping, Wyślij oraz audio zostały pominięte w aktywnym UI i aktywnej ścieżce payloadu.
- Opcje prostokąta cienia i Flicker nie są pokazywane w UI; dla zgodności z późniejszą strukturą payloadu pola `movingOverlay` i `flicker` są ustawiane lokalnie na `false`.

### Opis zmian w `index.html`

- Zastąpiono launcher z linkami do `GM.html`, `DataSlate.html` i widoków testowych pełnym formularzem `DataSlate Offline`.
- Dodano kontrolki: wybór tła, wybór logotypu, przełącznik widoczności loga, wybór fontu, wybór fillera, przełącznik fillerów, liczba linii fillerów, wysokość strefy fillerów, kolory wiadomości/fillerów/loga, rozmiary tekstu, treść wiadomości, `Generuj`, czyszczenie treści, reset formularza i losowanie fillerów.
- Dodano roboczy podgląd, który korzysta z wybranych lokalnych assetów, kolorów, fontu, treści i wylosowanych prefixów/suffixów. Podgląd nie jest jeszcze finalnym rendererem Etapu 4/5.
- Dodano lokalny mechanizm języka PL/EN dla etykiet formularza, statusów i komunikatu fallbacku fontów.

### Opis lokalnego ładowania `data.json`

- `index.html` ładuje dane przez `fetch('assets/data/data.json', { cache: 'no-store' })`.
- Dane z JSON-a wypełniają listy `backgrounds`, `logos`, `fonts` i `fillers`.
- Nie użyto runtime’owego parsowania `DataSlate_manifest.xlsx`.
- Nie użyto SheetJS ani żadnego CDN.
- Struktury `assets/data/data.json` nie zmieniano.

### Opis lokalnego budowania payloadu

- Funkcja `buildPayload()` zbiera bieżący stan formularza i tworzy lokalny obiekt o strukturze możliwie zbliżonej do payloadu z `GM.html`.
- Payload zawiera m.in. `type`, `text`, `backgroundId`, `backgroundFile`, `logoId`, `logoFile`, `fillerId`, `fillerSet`, `fontId`, `fontPreset`, `fillersEnabled`, `showLogo`, `prefixLines`, `suffixLines`, `fillerLineCount`, `fillerBandLines`, kolory, rozmiary fontów, `contentRect`, `nonce` i `createdAt`.
- Payload powstaje po kliknięciu `Generuj`, trafia do zmiennej `lastPayload` i do roboczego podsumowania w panelu.
- Payload nie jest wysyłany, utrwalany ani eksportowany.

### Opis usunięcia/wyłączenia Firebase, Firestore, Ping, Wyślij i audio z aktywnego UI

- `index.html` nie importuje `config/firebase-config.js`, Firebase App, Firestore ani żadnych skryptów zewnętrznych.
- `index.html` nie używa `currentRef.set(...)`, `onSnapshot(...)`, dokumentu `dataslate/current` ani statusów połączenia.
- Aktywny UI nie zawiera przycisków `Wyślij` ani `Ping`.
- Aktywny UI nie zawiera ustawień ani komunikatów audio.
- Brak konfiguracji Firebase nie generuje błędu w aktywnym `index.html`, ponieważ plik nie odwołuje się do Firebase.

### Opis obsługi fontów i fallbacku systemowego

- Menu wyboru fontu pozostało i korzysta z nazw fontów z `assets/data/data.json`.
- `index.html` nie importuje Google Fonts jako zależności wymaganej do działania offline.
- Podgląd i przyszły payload ustawiają wybrany font z fallbackiem `Calibri, Arial, sans-serif`.
- Generator sprawdza dostępność wybranego fontu przez `document.fonts.check(...)`; jeśli font nie jest dostępny w środowisku przeglądarki, pokazuje komunikat fallbacku i nadal działa z fontem systemowym.

### Opis obsługi komunikatu wielojęzycznego

- Dodano przełącznik języka `Polski` / `English`.
- Komunikat fallbacku fontów korzysta z tego samego mechanizmu tłumaczeń co etykiety UI.
- Treść PL: `Google Fonts są niedostępne. Generator użyje fontu systemowego.`
- Treść EN: `Google Fonts are unavailable. The generator will use a system font.`

### `CONTENT_RECTS_BY_BACKGROUND_ID`

- Mapa `CONTENT_RECTS_BY_BACKGROUND_ID` została przeniesiona z `DataSlate_Offline/DataSlate.html` do aktywnego `index.html` jako przygotowanie do kolejnych etapów.
- W Etapie 3 mapa jest już wykorzystywana pomocniczo do pozycjonowania roboczego podglądu i zapisywana w lokalnym payloadzie jako `contentRect`.
- Pełne użycie tej mapy w finalnym rendererze nowej karty pozostaje zakresem Etapu 4/5.

### Pliki backup/test

- Utworzono `DataSlate_Offline/index_backup.html` jako zsynchronizowaną kopię `index.html` po Etapie 3.
- Utworzono `DataSlate_Offline/index_test.html` jako zsynchronizowaną kopię `index.html` po Etapie 3.
- Nie usuwano ani nie modyfikowano starych plików `GM.html`, `DataSlate.html`, `GM_backup.html`, `DataSlate_backup.html`, `GM_test.html`, `DataSlate_test.html`.

### Zmienione pliki

- `DataSlate_Offline/index.html` — przebudowa launchera w aktywny panel generatora offline, lokalne ładowanie `data.json`, lokalne budowanie payloadu, roboczy podgląd, PL/EN, fallback fontów, przygotowana mapa layoutów.
- `DataSlate_Offline/index_backup.html` — nowy backup zsynchronizowany z `index.html` po Etapie 3.
- `DataSlate_Offline/index_test.html` — nowa wersja testowa zsynchronizowana z `index.html` po Etapie 3.
- `DataSlate_Offline/Offline.md` — niniejsza sekcja dokumentująca Etap 3, prompt użytkownika, decyzje, zmiany, testy i następne kroki.

### Testy/sprawdzenia

- `git status --short` przed zmianami — sprawdzono stan repozytorium; brak wcześniejszych zmian roboczych.
- `python3 - <<'PY' ... HTMLParser ... PY` — statyczny parser HTML przetworzył `index.html`, `index_backup.html` i `index_test.html` bez błędu strukturalnego.
- `node --check /tmp/index-script.js` — wyodrębniony skrypt z `index.html` nie ma oczywistych błędów składni JavaScript.
- `python3 -m json.tool DataSlate_Offline/assets/data/data.json >/tmp/data-json-ok` — `data.json` pozostaje poprawnym JSON-em.
- `rg -n "firebase|config/firebase-config|Firestore|onSnapshot|currentRef\.set|dataslate/current|SheetJS|xlsx|cdn" DataSlate_Offline/index.html || true` — aktywny `index.html` nie zawiera importów ani odwołań do Firebase/Firestore/SheetJS/CDN.
- `rg -n "Ping|Wyślij|audio|Audio|Dźwięk|dźwięk|sound|Sound" DataSlate_Offline/index.html || true` — aktywny `index.html` nie zawiera przycisków Ping/Wyślij ani widocznych śladów audio w UI.
- `rg -n "assets/data/data\.json" DataSlate_Offline/index.html` — potwierdzono lokalne ładowanie `assets/data/data.json`.
- `rg -n "localStorage|sessionStorage|postMessage|location\.hash|location\.search|URLSearchParams|document\.write|openOfflineSlate|buildOfflineSlateHTML" DataSlate_Offline/index.html` — potwierdzono brak zakazanych mechanizmów transportu payloadu i brak wejścia w Etap 4.
- `cmp -s DataSlate_Offline/index.html DataSlate_Offline/index_backup.html` oraz `cmp -s DataSlate_Offline/index.html DataSlate_Offline/index_test.html` — potwierdzono synchronizację kopii backup/test z głównym `index.html`.
- `git diff --name-only -- DataSlate` — brak zmian w chronionym folderze `DataSlate/`.
- `git status --short` po zmianach — potwierdzono zmiany tylko w zakresie Etapu 3 i dokumentacji.

### Ryzyka i następne kroki

- Etap 4 powinien dodać finalne `openOfflineSlate(payload)`, `buildOfflineSlateHTML(payload)` i generowanie kompletnej karty w nowej karcie.
- Etap 5 powinien przenieść lub zaadaptować właściwy renderer finalnego ekranu DataSlate, tak aby nowa karta wiernie odtwarzała wygląd wersji online.
- Należy wykonać ręczny test w przeglądarce po uruchomieniu przez lokalny serwer statyczny, ponieważ `fetch('assets/data/data.json')` może być blokowany przy bezpośrednim otwarciu pliku z dysku w części przeglądarek.
- W kolejnych etapach trzeba zdecydować, czy robocze podsumowanie payloadu widoczne w panelu pozostaje jako narzędzie deweloperskie, czy zostanie ukryte przed użytkownikiem końcowym.
- Po stabilizacji aktywnej ścieżki trzeba zdecydować, kiedy usunąć lub zarchiwizować tymczasowe pliki GM/DataSlate.
