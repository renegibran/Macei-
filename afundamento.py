import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import geopandas as gpd

st.set_page_config(layout="wide")

st.title("Afundamento")
st.write("O problema de afundamento da cidade de Maceió é uma questão de extrema relevância que afeta a capital do estado de Alagoas, localizada no nordeste do Brasil. Maceió, conhecida por suas belas praias e seu turismo, enfrenta um desafio significativo relacionado ao afundamento de terras em algumas áreas urbanas. Este fenômeno, muitas vezes referido como subsidência, é caracterizado pelo afundamento gradual do solo, resultando em problemas sérios de erosão costeira, inundações periódicas e ameaças às infraestruturas urbanas. O afundamento em Maceió é atribuído a uma combinação de fatores, incluindo a extração de água subterrânea, a ação das marés, o aumento do nível do mar e a expansão urbana desordenada. Essa problemática tem sérias implicações para a qualidade de vida dos moradores, a economia local e a preservação do meio ambiente. Portanto, é essencial abordar esse desafio de maneira abrangente, por meio de estudos científicos, planejamento urbano sustentável e políticas de gestão de recursos hídricos, a fim de mitigar os impactos do afundamento e proteger o futuro da cidade de Maceió.")

# Função para carregar os dados com caching
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

@st.cache_data
def load_image(url1):
    df1 = pd.read_excel(url1)
    return df1

@st.cache_data
def load_geojson(url2):
    gdf = gpd.read_file(url2)
    return gdf

url2 = 'https://raw.githubusercontent.com/renegibran/maceio/main/Maceio_afundando/maceio.geojson'
gdf = load_geojson(url2)

url1 = 'https://github.com/renegibran/maceio/blob/31bed3e588fb0d8842045e81447ce2c91371d779/IMG%20Macei%C3%B3%20afundado/links.xlsx?raw=true'
df1 = load_image(url1)

url = 'https://raw.githubusercontent.com/renegibran/maceio/main/Maceio_afundando/edifica%C3%A7%C3%B5esMaceioAfundadoFILTRADO.csv'
df = load_data(url)
df.rename(columns={'X': 'LONGITUDE', 'Y': 'LATITUDE'}, inplace=True)

# st.button("Rerun")

bairros = {
    'Bebedouro': 'blue',
    'Chã de Bebedouro': 'red',
    'Mutange': 'green',
    'Bom Parto': 'orange',
    'Pinheiro': 'purple',
    'Farol': 'pink',
    'Fernão Velho': 'brown'
}

#col1, col2 = st.columns(2)

mapa = folium.Map(location=(-9.60, -35.72), zoom_start=12.7, tiles='cartodbpositron')
#folium.LayerControl().add_to(mapa)

info_detalhadas = []

for bairro, cor in bairros.items():
    df_bairro = df[df['Bairro'] == bairro].copy()
    marker_layer = folium.FeatureGroup(name=bairro)
    for index, row in df_bairro.iterrows():
        popup_content = [row["Nome"], row['Descrição'], row['Endereço']]
        info_detalhadas.append(popup_content)
        # Adicione o número do índice à tooltip
        tooltip_text = f"{index} - {row['Nome']}"
        folium.Marker(
            location=[row['LATITUDE'], row['LONGITUDE']],
            popup=row['Nome'],
            tooltip=tooltip_text,
            icon=folium.Icon(color=cor)
        ).add_to(marker_layer)
    marker_layer.add_to(mapa)

    # Adiciona polígonos
    gdf_bairro = gdf[gdf['Bairro'] == bairro].copy()
    folium.GeoJson(gdf_bairro,
                   name=bairro,
                   style_function=lambda x, cor=cor: {'fillColor': cor, 'color': cor, 'weight': 1}).add_to(mapa)



# Coluna direita para o mapa
st.markdown("## Mapa:")
out = st_folium(mapa, width=1000, height=500, return_on_hover=True)

# Barra lateral para as informações
st.sidebar.markdown("## Informações:")
if out["last_object_clicked_popup"]:
    # Encontre o índice do marcador clicado
    index = int(out["last_object_clicked_tooltip"].split('-')[0].strip())

    st.sidebar.image(df1['Links'][index], caption='Imagem do Local')
    st.sidebar.write(info_detalhadas[index][0])
    st.sidebar.write(info_detalhadas[index][1])
    st.sidebar.write("Endereço:", info_detalhadas[index][2])

# pip install openpyxl
