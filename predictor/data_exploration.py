import pandas as pd
import plotly.express as px
import json
import requests  # For downloading GeoJSON

def dataset_exploration(df):
    return df.head().to_html(classes="table table-bordered table-striped table-sm", float_format="%.2f", justify="center", index=False)

def data_exploration(df):
    return df.describe().to_html(classes="table table-bordered table-striped table-sm", float_format="%.2f", justify="center")

# For exercise a: Rwanda map
def generate_rwanda_map(df):
    # Aggregate client counts per district
    district_counts = df['district'].value_counts().reset_index()
    district_counts.columns = ['district', 'client_count']

    # Download GeoJSON (Rwanda districts ADM2)
    geojson_url = 'https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/RWA/ADM2/geoBoundaries-RWA-ADM2.geojson'
    response = requests.get(geojson_url)
    geojson = json.loads(response.text)

    # Create choropleth map
    fig = px.choropleth(
        district_counts,
        geojson=geojson,
        locations='district',
        featureidkey='properties.shapeName',  # Matches district names in GeoJSON
        color='client_count',
        color_continuous_scale='Blues',
        labels={'client_count': 'Number of Clients'},
        title='Vehicle Clients per District in Rwanda'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig.to_html(full_html=False, include_plotlyjs='cdn')