from sklearn.tree import DecisionTreeClassifier

FEATURES = ["distance_km", "raining", "heavy_traffic"]


def train_model(X_train, y_train, max_depth=5):
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)
    return model
