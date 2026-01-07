"""
============================================================================
VISUALIZACIÓN DE RESULTADOS
Funciones para mostrar y visualizar resultados
============================================================================
"""

import matplotlib.pyplot as plt
from config import AREAS_REALES_KM2


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
    
    print("   Visualización generada")


def visualizar_previa(pais_gdf, nombre_pais):
    """Muestra una visualización rápida del país en coordenadas geográficas (Lat/Long)."""
    print(f"\n Generando vista previa de {nombre_pais} (Lat/Long)...")
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Dibujar el país usando coordenadas geográficas originales
    pais_gdf.plot(ax=ax, color='#e6e6e6', edgecolor='#333333', linewidth=1)
    
    # Configurar títulos y ejes
    ax.set_title(f"Vista Geográfica: {nombre_pais}\n(WGS84 - Grados)", fontsize=14, fontweight='bold')
    ax.set_xlabel("Longitud", fontsize=10)
    ax.set_ylabel("Latitud", fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    
    # Ajustar para que no se deforme visualmente
    ax.set_aspect('equal')
    
    plt.tight_layout()
    plt.show()
    print("   Vista previa cerrada. Continuando...")
