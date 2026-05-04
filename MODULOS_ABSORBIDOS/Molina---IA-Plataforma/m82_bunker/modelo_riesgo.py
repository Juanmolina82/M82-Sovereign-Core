from sklearn.ensemble import RandomForestClassifier

def entrenar_modelo_riesgo(X_train, y_train):
    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=None,
        class_weight="balanced"
    )
    model.fit(X_train, y_train)
    return model
