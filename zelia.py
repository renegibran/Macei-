import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import geopandas as gpd

# Função para carregar os dados com caching
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

@st.cache_data
def load_geojson(url2):
    gdf = gpd.read_file(url2)
    return gdf

url2 = 'https://raw.githubusercontent.com/renegibran/maceio/main/Maceio_afundando/maceio.geojson'
gdf = load_geojson(url2)

url ='https://raw.githubusercontent.com/renegibran/zelia/main/dataframe_zelia_total.csv'
df = load_data(url)

@st.cache_data
def create_marker_layer(df, name):
    marker_layer = folium.FeatureGroup(name=name)
    for index, row in df.iterrows():
        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            tooltip=row['Nome']
        ).add_to(marker_layer)
    return marker_layer

# Adicione polígonos para diferentes bairros
mapa = folium.Map(location=(-9.60, -35.72), zoom_start=12.7, tiles='cartodbpositron')

bairros = {
    'Bebedouro': 'blue',
    'Chã de Bebedouro': 'red',
    'Mutange': 'green',
    'Bom Parto': 'orange',
    'Pinheiro': 'purple',
    'Farol': 'pink',
    'Fernão Velho': 'brown'
}

for bairro, cor in bairros.items():
    # Adiciona polígonos
    gdf_bairro = gdf[gdf['Bairro'] == bairro].copy()
    folium.GeoJson(gdf_bairro,
                   name=bairro,
                   style_function=lambda x, cor=cor: {'fillColor': cor, 'color': cor, 'weight': 1}).add_to(mapa)

# Categorias de anos
years = ['1950', '1960', '1970', '1980 e 1990']

for year in years:
    df_year = df[df['Ano de construção'] == year].copy()
    marker_layer = create_marker_layer(df_year, f'Marcadores {year}')
    marker_layer.add_to(mapa)

# Adicione a camada de marcação ao mapa
folium.LayerControl().add_to(mapa)

st.title("Zélia Matos")
st.write("Mapa")

st_data = st_folium(mapa, width=700)

mapa
