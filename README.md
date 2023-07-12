# web-trip - przykładowa aplikacja Django + DRF


## Fronted
### Wymagania

- Node.js 18.x
- npm 9.6.x

### Setup

1. W konsoli wejdź do katalogu z aplikacją frontendową, np: `cd toys-fe`
2. Zainstaluj zależności: `npm install`

### Uruchomienie

W katalogu z aplikacją frontendową: `npm start`

## Backend
### Wymagania

- Python 3.11.x

### Setup

1. Jeżeli nie utworzyliśmy wirtualnego środowiska np. otwierając projekt w PyCharmie
należy je przygotować. W katalogu z aplikacją backendową: `python -m venv ./venv`

2. Aktywacja środowiska `source ./venv/bin/activate`
3. Instalacja zależnosci: `pip install -r requirements.txt`
4. Wykonanie migracji: `python manage.py migrate`
5. Utworzenie użytkownika panelu administracyjnego: `python manage.py createsuperuser`
6. Pobranie danych z Otwartego Gdańska:
   1. W katalogu z aplikacją backendową utwórz katalog o nazwie `bus_data`
   2. W `bus_data` utwórz katalog o nazwie `schedules`
   3. Zapisz plik z przystankami:
      1. Znajdź plik z przystankami wyszukując 'Lista Przystanków' na stronie https://ckan.multimediagdansk.pl/dataset/tristar 
      2. Pobierz go i zapisz jako `bus_stops.json` w katalogu `bus_data`
   4. Użyj pomocniczego skryptu do pobrania rozkładów:
      1. Znajdź plik z linkami do rozkładów jazdy wyszukując 'Rozkład Jazdy' na stronie https://ckan.multimediagdansk.pl/dataset/tristar
      2. Pobierz go i zapisz jako `stop_times.json` w katalogu `bus_data`
      3. Uruchom skrypt `download_schedules_helper.py`

### Uruchomienie

W katalogu z aplikacją backendową aktywacja środowiska:`source ./venv/bin/activate`
Uruchomienie serwera deweloperskiego: `python manage.py runserver`
