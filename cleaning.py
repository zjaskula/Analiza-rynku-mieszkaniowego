import sys
import pandas as pd

city = sys.argv[1]
df = pd.read_json("output.json")

# wybór kolumn
df = df[["ID", "URL", "Cena", "Cena_mkw", "Adres", "Opis", "Sprzedawca", "Powierzchnia", "Liczba pokoi", "Piętro", "Czynsz", "Stan wykończenia", "Rynek",
               "Typ ogłoszeniodawcy", "Informacje dodatkowe", "Rok budowy", "Winda", "Rodzaj zabudowy"]].copy()

df.columns = ["ID", "URL", "Cena", "Cena_mkw", "Adres", "Opis", "Sprzedawca", "Powierzchnia", "Pokoje", "Pietro", "Czynsz", "Stan", "Rynek",
               "Typ_ogl", "Informacje", "Rok", "Winda", "Rodzaj"]

# usunięcie ogłoszeń od 2 ogłoszeniodawców, których uznałam za b. niewiarygodnych
df = df[~df['Sprzedawca'].str.contains("https://www.otodom.pl/pl/firmy/biura-nieruchomosci/biuro-sprzedazy-nowych-mieszkanumow-dni-otwarte-ID10104524|https://www.otodom.pl/pl/firmy/biura-nieruchomosci/rynek-pierwotny-biuro-sprzedazy-mieszkan-k-l-sp-z-o-o-ID9169779", case=False, na=False)]
df = df.drop(columns = ["Sprzedawca"])

# usunięcie ogłoszeń z miast, które nie są obecnie rozpatrywane
df = df[df["Adres"].str.contains(city, case=False, na=False)]

# ID - usunięcie "ID: i duplikatów"
df['ID'] = df['ID'].str.replace('ID:', '')
df = df.drop_duplicates(subset='ID', keep='first').reset_index(drop=True)

# usunięcie ogłoszeń, gdzie Adres zawiera wyrażenie "gdański"
df = df[~df['Adres'].str.contains('gdański', case=False, na=False)]

# Adres - podzielenie na ulicę i dzielnicę
df['Adres'] = df['Adres'].map(lambda x: x.lstrip('ul. ').removesuffix(', pomorskie'))
df[['Ulica', 'Dzielnica', 'Miasto']] = df['Adres'].str.split(',', n=2, expand=True)

mask = df['Miasto'].isna() | (df['Miasto'] == "None")
df.loc[mask, 'Miasto'] = df.loc[mask, 'Dzielnica']
df.loc[mask, 'Dzielnica'] = df.loc[mask, 'Ulica']
df.loc[mask, 'Ulica'] = ''

df['Dzielnica'] = df['Dzielnica'].map(lambda x: x.lstrip(' '))
df['Miasto'] = df['Miasto'].map(lambda x: x.lstrip(' '))

df = df.drop(columns = ["Adres"])

# uporządkowanie nazwy Sopotu
df.loc[df['Miasto'].str.contains('Sopot', case=False, na=False), 'Miasto'] = 'Sopot'
df.loc[df['Dzielnica'] == 'Dolny Sopot', 'Dzielnica'] = ''
df.loc[df['Dzielnica'] == 'Górny Sopot', 'Dzielnica'] = ''

# spacje wokół myślnika
df['Dzielnica'] = df['Dzielnica'].str.replace(r'\s*-\s*', '-', regex=True)

# Jelitkowo / Żabianka / Tysiąclecia / Wejhera
mask = df['Dzielnica'].str.contains(r'Jelitkowo|Żabianka|Tysiąclecia|Wejhera', na=False)
df.loc[mask, 'Dzielnica'] = 'Żabianka-Wejhera-Jelitkowo-Tysiąclecia'

# Pustki Cisowskie / Demptowo
mask = df['Dzielnica'].isin(['Pustki Cisowskie', 'Demptowo'])
df.loc[mask, 'Dzielnica'] = 'Pustki Cisowskie-Demptowo'

# Witomino
mask = df['Dzielnica'].str.contains('Witomino', na=False)
df.loc[mask, 'Dzielnica'] = 'Witomino'

# poprawienie nazw ulic
df['Ulica'] = df['Ulica'].str.replace(r'^(al\.|Al\.?|aleja)\s+', 'Aleja ', regex=True)

# Cena - usunięcie [zł]
df['Cena'] = df['Cena'].str[:-2]
df['Cena'] = (df['Cena'].str.replace(' ', '', regex=False).str.replace(',', '.', regex=False))
df['Cena'] = pd.to_numeric(df['Cena'])

# Cena_mkw - usunięcie [zł/m2]
df['Cena_mkw'] = df['Cena_mkw'].str[:-5]
df['Cena_mkw'] = (df['Cena_mkw'].str.replace(' ', '', regex=False).str.replace(',', '.', regex=False))
df['Cena_mkw'] = pd.to_numeric(df['Cena_mkw'])

# Powierzchnia - usunięcie [m2]
df['Powierzchnia'] = df['Powierzchnia'].str[:-3]
df['Powierzchnia'] = df['Powierzchnia'].str.replace(' ','')
df['Powierzchnia'] = pd.to_numeric(df['Powierzchnia'], errors='coerce').round(0)

# Pietro - podział na numer piętra i ilośc pięter w budynku
df[['Pietro', 'L_pieter']] = df['Pietro'].str.split('/', n=1, expand=True)
df.loc[df['Pietro'] == 'parter', 'Pietro'] = '0'
df.loc[df['Pietro'] == 'brak informacji', 'Pietro'] = ''

# Czynsz - brak informacji, usunięcie [zł]
df.loc[df['Czynsz'] == 'brak informacji', 'Czynsz'] = ''
df['Czynsz'] = df['Czynsz'].str[:-11]
df.loc[df['Czynsz'] == '0', 'Czynsz'] = ''
df['Czynsz'] = df['Czynsz'].str.replace(' ','')
df['Czynsz'] = pd.to_numeric(df['Czynsz'])

# Stan
df.loc[df['Stan'] == 'brak informacji', 'Stan'] = ''

# Rynek pierwotny
df.loc[df['Rynek'] == 'brak informacji', 'Rynek'] = ''

# Typ_ogl
df.loc[df['Typ_ogl'] == 'brak informacji', 'Typ_ogl'] = ''

# Winda
df['Winda'] = df['Winda'].map(dict(tak=1, nie=0))

# Informacje - tworzenie nowych kolumn
df.loc[df['Informacje'] == 'brak informacji', 'Informacje'] = ''

df.loc[df['Informacje'].str.contains('balkon', case=False, na=False), 'Balkon'] = 1
df.loc[df['Informacje'].str.contains('dwupoziomowe', case=False, na=False), 'Dwupoziomowe'] = 1
df.loc[df['Informacje'].str.contains('garaż/miejsce parkingowe', case=False, na=False), 'Garaz/miejsce parkingowe'] = 1
df.loc[df['Informacje'].str.contains('oddzielna kuchnia', case=False, na=False), 'Kuchnia'] = 1
df.loc[df['Informacje'].str.contains('ogródek', case=False, na=False), 'Ogrodek'] = 1
df.loc[df['Informacje'].str.contains(r'piwnica|pom\. użytkowe', case=False, na=False), 'Piwnica/komorka'] = 1
df.loc[df['Informacje'].str.contains('taras', case=False, na=False), 'Taras'] = 1

df = df.drop(columns = ["Informacje"])

df = df[['ID', 'Ulica', 'Dzielnica', 'Miasto', 'Cena', 'Powierzchnia', 'Cena_mkw', 'Pokoje', 'Pietro', 'L_pieter', 'Czynsz', 'Stan',
        'Rynek', 'Typ_ogl', 'Rok', 'Rodzaj', 'Winda', 'Balkon', 'Dwupoziomowe', 'Garaz/miejsce parkingowe',
        'Kuchnia', 'Ogrodek', 'Piwnica/komorka', 'Taras', 'URL', 'Opis']]

df.to_excel('cleaned_data.xlsx')