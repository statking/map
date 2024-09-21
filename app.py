import streamlit as st
import folium
import xml.etree.ElementTree as ET
from streamlit_folium import st_folium
import os

# Function to read and parse all GPX files in the log folder
def get_all_coordinates(log_folder='log'):
    coords = []
    
    # Check if the folder exists
    if not os.path.exists(log_folder):
        st.error(f"The folder '{log_folder}' does not exist.")
        return coords
    
    # Read all XML files in the folder
    for file_name in os.listdir(log_folder):
        if file_name.endswith('.xml'):
            file_path = os.path.join(log_folder, file_name)
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Extract coordinates from the XML file
            for trkpt in root.findall('.//{http://www.topografix.com/GPX/1/1}trkpt'):
                lat = float(trkpt.get('lat'))
                lon = float(trkpt.get('lon'))
                coords.append((lat, lon))
                
    return coords

# Get coordinates from all files in the 'log' folder
coords = get_all_coordinates()

# Check if there are any coordinates to plot
if coords:
    # Create a Folium map centered at the first coordinate
    m = folium.Map(location=coords[0], zoom_start=15)

    # Add the combined route to the map with a thicker line and blue color
    folium.PolyLine(coords, color='blue', weight=5, opacity=1).add_to(m)

    # Streamlit app layout
    st.title("Combined Route Visualization on Map")
    st.write("This map displays the combined movement path from all GPX log files in the 'log' folder.")

    # Display the map in Streamlit
    st_folium(m, width=700, height=500)
else:
    st.warning("No valid GPX data found in the 'log' folder. Please add GPX files.")
