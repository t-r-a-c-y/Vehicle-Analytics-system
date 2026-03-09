import pandas as pd
import plotly.express as px
import json

# Existing functions (dataset_exploration, data_exploration) ...

def generate_rwanda_map(df):
    if 'district' not in df.columns:
        return "<p>Error: No 'district' column in dataset.</p>"

    # Normalize districts to match GeoJSON (e.g., title case)
    df['district'] = df['district'].str.title().str.strip()

    district_counts = df['district'].value_counts().reset_index()
    district_counts.columns = ['district', 'client_count']

    try:
        with open('dummy-data/rwanda_districts.geojson') as f:
            geojson = json.load(f)
    except Exception as e:
        return f"<p>Error loading GeoJSON: {str(e)}</p>"

    fig = px.choropleth(
        district_counts,
        geojson=geojson,
        locations='district',
        featureidkey='properties.shapeName',  # Confirm this matches your GeoJSON (from Step 2)
        color='client_count',
        color_continuous_scale='Blues',
        labels={'client_count': 'Number of Clients'},
        title='Vehicle Clients per District in Rwanda'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # For debug: Print to terminal if no data matches
    if district_counts.empty:
        print("No district data for map")
        return "<p>No district data available.</p>"

    return fig.to_html(full_html=False, include_plotlyjs=True)  # Embed JS to avoid CDN issues