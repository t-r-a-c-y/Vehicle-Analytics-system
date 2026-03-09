import pandas as pd
import plotly.express as px
import json

def dataset_exploration(df):
    return df.head().to_html(classes="table table-bordered table-striped table-sm", float_format="%.2f", justify="center", index=False)

def data_exploration(df):
    return df.describe().to_html(classes="table table-bordered table-striped table-sm", float_format="%.2f", justify="center")

def generate_rwanda_map(df):
    if 'district' not in df.columns:
        return "<p>Error: 'district' column missing in vehicles_ml_dataset.csv. Add it with Rwanda district names.</p>"

    # Normalize names to match GeoJSON (title case, remove extras)
    df['district'] = df['district'].str.title().str.replace(' District', '').str.strip()

    district_counts = df['district'].value_counts().reset_index()
    district_counts.columns = ['district', 'client_count']

    try:
        with open('dummy-data/rwanda_districts.geojson') as f:
            geojson = json.load(f)
    except Exception as e:
        return f"<p>Error loading GeoJSON: {str(e)}. Ensure rwanda_districts.geojson is in dummy-data/.</p>"

    fig = px.choropleth(
        district_counts,
        geojson=geojson,
        locations='district',
        featureidkey='properties.NAME_2',  # Changed to match your GeoJSON key
        color='client_count',
        color_continuous_scale='Blues',
        labels={'client_count': 'Number of Clients'},
        title='Vehicle Clients per District in Rwanda',
        hover_name='district'  # Show district names on hover
    )
    fig.update_geos(fitbounds="locations", visible=False)  # Zoom to Rwanda boundaries
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Debug: If no matches, show message
    if not any(d in [f['properties']['NAME_2'] for f in geojson['features']] for d in district_counts['district']):
        return "<p>Error: District names don't match GeoJSON. Use standard names like 'Rwamagana', 'Gasabo'.</p>"

    return fig.to_html(full_html=False, include_plotlyjs=True)  # Embed JS, no CDN needed