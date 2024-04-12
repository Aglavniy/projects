from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
import pandas as pd


def load_data() -> str:
    """Загрузка датасета Iris."""
    data = load_iris()

    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.DataFrame(data.target, columns=['target'])

    iris = pd.concat([X, y], axis=1)

    iris.to_csv('./dataset/iris.csv', index=False)

    return


def prepare_data(csv_path: str) -> list[str]:
    """Чтение загруженного датасета и разделение на train и test выборки."""
    df = pd.read_csv(csv_path)
    X = df.drop('target', axis=1)
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=0.2,
                                                        random_state=42)

    iris_test = pd.concat([X_train, y_train], axis=1)
    iris_train = pd.concat([X_test, y_test], axis=1)

    iris_test.to_csv('./dataset/iris_test.csv', index=False)
    iris_train.to_csv('./dataset/iris_train.csv', index=False)

    return


# load_data()
# prepare_data('./dataset/iris.csv')


# print(pd.read_csv('./dataset/iris_test.csv'))
# print(pd.read_csv('./dataset/iris_train.csv'))
# print(pd.read_csv('./dataset/iris.csv'))
