# AGENTS.md — instrukcje dla agentów pracujących w module `DataSlate_Offline`

Ten plik obowiązuje dla folderu `DataSlate_Offline/` oraz wszystkich jego podfolderów.

Moduł `DataSlate_Offline` jest offline’ową wersją modułu DataSlate. Jego celem jest generowanie statycznych ekranów DataSlate w nowej karcie przeglądarki, bez Firebase, bez komunikacji sieciowej i bez odtwarzania dźwięków.

Głównym plikiem kontekstu, dziennikiem decyzji i changelogiem modułu jest:

    DataSlate_Offline/Offline.md

Przed każdą analizą, zmianą kodu, zmianą dokumentacji, refaktoryzacją, testem albo przygotowaniem odpowiedzi dotyczącej tego modułu agent AI musi przeczytać aktualną treść `DataSlate_Offline/Offline.md`.

---

## 1. Zakres modułu

`DataSlate_Offline` ma działać jako samodzielny generator screenshotów dla Mistrza Gry.

Docelowy model działania:

    DataSlate_Offline/index.html → klik „Generuj” → nowa karta przeglądarki z gotowym ekranem DataSlate

Moduł nie jest ekranem odbiorczym dla graczy i nie służy do komunikacji między urządzeniami.

Nie należy przywracać architektury:

    GM → Firebase → DataSlate

W tym module obowiązuje architektura:

    lokalny formularz → lokalny payload → lokalny renderer → nowa karta przeglądarki

---

## 2. Folder `DataSlate/` jest chroniony przed edycją

Agent AI nie może modyfikować folderu `DataSlate/` ani żadnej jego zawartości.

Zakaz obejmuje w szczególności:

- edytowanie plików w `DataSlate/`;
- tworzenie nowych plików w `DataSlate/`;
- usuwanie plików z `DataSlate/`;
- przenoszenie plików z lub do `DataSlate/`;
- zmianę nazw plików w `DataSlate/`;
- formatowanie, porządkowanie albo refaktoryzowanie plików w `DataSlate/`;
- aktualizowanie dokumentacji znajdującej się w `DataSlate/`;
- poprawianie komentarzy w `DataSlate/`;
- podmienianie assetów w `DataSlate/`.

Folder `DataSlate/` może być czytany wyłącznie jako materiał referencyjny dla implementacji wersji offline.

Wszystkie zmiany dotyczące tej pracy mogą być przeprowadzane tylko w folderze:

    DataSlate_Offline/

Jeżeli użytkownik poprosi o zmianę, która wymagałaby ingerencji w `DataSlate/`, agent AI ma nie wykonywać tej zmiany i powinien wyjaśnić, że zgodnie z lokalną instrukcją modyfikacje są ograniczone do `DataSlate_Offline/`.

---

## 3. `Offline.md` jako główne źródło prawdy i changelog

`DataSlate_Offline/Offline.md` należy traktować jako:

- główne źródło prawdy dla modułu offline;
- changelog;
- dziennik decyzji;
- dziennik wymagań;
- dziennik implementacji;
- rejestr promptów użytkownika;
- rejestr testów;
- rejestr ryzyk i następnych kroków.

Nie należy tworzyć osobnych plików changelogowych dla `DataSlate_Offline`, chyba że użytkownik wyraźnie o to poprosi.

Nie wolno usuwać starszych wpisów z `Offline.md`.

Jeżeli późniejsza decyzja zmienia wcześniejsze ustalenia, należy dopisać nową datowaną sekcję wyjaśniającą zmianę i jej wpływ. Nie należy kasować ani przepisywać historii bez wyraźnej prośby użytkownika.

---

## 4. Obowiązkowe dopisywanie promptu użytkownika

Przy każdym nowym poleceniu użytkownika dotyczącym `DataSlate_Offline` agent AI musi dopisać do `DataSlate_Offline/Offline.md` pełen oryginalny prompt użytkownika.

Prompt musi być zapisany bez skracania, parafrazowania i streszczania.

Dotyczy to zarówno poleceń skutkujących zmianą kodu, jak i poleceń analitycznych, projektowych, testowych lub dokumentacyjnych.

Jeżeli użytkownik przekazuje kilka wiadomości, które razem definiują jedno zadanie, należy zapisać wszystkie istotne wiadomości w kolejności chronologicznej albo jasno wskazać, że wpis dotyczy kontynuacji wcześniejszego zadania.

---

## 5. Obowiązkowa aktualizacja `Offline.md` po każdej zmianie

Po każdej modyfikacji modułu `DataSlate_Offline` należy zaktualizować `DataSlate_Offline/Offline.md`.

Aktualizacja musi zawierać informację, co zostało zmienione.

Dotyczy to w szczególności:

- zmian w `index.html`;
- zmian w `GM.html`, jeśli plik pozostanie w module;
- zmian w `DataSlate.html`, jeśli plik pozostanie w module;
- zmian w plikach CSS;
- zmian w plikach JavaScript;
- zmian w assetach;
- zmian w `assets/data/data.json`;
- zmian w nazwach plików;
- zmian w strukturze folderów;
- zmian w dokumentacji;
- zmian w sposobie generowania nowej karty;
- zmian w sposobie działania payloadu;
- zmian w usuwaniu lub ignorowaniu Firebase;
- zmian w usuwaniu lub ignorowaniu audio;
- zmian w testach.

Jeżeli zadanie było tylko analizą i nie zmieniono kodu, należy również dopisać wpis do `Offline.md` z informacją, że kod nie został zmieniony.

---

## 6. Zalecany format wpisu w `Offline.md`

Każda nowa aktualizacja powinna mieć osobną sekcję.

Zalecany format:

    ## Aktualizacja — RRRR-MM-DD — krótki tytuł

    ### Oryginalny pełny prompt użytkownika

    Pełny prompt użytkownika bez skracania.

    ### Zakres prac

    Co zostało sprawdzone, zaplanowane albo zmienione.

    ### Ustalenia i decyzje

    Jakie decyzje, wymagania albo reguły wynikają z tego zadania.

    ### Zmienione pliki

    - `ścieżka/do/pliku` — krótki opis zmiany.

    Jeżeli nie zmieniono plików:

    - Brak zmian w plikach. Zadanie miało charakter analityczny.

    ### Szczegóły zmian

    Dla każdej istotnej zmiany należy opisać:
    - stan przed zmianą;
    - stan po zmianie;
    - powód zmiany.

    ### Testy

    Co zostało sprawdzone i z jakim wynikiem.

    ### Ryzyka i następne kroki

    Co nadal wymaga decyzji, testu albo dalszej pracy.

Jeżeli zakres zadania jest mały, sekcje mogą być krótsze, ale wpis musi zawsze zawierać pełny prompt użytkownika oraz informację, czy i co zmieniono.

---

## 7. Firebase jest poza zakresem modułu offline

W `DataSlate_Offline` nie wolno dodawać ani przywracać zależności od Firebase.

Nie należy używać:

- `firebase-config.js`;
- Firebase App;
- Firebase Auth;
- Firestore;
- Realtime Database;
- dokumentu `dataslate/current`;
- `currentRef.set(...)`;
- `onSnapshot(...)`;
- mechanizmu `GM → Firebase → ekran gracza`;
- komunikatów typu „połączono z Firebase”;
- instrukcji konfiguracji Firebase jako wymagania działania modułu offline.

Jeżeli pliki pochodzące z kopii normalnego DataSlate nadal zawierają kod Firebase, należy go usunąć, odłączyć albo pozostawić wyłącznie jako martwy kod przejściowy do usunięcia w ramach najbliższej refaktoryzacji. Preferowane jest pełne usunięcie zależności Firebase z wersji offline.

---

## 8. Brak komunikacji sieciowej

Moduł `DataSlate_Offline` ma działać bez internetu.

Nie wolno dodawać zależności od:

- CDN;
- zewnętrznych skryptów;
- zewnętrznych fontów;
- zewnętrznych API;
- Firebase;
- zdalnych obrazów;
- zdalnych dźwięków;
- zdalnych arkuszy;
- zdalnych plików JSON.

Wszystkie zasoby potrzebne do działania modułu muszą znajdować się lokalnie w folderze `DataSlate_Offline/`.

---

## 9. Dane wejściowe

Preferowanym źródłem danych dla wersji offline jest:

    DataSlate_Offline/assets/data/data.json

Nie należy opierać podstawowego działania modułu offline na runtime’owym parsowaniu `DataSlate_manifest.xlsx`.

`DataSlate_manifest.xlsx` może pozostać jako materiał źródłowy lub deweloperski, jeżeli użytkownik chce go zachować, ale aplikacja offline powinna działać na gotowym statycznym JSON-ie.

Jeżeli zmieniana jest struktura `data.json`, należy sprawdzić i opisać w `Offline.md`, czy nadal działają:

- lista teł;
- lista logotypów;
- lista fontów;
- lista fillerów;
- mapowanie ścieżek assetów;
- generowanie prefixów i suffixów;
- wybór tła, loga i fontu.

---

## 10. Audio jest poza zakresem modułu offline

W `DataSlate_Offline` nie jest potrzebne odtwarzanie dźwięków.

Nie należy implementować ani naprawiać:

- przycisku `Ping`;
- odtwarzania `Ping.mp3`;
- odtwarzania dźwięku wiadomości;
- wymogu kliknięcia ekranu w celu odblokowania audio;
- ustawień `audioEnabled`;
- ustawień `messageAudioId`;
- ustawień `messageAudioFile`.

Jeżeli pola audio pozostają tymczasowo w payloadzie dla zgodności z wersją online, renderer offline powinien je ignorować.

---

## 11. Przycisk `Generuj`

W module offline podstawową akcją użytkownika ma być przycisk:

    Generuj

Przycisk `Generuj` ma:

1. zebrać aktualny stan formularza;
2. zbudować lokalny payload wiadomości;
3. otworzyć nową kartę przeglądarki;
4. wyrenderować gotowy ekran DataSlate w tej nowej karcie.

Nie wolno zamieniać przycisku `Generuj` na wysyłkę do Firebase.

Nie należy przywracać przycisków `Wyślij` i `Ping`, chyba że użytkownik wyraźnie poprosi o osobny tryb porównawczy lub testowy. Nawet wtedy nie mogą one wymagać Firebase.

---

## 12. Generowanie nowej karty

Preferowany mechanizm generowania powinien być podobny do modułu GeneratorNPC:

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

Nie jest wymagane użycie dokładnie tej funkcji, ale zachowanie ma być równoważne.

Nowa karta powinna zawierać kompletny widok gotowy do screenshotu.

---

## 13. Zachowanie zgodności wizualnej z normalnym DataSlate

Wersja offline powinna możliwie wiernie odtwarzać wygląd normalnego DataSlate.

Należy zachować:

- renderowanie tła;
- renderowanie logo;
- maskowanie lub kolorowanie logo, jeżeli istnieje;
- wybrany font;
- kolory tekstu;
- kolory akcentów;
- fillery;
- prefixy i suffixy;
- ramkę/obszar treści zależny od tła;
- efekty wizualne, o ile mają sens w statycznym screen generatorze;
- dopasowanie do rozmiaru okna.

Każda zmiana wizualna powinna zostać opisana w `Offline.md`.

---

## 14. Payload

Warto zachować strukturę payloadu możliwie bliską wersji online, nawet jeśli część pól nie będzie używana.

Ułatwia to:

- porównywanie wersji online i offline;
- kopiowanie logiki z `GM.html`;
- kopiowanie logiki renderera z `DataSlate.html`;
- przyszłe utrzymanie obu wariantów.

Pola Firebase, audio albo ping mogą pozostać tylko wtedy, gdy nie wymuszają zależności sieciowej i są ignorowane przez renderer offline.

---

## 15. Ścieżki i nazewnictwo

Obowiązująca nazwa folderu:

    DataSlate_Offline

Nie należy samowolnie zmieniać nazwy na:

- `DataSlate_offline`;
- `DataSlateOffline`;
- `OfflineDataSlate`;
- `DataSlate-Offline`.

Jeżeli w repozytorium istnieją inne warianty nazwy, przed zmianą należy zapytać użytkownika albo opisać ryzyko w `Offline.md`.

---

## 16. Komentarze w kodzie

Komentarze w kodzie powinny być aktualne i użyteczne.

Jeżeli plik ma już komentarze dwujęzyczne PL/EN, można zachować ten styl.

Nie wolno zostawiać komentarzy sugerujących, że wersja offline:

- wymaga Firebase;
- wysyła dane do Firestore;
- nasłuchuje dokumentu `dataslate/current`;
- wymaga konfiguracji online;
- wymaga audio;
- działa jako ekran odbiorczy dla drugiego urządzenia.

Komentarze opisujące usuniętą logikę należy usunąć albo zaktualizować.

---

## 17. Testy

Po każdej zmianie należy wykonać testy adekwatne do zakresu pracy i opisać je w `Offline.md`.

Minimalnie należy sprawdzić:

- czy moduł otwiera się bez Firebase;
- czy nie ma błędów wynikających z braku Firebase;
- czy `Generuj` otwiera nową kartę;
- czy nowa karta pokazuje wybrane tło;
- czy nowa karta pokazuje wybrane logo, jeśli logo jest włączone;
- czy treść wiadomości jest widoczna;
- czy fillery są widoczne zgodnie z ustawieniami;
- czy kolory i fonty są stosowane;
- czy moduł nie próbuje odtwarzać dźwięku;
- czy moduł nie wykonuje zewnętrznych żądań sieciowych.

Jeżeli testu nie można wykonać, należy zapisać w `Offline.md`, że test nie został wykonany, oraz podać powód.

---

## 18. Zasady pracy z repozytorium

Nie wolno commitować zmian, chyba że użytkownik wyraźnie o to poprosi.

Nie wolno tworzyć pull requestów, chyba że użytkownik wyraźnie o to poprosi.

Przed zmianą plików należy sprawdzić aktualny stan repozytorium. Nie wolno zakładać, że wcześniejsza analiza jest nadal w pełni aktualna.

Jeżeli użytkownik prosi o przygotowanie treści pliku, należy podać treść w odpowiedzi albo zapisać plik zgodnie z poleceniem użytkownika.

Zmiany powinny być możliwie małe, czytelne i łatwe do opisania w `Offline.md`.
