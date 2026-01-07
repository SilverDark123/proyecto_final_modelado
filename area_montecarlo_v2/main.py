"""
============================================================================
CALCULADOR DE ÁREA CON MÉTODO DE MONTE CARLO
Países de Sudamérica - Programa Principal
============================================================================
Autor: Proyecto de Modelado y Simulación
Fecha: Enero 2026
============================================================================
"""

from config import PAISES_SUDAMERICA
from data_loader import cargar_datos
from geometry_processor import proyectar_y_calcular_bbox
from montecarlo_simulator import simulacion_montecarlo
from results_display import mostrar_resultados, visualizar_resultados, visualizar_previa
from ui_menu import mostrar_menu, solicitar_cantidad_puntos


def main():
    """Función principal del programa."""
    # Cargar datos al inicio
    mundo = cargar_datos()
    if mundo is None:
        return
    
    while True:
        mostrar_menu()

        # Paso 1        
        try:
            opcion = input("\n→ Ingrese el número del país (0 para salir): ").strip()
            
            if opcion == "0":
                print("\n¡Hasta luego!")
                break
            
            opcion = int(opcion)
            
            if opcion < 1 or opcion > len(PAISES_SUDAMERICA):
                print("\n Opción inválida. Por favor seleccione un número del menú.")
                continue
            
            nombre_pais = PAISES_SUDAMERICA[opcion - 1]
            
        except ValueError:
            print("\n Por favor ingrese un número válido.")
            continue
        
        # --- Filtrar el país seleccionado ---
        pais_gdf = mundo[mundo['NAME'] == nombre_pais]
        
        if pais_gdf.empty:
            print(f"\n No se encontró el país '{nombre_pais}' en la base de datos.")
            continue
        
        print(f"\n País seleccionado: {nombre_pais}")
        
        # --- Visualización Previa (Lat/Long) ---
        visualizar_previa(pais_gdf, nombre_pais)
        
        # Paso 2, 3 y 4
        # --- Proyectar y calcular bounding box ---
        pais_proyectado, bbox = proyectar_y_calcular_bbox(pais_gdf, nombre_pais)
        
        # Paso 5
        # --- Solicitar cantidad de puntos ---
        n_puntos = solicitar_cantidad_puntos()
        
        # Paso 6
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
            print("\n ¡Hasta luego!")
            break


if __name__ == "__main__":
    main()
