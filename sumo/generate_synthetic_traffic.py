import subprocess
import os   
import sys

# Generate synthetic traffic trips and routes for a given sumo network
def generate_traffic(net_file, trip_file, route_file, num_vehicles, end_time):
    if 'SUMO_HOME' not in os.environ: # Check if SUMO_HOME is set 
        print("Error: SUMO_HOME environment variable is not set.")
        sys.exit(1)

    tools_path = os.path.join(os.environ['SUMO_HOME'], 'tools')
    random_trips_script = os.path.join(tools_path, 'randomTrips.py')

    print(f"--- Generating {num_vehicle} synthetic trips ---")

    # Command to generate random trips 
    # -n: network file
    # -o: output trips file
    # -e: end time of generation
    # -p: period (calculates how often to spawn a car to reach num_vehicles by end_time)
    period = end_time / num_vehicles

    trip_cmd = [
        sys.executable, random_trips_script,
        "-n", net_file,
        "-0", trip_file,
        "-e", str(end_time),
        "-p", str(period)
    ]

    subprocess.run(trip_cmd, check=True)
    print(f"Success: Trips saved to {trip_file}")

    print("--- Routing vehicles through the network ---")

    # Command to generate exact routes using sumo's duarouter. This figures out the shortest path for each trip on your specific map
    route_cmd = [
        "duarouter",
        "-n", net_file,
        "-t", trip_file,
        "-o", route_file,
        "--ignore-errors", "true" # Ignores trips that are geographically impossible
    ]

    subprocess.run(route_cmd, check=True)
    print(f"Success: Routes saved to {route_file}")

if __name__ == "__main__":
    NETWORK_FILE = "mapL.net.xml" # Existing network file 
    TRIPS_OUTPUT = "synthetic_trips.trips.xml" # Files to be created 
    ROUTES_OUTPUT = "synthetic_routes.row.xml"

    TOTAL_VEHICLES = 5000 # No. of cars to spawn 
    SIMULATION_SECONDS = 3600 # Simulate 1 hr of traffic

    if not os.path.exists(NETWORK_FILE): 
        print(f"Error: Could not find {NETWORK_FILE}. Make sure it is in the same directory.")
    else:
        generate_traffic(
            net_file=NETWORK_FILE,
            trip_file=TRIPS_OUTPUT,
            route_file=ROUTES_OUTPUT,
            num_vehicles=TOTAL_VEHICLES,
            end_time=SIMULATION_SECONDS
        )