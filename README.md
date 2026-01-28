# Analiza rynku mieszkaniowego

## Spis treści
* [Charakterystyka oprogramowania](#charakterystyka-oprogramowania)
* [Prawa autorskie](#prawa-autorskie)
* [Specyfikacja wymagań](#specyfikacja-wymagań)
* [Architektua systemu/oprogramowania](#architektura-systemu-/-oprogramowania)
* [Procedura instalacji i uruchomienia](#procedura-instalacji-i-uruchomienia)
* [Testy](#testy)
* [Instrukcja uruchomiania projektu](#instrukcja-uruchomiania-projektu)

## Charakterystyka oprogramowania
**Analiza rynku mieszkaniowego** to aplikacja analityczna prezentująca podstawową analizę ofert mieszkań na sprzedaż publikowanych na portalu ogłoszeniowym Otodom.pl. System służy do eksploracji struktury rynku nieruchomości mieszkaniowych w Trójmieście w formie interaktywnego dashboardu. Aplikacja umożliwia pracę w dwóch trybach analizy:
- **dane historyczne** – zestaw danych obejmujący styczeń 2026 roku dla obszaru całego Trójmiasta.
- **dane bieżące (webscraping na żywo)** – oferty pobierane dynamicznie dla jednego, wybranego miasta (Gdańsk, Gdynia lub Sopot) w zadanym przedziale czasowym: 1, 3 lub 7 dni.

Użytkownik może zdecydować, czy chce analizować pełny zbiór historyczny dla całej aglomeracji (poprzez zaznaczenie odpowiedniego pola wyboru), czy skupić się na aktualnych ofertach z konkretnego miasta w krótkim zakresie czasu. Wszystkie wyniki prezentowane są w postaci interaktywnych wykresów oraz zagregowanych statystyk opisowych. Dashboard pełni funkcję eksploracyjną i porównawczą, wspierając analizę rynku mieszkaniowego w ujęciu przestrzennym i czasowym.

## Prawa autorskie
* **Autor:** Zuzanna Jaskuła
* **Licencja:** MIT

## Specyfikacja wymagań
*Opis priorytetów: 1 – niezbędne, 2 – istotne.*

| ID        | NAZWA                                  | OPIS                                                                                                                                                       | PRIORYTET | KATEGORIA |
|-----------|----------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|-----------|
| **F-01**  | Wybór trybu analizy                    | Użytkownik może wybrać analizę danych historycznych dla całego Trójmiasta (styczeń 2026) lub danych bieżących dla wybranego miasta i przedziału czasowego. | 1         | Funkcjonalne |
| **F-02**  | Walidacja wyboru parametrów            | System sprawdza, czy użytkownik zaznaczył poprawnie checkbox lub wybrał miasto i przedział czasowy; w przypadku błędu wyświetla ostrzeżenie.               | 1         | Funkcjonalne |
| **F-03**  | Pobieranie danych historycznych        | Po wybraniu danych historycznych aplikacja wczytuje plik `data_january.xlsx` z danymi stycznia 2026.                                                       | 1         | Funkcjonalne |
| **F-04**  | Pobieranie danych bieżących            | System uruchamia skrypty `urls.py`, `webscraping.py` i `cleaning.py` w celu zebrania i przygotowania bieżących ofert mieszkań.                             | 1         | Funkcjonalne |
| **F-05**  | Wyświetlanie interaktywnego dashboardu | Dashboard prezentuje zestawienie kluczowych metryk i wykresów z możliwością porównania wybranych miast lub dzielnic.                                       | 1         | Funkcjonalne |
| **F-06**  | Wyświetlenie danych w postaci tabeli   | W zakładce "Dane" można przeanalizować tabelę, na której oparty jest dashboard.                                                                            | 2         | Funkcjonalne |
| **F-07**  | Zapisywanie wykresów                   | Każdy wykres można powiększyć, przybliżyć, otworzyć w trybie pełnoekranowym i zapisać na urządzeniu.                                                       | 2         | Funkcjonalne |
| **NF-01** | Interaktywność                         | Dashboard umożliwia interaktywną eksplorację danych w przeglądarce.                                                                                        | 1         | Niefunkcjonalne |
| **NF-02** | Obsługa błędów                         | System wyświetla ostrzeżenia przy niepoprawnym wyborze parametrów lub błędach w skryptach.                                                                 | 1         | Niefunkcjonalne |
| **NF-03** | Czytelność interfejsu                  | Dashboard prezentuje dane w formie graficznej i tabelarycznej w sposób przejrzysty i zrozumiały.                                                           | 1         | Niefunkcjonalne |
| **NF-04** | Wydajność                              | Analiza bieżących danych wykonywana w czasie akceptowalnym dla użytkownika.                                                                                | 2         | Niefunkcjonalne |


## Architektura systemu/oprogramowania
Do Architektury rozwoju musisz dopisa Streamlit Architektury uruchomieniowej dopisa wszystkie biblioteki z pythona
### Architektura rozwoju
*Technologie i narzędzia wykorzystywane na etapie tworzenia, testowania i wersjonowania aplikacji.*

| Nazwa technologii | Przeznaczenie |
|------------------|--------------|
| **Python** | Główny język programowania aplikacji |
| **PyCharm 2025.1.1.1** | Zintegrowane środowisko programistyczne (IDE) |
| **GitHub** | Repozytorium kodu źródłowego i kontrola wersji |
| **ChatGPT** | Pomoc przy projektowaniu struktury kodu oraz rozwiązywaniu problemów |
| **pandas** | Przetwarzanie danych, agregacje, statystyki opisowe |
| **plotly.express** | Tworzenie interaktywnych wykresów |
| **BeautifulSoup** | Parsowanie kodu HTML w procesie scrapowania |
| **selenium** | Automatyzacja przeglądarki i dynamiczne pobieranie ofert |
| **requests** | Obsługa zapytań HTTP |
| **json** | Obsługa danych i konfiguracji w formacie JSON |
| **sys** | Zarządzanie środowiskiem uruchomieniowym |
| **subprocess** | Wywoływanie procesów systemowych |
| **time** | Kontrola opóźnień i synchronizacja scrapowania |

### Architektura uruchomieniowa
*Elementy niezbędne do działania aplikacji w środowisku użytkownika końcowego.*

| Nazwa technologii | Przeznaczenie |
|------------------|--------------|
| **Python** | Środowisko uruchomieniowe aplikacji |
| **Streamlit** | Framework webowy do budowy i renderowania dashboardu |
| **Przeglądarka internetowa** | Interfejs dostępu do aplikacji |
| **Pliki `.xlsx`** | Trwałe przechowywanie danych historycznych |
| **Otodom.pl** | Źródło danych ofertowych (scraping bieżący) |

Aplikacja uruchamiana jest lokalnie poprzez interpreter Pythona i framework Streamlit. Interfejs użytkownika renderowany jest w przeglądarce internetowej, gdzie dynamicznie generowany jest dashboard prezentujący wyniki analiz.

## Testy

### Scenariusze testów

| ID       | Wymaganie  | Nazwa scenariusza                      | Kroki do wykonania                                                                                                       | Oczekiwany rezultat                                                                                  |
|----------|------------|----------------------------------------|--------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|
| **T-01** | F-01, F-03 | Wczytanie danych historycznych         | 1. Zaznacz checkbox „Pokaż dane z całego Trójmiasta (styczeń 2026)”.<br>2. Kliknij przycisk „Szukaj”.                    | Dane zostają poprawnie wczytane z pliku `.xlsx`. Wyświetla się dashboard z metrykami i wykresami.    |
| **T-02** | F-01, F-04 | Pobieranie danych bieżących            | 1. Wybierz miasto.<br>2. Wybierz zakres czasowy (1, 3 lub 7 dni).<br>3. Kliknij „Szukaj”.                                | Skrypty scrapujące zostają uruchomione. Dane są pobrane, przetworzone i wyświetlone na dashboardzie. |
| **T-03** | F-02       | Walidacja błędnych parametrów          | 1. Kliknij „Szukaj” bez wyboru miasta i zakresu czasu.<br>2. Nie zaznacz checkboxa.                                      | Wyświetlane jest ostrzeżenie o niepoprawnym wyborze parametrów. Dane nie są wczytywane.              |
| **T-04** | F-02       | Konflikt trybów analizy                | 1. Zaznacz checkbox danych historycznych.<br>2. Jednocześnie wybierz miasto i zakres czasu.<br>3. Kliknij „Szukaj”.      | Aplikacja wyświetla ostrzeżenie i nie przechodzi do analizy.                                         |
| **T-05** | F-05       | Wyświetlanie interaktywnego dashboardu | 1. Przejdź do sekcji "Dashboard" i sprawdź wykresy.                                                                      | Widoczne są statystyki i interaktywne wykresy.                                                       | 
| **T-06** | F-06       | Widok danych surowych                  | 1. Przejdź do zakładki „Dane”.                                                                                           | Wyświetlana jest tabela z pełnym zestawem danych ofertowych.                                         |
| **T-07** | F-07       | Zapisanie wykresu                      | 1. Najedź na wykres.<br>2. W prawym górnym rogu kliknij ikonę aparatu.                                                   | Obraz w rozszerzeniu `.jpg` zostaje zapisany na urządzeniu.                                          |
| **T-08** | NF-02      | Brak wyboru miasta w filtrze           | 1. Zaznacz checkbox „Pokaż dane z całego Trójmiasta (styczeń 2026)”.<br>2. Odznacz wszystkie miasta w filtrze.           | Wyświetlane jest ostrzeżenie o konieczności wybrania minimum jednego miasta. Dane nie są reprezentowane w postaci wizualnej.|
| **T-09** | NF-02      | Przerwanie pobierania danych bieżących | 1. Wybierz miasto.<br>2. Wybierz zakres czasowy (1, 3 lub 7 dni).<br>3. Kliknij „Szukaj”.<br>4.Zamknij wyskakujące okno. | Wyświetlany jest komunikat o zaprzestaniu pobierania danych i konieczności ponownego klinięcia "Szukaj".|

### Sprawozdanie z wykonania scenariuszy testów
Wszystkie testy zostały pozytywnie zaliczone.

## Instrukcja uruchomiania projektu
Poniższa instrukcja opisuje kroki niezbędne do uruchomienia aplikacji w środowisku lokalnym.
1. Pobranie repozytorium – należy sklonować repozytorium projektu na dysk lokalny przy użyciu systemu kontroli wersji Git.
2. Instalacja zależności – projekt wykorzystuje zewnętrzne biblioteki języka Python, których lista znajduje się w pliku `requirements.txt`.
W celu ich instalacji należy wykonać polecenie: ```pip3 install -r requirements.txt```.
3. Uruchomienie aplikacji – po poprawnej instalacji zależności aplikację można uruchomić za pomocą frameworka Streamlit, wykonując jedno z poniższych poleceń:
```streamlit run main.py ``` lub ```python3 -m streamlit run main.py```. Po uruchomieniu aplikacja zostanie automatycznie udostępniona w przeglądarce internetowej.