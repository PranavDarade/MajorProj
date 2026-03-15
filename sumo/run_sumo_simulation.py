import os
import sys
import pandas as pd
import traci 

def run_simulation(net_file, route_file, output_csv):
    if 'SUMO_HOME' not in os.environ: # Runs the sumo simulation and extracts edge level traffic data
        sys.exit("Please declare environment variable 'SUMO_HOME'")

    sumo_cmd = [
        "sumo",
        "-m", net_file,
        "-r", route_file,
        "--no-warnings"
    ]

    print("--- Starting SUMO Simulation ---")
    traci.start(sumo_cmd)

    data_records = []
    step = 0

    while traci.simulation.getMinExpectedNumber() > 0: # Run the simulation until all cars have arrived
        traci.simulationStep()

        if step % 60 == 0: # Every 60 steps, record the data (every 60 seconds)
            edge_ids = traci.edge.getIDList()

            for edge_id in edge_ids:
                if not edge_id.startswith(":"): # Skip internal sumo edges
                    vehicle_count = traci.edge.getLastStepVehicleNumber(edge_id)
                    mean_speed = traci.edge.getLastStepMeanSpeed(edge_id)

                    if vehicle_count > 0: # Only record roads that actually have cars on them to keep data clean
                        data_records.append({
                            "timestamp_sec": step,
                            "edge_id": edge_id,
                            "vehicle_count": vehicle_count,
                            "mean_speed_mps": mean_speed
                        })
        step +=1
    
    traci.close()
    print("--- Simulation Complete ---")

    df = pd.DataFrame(data_records) # Transform the raw records into a pandas dataframe
    df.to_csv(output_csv, index=False)
    print(f"Success: Traffic data exported to {output_csv}")
    print(df.head())

if __name__ == "__main__":
    NETWORK_FILE = "mapL.net.xml"
    ROUTE_FILE = "synthetic_routes.rou.xml"
    OUTPUT_CSV = "synthetic_traffic_data.csv"

    run_simulation(NETWORK_FILE, ROUTE_FILE, OUTPUT_CSV)