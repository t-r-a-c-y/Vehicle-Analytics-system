import pandas as pd
import plotly.express as px
import json

def dataset_exploration(df):
    return df.head().to_html(classes="table table-bordered table-striped table-sm", float_format="%.2f", justify="center", index=False)

def data_exploration(df):
    return df.describe().to_html(classes="table table-bordered table-striped table-sm", float_format="%.2f", justify="center")

def generate_rwanda_map(df):
    if 'district' not in df.columns:
        return "<p>Error: 'district' column missing.</p>"

    df['district'] = df['district'].str.title().str.strip()

    district_counts = df['district'].value_counts().reset_index()
    district_counts.columns = ['district', 'client_count']

    try:
        with open('dummy-data/rwanda_districts.geojson') as f:
            geojson = json.load(f)
    except Exception as e:
        return f"<p>Error loading rwanda_districts.geojson: {str(e)}.</p>"

    fig = px.choropleth(
        district_counts,
        geojson=geojson,
        locations='district',
        featureidkey='properties.NAME_2',
        color='client_count',
        color_continuous_scale='Blues',
        labels={'client_count': 'Number of Clients'},
        title='Vehicle Clients per District in Rwanda',
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    centroids = []
    for feature in geojson['features']:
        district = feature['properties']['NAME_2']
        count = district_counts[district_counts['district'] == district]['client_count'].values
        count = count[0] if len(count) > 0 else 0
        if feature['geometry']['type'] == 'MultiPolygon':
            coords = feature['geometry']['coordinates'][0][0]
        else:
            coords = feature['geometry']['coordinates'][0]
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
        return "<p>Error: District names don't match GeoJSON.</p>"

    return fig.to_html(full_html=False, include_plotlyjs=True)

def generate_world_map(df):
    if 'country' not in df.columns:
        return "<p>Error: 'country' column missing.</p>"

    df['country'] = df['country'].str.title().str.strip()

    country_counts = df['country'].value_counts().reset_index()
    country_counts.columns = ['country', 'client_count']

    try:
        with open('dummy-data/world.geojson') as f:
            geojson = json.load(f)
    except Exception as e:
        return f"<p>Error loading world.geojson: {str(e)}.</p>"

    fig = px.choropleth(
        country_counts,
        geojson=geojson,
        locations='country',
        featureidkey='properties.ADMIN',
        color='client_count',
        color_continuous_scale='Blues',
        labels={'client_count': 'Number of Clients'},
        title='Vehicle Clients per Country Worldwide',
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    centroids = []
    for feature in geojson['features']:
        country = feature['properties']['ADMIN']
        count = country_counts[country_counts['country'] == country]['client_count'].values
        count = count[0] if len(count) > 0 else 0
        if feature['geometry']['type'] == 'MultiPolygon':
            coords = feature['geometry']['coordinates'][0][0]
        else:
            coords = feature['geometry']['coordinates'][0]
        lon = sum(c[0] for c in coords) / len(coords)
        lat = sum(c[1] for c in coords) / len(coords)
        centroids.append({'country': country, 'lon': lon, 'lat': lat, 'label': f"{country}: {count}"})

    centroid_df = pd.DataFrame(centroids)

    fig.add_scattergeo(
        lon=centroid_df['lon'],
        lat=centroid_df['lat'],
        text=centroid_df['label'],
        mode='text',
        textfont=dict(size=8, color='black', family='Arial'),
        textposition='middle center'
    )

    return fig.to_html(full_html=False, include_plotlyjs=True)