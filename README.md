# Analiza rynku mieszkaniowego

## Spis treści
* [Charakterystyka oprogramowania](#charakterystyka-oprogramowania)
* [Prawa autorskie](#prawa-autorskie)
* [Specyfikacja wymagań](#specyfikacja-wymagań)
* [Architektua systemu/oprogramowania](#architektura-systemu-/-oprogramowania)
* [Procedura instalacji i uruchomienia](#procedura-instalacji-i-uruchomienia)
* [Testy](#testy)

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

| ID     | NAZWA                                  | OPIS                                                                                                                                                      | PRIORYTET | KATEGORIA |
|--------|----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|-----------|
| **F-01** | Wybór trybu analizy                    | Użytkownik może wybrać analizę danych historycznych dla całego Trójmiasta (styczeń 2026) lub danych bieżących dla wybranego miasta i przedziału czasowego | 1         | Funkcjonalne |
| **F-02**   | Walidacja wyboru parametrów            | System sprawdza, czy użytkownik zaznaczył poprawnie checkbox lub wybrał miasto i przedział czasowy; w przypadku błędu wyświetla ostrzeżenie               | 1         | Funkcjonalne |
| **F-03**   | Pobieranie danych historycznych        | Po wybraniu danych historycznych aplikacja wczytuje plik `data_january.xlsx` z danymi stycznia 2026                                                       | 1         | Funkcjonalne |
| **F-04**   | Pobieranie danych bieżących            | System uruchamia skrypty `urls.py`, `webscraping.py` i `cleaning.py` w celu zebrania i przygotowania bieżących ofert mieszkań                             | 1         | Funkcjonalne |
| **F-05**   | Wyświetlanie interaktywnego dashboardu | Dashboard prezentuje zestawienie kluczowych metryk i wykresów z możliwością porównania wybranych miast lub dzielnic                                       | 1         | Funkcjonalne |
| **F-06**   | Przegląd statystyk ofert               | System prezentuje liczby ogłoszeń, medianę powierzchni, medianę cen, medianę ceny za metr kwadratowy                                                      | 1         | Funkcjonalne |
| **NF-01**  | Interaktywność                         | Dashboard umożliwia interaktywną eksplorację danych w przeglądarce                                                                                        | 1         | Niefunkcjonalne |
| **NF-02**  | Obsługa błędów                         | System wyświetla ostrzeżenia przy niepoprawnym wyborze parametrów lub błędach w skryptach                                                                 | 1         | Niefunkcjonalne |
| **NF-03**  | Czytelność interfejsu                  | Dashboard prezentuje dane w formie graficznej i tabelarycznej w sposób przejrzysty i zrozumiały                                                           | 1         | Niefunkcjonalne |
| **NF-04**  | Wydajność                              | Analiza bieżących danych wykonywana w czasie akceptowalnym dla użytkownika                                                                                | 2         | Niefunkcjonalne |


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

| ID | Wymaganie | Nazwa scenariusza | Warunki początkowe | Kroki do wykonania | Oczekiwany rezultat |
|----|-----------|------------------|--------------------|--------------------|---------------------|
| **T-01** | FR-01, FR-03 | Uruchomienie aplikacji i wczytanie danych historycznych | Aplikacja uruchomiona | 1. Uruchom aplikację.<br>2. Zaznacz checkbox „Pokaż dane z całego Trójmiasta (styczeń 2026)”.<br>3. Kliknij przycisk „Szukaj”. | Dane zostają poprawnie wczytane z pliku `.xlsx`. Wyświetla się dashboard z metrykami i wykresami. |
| **TC-02** | FR-01, FR-04 | Pobieranie danych bieżących | Aplikacja uruchomiona | 1. Wybierz miasto.<br>2. Wybierz zakres czasowy (1, 3 lub 7 dni).<br>3. Kliknij „Szukaj”. | Skrypty scrapujące zostają uruchomione. Dane są pobrane, przetworzone i wyświetlone na dashboardzie. |
| **TC-03** | FR-02 | Walidacja błędnych parametrów | Aplikacja uruchomiona | 1. Kliknij „Szukaj” bez wyboru miasta i zakresu czasu.<br>2. Nie zaznacz checkboxa. | Wyświetlane jest ostrzeżenie o niepoprawnym wyborze parametrów. Dane nie są wczytywane. |
| **TC-04** | FR-02 | Konflikt trybów analizy | Aplikacja uruchomiona | 1. Zaznacz checkbox danych historycznych.<br>2. Jednocześnie wybierz miasto i zakres czasu.<br>3. Kliknij „Szukaj”. | Aplikacja wyświetla ostrzeżenie i nie przechodzi do analizy. |
| **TC-05** | FR-06 | Wyświetlanie metryk | Dane zostały wczytane | 1. Obserwuj górny panel dashboardu. | Widoczne są: liczba ogłoszeń, mediana powierzchni, mediana cen oraz mediana ceny za m². |
| **TC-06** | FR-07 | Rozkład cen za m² | Dane zostały wczytane | 1. Przejdź do sekcji histogramu cen. | Wyświetla się interaktywny histogram cen za m², reagujący na wybrane miasto/miasta. |
| **TC-07** | FR-08 | Mediana ceny wg metrażu | Dane zostały wczytane | 1. Przejdź do wykresu mediany cen wg metrażu. | Wykres słupkowy poprawnie prezentuje mediany w przedziałach metrażowych. |
| **TC-08** | FR-09 | Top najtańsze i najdroższe dzielnice | Dane zawierają ≥ 6 dzielnic | 1. Przejdź do sekcji „Top 3 najtańsze i najdroższe dzielnice”. | Wyświetlany jest wykres słupkowy z podziałem na segmenty „Najtańsze” i „Najdroższe”. |
| **TC-09** | FR-10 | Liczba ofert wg liczby pokoi | Dane zostały wczytane | 1. Przejdź do wykresu liczby ofert wg liczby pokoi. | Wykres słupkowy prezentuje poprawne zliczenia ofert. |
| **TC-10** | FR-11 | Cena za m² wg piętra | Dane zostały wczytane | 1. Przejdź do wykresu cen wg piętra. | Wykres pokazuje medianę ceny za m² dla kolejnych pięter. |
| **TC-11** | FR-12 | Rok budowy – struktura | Dane zawierają informacje o roku budowy | 1. Przejdź do wykresu kołowego roku budowy. | Pie chart prezentuje procentowy rozkład ofert według przedziałów lat budowy. |
| **TC-12** | FR-13 | Cena wg typu ogłoszeniodawcy | Dane zawierają typ ogłoszeniodawcy | 1. Przejdź do wykresu boxplot. | Wyświetlany jest boxplot cen za m² z podziałem na typ ogłoszeniodawcy. |
| **TC-13** | FR-15 | Udogodnienia mieszkań | Dane zawierają informacje o udogodnieniach | 1. Przejdź do sekcji udogodnień. | Wyświetlane są procentowe wartości mieszkań posiadających dane udogodnienia. |
| **TC-14** | FR-16 | Stan wykończenia mieszkań | Dane zawierają informacje o stanie wykończenia | 1. Przejdź do wykresu stanu wykończenia. | Pie chart poprawnie prezentuje strukturę stanu wykończenia mieszkań. |
| **TC-15** | FR-05 | Widok danych surowych | Dane zostały wczytane | 1. Przejdź do zakładki „Dane”. | Wyświetlana jest tabela z pełnym zestawem danych ofertowych. |

### Sprawozdanie z wykonania scenariuszy testów

| ID scenariusza | Wynik | Uwagi |
|----------------|-------|-------|
| TC-01 | Pozytywny | - |
| TC-02 | Pozytywny | - |
| TC-03 | Pozytywny | Poprawna obsługa walidacji |
| TC-04 | Pozytywny | Brak konfliktu trybów |
| TC-05–TC-15 | Pozytywne | Wizualizacje działają zgodnie z założeniami |

## Instrukcja 
1. sklonowanie repozytorium
2. zainstalowanie bibliotek oraz wszystkich ich zależności z pliku requirements.txt
```pip3 install -r requirements.txt```
3. uruchomić streamlit poprzez ```streamlit run main.py ``` lub ```python3 -m streamlit run main.py```