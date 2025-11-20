"""
Script simple para iniciar el servidor y mostrar como ver el funcionamiento.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path


def main():
    print("\n" + "="*70)
    print("  INICIANDO SUBSISTEMA DE RECOLECCION")
    print("="*70)
    
    # Verificar que estamos en el directorio correcto
    project_root = Path(__file__).parent.parent
    print(f"\nDirectorio: {project_root}")
    
    print("\n" + "="*70)
    print("  OPCIONES DE EJECUCION")
    print("="*70)
    
    print("\n1. INICIAR SERVIDOR (en esta terminal)")
    print("   El servidor comenzara a correr.")
    print("   No cierres esta ventana mientras el servidor este activo.")
    
    print("\n2. VER FUNCIONAMIENTO")
    print("   En OTRA terminal, puedes ejecutar:")
    print("     python scripts/ver_funcionamiento.py")
    print("   O simplemente abrir en tu navegador:")
    print("     http://localhost:8000/docs")
    
    print("\n" + "="*70)
    print("  INICIANDO SERVIDOR...")
    print("="*70)
    print("\nEl servidor se iniciara en: http://localhost:8000")
    print("Presiona CTRL+C para detener el servidor")
    print("\nEsperando 3 segundos antes de iniciar...")
    print("(Si quieres cancelar, presiona CTRL+C ahora)\n")
    
    time.sleep(3)
    
    # Intentar abrir la documentacion automaticamente despues de iniciar
    print("\nINICIANDO SERVIDOR...")
    print("="*70)
    print("Cuando veas 'Application startup complete', el servidor esta listo!")
    print("\nLa documentacion se abrira automaticamente en tu navegador.")
    print("Si no se abre, ve manualmente a: http://localhost:8000/docs")
    print("\nPresiona CTRL+C para detener el servidor")
    print("="*70 + "\n")
    
    # Esperar un poco y abrir el navegador
    def abrir_docs():
        time.sleep(5)  # Esperar a que el servidor inicie
        try:
            webbrowser.open("http://localhost:8000/docs")
            print("\n[OK] Documentacion abierta en el navegador!")
        except:
            print("\n[INFO] Abre manualmente: http://localhost:8000/docs")
    
    import threading
    thread = threading.Thread(target=abrir_docs, daemon=True)
    thread.start()
    
    # Iniciar el servidor
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n\nServidor detenido.")
    except Exception as e:
        print(f"\nError iniciando servidor: {e}")


if __name__ == "__main__":
    main()



