"""
============================================================================
CALCULADOR DE ÁREA CON MÉTODO DE MONTE CARLO
Países de Sudamérica
============================================================================
Este script permite calcular el área de cualquier país sudamericano
utilizando el método de Monte Carlo con proyección Albers para América Latina.

Autor: Proyecto de Modelado y Simulación
Fecha: Enero 2026
============================================================================
"""

import geopandas as gpd
import numpy as np
from shapely.geometry import Point
import matplotlib.pyplot as plt
import time

# --- CONFIGURACIÓN ---
# Lista de países de Sudamérica (nombres en inglés como aparecen en Natural Earth)
PAISES_SUDAMERICA = [
    "Argentina",
    "Bolivia",
    "Brazil",
    "Chile",
    "Colombia",
    "Ecuador",
    "Guyana",
    "Paraguay",
    "Peru",
    "Suriname",
    "Uruguay",
    "Venezuela"
]

# Áreas reales de referencia en km² (Fuente: Banco Mundial / Wikipedia)
AREAS_REALES_KM2 = {
    "Argentina": 2780400,
    "Bolivia": 1098581,
    "Brazil": 8515770,
    "Chile": 756102,
    "Colombia": 1138910,
    "Ecuador": 283561,
    "Guyana": 214969,
    "Paraguay": 406752,
    "Peru": 1285216,
    "Suriname": 165940,
    "Uruguay": 176215,
    "Venezuela": 916445
}


def mostrar_menu():
    """Muestra el menú de selección de países."""
    print("\n" + "=" * 60)
    print("   CALCULADOR DE ÁREA - MÉTODO DE MONTE CARLO")
    print("   Países de Sudamérica")
    print("=" * 60)
    print("\nSeleccione el país para calcular su área:\n")
    
    for i, pais in enumerate(PAISES_SUDAMERICA, 1):
        area_real = AREAS_REALES_KM2.get(pais, 0)
        print(f"  {i:2d}. {pais:20s} (Área real: {area_real:>12,} km²)")
    
    print(f"\n  0. Salir")
    print("-" * 60)


def cargar_datos():
    """Descarga y carga los datos de países desde Natural Earth."""
    print("\n📡 Descargando datos de Natural Earth...")
    print("   (Esto puede tardar unos segundos la primera vez)")
    
    url_mapa = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
    
    try:
        mundo = gpd.read_file(url_mapa)
        print("   ✓ Datos descargados correctamente!")
        return mundo
    except Exception as e:
        print(f"   ✗ Error al descargar: {e}")
        return None


def proyectar_y_calcular_bbox(pais_gdf, nombre_pais):
    """
    Proyecta el país a sistema métrico (Albers) y calcula el bounding box.
    
    Returns:
        pais_proyectado: GeoDataFrame proyectado
        bbox: tupla (min_x, min_y, max_x, max_y)
    """
    print(f"\n📐 Procesando geometría de {nombre_pais}...")
    
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
    print("\n🔄 Aplicando proyección Albers Equal Area (ESRI:102033)...")
    
    try:
        pais_proyectado = pais_gdf.to_crs("ESRI:102033")
        proyeccion_usada = "ESRI:102033 (South America Albers Equal Area)"
        print(f"   ✓ Proyección aplicada: {proyeccion_usada}")
    except:
        print("   ⚠ Usando proyección UTM 18S alternativa...")
        pais_proyectado = pais_gdf.to_crs(epsg=32718)
        proyeccion_usada = "EPSG:32718 (UTM Zone 18S)"
    
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


def simulacion_montecarlo(pais_proyectado, bbox, n_puntos):
    """
    Ejecuta la simulación de Monte Carlo para estimar el área.
    
    Args:
        pais_proyectado: GeoDataFrame con el polígono proyectado
        bbox: tupla (min_x, min_y, max_x, max_y)
        n_puntos: cantidad de puntos pseudoaleatorios a generar
    
    Returns:
        dict con resultados de la simulación
    """
    min_x, min_y, max_x, max_y = bbox
    
    # Calcular área del bounding box
    ancho = max_x - min_x
    alto = max_y - min_y
    area_bbox = ancho * alto
    
    print(f"\nIniciando simulación de Monte Carlo...")
    print(f"   Generando {n_puntos:,} puntos pseudoaleatorios...")
    
    start_time = time.time()
    
    # --- Generar puntos aleatorios con distribución uniforme ---
    x_rand = np.random.uniform(min_x, max_x, n_puntos)
    y_rand = np.random.uniform(min_y, max_y, n_puntos)
    
    print(f"   ✓ Puntos generados en el bounding box")
    
    # --- Obtener el polígono del país ---
    poligono_pais = pais_proyectado.geometry.iloc[0]
    
    # --- Contar puntos dentro del polígono ---
    print(f"   🔍 Verificando puntos dentro del polígono...")
    
    puntos_dentro = 0
    puntos_dentro_x = []  # Para visualización
    puntos_dentro_y = []
    puntos_fuera_x = []
    puntos_fuera_y = []
    
    # Límite de puntos a guardar para visualización
    max_puntos_viz = 5000
    
    for i, (x, y) in enumerate(zip(x_rand, y_rand)):
        # Mostrar progreso cada 10%
        if n_puntos >= 10000 and i % (n_puntos // 10) == 0:
            progreso = (i / n_puntos) * 100
            print(f"      Progreso: {progreso:.0f}%", end='\r')
        
        punto = Point(x, y)
        if poligono_pais.contains(punto):
            puntos_dentro += 1
            if len(puntos_dentro_x) < max_puntos_viz:
                puntos_dentro_x.append(x)
                puntos_dentro_y.append(y)
        else:
            if len(puntos_fuera_x) < max_puntos_viz // 2:
                puntos_fuera_x.append(x)
                puntos_fuera_y.append(y)
    
    end_time = time.time()
    tiempo_simulacion = end_time - start_time
    
    print(f"   ✓ Simulación completada en {tiempo_simulacion:.2f} segundos")
    
    # --- Calcular área estimada con Monte Carlo ---
    # Fórmula: Área_Estimada = Área_BBox × (puntos_dentro / total_puntos)
    area_estimada_m2 = area_bbox * (puntos_dentro / n_puntos)
    area_estimada_km2 = area_estimada_m2 / 1_000_000
    
    return {
        'n_puntos': n_puntos,
        'puntos_dentro': puntos_dentro,
        'puntos_fuera': n_puntos - puntos_dentro,
        'area_bbox_m2': area_bbox,
        'area_estimada_m2': area_estimada_m2,
        'area_estimada_km2': area_estimada_km2,
        'tiempo_simulacion': tiempo_simulacion,
        'puntos_dentro_x': puntos_dentro_x,
        'puntos_dentro_y': puntos_dentro_y,
        'puntos_fuera_x': puntos_fuera_x,
        'puntos_fuera_y': puntos_fuera_y,
        'bbox': bbox
    }


def mostrar_resultados(nombre_pais, resultados):
    """Muestra los resultados de la simulación."""
    area_real = AREAS_REALES_KM2.get(nombre_pais, 0)
    area_estimada = resultados['area_estimada_km2']
    
    # Calcular error
    if area_real > 0:
        error_absoluto = abs(area_estimada - area_real)
        error_relativo = (error_absoluto / area_real) * 100
    else:
        error_absoluto = 0
        error_relativo = 0
    
    print("\n" + "=" * 60)
    print("   RESULTADOS DE LA SIMULACIÓN DE MONTE CARLO")
    print("=" * 60)
    
    print(f"\n   País analizado: {nombre_pais}")
    print(f"\n   ESTADÍSTICAS DE LA SIMULACIÓN:")
    print(f"   ├─ Total de puntos generados:     {resultados['n_puntos']:>15,}")
    print(f"   ├─ Puntos dentro del país:        {resultados['puntos_dentro']:>15,}")
    print(f"   ├─ Puntos fuera del país:         {resultados['puntos_fuera']:>15,}")
    print(f"   └─ Tiempo de simulación:          {resultados['tiempo_simulacion']:>15.2f} seg")
    
    print(f"\n   CÁLCULO DEL ÁREA:")
    print(f"   ├─ Área del Bounding Box:         {resultados['area_bbox_m2']/1_000_000:>15,.2f} km²")
    print(f"   ├─ Proporción (dentro/total):     {resultados['puntos_dentro']/resultados['n_puntos']:>15.6f}")
    print(f"   └─ ÁREA ESTIMADA (Monte Carlo):   {area_estimada:>15,.2f} km²")
    
    print(f"\n   VALIDACIÓN:")
    print(f"   ├─ Área Real (dato oficial):      {area_real:>15,} km²")
    print(f"   ├─ Área Calculada (simulada):     {area_estimada:>15,.2f} km²")
    print(f"   ├─ Diferencia (Error Absoluto):   {error_absoluto:>15,.2f} km²")
    print(f"   └─ Error Relativo:                {error_relativo:>15.4f} %")
    
    print("\n" + "=" * 60)
    
    # Evaluar precisión
    if error_relativo < 1:
        print("   (Error < 1%)")
    elif error_relativo < 5:
        print("   (Error < 5%)")
    elif error_relativo < 10:
        print("   (Error < 10%)")
    else:
        print(f"Probablemente el ShapeFile de {nombre_pais} no este considerando islas o archipielagos")
    
    print("=" * 60)


def visualizar_resultados(pais_proyectado, nombre_pais, resultados):
    """Genera visualización gráfica de los resultados."""
    print("\nGenerando visualización...")
    
    bbox = resultados['bbox']
    min_x, min_y, max_x, max_y = bbox
    ancho = max_x - min_x
    alto = max_y - min_y
    
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Dibujar el país
    pais_proyectado.plot(ax=ax, color='lightblue', edgecolor='darkblue', 
                          linewidth=1.5, alpha=0.7, label='Área del país')
    
    # Dibujar bounding box
    rect = plt.Rectangle((min_x, min_y), ancho, alto,
                         linewidth=2, edgecolor='red', facecolor='none',
                         linestyle='--', label='Bounding Box')
    ax.add_patch(rect)
    
    # Dibujar puntos dentro (verde) - muestra
    if resultados['puntos_dentro_x']:
        ax.scatter(resultados['puntos_dentro_x'], resultados['puntos_dentro_y'],
                  color='green', s=2, alpha=0.5, label='Puntos dentro (muestra)')
    
    # Dibujar puntos fuera (rojo) - muestra
    if resultados['puntos_fuera_x']:
        ax.scatter(resultados['puntos_fuera_x'], resultados['puntos_fuera_y'],
                  color='red', s=1, alpha=0.3, label='Puntos fuera (muestra)')
    
    # Configuración del gráfico
    area_real = AREAS_REALES_KM2.get(nombre_pais, 0)
    area_estimada = resultados['area_estimada_km2']
    error = abs(area_estimada - area_real) / area_real * 100 if area_real > 0 else 0
    
    ax.set_title(f"Simulación de Monte Carlo - {nombre_pais}\n"
                f"N = {resultados['n_puntos']:,} puntos | "
                f"Área estimada: {area_estimada:,.2f} km² | "
                f"Error: {error:.2f}%",
                fontsize=14, fontweight='bold')
    
    ax.set_xlabel("Coordenada X (metros)", fontsize=11)
    ax.set_ylabel("Coordenada Y (metros)", fontsize=11)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    # Formatear ejes con separadores de miles
    ax.ticklabel_format(style='plain', axis='both')
    ax.get_xaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.tight_layout()
    plt.show()
    
    print("   ✓ Visualización generada")


def visualizar_previa(pais_gdf, nombre_pais):
    """Muestra una visualización rápida del país en coordenadas geográficas (Lat/Long)."""
    print(f"\n🗺️  Generando vista previa de {nombre_pais} (Lat/Long)...")
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Dibujar el país usando coordenadas geográficas originales
    pais_gdf.plot(ax=ax, color='#e6e6e6', edgecolor='#333333', linewidth=1)
    
    # Configurar títulos y ejes
    ax.set_title(f"Vista Geográfica: {nombre_pais}\n(WGS84 - Grados)", fontsize=14, fontweight='bold')
    ax.set_xlabel("Longitud", fontsize=10)
    ax.set_ylabel("Latitud", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Ajustar para que no se deforme visualmente
    # (Aunque lat/long no son euclidianos, esto ayuda a verlo 'normal')
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.show() # Bloqueante hasta que se cierra la ventana
    print("   ✓ Vista previa cerrada. Continuando...")


def main():
    """Función principal del programa."""
    # Cargar datos al inicio
    mundo = cargar_datos()
    if mundo is None:
        return
    
    while True:
        mostrar_menu()
        
        try:
            opcion = input("\n→ Ingrese el número del país (0 para salir): ").strip()
            
            if opcion == "0":
                print("\n¡Hasta luego!")
                break
            
            opcion = int(opcion)
            
            if opcion < 1 or opcion > len(PAISES_SUDAMERICA):
                print("\n⚠ Opción inválida. Por favor seleccione un número del menú.")
                continue
            
            nombre_pais = PAISES_SUDAMERICA[opcion - 1]
            
        except ValueError:
            print("\n⚠ Por favor ingrese un número válido.")
            continue
        
        # --- Filtrar el país seleccionado ---
        pais_gdf = mundo[mundo['NAME'] == nombre_pais]
        
        if pais_gdf.empty:
            print(f"\n⚠ No se encontró el país '{nombre_pais}' en la base de datos.")
            continue
        
        print(f"\n✓ País seleccionado: {nombre_pais}")
        
        # --- Visualización Previa (Lat/Long) ---
        visualizar_previa(pais_gdf, nombre_pais)
        
        # --- Proyectar y calcular bounding box ---
        pais_proyectado, bbox = proyectar_y_calcular_bbox(pais_gdf, nombre_pais)
        
        # --- Solicitar cantidad de puntos ---
        print("\n" + "-" * 60)
        print("   CONFIGURACIÓN DE LA SIMULACIÓN")
        print("-" * 60)
        print("\n   Recomendaciones de cantidad de puntos:")
        print("   • 10,000     → Prueba rápida (segundos)")
        print("   • 100,000    → Buena precisión (< 1 minuto)")
        print("   • 1,000,000  → Alta precisión (varios minutos)")
        
        while True:
            try:
                n_puntos = input("\n→ Ingrese la cantidad de puntos a generar: ").strip()
                n_puntos = n_puntos.replace(",", "").replace(".", "")
                n_puntos = int(n_puntos)
                
                if n_puntos < 100:
                    print("   ⚠ Se recomienda al menos 100 puntos.")
                    continue
                if n_puntos > 10_000_000:
                    print("   ⚠ Máximo recomendado: 10,000,000 puntos.")
                    continue
                break
            except ValueError:
                print("   ⚠ Por favor ingrese un número válido.")
        
        # --- Ejecutar simulación ---
        resultados = simulacion_montecarlo(pais_proyectado, bbox, n_puntos)
        
        # --- Mostrar resultados ---
        mostrar_resultados(nombre_pais, resultados)
        
        # --- Visualizar ---
        visualizar = input("\n→ ¿Desea ver la visualización gráfica? (s/n): ").strip().lower()
        if visualizar in ['s', 'si', 'sí', 'y', 'yes']:
            visualizar_resultados(pais_proyectado, nombre_pais, resultados)
        
        # --- Continuar o salir ---
        continuar = input("\n→ ¿Desea calcular el área de otro país? (s/n): ").strip().lower()
        if continuar not in ['s', 'si', 'sí', 'y', 'yes']:
            print("\n👋 ¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
