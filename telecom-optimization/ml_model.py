import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
def prepare_features(users, stations):
    import pandas as pd

    # User count per station
    user_count = users.groupby("station_id").size().reset_index(name="user_count")

    # Avg traffic per station
    avg_traffic = users.groupby("station_id")["traffic"].mean().reset_index(name="avg_traffic")

    # Merge everything
    data = stations.merge(user_count, left_on="id", right_on="station_id", how="left")
    data = data.merge(avg_traffic, on="station_id", how="left")

    # Fill missing values
    data["user_count"] = data["user_count"].fillna(0)
    data["avg_traffic"] = data["avg_traffic"].fillna(0)

    # IMPORTANT: include congestion label
    data["congested"] = data["load"] > data["capacity"]

    return data


def train_model(data):
    X = data[["load", "capacity"]]
    y = data["congested"]

    #  ADD THIS CHECK
    if len(y.unique()) < 2:
        print("Not enough classes to train ML model")
        return None

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    return model

def predict_congestion(model, data):
    if model is None:
        print("Skipping prediction (model not trained)")
        return data

    X = data[["load", "capacity"]]
    predictions = model.predict(X)

    data["predicted_congestion"] = predictions
    return data