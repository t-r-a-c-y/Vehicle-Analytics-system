import pandas as pd
import plotly.express as px
import json

# From manual page 5: Data Exploration (head of dataset)
def dataset_exploration(df):
    table_html = df.head().to_html(
        classes="table table-bordered table-striped table-sm",
        float_format="%.2f",
        justify="center",
        index=False,
    )
    return table_html

# From manual page 5: Data description (statistical summary)
def data_exploration(df):
    table_html = df.describe().to_html(
        classes="table table-bordered table-striped table-sm",
        float_format="%.2f",
        justify="center",
    )
    return table_html

# For exercise 19a: Generate Rwanda map with districts and client counts
def generate_rwanda_map(df):
    if 'district' not in df.columns:
        return "<p>Error: 'district' column missing in vehicles_ml_dataset.csv. Add it with Rwanda district names.</p>"

    # Normalize district names for matching (title case, strip whitespace)
    df['district'] = df['district'].str.title().str.strip()

    district_counts = df['district'].value_counts().reset_index()
    district_counts.columns = ['district', 'client_count']

    try:
        with open('dummy-data/rwanda_districts.geojson') as f:
            geojson = json.load(f)
    except Exception as e:
        return f"<p>Error loading rwanda_districts.geojson: {str(e)}</p>"

    fig = px.choropleth(
        district_counts,
        geojson=geojson,
        locations='district',
        featureidkey='properties.shapeName',  # Change to 'properties.name' if your GeoJSON uses that
        color='client_count',
        color_continuous_scale='Blues',
        labels={'client_count': 'Number of Clients'},
        title='Vehicle Clients per District in Rwanda'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    if district_counts.empty:
        return "<p>No district data available in dataset.</p>"

    # Embed Plotly JS to avoid CDN issues
    return fig.to_html(full_html=False, include_plotlyjs=True)