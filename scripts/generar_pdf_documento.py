"""
Script para generar el documento PDF final a partir de los documentos Markdown.
Requiere Pandoc instalado: https://pandoc.org/installing.html
"""
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs" / "proyecto"
OUTPUT_DIR = BASE_DIR / "docs" / "proyecto"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def check_pandoc():
    """Verifica si Pandoc está instalado."""
    try:
        result = subprocess.run(
            ["pandoc", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            version = result.stdout.split("\n")[0]
            print(f"[OK] Pandoc encontrado: {version}")
            return True
    except FileNotFoundError:
        print("[ERROR] Pandoc no está instalado")
        print("\nPara instalar Pandoc:")
        print("1. Windows: Descargar de https://pandoc.org/installing.html")
        print("2. O usar: winget install --id JohnMacFarlane.Pandoc")
        return False
    return False

def generate_pdf():
    """Genera el PDF combinando todos los documentos Markdown."""
    print("="*80)
    print("GENERANDO DOCUMENTO PDF FINAL")
    print("="*80)
    
    if not check_pandoc():
        print("\n[ALTERNATIVA] Generando documento combinado en Markdown...")
        generate_combined_markdown()
        return False
    
    # Archivos en orden
    files = [
        "00_DOCUMENTO_PRINCIPAL.md",
        "01_DESCRIPCION_SUBSISTEMA.md",
        "02_ESTRATEGIA_TDD.md",
        "03_REPORTE_COBERTURA.md",
        "04_RESULTADOS_APRENDIZAJES.md",
        "05_REFERENCIAS.md"
    ]
    
    # Verificar que todos los archivos existan
    missing_files = []
    for file in files:
        if not (DOCS_DIR / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"[ERROR] Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    # Generar PDF
    output_file = OUTPUT_DIR / f"PROYECTO_FINAL_RECOLECCION_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    print(f"\nGenerando PDF: {output_file}")
    
    try:
        # Construir comando Pandoc
        cmd = [
            "pandoc",
            "--from=markdown",
            "--to=pdf",
            "--output", str(output_file),
            "--pdf-engine=xelatex",  # o pdflatex
            "--toc",  # Tabla de contenidos
            "--toc-depth=3",
            "--number-sections",  # Numerar secciones
            "--highlight-style=tango",
            "--variable=geometry:margin=2.5cm",
            "--variable=fontsize:11pt",
            "--variable=documentclass:article",
        ]
        
        # Agregar archivos
        for file in files:
            cmd.append(str(DOCS_DIR / file))
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=BASE_DIR
        )
        
        if result.returncode == 0:
            print(f"[OK] PDF generado exitosamente: {output_file}")
            print(f"[OK] Tamaño: {output_file.stat().st_size / 1024:.1f} KB")
            return True
        else:
            print(f"[ERROR] Error al generar PDF:")
            print(result.stderr)
            print("\n[ALTERNATIVA] Intentando con pdflatex...")
            return generate_pdf_pdflatex(files, output_file)
            
    except Exception as e:
        print(f"[ERROR] Excepción: {e}")
        print("\n[ALTERNATIVA] Generando documento combinado en Markdown...")
        generate_combined_markdown()
        return False

def generate_pdf_pdflatex(files, output_file):
    """Intenta generar PDF con pdflatex."""
    try:
        cmd = [
            "pandoc",
            "--from=markdown",
            "--to=pdf",
            "--output", str(output_file),
            "--pdf-engine=pdflatex",
            "--toc",
            "--toc-depth=3",
            "--number-sections",
        ]
        
        for file in files:
            cmd.append(str(DOCS_DIR / file))
        
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE_DIR)
        
        if result.returncode == 0:
            print(f"[OK] PDF generado con pdflatex: {output_file}")
            return True
        else:
            print(f"[ERROR] Error con pdflatex: {result.stderr}")
            return False
    except Exception as e:
        print(f"[ERROR] Excepción: {e}")
        return False

def generate_combined_markdown():
    """Genera un documento Markdown combinado como alternativa."""
    print("\nGenerando documento Markdown combinado...")
    
    files = [
        "00_DOCUMENTO_PRINCIPAL.md",
        "01_DESCRIPCION_SUBSISTEMA.md",
        "02_ESTRATEGIA_TDD.md",
        "03_REPORTE_COBERTURA.md",
        "04_RESULTADOS_APRENDIZAJES.md",
        "05_REFERENCIAS.md"
    ]
    
    output_file = OUTPUT_DIR / f"DOCUMENTO_COMPLETO_{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(output_file, "w", encoding="utf-8") as out:
        for file in files:
            file_path = DOCS_DIR / file
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    out.write(f.read())
                    out.write("\n\n\\newpage\n\n")
    
    print(f"[OK] Documento combinado generado: {output_file}")
    print("\nPara convertir a PDF:")
    print("1. Usar herramienta online: https://www.markdowntopdf.com/")
    print("2. Usar Pandoc (si está instalado): pandoc documento.md -o documento.pdf")
    print("3. Abrir en Word/Google Docs y exportar a PDF")

if __name__ == "__main__":
    success = generate_pdf()
    sys.exit(0 if success else 1)



