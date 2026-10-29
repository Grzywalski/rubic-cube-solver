# Solver kostki Rubika 3x3 (kostka1_9.py)

Solver kostki Rubika napisany w czystym Pythonie, układający kostkę metodą warstwa po warstwie (cross → F2L → ostatnia warstwa). Zamiast zaszytych algorytmów speedcubingowych używa **przeszukiwania z gotowymi słownikami**: ruchy są wyszukiwane automatycznie, etap po etapie.

Ten dokument opisuje krótką historię projektu, wyniki testów z kolejnych wersji oraz instrukcję uruchomienia wersji 1.9.

---

## 1. Jak to działa

### Model kostki

Klasa `cube` trzyma sześć ścian jako listy 3x3. Kolory to liczby:

| Ściana | Kolor (liczba) |
|---|---|
| front | 1 |
| right | 2 |
| back | 3 |
| left | 4 |
| up (góra) | 5 |
| down (dół) | 6 |

Dostępne ruchy to `R, RPrime, L, LPrime, U, UPrime, D, DPrime, F, FPrime, B, BPrime` (metody `moveR`, `moveRPrime` itd.). `scramble()` wykonuje 15 losowych ruchów i wypisuje ich listę.

### Metoda: słownik + DFS (meet-in-the-middle)

Każdy etap działa tak samo:

1. **Budowanie słownika (raz).** Z ułożonej kostki wykonywane są wszystkie sekwencje ruchów do określonej głębokości. Dla każdego napotkanego stanu częściowego (klucz = naklejki istotne dla danego etapu) zapamiętywana jest najkrótsza sekwencja, która do niego prowadzi.
2. **Wyszukiwanie.** Z pomieszanej kostki uruchamiany jest DFS z iteracyjnym pogłębianiem (głębokość 1, 2, 3, ...). W każdym węźle sprawdzane jest, czy klucz aktualnego stanu jest w słowniku.
3. **Złożenie rozwiązania.** Jeśli tak, rozwiązaniem jest ścieżka z DFS plus odwrócona sekwencja ze słownika.
4. **Weryfikacja.** Ponieważ klucze są częściowe, kandydat jest sprawdzany na kopii kostki funkcją `check_*`. Dopiero wtedy ruchy są wykonywane na prawdziwej kostce.

Klucze obejmują też elementy ułożone we wcześniejszych etapach, więc kolejne etapy nie psują poprzednich.

### Etapy rozwiązywania

| # | Metoda | Co układa | Dozwolone ruchy | Głębokość słownika | Maks. głębokość DFS |
|---|---|---|---|---|---|
| 1 | `solve_to_cross` | krzyż na dole | wszystkie 12 | 4 | 7 |
| 2 | `solve_f2l_seg1` | slot przód-prawy (narożnik + krawędź) | R, L, U, F (z odwrotnościami) | 5 | 9 |
| 3 | `solve_f2l_seg2` | slot tył-prawy | L, U, B | 5 | 9 |
| 4 | `solve_f2l_seg3` | slot tył-lewy | L, U, B | 5 | 9 |
| 5 | `solve_f2l_seg4` | slot przód-lewy (koniec F2L) | L, U, F | 5 | 9 |
| 6 | `solve_top_cross` | krzyż na górze | R, U, F | 8 | 10 |
| 7 | `solve_top_perm` | orientacja całej górnej ściany (wszystkie narożniki) | R, U, F | 8 (ten sam słownik co krzyż) | 10 |
| 8 | `solve_top_last_edge` | permutacja krawędzi ostatniej warstwy | R, U, F | 10 | 9 |
| 9 | `solve_top_last_corner` | permutacja narożników, kostka kompletnie ułożona | R, U, F | 10 (ten sam słownik co krawędzie) | 9 |

Uwaga: nazwa `top_perm` w kodzie oznacza w praktyce domknięcie orientacji górnej ściany (cała ściana `up` ma kolor 5), a nie permutację.

Jeśli żadna głębokość z zakresu nie da wyniku, etap zwraca napis `"Nie znaleziono rozwiązania w zadanym limicie głębokości."` i taka próba liczy się jako porażka.

### Cache słowników

Słowniki (`dic_cross`, `dic_f2l1` ... `dic_f2l4`, `dic_top_cross`, `dic_top_last_edge`) są zapisywane do pliku `cube_dics.pkl` przez `pickle`. Przy kolejnych uruchomieniach są ładowane z dysku zamiast budowane od nowa.

---

## 2. Krótka historia projektu

| Wersja | Zmiana |
|---|---|
| **1.0** | Pierwszy działający solver, tylko do etapu cross. Kostka oparta o NumPy. Skuteczność 89%, a czas w teście wyszedł ujemny (patrz uwaga pod tabelą). |
| **1.1** | Zamiana NumPy na zwykłe listy Pythona. Ogromne przyspieszenie: średnio ok. 0,1 s na cross i 100% skuteczności. |
| **1.3** | Rozszerzenie do F2L. Najpierw tylko dolna ścianka (70% / 79%), potem obie dolne warstwy naraz (średnio 68,6 s, 60% skuteczności). Jedno wielkie przeszukiwanie okazało się za wolne i zawodne. |
| **1.4** | Podział F2L na **4 segmenty** (po jednym slocie: narożnik + krawędź). Skuteczność skoczyła do 97%, a po wyrzuceniu ruchów `D` i `DPrime` z puli ruchów F2L czas spadł z 10,5 s do 4,1 s (99%). |
| **1.5** | Dalsze odchudzenie pul ruchów w segmentach 1-4 (usunięcie zbędnych ruchów). F2L schodzi do ok. 1 s i 100% skuteczności. |
| **1.6** | Dodanie ostatniej warstwy (top cross, top perm, top last). Skuteczne, ale bardzo wolne: top perm i top last po ok. 20 s średnio. |
| **1.7** | Wyciągnięcie budowania słowników poza metody `solve_*` oraz budowanie ich od **ułożonej** kostki, nie od losowej. Pełne rozwiązanie w 18-26 s, 100% skuteczności. |
| **1.8** | Rozdzielenie `top last` na `top last edge` i `top last corner`. Duża rozbieżność wyników: jeden test 65 s i 90% skuteczności, drugi 1,2 s. |
| **1.9** | Usunięcie ruchów `B`, `BPrime`, `L`, `LPrime` z puli dla top perm, top edge i top corner (zostały R, U, F). Pełne rozwiązanie w ok. 1 s, skuteczność 98-100%. |

---

## 3. Wyniki testów

Każdy test to seria losowych scrambli (15 ruchów). Czas średni to czas całkowity podzielony przez liczbę prób. Liczbę prób wyliczono z czasu całkowitego i średniego.

### Cross (wersje 1.0-1.1)

| Wersja | Próby | Czas całkowity | Czas średni | Skuteczność |
|---|---|---|---|---|
| 1.0 (NumPy) | 100 | -366,19 s (*) | -3,66 s (*) | 89% (89 sukcesów) |
| 1.1 (listy zamiast NumPy) | 100 | 9,54 s | 0,095 s | 100% |
| 1.1 (listy zamiast NumPy) | 100 (**) | 100,63 s | 1,006 s | 100% |

(*) Ujemny czas to oczywisty artefakt pomiaru (np. zmiana zegara systemowego w trakcie testu) i nie należy go traktować jako wyniku. Ważna jest tu skuteczność.
(**) W oryginalnych notatkach przy tym teście wpisano 1000 sukcesów, ale z czasu średniego wynika 100 prób. Prawdopodobnie literówka, więc tu podano 100.

### F2L (wersje 1.3-1.5)

| Wersja | Zakres | Próby | Czas średni | Skuteczność |
|---|---|---|---|---|
| 1.3 | tylko dolna ścianka | 10 | 8,59 s | 70% |
| 1.3 | tylko dolna ścianka | 100 | 6,06 s | 79% |
| 1.3 | obie dolne warstwy | 10 | 68,59 s | 60% |
| 1.4 | F2L w 4 segmentach | 100 | 10,54 s | 97% |
| 1.4 | po usunięciu D i DPrime | 100 | 4,09 s | 99% |
| 1.5 | okrojone pule ruchów w seg. 1-4 | 100 | 1,01 s | 100% |
| 1.5 | okrojone pule ruchów w seg. 1-4 | 100 | 0,84 s | 100% |

### Pełne rozwiązanie (wersje 1.6-1.9)

| Wersja | Próby | Czas całkowity | Czas średni | Skuteczność |
|---|---|---|---|---|
| 1.6 | - | - | top perm i top last ok. 20 s | - |
| 1.7 | 10 | 259,61 s | 25,96 s | 100% |
| 1.7 | 10 | 182,01 s | 18,20 s | 100% |
| 1.8 (nieszczęśliwy test) | 10 | 652,86 s | 65,29 s | 90% (9/10) |
| 1.8 (szczęśliwy test) | 1 | 1,19 s | 1,19 s | 100% (1/1) |
| **1.9** | 100 | 100,19 s | 1,00 s | 98% |
| **1.9** | 100 | 107,28 s | 1,07 s | 99% |
| **1.9** | 100 | 83,54 s | 0,84 s | 100% |

### Wnioski

- Największy skok wydajności dały dwie zmiany: zamiana NumPy na listy (1.1) oraz zawężanie puli ruchów dla każdego etapu (1.4, 1.5, 1.9). Mniejsza pula to wykładowo mniejsze drzewo przeszukiwania.
- Podział dużych etapów na mniejsze (4 segmenty F2L, osobno krawędzie i narożniki ostatniej warstwy) poprawił zarówno skuteczność, jak i czas.
- Próby po 10 sztuk (1.7, 1.8) są za małe, żeby wyciągać twarde wnioski. Wersja 1.8 pokazuje dużą wariancję: pojedyncze trudne scramble potrafią wydłużyć średnią kilkudziesięciokrotnie.
- Wersja 1.9 jest stabilna: ok. 1 s na pełne ułożenie i 98-100% skuteczności na 100 próbach.
- Czasy dotyczą samego rozwiązywania. Budowanie lub wczytanie słowników odbywa się przed startem pomiaru.

---

## 4. Instrukcja uruchomienia

### Wymagania

- Python 3.8 lub nowszy
- Tylko biblioteka standardowa (`random`, `time`, `pickle`, `os`), bez instalowania paczek

### Krok 1: ustaw ścieżkę cache

W pliku `kostka1_9.py` znajduje się na stałe wpisana ścieżka:

```python
path = "C:/Users/PC/Desktop/cube/cube_dics.pkl"
```

Zmień ją na ścieżkę istniejącą na Twoim komputerze (katalog musi istnieć), np. `"cube_dics.pkl"`, żeby plik powstał obok skryptu.

### Krok 2: uruchom

```bash
python kostka1_9.py
```

### Co się dzieje po uruchomieniu

1. **Pierwszy start:** jeśli plik `.pkl` nie istnieje, skrypt buduje wszystkie słowniki (`create_all_dics()`) i zapisuje je na dysk. To najdłuższy i najbardziej pamięciożerny moment, głównie przez słownik ostatniej warstwy (głębokość 10 przy 6 ruchach daje ok. 11,7 mln sekwencji do przejrzenia).
2. **Kolejne starty:** słowniki są wczytywane z pliku, więc start jest dużo szybszy.
3. Skrypt wykonuje test na `rang = 100` losowych scramblach. Dla każdego wypisuje scramble, a po wszystkim:
   - całkowity i średni czas oraz współczynnik sukcesu,
   - średnie czasy poszczególnych etapów (cross, f2l-1...f2l-4, top-cross, top-perm, top-last-edge, top-last-corner),
   - listę nieudanych prób wraz z etapami, które zawiodły.

Liczbę prób zmienisz zmienną `rang` w dolnej części pliku.

### Ważne

- Jeśli zmienisz pule ruchów, głębokości lub definicje kluczy, **usuń stary plik `cube_dics.pkl`**. Inaczej skrypt wczyta nieaktualne słowniki.
- Test uruchamia się od razu przy imporcie pliku (kod jest na poziomie modułu, bez `if __name__ == "__main__":`).

### Użycie na własnej kostce

Metody `solve_*` modyfikują kostkę (wykonują znalezione ruchy) i zwracają listę ruchów jako napisy (`"R"`, `"UPrime"` itd.) albo napis z błędem. Pełne rozwiązanie jednej kostki wygląda tak:

```python
x = cube()
x.scramble()

stages = [x.solve_to_cross, x.solve_f2l_seg1, x.solve_f2l_seg2,
          x.solve_f2l_seg3, x.solve_f2l_seg4, x.solve_top_cross,
          x.solve_top_perm, x.solve_top_last_edge, x.solve_top_last_corner]

solution = []
for stage in stages:
    result = stage()
    if isinstance(result, str):      # napis = błąd (nie znaleziono rozwiązania)
        print("Błąd:", result)
        break
    solution += result

print(" ".join(solution))
```

Żeby użyć tego fragmentu, trzeba najpierw załadować słowniki (jak w pliku) i usunąć lub zakomentować pętlę testową na dole.

---

## 5. Znane ograniczenia i pomysły na dalszy rozwój

- Rozwiązanie składa się wyłącznie z ćwierćobrotów i nie jest optymalne pod względem liczby ruchów. Każdy etap jest optymalny lokalnie, ale nie globalnie.
- Porażki (1-2% w wersji 1.9) wynikają z limitów głębokości i zawężonych pul ruchów: dla części stanów rozwiązanie leży poza przeszukiwaną przestrzenią.
- Ścieżka do pliku `.pkl` jest zapisana na stałe.
- Kod pojedynczych etapów jest bardzo podobny (kopiuj-wklej). Można go zastąpić jedną generyczną funkcją parametryzowaną ruchami, funkcją klucza, słownikiem i funkcją sprawdzającą.
- Warto dodać `if __name__ == "__main__":` oraz wczytywanie własnego stanu kostki zamiast losowego scramble'a.
- Przydałby się większy zestaw testów (np. 1000 prób) dla wersji 1.9, żeby dokładniej oszacować skuteczność i wariancję czasu.
