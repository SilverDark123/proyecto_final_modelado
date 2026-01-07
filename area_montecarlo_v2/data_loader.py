"""
============================================================================
CARGA DE DATOS GEOGRÁFICOS
Funciones para descargar y cargar datos de Natural Earth
============================================================================
"""

import geopandas as gpd
from config import URL_MAPA


def cargar_datos():
    """Descarga y carga los datos de países desde Natural Earth."""
    print("\n Descargando datos de Natural Earth...")
    print("   (Esto puede tardar unos segundos la primera vez)")
    
    try:
        mundo = gpd.read_file(URL_MAPA)
        print("   Datos descargados correctamente!")
        return mundo
    except Exception as e:
        print(f"   Error al descargar: {e}")
        return None
