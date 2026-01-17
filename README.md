# Ewolucja Generowania Wideo AI

**Projekt na zaliczenie przedmiotu: Multimedialne metody opracowywania danych**

🔗 **Demo online:** [https://multimedialne-metody-opracowywania-danych.streamlit.app/](https://multimedialne-metody-opracowywania-danych.streamlit.app/)

Interaktywna prezentacja multimedialna w formie osi czasu, przedstawiająca historię rozwoju technologii generowania wideo przez sztuczną inteligencję (od sieci GAN, przez VAE, aż po modele dyfuzyjne).

Aplikacja została zbudowana przy użyciu **Streamlit** oraz biblioteki **TimelineJS** (własna implementacja komponentu).

## Funkcjonalności

*   **Interaktywna Oś Czasu:** Przegląd kluczowych kamieni milowych w rozwoju wideo AI (2014-2024).
*   **Wsparcie dla Dark Mode:** Automatyczne wykrywanie motywu Streamlit (Jasny/Ciemny) i dostosowywanie kolorystyki osi czasu za pomocą inwersji kolorów CSS, z zachowaniem poprawnych barw multimediów.
*   **Szczegółowe Opisy:** Techniczne wyjaśnienia architektur (GAN, VAE, Transformery, Dyfuzja) w panelu bocznym.
*   **Separacja Danych:** Wszystkie wydarzenia przechowywane są w zewnętrznym pliku `timeline_data.json` dla łatwej edycji.

## Wymagania

*   Python 3.12
*   Biblioteki wymienione w `requirements.txt`

## Instalacja

1.  Sklonuj repozytorium lub pobierz pliki projektu.
2.  Zainstaluj wymagane zależności:

```bash
pip install -r requirements.txt
```

## Uruchomienie

Aby uruchomić aplikację, wpisz w terminalu:

```bash
streamlit run app.py
```

Aplikacja powinna otworzyć się automatycznie w domyślnej przeglądarce.

## Struktura Projektu

*   `app.py`: Główny plik aplikacji zawierający logikę Streamlit oraz customowy komponent TimelineJS z obsługą trybu ciemnego.
*   `timeline_data.json`: Plik z danymi wydarzeń wyświetlanych na osi czasu (format zgodny z TimelineJS JSON).
*   `requirements.txt`: Lista wymaganych bibliotek Python.

## Edycja Danych

Aby dodać lub zmienić wydarzenia na osi czasu, edytuj plik `timeline_data.json`. Każde wydarzenie jest obiektem w liście `events` i zawiera pola takie jak:
*   `start_date`: Data rozpoczęcia.
*   `text`: Tytuł (`headline`) i treść (`text`).
*   `media`: Link do obrazu lub wideo (`url`) oraz podpis (`caption`).
