import streamlit as st
from streamlit_folium import st_folium
import folium
import pandas as pd
import geopandas as gpd
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Afundamento de Bairros em Maceió",
        page_icon="👋",layout = 'wide'
    )

    st.write("# Afundamento de Maceió 👋")
    st.sidebar.success("Select a demo above.")

    


if __name__ == "__main__":
    run()