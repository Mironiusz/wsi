import numpy as np

class ID3Solver:
    def __init__(self, max_depth=None):
        self.max_depth = max_depth
        self.tree = None

    def fit(self, X, y):
        """Tworzy drzewo decyzyjne"""
        self.tree = self._build_tree(X, y, depth=0)
        return self.tree

    def predict(self, X):
        """Przewiduje etykiety"""
        return X.apply(self._predict_row, axis=1)

    def _build_tree(self, X, y, depth):
        """Rekurencyjnie buduje drzewo"""
        majority_class = y.mode()[0]

        # Warunki stopu
        if (self.max_depth is not None and depth >= self.max_depth) or y.nunique() == 1 or X.empty:
            return majority_class

        # Szukanie najlepszego atrybutu do podziału
        best_attribute = self._find_best_attribute(X, y)
        if best_attribute is None:
            return majority_class

        tree = {'attribute': best_attribute, 'nodes': {}, 'majority_class': majority_class}

        # Iterujemy po unikalnych wartościach najlepszego atrybutu
        for value in X[best_attribute].unique():
            subset_X = X[X[best_attribute] == value]
            subset_y = y[X[best_attribute] == value]

            # Rekurencyjna budowa poddrzew
            subtree = self._build_tree(subset_X.drop(columns=[best_attribute]), subset_y, depth + 1)
            tree['nodes'][value] = subtree

        return tree

    def _find_best_attribute(self, X, y):
        """Znajduje atrybut z najwyższym information gain"""
        gains = {}
        for col in X.columns:
            gain = self._information_gain(X[col], y)
            gains[col] = gain

        best_attribute = max(gains, key=gains.get)
        if gains[best_attribute] == 0:
            return None
        return best_attribute

    def _information_gain(self, X_col, y):
        """Liczy information gain dla atrybutu"""
        total_entropy = self._entropy(y)
        values = X_col.unique()
        weighted_entropy = 0
        for value in values:
            subset_y = y[X_col == value]
            weight = len(subset_y) / len(y)
            weighted_entropy += weight * self._entropy(subset_y)
        gain = total_entropy - weighted_entropy
        return gain

    def _entropy(self, y):
        """Liczy entropię"""
        probabilities = y.value_counts(normalize=True)
        entropy = -np.sum(probabilities * np.log2(probabilities + 1e-9))
        return entropy

    def _predict_row(self, row):
        """Nawiguje po drzewie, żeby sklasyfikować nowy zestaw danych"""
        node = self.tree
        while isinstance(node, dict):
            attribute = node['attribute']
            majority_class = node['majority_class']
            value = row.get(attribute)

            # Warunek z zadania, gdzie w zbiorze nie ma wszystkich wartości jakiegoś atrybutu
            if value not in node['nodes']:
                return majority_class

            node = node['nodes'][value]

        return node
