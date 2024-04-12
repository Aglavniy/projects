from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib
import pandas as pd


def train(train_csv: str) -> str:
    """Обучение модели логистической регрессии
    на тренировочной выборке и сохранение модели."""

    train = pd.read_csv(train_csv)

    X = train.drop('target', axis=1)
    y = train['target']

    pipe = Pipeline([
        ('scaler', StandardScaler()),
        ('log', LogisticRegression())
    ])

    pipe.fit(X, y)

    joblib.dump(pipe, 'model.pkl')

    return


#train('./dataset/iris_train.csv')
