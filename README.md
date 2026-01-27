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

## Architektura systemu/oprogramowania

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
| **Pliki `.json`** | Zapis danych pomocniczych i wyników scrapowania |
| **Otodom.pl** | Źródło danych ofertowych (scraping bieżący) |

Aplikacja uruchamiana jest lokalnie poprzez interpreter Pythona i framework Streamlit. Interfejs użytkownika renderowany jest w przeglądarce internetowej, gdzie dynamicznie generowany jest dashboard prezentujący wyniki analiz.

