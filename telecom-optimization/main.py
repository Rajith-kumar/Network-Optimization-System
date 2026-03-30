from simulation import *
from load_balancer import *
from ml_model import *
from visualization import *

# 1. Create network
stations = create_base_stations()
users = create_users()

# 2. Assign users to nearest stations
users = assign_users(users, stations)

# 3. BEFORE balancing (calculate load + congestion)
stations_before = calculate_load(users, stations.copy())

# 4. Apply load balancing
users, stations_after = rebalance_load(users, stations_before.copy())

# 5. Prepare ML data (use BEFORE data for training)
data_before = prepare_features(users, stations_before)

# 6. Train ML model
model = train_model(data_before)

# 7. Predict congestion on AFTER data
data_after = prepare_features(users, stations_after)
data_after = predict_congestion(model, data_after)

# 8. Print results
print("\nFinal Predictions:\n")
print(data_after)

# 9. Visualization
plot_load(stations_before, stations_after)
plot_congestion(stations_before, stations_after)