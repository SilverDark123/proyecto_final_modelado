"""
============================================================================
INTERFAZ DE USUARIO
Funciones para menú y entrada de datos
============================================================================
"""

from config import PAISES_SUDAMERICA, AREAS_REALES_KM2


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


def solicitar_cantidad_puntos():
    """Solicita al usuario la cantidad de puntos para la simulación."""
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
                print("   Se recomienda al menos 100 puntos.")
                continue
            if n_puntos > 10_000_000:
                print("   Máximo recomendado: 10,000,000 puntos.")
                continue
            return n_puntos
        except ValueError:
            print("   Por favor ingrese un número válido.")
