import streamlit as st
import json
import os

# --- Load scenario data from JSON in root folder ---
def load_scenarios(json_file="default_scenarios.json"):
    if not os.path.exists(json_file):
        st.error(f"Missing data file: {json_file}")
        return {}
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to read JSON: {e}")
        return {}

# --- Case-insensitive key matcher to prevent field mismatch errors ---
def get_key_case_insensitive(data, target):
    for key in data.keys():
        if key.strip().lower() == target.strip().lower():
            return key
    return None

# --- Display ESG data for selected sector ---
def display_sector_data(sector_data, pretty_name):
    st.subheader(f"📌 Sector Summary: {pretty_name}")
    summary_key = get_key_case_insensitive(sector_data, "Sector Summary")
    for summary in sector_data.get(summary_key, []):
        st.markdown(f"{summary}")

    st.subheader("🌡️ Physical Risks")
    physical_key = get_key_case_insensitive(sector_data, "Physical Risks")
    for risk in sector_data.get(physical_key, []):
        st.markdown(f"- {risk}")

    st.subheader("⚙️ Transition Risks")
    transition_key = get_key_case_insensitive(sector_data, "Transition Risks")
    for risk in sector_data.get(transition_key, []):
        st.markdown(f"- {risk}")

    st.subheader("🔮 Scenario Descriptions")
    scenario_key = get_key_case_insensitive(sector_data, "Scenario Descriptions")
    for scenario in sector_data.get(scenario_key, []):
        st.markdown(f"- {scenario}")

    st.subheader("📘 Implications Under Key Climate Scenarios")
    implications_key = get_key_case_insensitive(sector_data, "Implications Under Key Climate Scenarios")
    implications = sector_data.get(implications_key, [])
    if implications:
        for point in implications:
            st.markdown(f"- {point}")
    else:
        st.write("No implications listed for this sector.")

# --- Main app logic ---
def main():
    st.set_page_config(page_title="ESG Scenario Viewer", layout="wide")
    st.title("🌍 ESG Scenario Viewer")
    st.markdown("Explore climate-related risks, transition impacts, and forward-looking scenarios by sector.")

    data = load_scenarios()
    if not data:
        st.warning("No data found. Please check your JSON file and folder setup.")
        return

    pretty_sectors = {
        key: key.replace("Sector: ", "") if key.startswith("Sector: ") else key
        for key in data.keys()
    }

    selected_pretty = st.selectbox("Choose a sector", list(pretty_sectors.values()))
    actual_key = next((k for k, v in pretty_sectors.items() if v == selected_pretty), None)

    if actual_key and actual_key in data:
        display_sector_data(data[actual_key], selected_pretty)
    else:
        st.warning("Could not find data for selected sector.")

if __name__ == "__main__":
    main()
