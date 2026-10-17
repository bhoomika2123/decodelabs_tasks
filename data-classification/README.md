# Data Classification Using AI

DecodeLabs Industrial Training Project 2: a beginner-level supervised machine-learning classifier for Iris flowers. It uses scikit-learn's built-in Iris dataset, StandardScaler, and a K-Nearest Neighbors (KNN) model with K=5.

## Dataset and features
The dataset contains 150 samples, four numerical features, and three classes: Setosa, Versicolor, and Virginica. Features are sepal length, sepal width, petal length, and petal width (cm).

## Technologies and workflow
Python, Pandas, NumPy, Matplotlib, and scikit-learn. The program loads and inspects the data, checks missing values, visualizes petal measurements, creates a stratified 80/20 split, fits StandardScaler on training data only, trains KNN, predicts test and new sample classes, and reports evaluation metrics. An optional K=1..15 chart is included; the final model remains K=5.

## Installation and run (Windows / VS Code)
Open the folder in VS Code and open its terminal. Create and activate a virtual environment, install requirements, and run:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

The built-in dataset needs no download. The program displays charts; close the chart windows to finish.

## Expected outputs
The `outputs/` folder contains `prediction_results.csv` (actual and predicted labels), `model_metrics.csv` (accuracy, macro precision, macro recall, macro F1, and K), `confusion_matrix.png`, and `k_value_accuracy.png`.

## Evaluation metrics
Accuracy is the share of correct predictions. Precision measures the correctness of predicted class labels; recall measures how many actual class examples were found; macro F1 averages class-wise F1 equally. Confusion matrix rows are actual classes and columns are predicted classes.

## Future scope
Try other traditional classifiers, compare feature combinations, or use cross-validation while keeping the workflow beginner-friendly.
