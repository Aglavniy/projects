from sklearn.metrics import classification_report
import joblib
import json
import pandas as pd


def test(model_path: str, test_csv: str) -> str:
    """Тестирование модели на тестовой выборке и сохранение результатов."""

    # load model
    model = joblib.load(model_path)

    # load test_csv
    test = pd.read_csv(test_csv)
    X_te = test.drop('target', axis=1)
    y_te = test['target']

    # accuracy
    acc = model.score(X_te, y_te)
    # classification report
    rep = classification_report(y_te, model.predict(X_te))

    metrics = {'accuracy': acc, 'report': rep}
    with open('model_metrics.json', 'w') as f:
        json.dump(metrics, f)
    
    return


#test('./model.pkl', './dataset/iris_test.csv')
