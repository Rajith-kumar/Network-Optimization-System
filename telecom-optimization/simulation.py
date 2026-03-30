import numpy as np
import pandas as pd

# Create base stations
def create_base_stations(num_stations=5, area_size=10):
    stations = []
    for i in range(num_stations):
        stations.append({
            "id": i,
            "x": np.random.uniform(0, area_size),
            "y": np.random.uniform(0, area_size),
           "capacity": np.random.uniform(300, 600)
        })
    return pd.DataFrame(stations)


# Create users
def create_users(num_users=300, area_size=10):
    users = []
    for i in range(num_users):
        users.append({
            "id": i,
            "x": np.random.uniform(0, area_size),
            "y": np.random.uniform(0, area_size),
            "traffic": np.random.uniform(1, 15)
        })
    return pd.DataFrame(users)


# Assign users to nearest base station

def assign_users(users, stations):
    import numpy as np

    # FORCE heavy load on station 0
    probs = [0.8] + [0.2/(len(stations)-1)]*(len(stations)-1)

    users["station_id"] = np.random.choice(
        stations["id"],
        size=len(users),
        p=probs
    )

    return users

#  PASTE HERE (at bottom or anywhere below functions)
def calculate_load(users, stations):
    load = users.groupby("station_id")["traffic"].sum().reset_index()
    load.columns = ["id", "load"]

    stations = stations.merge(load, on="id", how="left")
    stations["load"] = stations["load"].fillna(0)

    stations["congested"] = stations["load"] > stations["capacity"]

    return stations