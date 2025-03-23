import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Współczynniki funkcji celu.
funckja_celu = [20, -10]

# Ograniczenia dla zmiennych
k1_lower_bound = 0
k1_upper_bound = 60
k2_lower_bound = None
k2_upper_bound = 24
k3_lower_bound = 8
k3_upper_bound = None

k_upper_bounds = [k1_upper_bound, k2_upper_bound, k3_upper_bound]
k_lower_bounds = [k1_lower_bound, k2_lower_bound, k3_lower_bound]
k_lower_bounds = [value * -1 if value is not None else None for value in k_lower_bounds]

# Czas pracy krążków
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

# Zbudowanie macierzy A_ub i wektora b_ub
A_ub = macierz_wspolczynnikow_ograniczen_gornych + macierz_wspolczynnikow_ograniczen_dolnych
b_ub = k_upper_bounds + k_lower_bounds

# Usunięcie wartości None w A_ub i b_ub
b_ub, A_ub = zip(*[
    (bound, row) for bound, row in zip(b_ub, A_ub)
    if bound is not None
])
A_ub = list(A_ub)
b_ub = list(b_ub)

# Ograniczenia zmiennych decyzyjnych (x1 i x2)
x_bounds = (0, None)
y_bounds = (0, None)
wspolczynniki_funckji_celu=[-x for x in funckja_celu]
# Rozwiązywanie problemu optymalizacyjnego
result = linprog(wspolczynniki_funckji_celu, A_ub=A_ub, b_ub=b_ub, bounds=[x_bounds, y_bounds], method='highs')

# Wyświetlenie wyników
if result.success:
    print(f"Maksymalny zysk: {-result.fun} zł")
    print(f"Liczba godzin dla W1 (x1): {result.x[0]}")
    print(f"Liczba godzin dla W2 (x2): {result.x[1]}")
else:
    print("Nie znaleziono rozwiązania.")

# Rysowanie wykresu
plt.figure(figsize=(10, 8))

# Zakres dla x
x = np.linspace(0, 100)

# Rysowanie ograniczeń
for i in range(len(A_ub)):
    x1, x2 = A_ub[i]
    if x2 != 0:  # Jeśli współczynnik x2 != 0 (prosta ukośna)
        y = (b_ub[i] - x1 * x) / x2
        plt.plot(x, y, label=f'Ograniczenie {x1}x1 + {x2}x2 = {b_ub[i]}')
    else:  # Prosta pionowa (x2 == 0)
        x_vert = b_ub[i] / x1 if x1 != 0 else 0
        plt.axvline(x=x_vert, linestyle='--', label=f'Ograniczenie {x1}x1 + {x2}x2 = {b_ub[i]} (pionowe)')

# Wyświetlenie rozwiązania jako punkt na wykresie
if result.success:
    plt.scatter(result.x[0], result.x[1], color='red', label='Rozwiązanie optymalne')
    plt.annotate(f"({result.x[0]:.2f}, {result.x[1]:.2f})", (result.x[0], result.x[1]), textcoords="offset points",
                 xytext=(-10, 10), ha='center')

    # Rysowanie funkcji celu jako linii na wykresie
    z = wspolczynniki_funckji_celu[0] * result.x[0] + wspolczynniki_funckji_celu[1] * result.x[1]  # Obliczenie poziomu z w punkcie optymalnym
    y_cel = (z - wspolczynniki_funckji_celu[0] * x) / wspolczynniki_funckji_celu[1]  # Równanie funkcji celu przekształcone na y = ...
    plt.plot(x, y_cel, color='purple', linestyle='--', label=f'Funkcja celu f(x1, x2) = {funckja_celu[0]}x1 {'+' if funckja_celu[1] >= 0 else '-'} {wspolczynniki_funckji_celu[1].__abs__()}x2 --> max')

# Dodanie siatki, legendy, tytułu i etykiet osi
plt.axhline(0, color='black', linewidth=0.5, linestyle="--")  # Oś X
plt.axvline(0, color='black', linewidth=0.5, linestyle="--")  # Oś Y
plt.xlim(0, 30)
plt.ylim(0, 30)
plt.xlabel('x1 (Czas pracy W1)')
plt.ylabel('x2 (Czas pracy W2)')
plt.title('Wykres ograniczeń i rozwiązanie')
plt.legend()
plt.grid()
plt.show()
