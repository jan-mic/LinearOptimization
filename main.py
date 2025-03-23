from scipy.optimize import linprog

# Współczynniki funkcji celu.
# Chcemy maksymalizować Z = 20*x1 - 10*x2, więc zmieniamy na minimalizację: -Z
funckja_celu = [-20, 10]

k1_lower_bound = 0
k1_upper_bound = 60
k2_lower_bound = 0
k2_upper_bound = 24
k3_lower_bound = 8
k3_upper_bound = None

k_upper_bounds = [k1_upper_bound, k2_upper_bound, k3_upper_bound]
# k_upper_bounds = [value for value in k_upper_bounds if value is not None]
k_lower_bounds = [-k1_lower_bound, -k2_lower_bound, -k3_lower_bound]
# k_lower_bounds = [value for value in k_lower_bounds if value is not None]

# k time bounds
# k1_bounds = [k1_lower_bound, k1_upper_bound]
# k2_bounds = [k2_lower_bound, k2_upper_bound]
# k3_bounds = [k3_lower_bound, k3_upper_bound]

# czas pracy krazkow dla w1 i w2
k1_w1 = -1
k1_w2 = 6
k2_w1 = 1
k2_w2 = 2
k3_w1 = 4
k3_w2 = 1

k_time_values = {
    "k1": [k1_w1, k1_w2],
    "k2": [k2_w1, k2_w2],
    "k3": [k3_w1, k3_w2]
}

macierz_wspolczynnikow_ograniczen_gornych = [k_time_values[f"k{i}"] for i in range(1, len(k_time_values) + 1)]
macierz_wspolczynnikow_ograniczen_dolnych = [[value * -1 for value in row] for row in
                                             macierz_wspolczynnikow_ograniczen_gornych]

print("k_upper_bounds:", k_upper_bounds)
print("macierz_wspolczynnikow_ograniczen_gornych:", macierz_wspolczynnikow_ograniczen_gornych)
print("macierz_wspolczynnikow_ograniczen_dolnych:", macierz_wspolczynnikow_ograniczen_dolnych)

# Macierz współczynników lewych stron ograniczeń.
A = [
    [-1, 6],  # Ograniczenie dla K1
    [1, 2],  # Ograniczenie dla K2
    [-4, -1]  # Ograniczenie dla K3 (przekształcone na <=)

]

# Wektor wartości prawych stron ograniczeń.
b = [60, 24, -8]

# Ograniczenia dla zmiennych decyzyjnych (x1 >= 0, x2 >= 0).
x_bounds = (0, None)  # x1 >= 0
y_bounds = (0, None)  # x2 >= 0

# Rozwiązywanie problemu optymalizacyjnego.
# result = linprog(funckja_celu, A_ub=A, b_ub=b, bounds=[x_bounds, y_bounds], method='highs')

A_ub = macierz_wspolczynnikow_ograniczen_gornych + macierz_wspolczynnikow_ograniczen_dolnych
b_ub = k_upper_bounds + k_lower_bounds

# Tworzenie nowych list bez wartości None
b_ub, A_ub = zip(*[
    (bound, row) for bound, row in zip(b_ub, A_ub)
    if bound is not None
])

# Konwersja wyników z `zip` na listy
A_ub = list(A_ub)
b_ub = list(b_ub)

result = linprog(funckja_celu, A_ub=A_ub, b_ub=b_ub, bounds=[x_bounds, y_bounds], method='highs')

# Wyświetlenie wyników.
if result.success:
    print(f"Maksymalny zysk: {-result.fun} zł")
    print(f"Liczba godzin dla W1 (x1): {result.x[0]}")
    print(f"Liczba godzin dla W2 (x2): {result.x[1]}")
else:
    print("Nie znaleziono rozwiązania.")
