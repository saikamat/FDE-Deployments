from sklearn import datasets
from sklearn.model_selection import train_test_split

def load_iris(test_size=0.2, random_state=42):
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    return (X_train, y_train), (X_test, y_test), feature_names, target_names
