import pandas as pd
from solver import ID3Solver
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import concurrent.futures
import multiprocessing

def train_and_evaluate(depth, X_train, y_train, X_val, y_val):
    solver = ID3Solver(max_depth=depth)
    solver.fit(X_train, y_train)
    predictions = solver.predict(X_val)
    accuracy = accuracy_score(y_val, predictions)
    return depth, accuracy

def main(a, b, c, d ,e):
    # 1. Przygotowanie danych
    df = pd.read_csv('cardio_train.csv', delimiter=';')

    # Zamiana wieku z dni na lata
    df['age_years'] = df['age'] // 365

    # Dyskretyzacja atrybutów z obsługą duplikatów
    df['age_bin'] = pd.cut(df['age_years'], bins=a, labels=False)
    df['weight_bin'] = pd.qcut(df['weight'], q=b, labels=False, duplicates='drop')
    df['height_bin'] = pd.qcut(df['height'], q=c, labels=False, duplicates='drop')
    df['ap_hi_bin'] = pd.qcut(df['ap_hi'], q=d, labels=False, duplicates='drop')
    df['ap_lo_bin'] = pd.qcut(df['ap_lo'], q=e, labels=False, duplicates='drop')

    # Mapowanie 'cardio' na etykiety stringowe
    df['cardio'] = df['cardio'].map({0: "No", 1: "Yes"})

    # Usunięcie oryginalnych kolumn ciągłych
    df = df.drop(columns=['id', 'age', 'weight', 'ap_hi', 'ap_lo', 'age_years', 'height'])

    # Sprawdzenie, czy dyskretyzacja powiodła się
    # print("Rozkład wartości po dyskretyzacji:")
    # print(df.describe())
    # print("Unikalne wartości w binach:")
    # print("age_bin:", df['age_bin'].unique())
    # print("weight_bin:", df['weight_bin'].unique())
    # print("ap_hi_bin:", df['ap_hi_bin'].unique())
    # print("ap_lo_bin:", df['ap_lo_bin'].unique())



    # 2. Podział na zbiory treningowe, walidacyjne i testowe
    X = df.drop(columns=['cardio'])
    y = df['cardio']
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.4, random_state=42, stratify=y
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
    )
    # print("Rozkład klas:")
    # print(y.value_counts())



    # 3. Trenowanie i walidacja
    depths = range(1, 8)
    validation_results = []

    num_workers = multiprocessing.cpu_count()
    print(f"Używanie {num_workers} procesów do równoległego przetwarzania.")

    # Przygotowanie argumentów dla procesów
    args = [(depth, X_train, y_train, X_val, y_val) for depth in depths]

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(train_and_evaluate, *arg) for arg in args]
        for future in concurrent.futures.as_completed(futures):
            depth, accuracy = future.result()
            validation_results.append((depth, accuracy))
            print(f"Dokładność dla głębokości {depth}: {accuracy:.4f}")

    # Sortowanie wyników według głębokości
    validation_results.sort(key=lambda x: x[0])
    depths_sorted = [item[0] for item in validation_results]
    accuracies_sorted = [item[1] for item in validation_results]

    # Znalezienie najlepszej głębokości
    best_depth, best_accuracy = max(validation_results, key=lambda x: x[1])
    print(f"\nNajlepsza głębokość: {best_depth} z dokładnością walidacji: {best_accuracy:.4f}")
    return best_accuracy



    # 4. Ostateczna ocena na zbiorze testowym
    solver = ID3Solver(max_depth=best_depth)
    solver.fit(X_train, y_train)
    test_predictions = solver.predict(X_test)
    test_accuracy = accuracy_score(y_test, test_predictions)
    print(f"Dokładność na zbiorze testowym: {test_accuracy:.4f}")



    # 5. Wykresiki
    plt.figure(figsize=(10, 6))
    plt.plot(depths_sorted, accuracies_sorted, marker='o', linestyle='-')
    plt.title('Dokładność walidacji vs Głębokość drzewa')
    plt.xlabel('Głębokość drzewa')
    plt.ylabel('Dokładność walidacji')
    plt.xticks(depths_sorted)
    plt.grid(True)



if __name__ == '__main__':
    """
    Główna pętla poszukująca najlepszej konfiguracji binów dla cech.
    Iteruje przez wszystkie kombinacje binów (1-5) dla pięciu cech i znajduje najlepszą konfigurację na podstawie dokładności walidacji.
    """
    soFarBest = (0, 0, 0, 0, 0, 0, 0)  # (best_accuracy, a, b, c, d, e)
    total_iterations = 5 ** 5  # 3125 kombinacji
    current_iteration = 0

    for i in range(1, 6):
        for j in range(1, 6):
            for k in range(1, 6):
                for l in range(1, 6):
                    for m in range(1, 6):
                        current_iteration += 1
                        print(f"\nKombinacja {current_iteration}/{total_iterations}: a={i}, b={j}, c={k}, d={l}, e={m}")
                        try:
                            best = (main(i, j, k, l, m), i, j, k, l, m)  # best = (accuracy, a, b, c, d, e)
                            if best[0] > soFarBest[0]:
                                soFarBest = best
                                print(f"Nowa najlepsza konfiguracja: {soFarBest}")
                            else:
                                print(f"Konfiguracja {best[1:]} nie jest lepsza od {soFarBest}")
                        except Exception as e:
                            print(f"Wyjątek dla konfiguracji a={i}, b={j}, c={k}, d={l}, e={m}: {e}")

    print("\nNajlepsza konfiguracja binów:")
    print(f"Dokładność walidacji: {soFarBest[0]:.4f}")
    print(f"Biny: a={soFarBest[1]}, b={soFarBest[2]}, c={soFarBest[3]}, d={soFarBest[4]}, e={soFarBest[5]}")