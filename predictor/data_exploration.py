import pandas as pd
import json
import plotly.express as px
import plotly.io as pio

# Data Preview Table
def dataset_exploration(df):
    table_html = df.head().to_html(
        classes="table table-bordered table-striped table-sm",
        float_format="%.2f",
        justify="center",
        index=False,
    )
    return table_html

# Statistical Description Table
def data_exploration(df):
    table_html = df.describe().to_html(
        classes="table table-bordered table-striped table-sm",
        float_format="%.2f",
        justify="center",
    )
    return table_html

# NEW: Rwanda Map Function (Exercise a)
def get_rwanda_map(df):
    # Prepare the data
    district_counts = df['district'].value_counts().reset_index()
    district_counts.columns = ['district', 'client_count']

    # Load the GeoJSON file
    with open('dummy-data/rwanda_districts.geojson', 'r', encoding='utf-8') as f:
        rwanda_geojson = json.load(f)

    # Create the map
    fig = px.choropleth(
        district_counts,
        geojson=rwanda_geojson,
        locations='district',
        # NOTE: Make sure 'NAME_2' matches the key inside your GeoJSON file
        featureidkey='properties.NAME_2', 
        color='client_count',
        color_continuous_scale="Viridis",
        title="Vehicle Clients per District in Rwanda",
        labels={'client_count': 'Number of Clients'}
    )
    
    # Zoom to Rwanda
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

    # Return the map as an HTML string
    return pio.to_html(fig, full_html=False)
