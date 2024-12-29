import os
import json  # Corrected from `import data.json`
import requests
import matplotlib.pyplot as plt
import warnings

# Ignore urllib3 warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

# Dynamically determine the path to the JSON file
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_dir, "data.json")

# Fetch Climate Data
def fetch_climate_data():
    try:
        api_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 37.7749,  # Example: San Francisco coordinates
            "longitude": -122.4194,
            "current_weather": True
        }
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        current_weather = data.get("current_weather", {})
        return {
            "global_temp_anomaly": current_weather.get("temperature", 1.2),
            "sea_level_rise_rate": 3.2  # Replace with actual API if available
        }
    except Exception as e:
        print(f"Error fetching climate data: {e}")
        return {
            "global_temp_anomaly": 1.2,
            "sea_level_rise_rate": 3.2
        }

# Fetch Biological Risk Data
def fetch_bio_data():
    return {
        "bio_threat_level": 7,
        "pandemic_preparedness_score": 6.5
    }

# Fetch AI Risk Data
def fetch_ai_data():
    return {
        "ai_threat_level": 8,
        "alignment_progress": 5
    }

# Calculate overall risk score
def calculate_risk(data):
    nuclear_risk = (data["active_nuclear_states"] * 0.4 +
                    data["threat_level"] * 0.4 +
                    data["global_tension_index"] * 0.1 +
                    data["conflict_count"] * 0.1)
    climate_risk = data["global_temp_anomaly"] * 0.6 + data["sea_level_rise_rate"] * 0.4
    bio_risk = data["bio_threat_level"] * 0.7 + (10 - data["pandemic_preparedness_score"]) * 0.3
    ai_risk = data["ai_threat_level"] * 0.6 + (10 - data["alignment_progress"]) * 0.4

    return {
        "nuclear_risk": nuclear_risk,
        "climate_risk": climate_risk,
        "bio_risk": bio_risk,
        "ai_risk": ai_risk,
        "total_risk": nuclear_risk + climate_risk + bio_risk + ai_risk
    }

# Adjusted function for estimated time left
def estimate_time_left(total_risk):
    max_years = 250_000_000  # Best-case scenario (250 million years)
    min_years = 0            # Worst-case scenario
    return max_years - (total_risk / 100 * (max_years - min_years))

# Update JSON Data
def update_json():
    try:
        with open(data_file_path, "r") as file:
            data = json.load(file)

        # Fetch new data
        climate_data = fetch_climate_data()
        bio_data = fetch_bio_data()
        ai_data = fetch_ai_data()

        # Update the JSON data
        data.update(climate_data)
        data.update(bio_data)
        data.update(ai_data)

        # Write the updated data back to the JSON file
        with open(data_file_path, "w") as file:
            json.dump(data, file, indent=4)

        print("data.json updated successfully.")
        return data

    except Exception as e:
        print(f"Error updating JSON: {e}")
        return None

# Visualization for risk index scores
def display_risk_bar_graph(risks, years_left):
    labels = ["Nuclear", "Climate", "Biological", "AI"]
    scores = [risks["nuclear_risk"], risks["climate_risk"], risks["bio_risk"], risks["ai_risk"]]

    plt.figure(figsize=(10, 6))
    plt.bar(labels, scores, color=["red", "green", "purple", "orange"])
    plt.title("Current Risk Index Scores", fontname="Times New Roman", fontsize=14)
    plt.ylabel("Risk Score", fontname="Times New Roman", fontsize=12)
    plt.xlabel("Risk Categories", fontname="Times New Roman", fontsize=12)
    plt.xticks(fontname="Times New Roman", fontsize=10)
    plt.yticks(fontname="Times New Roman", fontsize=10)
    plt.ylim(0, 10)

    # Adjust layout to create more space below the graph
    plt.subplots_adjust(bottom=0.4)

    # Add footnote with years left and sources
    plt.figtext(0.5, 0.15,
                f"Estimated Time Left for Humanity: {years_left:,.2f} years",
                wrap=True, horizontalalignment='center', fontsize=10, color="black", fontweight="bold")

    plt.figtext(0.5, 0.05,
                ("Sources: Nuclear: Calculated based on the number of active nuclear states, their threat level, and global conflict count. "
                 "Climate: Open-Meteo API (https://api.open-meteo.com). "
                 "Biological: The GHS Index (https://www.ghsindex.org). "
                 "AI: The Stanford AI Index (https://index.stanford.edu)."),
                wrap=True, horizontalalignment='center', fontsize=8, color="gray")

    plt.show()

# Main Function
def main():
    data = update_json()
    if not data:
        print("Failed to update data.json. Exiting...")
        return

    # Calculate risk scores
    risks = calculate_risk(data)

    # Estimate time left
    time_left = estimate_time_left(risks["total_risk"])

    # Display results
    print("Risk Scores:")
    for key, value in risks.items():
        if key != "total_risk":
            print(f"{key.replace('_', ' ').title()}: {value:.2f}")
    print(f"Total Risk: {risks['total_risk']:.2f}")
    print(f"Estimated Time Left for Humanity: {time_left:,.2f} years")

    # Visualize results
    display_risk_bar_graph(risks, time_left)

# Run the main function
if __name__ == "__main__":
    main()
