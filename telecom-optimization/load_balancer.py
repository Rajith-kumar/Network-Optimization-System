import numpy as np

def rebalance_load(users, stations):
    users = users.copy()
    stations = stations.copy()

    congested_stations = stations[stations["congested"] == True]

    for _, station in congested_stations.iterrows():
        station_id = station["id"]

        station_users = users[users["station_id"] == station_id]

        for user_index, user in station_users.iterrows():

            # Compute distances
            distances = np.sqrt(
                (stations["x"] - user["x"])**2 + 
                (stations["y"] - user["y"])**2
            )

            sorted_stations = stations.iloc[distances.argsort()]

            moved = False

            # First try: move to station with available capacity
            for _, target in sorted_stations.iterrows():
                if target["id"] == station_id:
                    continue

                if target["load"] + user["traffic"] <= target["capacity"]:
                    users.at[user_index, "station_id"] = target["id"]

                    stations.loc[stations["id"] == station_id, "load"] -= user["traffic"]
                    stations.loc[stations["id"] == target["id"], "load"] += user["traffic"]

                    moved = True
                    break

            #  Second fallback: move to least loaded station (IMPORTANT)
            if not moved:
                least_loaded = stations.loc[stations["load"].idxmin()]

                if least_loaded["id"] != station_id:
                    users.at[user_index, "station_id"] = least_loaded["id"]

                    stations.loc[stations["id"] == station_id, "load"] -= user["traffic"]
                    stations.loc[stations["id"] == least_loaded["id"], "load"] += user["traffic"]

    # Recalculate congestion
    stations["congested"] = stations["load"] > stations["capacity"]

    return users, stations