import sys
from pathlib import Path

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import (accuracy_score, precision_score, recall_score,
        f1_score, confusion_matrix, classification_report, ConfusionMatrixDisplay)
except ImportError as error:
    print(f"A required library is missing: {error}. Run: pip install -r requirements.txt")
    sys.exit(1)

def main():
    try:
        iris = load_iris()
        X = pd.DataFrame(iris.data, columns=iris.feature_names)
        y = pd.Series(iris.target, name="target")
        class_names = iris.target_names
        print("Number of samples:", len(X))
        print("Number of features:", X.shape[1])
        print("Feature names:", list(X.columns))
        print("Target names:", list(class_names))
        print("Dataset shape:", X.shape)
        print("First 5 rows:\n", X.head())
        print("Descriptive statistics:\n", X.describe())
        labels = y.map(dict(enumerate(class_names)))
        print("Class distribution:\n", labels.value_counts())
        print("Missing values:\n", X.isnull().sum())
        if X.isnull().any().any():
            raise ValueError("Dataset contains missing values.")

        for name in class_names:
            group = X.loc[labels == name]
            plt.scatter(group["petal length (cm)"], group["petal width (cm)"], label=name)
        plt.xlabel("Petal length (cm)")
        plt.ylabel("Petal width (cm)")
        plt.title("Iris Classes: Petal Measurements")
        plt.legend()
        plt.tight_layout()
        plt.show(block=False)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=42, stratify=y)
        print(f"Training samples: {len(X_train)}")
        print(f"Testing samples: {len(X_test)}")

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        model = KNeighborsClassifier(n_neighbors=5)
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="macro", zero_division=0)
        recall = recall_score(y_test, y_pred, average="macro", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)
        print("Accuracy = correct predictions / total predictions")
        print("Binary formula: (TP + TN) / (TP + TN + FP + FN). Iris is multiclass,")
        print("so overall accuracy counts correct predictions across all three classes.")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision (macro): {precision:.4f}")
        print(f"Recall (macro): {recall:.4f}")
        print(f"F1 Score (macro): {f1:.4f}")
        print("Macro F1 combines precision and recall, averaging the three classes equally.")
        print("TP/TN/FP/FN mean true/false positive/negative in a one-class-vs-rest view.")
        print("Multiclass matrix rows are actual classes; columns are predicted classes.")
        print("Classification report:\n", classification_report(y_test, y_pred, target_names=class_names))

        output_dir = Path(__file__).parent / "outputs"
        output_dir.mkdir(exist_ok=True)
        pd.DataFrame({"Actual": [class_names[i] for i in y_test],
                      "Predicted": [class_names[i] for i in y_pred]}).to_csv(
                          output_dir / "prediction_results.csv", index=False)
        pd.DataFrame({"Metric": ["Accuracy", "Precision", "Recall", "F1 Score", "K"],
                      "Value": [accuracy, precision, recall, f1, 5]}).to_csv(
                          output_dir / "model_metrics.csv", index=False)

        display = ConfusionMatrixDisplay(
            confusion_matrix=confusion_matrix(y_test, y_pred), display_labels=class_names)
        display.plot(cmap="Blues", values_format="d")
        plt.title("KNN Confusion Matrix - Iris Dataset")
        plt.tight_layout()
        plt.savefig(output_dir / "confusion_matrix.png", dpi=150)
        plt.show(block=False)

        k_values, accuracies = [], []
        for k in range(1, 16):
            experiment = KNeighborsClassifier(n_neighbors=k)
            experiment.fit(X_train_scaled, y_train)
            k_values.append(k)
            accuracies.append(accuracy_score(y_test, experiment.predict(X_test_scaled)))
        plt.figure()
        plt.plot(k_values, accuracies, marker="o")
        plt.xlabel("K value")
        plt.ylabel("Accuracy")
        plt.title("K Value vs Accuracy")
        plt.xticks(k_values)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_dir / "k_value_accuracy.png", dpi=150)
        plt.show()

        new_flower = np.array([[5.1, 3.5, 1.4, 0.2]])
        predicted_class = class_names[model.predict(scaler.transform(new_flower))[0]]
        print("Input:", new_flower[0].tolist())
        print("Predicted Class:", predicted_class)
    except Exception as error:
        print(f"The project could not complete: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
