"""
============================================================================
PROCESAMIENTO DE GEOMETRÍA
Funciones para proyectar y calcular bounding box
============================================================================
"""

from config import PROYECCION_PRINCIPAL, PROYECCION_ALTERNATIVA


def proyectar_y_calcular_bbox(pais_gdf, nombre_pais):
    """
    Proyecta el país a sistema métrico (Albers) y calcula el bounding box.
    
    Returns:
        pais_proyectado: GeoDataFrame proyectado
        bbox: tupla (min_x, min_y, max_x, max_y)
    """
    print(f"\n Procesando geometría de {nombre_pais}...")
    
    # --- Mostrar coordenadas originales (lat/long) ---
    bounds_geo = pais_gdf.total_bounds
    min_lon, min_lat, max_lon, max_lat = bounds_geo
    
    print("\n   COORDENADAS GEOGRÁFICAS (WGS84 - Grados):")
    print(f"   ┌─────────────────────────────────────────────┐")
    print(f"   │ Latitud:   Min = {min_lat:>10.4f}°              │")
    print(f"   │            Max = {max_lat:>10.4f}°              │")
    print(f"   │ Longitud:  Min = {min_lon:>10.4f}°              │")
    print(f"   │            Max = {max_lon:>10.4f}°              │")
    print(f"   └─────────────────────────────────────────────┘")
    
    # --- Proyección a Albers Equal Area para América Latina ---
    print(f"\n Aplicando proyección Albers Equal Area ({PROYECCION_PRINCIPAL})...")
    
    try:
        pais_proyectado = pais_gdf.to_crs(PROYECCION_PRINCIPAL)
        proyeccion_usada = f"{PROYECCION_PRINCIPAL} (South America Albers Equal Area)"
        print(f"   Proyección aplicada: {proyeccion_usada}")
    except:
        print(f"   Usando proyección UTM alternativa ({PROYECCION_ALTERNATIVA})...")
        pais_proyectado = pais_gdf.to_crs(PROYECCION_ALTERNATIVA)
        proyeccion_usada = f"{PROYECCION_ALTERNATIVA} (UTM Zone 18S)"
    
    # --- Calcular bounding box en metros ---
    min_x, min_y, max_x, max_y = pais_proyectado.total_bounds
    
    ancho = max_x - min_x
    alto = max_y - min_y
    area_bbox = ancho * alto
    
    print("\n   COORDENADAS PROYECTADAS (Metros):")
    print(f"   ┌─────────────────────────────────────────────────────────┐")
    print(f"   │ Eje X:  Min = {min_x:>15,.2f} m                     │")
    print(f"   │         Max = {max_x:>15,.2f} m                     │")
    print(f"   │ Eje Y:  Min = {min_y:>15,.2f} m                     │")
    print(f"   │         Max = {max_y:>15,.2f} m                     │")
    print(f"   └─────────────────────────────────────────────────────────┘")
    
    print("\n   BOUNDING BOX (Caja Contenedora):")
    print(f"   ┌─────────────────────────────────────────────────────────┐")
    print(f"   │ Ancho:            {ancho:>20,.2f} m              │")
    print(f"   │ Alto:             {alto:>20,.2f} m              │")
    print(f"   │ Área del BBox:    {area_bbox:>20,.2f} m²             │")
    print(f"   │                   {area_bbox/1_000_000:>20,.2f} km²            │")
    print(f"   └─────────────────────────────────────────────────────────┘")
    
    return pais_proyectado, (min_x, min_y, max_x, max_y)
