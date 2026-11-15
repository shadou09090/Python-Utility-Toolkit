#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador interactivo de dependencias para el repositorio Programas_utiles.
Lee el archivo 'requirements.txt', detecta en tiempo real qué módulos ya están
instalados y cuáles faltan, permitiendo la instalación global, selectiva o únicamente
de los paquetes faltantes.
"""

import os
import re
import sys
import subprocess
import importlib.util
from pathlib import Path
from typing import Dict, List, Tuple

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

NOMBRE_ARCHIVO_REQ = "requirements.txt"

# Mapeo de nombre de paquete en PyPI a nombre de módulo importable en Python
PKG_A_MODULO = {
    "pillow": "PIL",
    "pymupdf": "fitz",
    "pypdf": "pypdf",
    "pycryptodome": "Crypto",
    "msoffcrypto-tool": "msoffcrypto",
    "cryptography": "cryptography",
    "pandas": "pandas",
    "openpyxl": "openpyxl",
    "tabulate": "tabulate",
    "psutil": "psutil",
    "altair": "altair",
    "streamlit": "streamlit",
    "rembg": "rembg",
    "yt-dlp": "yt_dlp",
    "imageio-ffmpeg": "imageio_ffmpeg",
    "keyboard": "keyboard",
    "qrcode": "qrcode",
    "gtts": "gtts",
}


class ProgramaDependencias:
    def __init__(self, nombre: str, archivo: str = "", dependencias: List[str] = None, solo_estandar: bool = False):
        self.nombre = nombre
        self.archivo = archivo
        self.dependencias = dependencias or []
        self.solo_estandar = solo_estandar

    def __repr__(self):
        return f"<Programa {self.nombre} (deps={len(self.dependencias)})>"

    def obtener_faltantes(self) -> List[str]:
        if self.solo_estandar:
            return []
        return [p for p in self.dependencias if not paquete_esta_instalado(p)]


def paquete_esta_instalado(pkg_spec: str) -> bool:
    """Verifica si el módulo correspondiente al paquete está instalado en el entorno activo."""
    pkg_nombre = re.split(r"[><=~!;]", pkg_spec)[0].strip().lower()
    modulo = PKG_A_MODULO.get(pkg_nombre, pkg_nombre.replace("-", "_"))
    try:
        return importlib.util.find_spec(modulo) is not None
    except Exception:
        return False


def obtener_ruta_requirements() -> Path:
    """Busca el archivo requirements.txt en el directorio actual o junto al script."""
    script_dir = Path(__file__).resolve().parent
    candidatos = [
        script_dir / NOMBRE_ARCHIVO_REQ,
        Path.cwd() / NOMBRE_ARCHIVO_REQ,
        script_dir / "dependencias.txt",
        Path.cwd() / "dependencias.txt",
    ]
    for ruta in candidatos:
        if ruta.is_file():
            return ruta
    return script_dir / NOMBRE_ARCHIVO_REQ


def parsear_requirements(ruta_txt: Path) -> Tuple[List[ProgramaDependencias], List[str]]:
    """
    Parsea el archivo requirements.txt extrayendo las secciones por programa
    y la lista consolidada de todas las dependencias únicas.
    """
    if not ruta_txt.is_file():
        print(f"{ROJO}[!] Error: No se encontró el archivo de dependencias en:\n    {ruta_txt}{RESET}")
        sys.exit(1)

    programas: List[ProgramaDependencias] = []
    prog_actual: ProgramaDependencias = None
    todas_las_dependencias: List[str] = []
    vistas = set()

    with open(ruta_txt, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    patron_header = re.compile(r"^#\s*\[PROGRAMA:\s*(.+?)\]", re.IGNORECASE)
    patron_archivo = re.compile(r"^#\s*Archivo:\s*(.+)", re.IGNORECASE)
    patron_estandar = re.compile(r"^#\s*-\s*\[PROGRAMA:\s*(.+?)\]\s*->\s*(.+)", re.IGNORECASE)

    for linea in lineas:
        linea_strip = linea.strip()

        # Detección de programas sin dependencias externas (biblioteca estándar)
        match_std = patron_estandar.match(linea_strip)
        if match_std:
            if prog_actual is not None:
                programas.append(prog_actual)
                prog_actual = None
            nom = match_std.group(1).strip()
            arch = match_std.group(2).strip()
            programas.append(ProgramaDependencias(nombre=nom, archivo=arch, dependencias=[], solo_estandar=True))
            continue

        # Detección de cabecera de programa con dependencias
        match_head = patron_header.match(linea_strip)
        if match_head:
            if prog_actual is not None:
                programas.append(prog_actual)
            nombre_prog = match_head.group(1).strip()
            prog_actual = ProgramaDependencias(nombre=nombre_prog, dependencias=[])
            continue

        # Detección de ruta del archivo del programa
        if prog_actual is not None:
            match_arc = patron_archivo.match(linea_strip)
            if match_arc:
                prog_actual.archivo = match_arc.group(1).strip()
                continue

            # Si es un paquete pip (no comentario, no vacío)
            if linea_strip and not linea_strip.startswith("#"):
                paquete = linea_strip
                prog_actual.dependencias.append(paquete)
                nombre_base = re.split(r"[><=~!;]", paquete)[0].strip().lower()
                if nombre_base not in vistas:
                    vistas.add(nombre_base)
                    todas_las_dependencias.append(paquete)

    if prog_actual is not None:
        programas.append(prog_actual)

    return programas, todas_las_dependencias


def limpiar_consola():
    """Limpia la terminal según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


def instalar_paquetes(lista_paquetes: List[str], descripcion: str) -> bool:
    """Ejecuta pip install con el intérprete actual de Python."""
    if not lista_paquetes:
        print(f"\n{VERDE}[✓] Todas las dependencias requeridas ya están instaladas en el sistema.{RESET}")
        return True

    print(f"\n{AZUL}{'═' * 74}{RESET}")
    print(f"  {NEGRITA}{BLANCO}📦 INSTALANDO DEPENDENCIAS PARA:{RESET} {CYAN}{descripcion}{RESET}")
    print(f"{AZUL}{'─' * 74}{RESET}")
    print(f"  {CYAN}Intérprete Python:{RESET} {sys.executable}")
    print(f"  {CYAN}Paquetes a pedir :{RESET} {', '.join(lista_paquetes)}")
    print(f"{AZUL}{'═' * 74}{RESET}")
    print(f"\n{AMARILLO}[*] Ejecutando pip install en segundo plano...{RESET}\n")

    comando = [sys.executable, "-m", "pip", "install", *lista_paquetes]

    try:
        resultado = subprocess.run(comando, check=False)
        print(f"\n{AZUL}{'─' * 74}{RESET}")
        if resultado.returncode == 0:
            print(f"  {VERDE}{NEGRITA}✓ [ÉXITO] Instalación completada correctamente.{RESET}")
            return True
        else:
            print(f"  {ROJO}[!] pip finalizó con código de error: {resultado.returncode}{RESET}")
            return False
    except Exception as e:
        print(f"\n{ROJO}[!] Ocurrió un error al ejecutar pip: {e}{RESET}")
        return False


def mostrar_menu(programas: List[ProgramaDependencias], todas_las_deps: List[str]):
    """Imprime el menú de opciones en consola con detección en tiempo real de faltantes."""
    faltantes_globales = [p for p in todas_las_deps if not paquete_esta_instalado(p)]
    instalados_count = len(todas_las_deps) - len(faltantes_globales)

    print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{AZUL}{NEGRITA}║                   📦 GESTOR DE INSTALACIÓN DE DEPENDENCIAS (PIP)                   ║{RESET}")
    print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"  {CYAN}Intérprete activo:{RESET} {sys.executable}")
    print(f"  {CYAN}Estado de paquetes:{RESET} {VERDE}{instalados_count} instalados{RESET} | {AMARILLO if faltantes_globales else VERDE}{len(faltantes_globales)} faltantes{RESET} de {len(todas_las_deps)} totales")
    print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")

    if faltantes_globales:
        print(f"║  {VERDE}[ F]{RESET} {BLANCO}{NEGRITA}⚡ Instalar ÚNICAMENTE las {len(faltantes_globales)} dependencias faltantes{RESET}                    ║")
    else:
        print(f"║  {VERDE}[ F]{RESET} {VERDE}✓ Todas las dependencias del proyecto ya están 100% instaladas{RESET}         ║")

    print(f"║  {MAGENTA}[ 1]{RESET} {BLANCO}🌟 Reinstalar / actualizar TODAS las {len(todas_las_deps)} dependencias del proyecto{RESET}     ║")
    print(f"  {AZUL}{'─' * 80}{RESET}")

    for idx, prog in enumerate(programas, start=2):
        if prog.solo_estandar:
            badge_dep = f"{CYAN}[Biblioteca estándar]{RESET}"
            print(f"  {BLANCO}[{idx:2d}]{RESET} {BLANCO}{prog.nombre:<45}{RESET} {badge_dep}")
        else:
            faltantes_prog = prog.obtener_faltantes()
            if not faltantes_prog:
                badge_dep = f"{VERDE}[✓ Instalado]{RESET}"
            else:
                nombres_falt = [re.split(r"[><=~!;]", f)[0].strip() for f in faltantes_prog]
                badge_dep = f"{AMARILLO}[✗ Falta: {', '.join(nombres_falt)}]{RESET}"
            print(f"  {VERDE}[{idx:2d}]{RESET} {BLANCO}{prog.nombre:<45}{RESET} {badge_dep}")

    print(f"  {AZUL}{'─' * 80}{RESET}")
    print(f"║  {ROJO}[ 0]{RESET} {BLANCO}🚪 Salir del instalador{RESET}                                                 ║")
    print(f"{AZUL}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")


def main():
    ruta_txt = obtener_ruta_requirements()
    programas, todas_las_deps = parsear_requirements(ruta_txt)

    while True:
        limpiar_consola()
        mostrar_menu(programas, todas_las_deps)
        opcion = input(f"  {VERDE}{NEGRITA}Seleccione una opción (F, 1-{len(programas)+1}, 0): {RESET}").strip().upper()

        if opcion in ("0", "Q", "EXIT", "SALIR"):
            print(f"\n{CYAN}Saliendo del instalador. ¡Hasta luego!{RESET}\n")
            sys.exit(0)

        elif opcion == "F":
            faltantes_globales = [p for p in todas_las_deps if not paquete_esta_instalado(p)]
            if not faltantes_globales:
                print(f"\n{VERDE}✓ ¡Excelente! Todas las dependencias del proyecto ya están instaladas.{RESET}")
            else:
                print(f"\n{CYAN}Se instalarán las siguientes {len(faltantes_globales)} dependencias faltantes:{RESET}")
                for d in faltantes_globales:
                    print(f"  {VERDE}•{RESET} {BLANCO}{d}{RESET}")
                confirmar = input(f"\n{AMARILLO}¿Proceder con la instalación de los paquetes faltantes? (S/n): {RESET}").strip().lower()
                if confirmar not in ("n", "no"):
                    instalar_paquetes(faltantes_globales, "DEPENDENCIAS FALTANTES")
                else:
                    print(f"\n{AMARILLO}Operación cancelada.{RESET}")
            input(f"\n{BLANCO}Presione Enter para volver al menú...{RESET}")

        elif opcion == "1":
            print(f"\n{CYAN}Se verificarán e instalarán las {len(todas_las_deps)} dependencias del proyecto:{RESET}")
            for d in todas_las_deps:
                print(f"  {VERDE}•{RESET} {BLANCO}{d}{RESET}")
            confirmar = input(f"\n{AMARILLO}¿Proceder con la instalación global? (s/N): {RESET}").strip().lower()
            if confirmar in ("s", "si", "y", "yes"):
                instalar_paquetes(todas_las_deps, "TODOS LOS PROGRAMAS (Global)")
            else:
                print(f"\n{AMARILLO}Operación cancelada.{RESET}")
            input(f"\n{BLANCO}Presione Enter para volver al menú...{RESET}")

        else:
            try:
                num = int(opcion)
                indice = num - 2
                if 0 <= indice < len(programas):
                    prog = programas[indice]
                    if prog.solo_estandar:
                        print(f"\n{AZUL}{'═' * 70}{RESET}")
                        print(f"  {CYAN}[*] Programa:{RESET} {BLANCO}{prog.nombre}{RESET}")
                        print(f"  {CYAN}    Archivo :{RESET} {BLANCO}{prog.archivo}{RESET}")
                        print(f"  {VERDE}    Detalle :{RESET} Este programa SOLO utiliza módulos de la biblioteca")
                        print("              estándar de Python (os, sys, socket, hashlib, etc.).")
                        print(f"  {VERDE}✓ No requiere instalar paquetes externos de pip.{RESET}")
                        print(f"{AZUL}{'═' * 70}{RESET}")
                    else:
                        faltantes = prog.obtener_faltantes()
                        print(f"\n{CYAN}Dependencias de '{prog.nombre}':{RESET}")
                        for d in prog.dependencias:
                            st = f"{VERDE}[✓ Instalado]{RESET}" if paquete_esta_instalado(d) else f"{AMARILLO}[✗ Falta]{RESET}"
                            print(f"  {VERDE}•{RESET} {BLANCO}{d:<25}{RESET} {st}")

                        if not faltantes:
                            print(f"\n{VERDE}✓ Todas las dependencias de este programa ya están instaladas.{RESET}")
                            reinst = input(f"\n{BLANCO}¿Deseas forzar la reinstalación? (s/N): {RESET}").strip().lower()
                            if reinst in ("s", "si", "y", "yes"):
                                instalar_paquetes(prog.dependencias, prog.nombre)
                        else:
                            confirmar = input(f"\n{AMARILLO}¿Proceder con la instalación de los paquetes faltantes? (S/n): {RESET}").strip().lower()
                            if confirmar not in ("n", "no"):
                                instalar_paquetes(faltantes, prog.nombre)
                            else:
                                print(f"\n{AMARILLO}Operación cancelada.{RESET}")
                    input(f"\n{BLANCO}Presione Enter para volver al menú...{RESET}")
                else:
                    print(f"\n{ROJO}[!] Opción no válida. Seleccione un número de la lista.{RESET}")
                    input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")
            except ValueError:
                print(f"\n{ROJO}[!] Entrada inválida. Ingrese una opción válida (ej. F, 1, 2... o 0).{RESET}")
                input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")


if __name__ == "__main__":
    main()
