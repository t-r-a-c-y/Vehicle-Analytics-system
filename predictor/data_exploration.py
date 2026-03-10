import pandas as pd
import plotly.express as px
import json

# Data Exploration (from manual screenshot: df.head())
def dataset_exploration(df):
    table_html = df.head().to_html(
        classes="table table-bordered table-striped table-sm",
        float_format="%.2f",
        justify="center",
        index=False,
    )
    return table_html

# Data description (fixed to df.describe() for stats; manual has df.head() twice, likely typo)
def data_exploration(df):
    table_html = df.describe().to_html(
        classes="table table-bordered table-striped table-sm",
        float_format="%.2f",
        justify="center",
    )
    return table_html

# Exercise a: Rwanda map with districts, boundaries, names, and client counts (always visible labels)
def generate_rwanda_map(df):
    if 'district' not in df.columns:
        return "<p>Error: Add 'district' column to vehicles_ml_dataset.csv with Rwanda district names (e.g., 'Rwamagana').</p>"

    df['district'] = df['district'].str.title().str.strip()

    district_counts = df['district'].value_counts().reset_index()
    district_counts.columns = ['district', 'client_count']

    try:
        with open('dummy-data/rwanda_districts.geojson') as f:
            geojson = json.load(f)
    except Exception as e:
        return f"<p>Error loading GeoJSON: {str(e)}.</p>"

    fig = px.choropleth(
        district_counts,
        geojson=geojson,
        locations='district',
        featureidkey='properties.NAME_2',
        color='client_count',
        color_continuous_scale='Blues',
        labels={'client_count': 'Number of Clients'},
        title='Vehicle Clients per District in Rwanda'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Add always-visible labels with district name and count
    centroids = []
    for feature in geojson['features']:
        district = feature['properties']['NAME_2']
        count = district_counts[district_counts['district'] == district]['client_count'].values
        count = count[0] if len(count) > 0 else 0
        coords = feature['geometry']['coordinates'][0][0] if feature['geometry']['type'] == 'MultiPolygon' else feature['geometry']['coordinates'][0]
        lon = sum(c[0] for c in coords) / len(coords)
        lat = sum(c[1] for c in coords) / len(coords)
        centroids.append({'district': district, 'lon': lon, 'lat': lat, 'label': f"{district}: {count}"})

    centroid_df = pd.DataFrame(centroids)

    fig.add_scattergeo(
        lon=centroid_df['lon'],
        lat=centroid_df['lat'],
        text=centroid_df['label'],
        mode='text',
        textfont=dict(size=10, color='black', family='Arial'),
        textposition='middle center'
    )

    if not any(d in [f['properties']['NAME_2'] for f in geojson['features']] for d in district_counts['district']):
        return "<p>Error: District names don't match GeoJSON. Run update_dataset.py to fix.</p>"

    return fig.to_html(full_html=False, include_plotlyjs=True)