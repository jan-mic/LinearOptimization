import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.optimize import linprog


# from numpy.matlib import empty

# Współczynniki funkcji celu.
# funckja_celu = [20, -10]

def oblicz(wspolczynniki_k, ograniczenia_k_dolne, ograniczenia_k_gorne, funckja_celu):
    # macierz_wspolczynnikow_ograniczen_gornych = wspolczynniki_k
    wspolczynniki_k_przeciwne = [[value * -1 for value in row] for row in
                                 wspolczynniki_k]
    ograniczenia_k_dolne_przeciwne = [value * -1 if value is not None else None for value in ograniczenia_k_dolne]

    # Zbudowanie macierzy A_ub i wektora b_ub
    wspolczynniki_funkcji_ograniczajacych = wspolczynniki_k + wspolczynniki_k_przeciwne
    ograniczenia_funkcji = ograniczenia_k_gorne + ograniczenia_k_dolne_przeciwne

    # Usunięcie wartości None w A_ub i b_ub
    # if wspolczynniki_funkcji and ograniczenia_funkcji:
    #     ograniczenia_funkcji, wspolczynniki_funkcji = zip(*[
    #         (bound, row) for bound, row in zip(ograniczenia_funkcji, wspolczynniki_funkcji)
    #         if bound is not None
    #     ])
    #     wspolczynniki_funkcji = list(wspolczynniki_funkcji)
    #     ograniczenia_funkcji = list(ograniczenia_funkcji)
    if wspolczynniki_funkcji_ograniczajacych and ograniczenia_funkcji:
        filtered_data = [
            (ograniczenie, wspolczynniki) for ograniczenie, wspolczynniki in
            zip(ograniczenia_funkcji, wspolczynniki_funkcji_ograniczajacych)
            if ograniczenie is not None
        ]

        if filtered_data:  # Sprawdź, czy lista po filtrowaniu nie jest pusta
            ograniczenia_funkcji, wspolczynniki_funkcji_ograniczajacych = zip(*filtered_data)
            wspolczynniki_funkcji_ograniczajacych = list(wspolczynniki_funkcji_ograniczajacych)
            ograniczenia_funkcji = list(ograniczenia_funkcji)

            # for wspolczynnik, ograniczenie in zip(wspolczynniki_funkcji, ograniczenia_funkcji):
            #     if ograniczenie is None:
            #         wspolczynniki_funkcji.remove(wspolczynnik)
            #         ograniczenia_funkcji.remove(ograniczenie)

            #########
            wspolczynniki_funckji_celu = [-x for x in funckja_celu]
            # optymalizacja liniowa: minimalizuje liniowa funkcje celu, rzy zadanych ograniczeniach
            result = linprog(c=wspolczynniki_funckji_celu, A_ub=wspolczynniki_funkcji_ograniczajacych,
                             b_ub=ograniczenia_funkcji,
                             method='highs')

            result2 = linprog(c=funckja_celu, A_ub=wspolczynniki_funkcji_ograniczajacych,
                             b_ub=ograniczenia_funkcji,
                             method='highs')

            # Wyświetlenie wyników
            if result.success:
                print(f"Maksymalny zysk: {-result.fun} zł")
                print(f"Liczba godzin dla W1 (x1): {result.x[0]}")
                print(f"Liczba godzin dla W2 (x2): {result.x[1]}")
                print(f"Liczba godzin dla W1 (x1) i W2 (x2): {result2.x[0]} : {result2.x[1]}")
            else:
                print("Nie znaleziono rozwiązania.")

            # Wyświetlenie rozwiązania jako punkt na wykresie
            if result.success:
                # Rysowanie wykresu
                # plt.figure(figsize=(10, 8))

                # Zakres dla x
                x = np.linspace(0, result.x[0] + 100)

                ##########################

                # Nowe okno w Tkinter
                plot_window = tk.Toplevel()
                plot_window.title("Wykres ograniczeń i rozwiązanie")
                plot_window.geometry("1200x900")

                # Tworzenie figury wykresu
                fig = Figure(figsize=(7, 5), dpi=100)
                ax = fig.add_subplot(111)

                #####################33
                # Rysowanie ograniczeń
                for i in range(len(wspolczynniki_funkcji_ograniczajacych)):
                    x1, x2 = wspolczynniki_funkcji_ograniczajacych[i]
                    if x2 != 0:  # Jeśli współczynnik x2 != 0 (prosta ukośna)
                        y = (ograniczenia_funkcji[i] - x1 * x) / x2
                        ax.plot(x, y, label=f'Ograniczenie {x1}x1 + {x2}x2 = {ograniczenia_funkcji[i]}')
                    else:  # Prosta pionowa (x2 == 0)
                        x_vert = ograniczenia_funkcji[i] / x1 if x1 != 0 else 0
                        ax.axvline(x=x_vert, linestyle='--',
                                   label=f'Ograniczenie {x1}x1 + {x2}x2 = {ograniczenia_funkcji[i]} (pionowe)')

                ax.scatter(result.x[0], result.x[1], color='red', label='Rozwiązanie optymalne')
                ax.annotate(f"({result.x[0]:.2f}, {result.x[1]:.2f})", (result.x[0], result.x[1]),
                            textcoords="offset points",
                            xytext=(-10, 10), ha='center')

                # Rysowanie funkcji celu jako linii na wykresie
                z = wspolczynniki_funckji_celu[0] * result.x[0] + wspolczynniki_funckji_celu[1] * result.x[
                    1]  # Obliczenie poziomu z w punkcie optymalnym
                y_cel = (z - wspolczynniki_funckji_celu[0] * x) / wspolczynniki_funckji_celu[
                    1]  # Równanie funkcji celu przekształcone na y = ...
                ax.plot(x, y_cel, color='purple', linestyle='--',
                        label=f'Funkcja celu f(x1, x2) = {funckja_celu[0]}x1 {"+" if funckja_celu[1] >= 0 else "-"} {abs(funckja_celu[1])}x2 --> max')

                # Dodanie siatki, legendy, tytułu i etykiet osi
                ax.axhline(0, color='black', linewidth=0.5, linestyle="--")
                ax.axvline(0, color='black', linewidth=0.5, linestyle="--")
                ax.set_xlim(0, result.x[0] + 10)
                ax.set_ylim(0, result.x[1] + 10)
                ax.set_xlabel('x1 (Czas pracy W1)')
                ax.set_ylabel('x2 (Czas pracy W2)')
                ax.set_title('Wykres ograniczeń i rozwiązanie')
                ax.legend(loc='upper right')
                ax.grid()
                # ax.show()

                # Osadzanie figury w oknie Tkinter
                canvas = FigureCanvasTkAgg(fig, master=plot_window)
                canvas.draw()
                canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            #########

        else:
            ograniczenia_funkcji = []
            wspolczynniki_funkcji_ograniczajacych = [[], []]
    else:
        ograniczenia_funkcji = []
        wspolczynniki_funkcji_ograniczajacych = [[], []]

    print(ograniczenia_funkcji, wspolczynniki_funkcji_ograniczajacych)


def validate_entry(new_value):
    if new_value == "":
        return True
    if new_value.isdigit():
        return True
    if new_value.startswith('-') and (new_value[1:].isdigit() or new_value[1:] == ""):
        return True
    return False


def window():
    window = tk.Tk()
    window.title("Wybor parametrow")

    # Zarejestruj funkcję walidacji dla pól tekstowych
    validate_command = window.register(validate_entry)

    columns = ["Wyrób szklany", "K1", "K2", "K3"]
    rows = ["W1", "W2"]

    frame = tk.Frame(window)
    frame.pack(anchor='w', padx=10, pady=10)

    entry_params = {
        "width": 10,
        "justify": "center",
        "validate": "key",
        "validatecommand": (validate_command, '%P')  # Rejestracja walidatora
    }

    for column in columns:
        label = tk.Label(frame, text=column, borderwidth=1, relief="solid", width=12, anchor="center")
        label.grid(row=0, column=columns.index(column))

    for row in rows:
        label = tk.Label(frame, text=row, borderwidth=1, relief="solid", width=12, anchor="center")
        label.grid(row=rows.index(row) + 1, column=0)

    entry_k1_w1 = tk.Entry(frame, **entry_params)
    entry_k1_w1.grid(row=1, column=1)
    entry_k1_w2 = tk.Entry(frame, **entry_params)
    entry_k1_w2.grid(row=2, column=1)
    entry_k2_w1 = tk.Entry(frame, **entry_params)
    entry_k2_w1.grid(row=1, column=2)
    entry_k2_w2 = tk.Entry(frame, **entry_params)
    entry_k2_w2.grid(row=2, column=2)
    entry_k3_w1 = tk.Entry(frame, **entry_params)
    entry_k3_w1.grid(row=1, column=3)
    entry_k3_w2 = tk.Entry(frame, **entry_params)
    entry_k3_w2.grid(row=2, column=3)

    entry_k1_w1.insert(0, '-1')
    entry_k1_w2.insert(0, '6')
    entry_k2_w1.insert(0, '1')
    entry_k2_w2.insert(0, '2')
    entry_k3_w1.insert(0, '4')
    entry_k3_w2.insert(0, '1')

    entries = [
        [entry_k1_w1, entry_k1_w2],
        [entry_k2_w1, entry_k2_w2],
        [entry_k3_w1, entry_k3_w2]
    ]

    columns_k = ["Ograniczenia", "MIN", "MAX"]
    rows_k = ["K1", "K2", "K3"]

    frame_k = tk.Frame(window)
    frame_k.pack(anchor="w", padx=10, pady=10)

    for column in columns_k:
        label = tk.Label(frame_k, text=column, borderwidth=1, relief="solid", width=12, anchor="center")
        label.grid(row=0, column=columns_k.index(column))

    for row in rows_k:
        label = tk.Label(frame_k, text=row, borderwidth=1, relief="solid", width=12, anchor="center")
        label.grid(row=rows_k.index(row) + 1, column=0)

    entry_k1_lower_bound = tk.Entry(frame_k, **entry_params)
    entry_k1_lower_bound.grid(row=1, column=1)
    entry_k1_upper_bound = tk.Entry(frame_k, **entry_params)
    entry_k1_upper_bound.grid(row=1, column=2)
    entry_k2_lower_bound = tk.Entry(frame_k, **entry_params)
    entry_k2_lower_bound.grid(row=2, column=1)
    entry_k2_upper_bound = tk.Entry(frame_k, **entry_params)
    entry_k2_upper_bound.grid(row=2, column=2)
    entry_k3_lower_bound = tk.Entry(frame_k, **entry_params)
    entry_k3_lower_bound.grid(row=3, column=1)
    entry_k3_upper_bound = tk.Entry(frame_k, **entry_params)
    entry_k3_upper_bound.grid(row=3, column=2)

    entry_k1_lower_bound.insert(0, '0')
    entry_k1_upper_bound.insert(0, '60')
    entry_k2_lower_bound.insert(0, "")
    entry_k2_upper_bound.insert(0, '24')
    entry_k3_lower_bound.insert(0, '8')
    entry_k3_upper_bound.insert(0, '')

    entries_k_dolne = [entry_k1_lower_bound, entry_k2_lower_bound, entry_k3_lower_bound]
    entries_k_gorne = [entry_k1_upper_bound, entry_k2_upper_bound, entry_k3_upper_bound]

    columns_f = ["Funkcja celu", "W1", "W2"]
    rows_f = ["Zysk"]

    frame_f = tk.Frame(window)
    frame_f.pack(anchor="w", padx=10, pady=10)

    for column in columns_f:
        label = tk.Label(frame_f, text=column, borderwidth=1, relief="solid", width=12, anchor="center")
        label.grid(row=0, column=columns_f.index(column))

    for row in rows_f:
        label = tk.Label(frame_f, text=row, borderwidth=1, relief="solid", width=12, anchor="center")
        label.grid(row=rows_f.index(row) + 1, column=0)

    entry_x1 = tk.Entry(frame_f, **entry_params)
    entry_x1.grid(row=1, column=1)
    entry_x2 = tk.Entry(frame_f, **entry_params)
    entry_x2.grid(row=1, column=2)

    entry_x1.insert(0, '20')
    entry_x2.insert(0, '-10')

    entries_funkcja_celu = [entry_x1, entry_x2]

    def ustaw_ograniczenia(entries, ograniczenia_k):
        for entry in entries:
            value = entry.get()
            if value == "":
                value = None
            else:
                value = int(value)
            ograniczenia_k.append(value)

    def update_data():
        wspolczynniki_k = []
        for row in entries:
            row_values = []
            for entry in row:
                value = entry.get()
                if value == "":
                    value = 0
                else:
                    value = int(value)
                row_values.append(value)
            wspolczynniki_k.append(row_values)

        ograniczenia_k_dolne = []
        ograniczenia_k_gorne = []
        funckja_celu = []

        ustaw_ograniczenia(entries_k_dolne, ograniczenia_k_dolne)
        ustaw_ograniczenia(entries_k_gorne, ograniczenia_k_gorne)
        ustaw_ograniczenia(entries_funkcja_celu, funckja_celu)

        print(wspolczynniki_k, ograniczenia_k_dolne, ograniczenia_k_gorne)
        oblicz(wspolczynniki_k, ograniczenia_k_dolne, ograniczenia_k_gorne, funckja_celu)

    update_button = tk.Button(window, anchor='w', text="Oblicz", command=update_data)
    update_button.pack(anchor='w', padx=10, pady=10)

    window.mainloop()


if __name__ == "__main__":
    window()
