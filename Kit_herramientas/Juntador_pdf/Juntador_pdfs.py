import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    PdfReader, PdfWriter = None, None

if os.name == "nt":
    os.system("")

CYAN = "\033[96m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
ROJO = "\033[91m"
MAGENTA = "\033[95m"
AZUL = "\033[94m"
BLANCO = "\033[97m"
NEGRITA = "\033[1m"
RESET = "\033[0m"


def abrir_archivo_o_carpeta(ruta: Path):
    try:
        if os.name == "nt":
            os.startfile(str(ruta))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(ruta)], check=False)
        else:
            subprocess.run(["xdg-open", str(ruta)], check=False)
    except Exception:
        pass


def obtener_pdfs(directorio: Path):
    if not directorio.is_dir():
        return []
    return sorted([f for f in directorio.iterdir() if f.is_file() and f.suffix.lower() == ".pdf"])


def fusionar_pdfs(directorio: Path, nombre_salida: str = ""):
    if PdfWriter is None or PdfReader is None:
        print(f"\n{ROJO}❌ Error: La librería 'pypdf' no está instalada. Ejecute: pip install pypdf{RESET}")
        return None

    archivos = obtener_pdfs(directorio)
    if not archivos:
        print(f"\n{AMARILLO}[!] No se encontraron archivos PDF en: {directorio}{RESET}")
        return None

    if not nombre_salida:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_salida = f"pdf_unificado_{timestamp}.pdf"
    elif not nombre_salida.lower().endswith(".pdf"):
        nombre_salida += ".pdf"

    ruta_salida = directorio / nombre_salida

    print(f"\n{CYAN}{NEGRITA}Iniciando fusión de {len(archivos)} documentos PDF:{RESET}")
    print(f"{AZUL}{'─' * 70}{RESET}")

    writer = PdfWriter()
    total_paginas = 0

    for idx, arc in enumerate(archivos, start=1):
        try:
            reader = PdfReader(str(arc))
            num_pags = len(reader.pages)
            for page in reader.pages:
                writer.add_page(page)
            total_paginas += num_pags
            print(f"  {VERDE}[{idx}/{len(archivos)}]{RESET} {BLANCO}{arc.name}{RESET} ({CYAN}{num_pags} pág(s){RESET})")
        except Exception as e:
            print(f"  {ROJO}[!] Error al leer '{arc.name}': {e}{RESET}")

    try:
        with open(ruta_salida, "wb") as f_out:
            writer.write(f_out)

        tamano_mb = round(ruta_salida.stat().st_size / (1024 * 1024), 2)
        print(f"{AZUL}{'─' * 70}{RESET}")
        print(f"{VERDE}{NEGRITA}✓ [ÉXITO] Documentos fusionados correctamente:{RESET}")
        print(f"  {CYAN}📄 Archivo generado :{RESET} {BLANCO}{ruta_salida.name}{RESET}")
        print(f"  {CYAN}📁 Ruta completa    :{RESET} {ruta_salida}")
        print(f"  {AMARILLO}📊 Total de páginas :{RESET} {total_paginas} páginas")
        print(f"  {AMARILLO}📦 Tamaño final     :{RESET} {tamano_mb} MB")

        abrir = input(f"\n{BLANCO}¿Desea abrir el PDF unificado ahora mismo? (S/n): {RESET}").strip().lower()
        if abrir not in ("n", "no"):
            abrir_archivo_o_carpeta(ruta_salida)

        return ruta_salida
    except Exception as e:
        print(f"\n{ROJO}❌ Error al guardar el archivo unificado: {e}{RESET}")
        return None


def main():
    carpeta_actual = Path(__file__).resolve().parent

    while True:
        pdfs_encontrados = obtener_pdfs(carpeta_actual)

        print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{AZUL}{NEGRITA}║                   📚 JUNTADOR Y FUSIONADOR PROFESIONAL DE PDFS                     ║{RESET}")
        print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"  {CYAN}📁 Carpeta activa:{RESET} {carpeta_actual}")
        print(f"  {CYAN}📄 PDFs detectados:{RESET} {VERDE}{len(pdfs_encontrados)} archivos{RESET}")
        print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"║  {VERDE}[1]{RESET} {BLANCO}⚡ Fusionar todos los PDFs de esta carpeta en uno solo{RESET}                 ║")
        print(f"║  {CYAN}[2]{RESET} {BLANCO}📋 Listar nombres y detalles de los PDFs detectados{RESET}                    ║")
        print(f"║  {AMARILLO}[3]{RESET} {BLANCO}📂 Cambiar carpeta de trabajo{RESET}                                          ║")
        print(f"║  {ROJO}[0]{RESET} {BLANCO}🚪 Salir del programa{RESET}                                                 ║")
        print(f"{AZUL}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

        opcion = input(f"{VERDE}{NEGRITA}Seleccione una opción (0-3): {RESET}").strip()

        if opcion == "1":
            if not pdfs_encontrados:
                print(f"\n{AMARILLO}[!] No hay archivos PDF en la carpeta actual para unir.{RESET}")
                input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")
                continue

            nombre = input(f"\n{CYAN}Nombre para el archivo fusionado (Enter para automático): {RESET}").strip()
            fusionar_pdfs(carpeta_actual, nombre)
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "2":
            if not pdfs_encontrados:
                print(f"\n{AMARILLO}[!] No hay archivos PDF en la carpeta actual.{RESET}")
            else:
                print(f"\n{CYAN}PDFs encontrados en {carpeta_actual}:{RESET}")
                for idx, p in enumerate(pdfs_encontrados, start=1):
                    tam_kb = round(p.stat().st_size / 1024, 1)
                    print(f"  {VERDE}[{idx}]{RESET} {BLANCO}{p.name}{RESET} ({CYAN}{tam_kb} KB{RESET})")
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "3":
            nueva = input(f"\n{CYAN}Ingrese la nueva ruta absoluta de la carpeta: {RESET}").strip().strip('"').strip("'")
            if nueva:
                p_nueva = Path(nueva).expanduser().resolve()
                if p_nueva.is_dir():
                    carpeta_actual = p_nueva
                    print(f"\n{VERDE}✓ Carpeta cambiada a: {carpeta_actual}{RESET}")
                else:
                    print(f"\n{ROJO}❌ La ruta indicada no existe o no es un directorio válido.{RESET}")
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion in ("0", "q", "exit", "salir"):
            print(f"\n{CYAN}Saliendo del fusionador de PDFs. ¡Hasta luego!{RESET}\n")
            break
        else:
            print(f"\n{ROJO}[!] Opción no válida. Intente de nuevo.{RESET}")


if __name__ == "__main__":
    main()
