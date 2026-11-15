#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
PROGRAMAS ÚTILES - CENTRO DE CONTROL Y LANZADOR PRINCIPAL
==============================================================================
Punto de entrada unificado para explorar, diagnosticar y ejecutar cualquiera
de las herramientas y utilidades del repositorio.
de las herramientas y utilidades del repositorio (tanto en consola CLI como
mediante panel gráfico interactivo en Streamlit).
==============================================================================
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path
from typing import List, Dict, Optional

# Habilitar secuencias de escape ANSI en consolas Windows modernas
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

# Directorio raíz del proyecto
PROYECTO_ROOT = Path(__file__).resolve().parent


def is_running_in_streamlit() -> bool:
    """Detecta si el script se está ejecutando dentro del entorno de Streamlit."""
    try:
        from streamlit import runtime
        return runtime.exists()
    except Exception:
        try:
            import streamlit
            return getattr(streamlit, "_is_running_with_streamlit", False)
        except Exception:
            return False


def lanzar_streamlit_dashboard():
    """Lanza la interfaz web de Streamlit para el Centro de Control."""
    print("\n[*] Iniciando Centro de Control Web con Streamlit...")
    print("[*] Presione Ctrl+C en esta terminal para detener el servidor web.\n")
    cmd = [sys.executable, "-m", "streamlit", "run", str(Path(__file__).resolve())]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[*] Centro de Control Web cerrado. Regresando a la terminal...")


def solicitar_entrada(prompt: str = "") -> str:
    """Solicita entrada al usuario controlando EOFError y KeyboardInterrupt de forma segura."""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return ""


def esperar_enter(prompt: str = "Presione Enter para continuar..."):
    """Pausa la ejecución esperando Enter controlando interrupciones."""
    try:
        input(prompt)
    except (EOFError, KeyboardInterrupt):
        pass


# Mapeo de nombre de paquete pip a nombre de módulo importable en Python
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


class Herramienta:
    def __init__(
        self,
        id_num: int,
        categoria: str,
        nombre: str,
        archivo: str,
        descripcion: str,
        dependencias: List[str],
        soporta_web: bool = False,
    ):
        self.id_num = id_num
        self.categoria = categoria
        self.nombre = nombre
        self.archivo = archivo
        self.descripcion = descripcion
        self.dependencias = dependencias
        self.soporta_web = soporta_web

    @property
    def ruta_absoluta(self) -> Path:
        return PROYECTO_ROOT / self.archivo

    def existe_archivo(self) -> bool:
        return self.ruta_absoluta.is_file()

    def obtener_dependencias_faltantes(self) -> List[str]:
        """Devuelve la lista de paquetes pip no instalados en el entorno actual."""
        faltantes = []
        for dep in self.dependencias:
            dep_clean = dep.strip().lower()
            modulo = PKG_A_MODULO.get(dep_clean, dep_clean.replace("-", "_"))
            if importlib.util.find_spec(modulo) is None:
                faltantes.append(dep)
        return faltantes


# Catálogo completo y estructurado de herramientas
CATALOGO: List[Herramienta] = [
    # -------------------------------------------------------------------------
    # CIBERSEGURIDAD Y PRIVACIDAD
    # -------------------------------------------------------------------------
    Herramienta(
        id_num=1,
        categoria="Ciberseguridad y Privacidad",
        nombre="Gestor y Modificador de Metadatos EXIF",
        archivo="ciberseguridad/metadatos.py",
        descripcion="Audita, inyecta (GPS, autor, fecha) y sanitiza metadatos en imágenes digitales (JPG, PNG, WebP, TIFF).",
        dependencias=["pillow", "streamlit"],
        soporta_web=True,
    ),
    Herramienta(
        id_num=2,
        categoria="Ciberseguridad y Privacidad",
        nombre="Desbloqueador de PDF y Excel (GPU OpenCL & CPU)",
        archivo="ciberseguridad/Desbloqueador_pdf_excel/Buscador.py",
        descripcion="Recuperación de claves por fuerza bruta acelerada por tarjeta gráfica (GPU OpenCL) o multiproceso CPU.",
        dependencias=["pypdf", "pycryptodome", "streamlit"],
        soporta_web=True,
    ),
    Herramienta(
        id_num=3,
        categoria="Ciberseguridad y Privacidad",
        nombre="Encriptador de Archivos (PDF, Excel, CSV)",
        archivo="ciberseguridad/encriptador/encriptador.py",
        descripcion="Cifrado criptográfico fuerte (AES-256 y Fernet) para documentos sensibles con doble interfaz.",
        dependencias=["pypdf", "msoffcrypto-tool", "cryptography", "streamlit"],
        soporta_web=True,
    ),
    Herramienta(
        id_num=4,
        categoria="Ciberseguridad y Privacidad",
        nombre="SpectraScan / NetRecon (Escáner de Red y Auditor Web)",
        archivo="ciberseguridad/Puertos/SpectraScan.py",
        descripcion="Escaneo multihilo de puertos TCP, fingerprinting de servicios, auditoría de cabeceras HTTP y certificados SSL.",
        dependencias=[],
        soporta_web=False,
    ),
    Herramienta(
        id_num=5,
        categoria="Ciberseguridad y Privacidad",
        nombre="Cifrador de Mensajes por XOR",
        archivo="ciberseguridad/Cifrador_de_mensajes.py",
        descripcion="Cifrado y descifrado simétrico ultrarrápido de cadenas de texto mediante operaciones XOR bit a bit.",
        dependencias=[],
        soporta_web=False,
    ),
    Herramienta(
        id_num=6,
        categoria="Ciberseguridad y Privacidad",
        nombre="Cracker de Hashes SHA-256 por Diccionario",
        archivo="ciberseguridad/Hash_fuerza_bruta.py",
        descripcion="Ataque de diccionario contra hashes SHA-256 con cálculo de hashrate (intentos por segundo en microsegundos).",
        dependencias=[],
        soporta_web=False,
    ),
    # -------------------------------------------------------------------------
    # KIT DE HERRAMIENTAS Y PRODUCTIVIDAD
    # -------------------------------------------------------------------------
    Herramienta(
        id_num=7,
        categoria="Kit de Herramientas y Productividad",
        nombre="Optimizador de PDFs/Imágenes y Recorte de Fondos por IA",
        archivo="Kit_herramientas/Compresor_removedor_fondos/Compresor_removedor_fondos.py",
        descripcion="Compresión de documentos, conversión de formatos y eliminación automática de fondos mediante IA (rembg).",
        dependencias=["pymupdf", "pillow", "rembg", "streamlit"],
        soporta_web=True,
    ),
    Herramienta(
        id_num=8,
        categoria="Kit de Herramientas y Productividad",
        nombre="Convertidor de Tablas (PDF, CSV, Excel a LaTeX/Markdown)",
        archivo="Kit_herramientas/Convertidor_tablas/Convertidor_tablas.py",
        descripcion="Extrae tablas estructuradas de documentos y genera código LaTeX o Markdown listo para publicaciones.",
        dependencias=["pandas", "openpyxl", "pymupdf", "tabulate", "streamlit"],
        soporta_web=True,
    ),
    Herramienta(
        id_num=9,
        categoria="Kit de Herramientas y Productividad",
        nombre="Auditor de Procesos y Puertos Locales",
        archivo="Kit_herramientas/Auditor_procesos_puertos/Auditor_procesos_puertos.py",
        descripcion="Inspección en tiempo real de recursos (CPU/RAM), conexiones de red activas y gestión de procesos.",
        dependencias=["psutil", "pandas", "altair", "streamlit"],
        soporta_web=True,
    ),
    Herramienta(
        id_num=10,
        categoria="Kit de Herramientas y Productividad",
        nombre="Organizador Inteligente de Directorios (Smart Organizer)",
        archivo="Kit_herramientas/smart_organizer.py",
        descripcion="Clasifica y ordena automáticamente archivos desorganizados por extensión, categoría o fecha.",
        dependencias=["streamlit"],
        soporta_web=True,
    ),
    Herramienta(
        id_num=11,
        categoria="Kit de Herramientas y Productividad",
        nombre="Automatizador de Respaldos Incrementales",
        archivo="Kit_herramientas/Respaldos_incrementales/Respaldos_incrementales.py",
        descripcion="Copias de seguridad automáticas completas e incrementales (.zip / .tar.gz) basadas en modificación mtime.",
        dependencias=["streamlit"],
        soporta_web=True,
    ),
    Herramienta(
        id_num=12,
        categoria="Kit de Herramientas y Productividad",
        nombre="Monitor de Latencia y Microcortes (Ping Logger)",
        archivo="Kit_herramientas/Ping_Logger/Ping_Logger.py",
        descripcion="Monitoreo continuo de hosts con registro histórico en CSV y visualización interactiva de caídas.",
        dependencias=["pandas", "streamlit"],
        soporta_web=True,
    ),
    Herramienta(
        id_num=13,
        categoria="Kit de Herramientas y Productividad",
        nombre="Descargador de Videos y Playlists de YouTube",
        archivo="Kit_herramientas/Descargar_video_YT/Descargar_videos_youtube.py",
        descripcion="Descarga en múltiples formatos (MP4, MP3, WebM, M4A, WAV), gestión de rutas y reproductor integrado (CLI y Web).",
        dependencias=["yt-dlp", "imageio-ffmpeg", "streamlit"],
        soporta_web=True,
    ),
    Herramienta(
        id_num=14,
        categoria="Kit de Herramientas y Productividad",
        nombre="Generador de Códigos QR Personalizados",
        archivo="Kit_herramientas/Generador_QR/Generador_de_QR_por_link.py",
        descripcion="Creación de códigos QR de alta resolución con enlaces, textos, vCards y personalización visual.",
        dependencias=["qrcode", "pillow"],
        soporta_web=False,
    ),
    Herramienta(
        id_num=15,
        categoria="Kit de Herramientas y Productividad",
        nombre="Juntador y Fusionador de Archivos PDF",
        archivo="Kit_herramientas/Juntador_pdf/Juntador_pdfs.py",
        descripcion="Fusión y ordenamiento de múltiples archivos PDF en un único documento preservando metadatos y enlaces.",
        dependencias=["pypdf"],
        soporta_web=False,
    ),
    Herramienta(
        id_num=16,
        categoria="Kit de Herramientas y Productividad",
        nombre="Generador de Audio por Texto (TTS)",
        archivo="Kit_herramientas/Genera_y_poner_audio_por_texto.py",
        descripcion="Conversión de cadenas de texto a voz natural mediante síntesis TTS con reproducción automática.",
        dependencias=["gtts"],
        soporta_web=False,
    ),
    Herramienta(
        id_num=17,
        categoria="Kit de Herramientas y Productividad",
        nombre="Escritor Automatizado de Mensajes (Auto-Typer)",
        archivo="Kit_herramientas/Escribir_mensajes.py",
        descripcion="Simulación de escritura por teclado con control de velocidad a nivel de kernel y atajos de interrupción.",
        dependencias=["keyboard"],
        soporta_web=False,
    ),
    # -------------------------------------------------------------------------
    # CURIOSIDADES Y SIMULACIONES
    # -------------------------------------------------------------------------
    Herramienta(
        id_num=18,
        categoria="Curiosidades y Simulaciones",
        nombre="Simulador del Juego de la Vida de Conway",
        archivo="Programas_para_curiosidad/Simulador_de_vida_cow.py",
        descripcion="Autómata celular interactivo en consola con simulación matemática de evolución y patrones oscilantes.",
        dependencias=[],
        soporta_web=False,
    ),
]


def limpiar_pantalla():
    """Limpia la consola."""
    os.system("cls" if os.name == "nt" else "clear")


def instalar_paquetes(paquetes: List[str]) -> bool:
    """Instala dependencias faltantes usando el intérprete actual."""
    print("\n" + "=" * 65)
    print(f"[*] Instalando paquetes requeridos: {', '.join(paquetes)}")
    print("=" * 65)
    cmd = [sys.executable, "-m", "pip", "install", *paquetes]
    try:
        resultado = subprocess.run(cmd, check=False)
        return resultado.returncode == 0
    except Exception as e:
        print(f"[!] Error al invocar pip: {e}")
        return False


def verificar_e_instalar_dependencias(herramienta: Herramienta) -> bool:
    """Comprueba si las dependencias están instaladas y ofrece descargarlas si faltan."""
    faltantes = herramienta.obtener_dependencias_faltantes()
    if not faltantes:
        return True

    print("\n" + "!" * 65)
    print(f"[!] ATENCIÓN: Para ejecutar '{herramienta.nombre}'")
    print(f"    se requieren las siguientes librerías faltantes:")
    for dep in faltantes:
        print(f"    - {dep}")
    print("!" * 65)

    resp = solicitar_entrada("\n¿Desea instalar estas librerías automáticamente ahora? (S/n): ").strip().lower()
    if resp in ("", "s", "si", "sí", "y", "yes"):
        exito = instalar_paquetes(faltantes)
        if exito:
            print("\n[+] Librerías instaladas con éxito.")
            return True
        else:
            print("\n[-] Error durante la instalación de paquetes.")
            esperar_enter("Presione Enter para continuar...")
            return False
    else:
        print("\n[-] Ejecución cancelada por falta de dependencias.")
        esperar_enter("Presione Enter para continuar...")
        return False


def ejecutar_herramienta(herramienta: Herramienta):
    """Ejecuta la herramienta seleccionada en CLI o en Streamlit según la elección del usuario."""
    if not herramienta.existe_archivo():
        print(f"\n[!] Error: No se encontró el archivo del programa en:\n    {herramienta.ruta_absoluta}")
        esperar_enter("Presione Enter para continuar...")
        return

    # Verificar dependencias
    if not verificar_e_instalar_dependencias(herramienta):
        return

    modo_web = False
    if herramienta.soporta_web:
        print("\n" + "=" * 60)
        print(f"  SELECCIÓN DE INTERFAZ: {herramienta.nombre}")
        print("=" * 60)
        print("  [1] Consola / Menú Interactivo (Terminal CLI)")
        print("  [2] Interfaz Gráfica Web (Streamlit en el navegador)")
        print("=" * 60)
        eleccion = solicitar_entrada("Seleccione el modo de ejecución [1]: ").strip()
        if eleccion == "2":
            modo_web = True

    script_path = herramienta.ruta_absoluta
    cwd_dir = script_path.parent

    print("\n" + "-" * 65)
    if modo_web:
        print(f"[*] Lanzando servidor Streamlit para: {herramienta.nombre}...")
        print("[*] Presione Ctrl+C en esta terminal para detener el servidor web.")
        cmd = [sys.executable, "-m", "streamlit", "run", str(script_path)]
    else:
        print(f"[*] Iniciando: {herramienta.nombre}...")
        cmd = [sys.executable, str(script_path)]
    print("-" * 65 + "\n")

    try:
        subprocess.run(cmd, cwd=str(cwd_dir))
    except KeyboardInterrupt:
        print(f"\n\n[*] Proceso de '{herramienta.nombre}' finalizado por el usuario.")
    except Exception as e:
        print(f"\n[!] Ocurrió un error al ejecutar el programa: {e}")

    print("\n" + "=" * 65)
    esperar_enter("[*] Programa finalizado. Presione Enter para regresar al menú principal...")


def diagnostico_repositorio(pausar: bool = True):
    """Revisa el estado de archivos y dependencias de todas las herramientas."""
    limpiar_pantalla()
    print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{AZUL}{NEGRITA}║              🩺 DIAGNÓSTICO INTEGRAL DEL REPOSITORIO DE HERRAMIENTAS               ║{RESET}")
    print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"  {CYAN}Directorio raíz:{RESET}   {PROYECTO_ROOT}")
    print(f"  {CYAN}Intérprete Python:{RESET} {sys.executable}")
    print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
    print(f"  {BLANCO}{NEGRITA}{'#':<3} {'NOMBRE':<40} {'ARCHIVO':<9} {'DEPENDENCIAS'}{RESET}")
    print(f"  {AZUL}{'─' * 80}{RESET}")

    listos = 0
    total = len(CATALOGO)

    for h in CATALOGO:
        arch_ok = h.existe_archivo()
        arch_str = f"{VERDE}[OK]{RESET}" if arch_ok else f"{ROJO}[FALTA]{RESET}"

        faltantes = h.obtener_dependencias_faltantes()
        if not h.dependencias:
            deps_str = f"{CYAN}Estándar (0 deps){RESET}"
        elif not faltantes:
            deps_str = f"{VERDE}Completas [OK]{RESET}"
        else:
            deps_str = f"{ROJO}Faltan: {', '.join(faltantes)}{RESET}"

        if arch_ok and not faltantes:
            listos += 1

        print(f"  {BLANCO}{h.id_num:<3}{RESET} {BLANCO}{h.nombre[:39]:<40}{RESET} {arch_str:<18} {deps_str}")

    print(f"  {AZUL}{'═' * 80}{RESET}")
    print(f"  {VERDE if listos == total else AMARILLO}{NEGRITA}Estado global: {listos} de {total} programas 100% listos para usar de inmediato.{RESET}")
    print(f"  {AZUL}{'═' * 80}{RESET}")
    if pausar:
        esperar_enter(f"\n{BLANCO}Presione Enter para volver al menú principal...{RESET}")


def buscar_herramientas():
    """Permite buscar herramientas por nombre, descripción o categoría."""
    limpiar_pantalla()
    print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{AZUL}{NEGRITA}║                   🔍 BÚSQUEDA RÁPIDA DE HERRAMIENTAS                               ║{RESET}")
    print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")
    termino = solicitar_entrada(f"{VERDE}{NEGRITA}Ingrese palabra clave a buscar (ej. pdf, qr, red, wifi, hash, video): {RESET}").strip().lower()
    if not termino:
        return

    coincidencias = [
        h for h in CATALOGO
        if termino in h.nombre.lower() or termino in h.descripcion.lower() or termino in h.archivo.lower()
    ]

    print(f"\n{AZUL}{'═' * 80}{RESET}")
    if not coincidencias:
        print(f"  {ROJO}[-] No se encontraron herramientas que coincidan con '{termino}'.{RESET}")
        print(f"{AZUL}{'═' * 80}{RESET}")
        esperar_enter(f"\n{BLANCO}Presione Enter para volver al menú...{RESET}")
        return

    print(f"  {VERDE}{NEGRITA}✓ Se encontraron {len(coincidencias)} herramientas coincidentes:{RESET}")
    print(f"{AZUL}{'═' * 80}{RESET}")
    for idx, h in enumerate(coincidencias, start=1):
        web_badge = f"{CYAN}[CLI + Web]{RESET}" if h.soporta_web else f"{BLANCO}[CLI]{RESET}"
        print(f"  {VERDE}[{idx}]{RESET} {BLANCO}{NEGRITA}{h.nombre}{RESET} {web_badge}")
        print(f"      {AMARILLO}↳{RESET} {h.descripcion}")
        print(f"      {CYAN}📁 Ruta:{RESET} {h.archivo}\n")

    print(f"{AZUL}{'─' * 80}{RESET}")
    opc = solicitar_entrada(f"{VERDE}{NEGRITA}Ingrese el número de la herramienta a probar (o Enter para cancelar): {RESET}").strip()
    if opc.isdigit():
        idx_sel = int(opc) - 1
        if 0 <= idx_sel < len(coincidencias):
            ejecutar_herramienta(coincidencias[idx_sel])


def mostrar_menu_principal():
    """Muestra el menú interactivo con todas las herramientas agrupadas por categorías."""
    limpiar_pantalla()
    print(f"{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{AZUL}{NEGRITA}║         🛠️  PROGRAMAS ÚTILES - CENTRO DE CONTROL Y PRUEBAS CENTRALIZADO            ║{RESET}")
    print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")

    cat_actual = None
    for h in CATALOGO:
        if h.categoria != cat_actual:
            cat_actual = h.categoria
            print(f"\n  {MAGENTA}{NEGRITA}📌  {cat_actual.upper()}{RESET}")
            print(f"  {AZUL}{'─' * 80}{RESET}")

        badge = f"{CYAN}[CLI + Web]{RESET}" if h.soporta_web else f"{BLANCO}[CLI]{RESET}"
        print(f"  {VERDE}[{h.id_num:2d}]{RESET} {BLANCO}{NEGRITA}{h.nombre:<48}{RESET} {badge:>12}")
        print(f"       {AMARILLO}↳{RESET} {BLANCO}{h.descripcion}{RESET}")

    print(f"\n  {AZUL}{'═' * 80}{RESET}")
    print(f"  {NEGRITA}{BLANCO}⚡ ACCIONES Y UTILIDADES DEL SISTEMA:{RESET}")
    print(f"  {MAGENTA}[ W]{RESET} {BLANCO}🌐 Iniciar Centro de Control en Interfaz Web (Streamlit){RESET}")
    print(f"  {CYAN}[ B]{RESET} {BLANCO}🔍 Buscar herramienta por palabra clave{RESET}")
    print(f"  {VERDE}[ D]{RESET} {BLANCO}🩺 Diagnóstico general de archivos y dependencias{RESET}")
    print(f"  {AMARILLO}[ I]{RESET} {BLANCO}📦 Gestor interactivo de instalación de dependencias{RESET}")
    print(f"  {ROJO}[ 0]{RESET} {BLANCO}🚪 Salir del programa{RESET}")
    print(f"  {AZUL}{'═' * 80}{RESET}\n")


# ==============================================================================
# INTERFAZ GRÁFICA INTERACTIVA WEB (STREAMLIT) PARA MAIN.PY
# ==============================================================================
def run_streamlit_dashboard():
    """Ejecuta el panel interactivo web de Streamlit para todo el repositorio."""
    import streamlit as st

    st.set_page_config(
        page_title="Centro de Control - Programas Útiles",
        page_icon="🛠️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .dash-header {
            font-size: 2.2rem;
            font-weight: 800;
            color: #0D47A1;
            margin-bottom: 0.1rem;
        }
        .dash-sub {
            font-size: 1.05rem;
            color: #555;
            margin-bottom: 1.5rem;
        }
        .tool-card {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        }
        .badge-web {
            background-color: #E3F2FD;
            color: #1565C0;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
        }
        .badge-cli {
            background-color: #ECEFF1;
            color: #37474F;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
        }
        .badge-ok {
            background-color: #E8F5E9;
            color: #2E7D32;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
        }
        .badge-warn {
            background-color: #FFF3E0;
            color: #E65100;
            font-weight: 600;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="dash-header">🛠️ Centro de Control Unificado</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="dash-sub">Explora, diagnostica y ejecuta cualquiera de las 18 herramientas del repositorio desde una interfaz moderna.</div>',
        unsafe_allow_html=True,
    )

    # Métricas superiores
    total_tools = len(CATALOGO)
    ciber_count = sum(1 for h in CATALOGO if h.categoria == "Ciberseguridad y Privacidad")
    prod_count = sum(1 for h in CATALOGO if h.categoria == "Kit de Herramientas y Productividad")
    curio_count = sum(1 for h in CATALOGO if h.categoria == "Curiosidades y Simulaciones")
    listas_count = sum(1 for h in CATALOGO if h.existe_archivo() and not h.obtener_dependencias_faltantes())

    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    col_m1.metric("Total Herramientas", f"{total_tools}")
    col_m2.metric("🛡️ Ciberseguridad", f"{ciber_count}")
    col_m3.metric("🛠️ Productividad", f"{prod_count}")
    col_m4.metric("🧪 Curiosidades", f"{curio_count}")
    col_m5.metric("🩺 Listas para Usar", f"{listas_count} / {total_tools}")

    # Barra lateral de filtros
    st.sidebar.title("🧭 Navegación")
    seccion = st.sidebar.radio(
        "Ir a sección:",
        ["🎛️ Centro de Herramientas", "🩺 Diagnóstico de Integridad", "📦 Gestor de Dependencias"],
    )

    if seccion == "🎛️ Centro de Herramientas":
        st.sidebar.markdown("---")
        st.sidebar.subheader("Filtros y Búsqueda")
        filtro_cat = st.sidebar.selectbox(
            "Filtrar por Categoría:",
            ["Todas", "Ciberseguridad y Privacidad", "Kit de Herramientas y Productividad", "Curiosidades y Simulaciones"],
        )
        filtro_interfaz = st.sidebar.selectbox(
            "Tipo de Interfaz:",
            ["Todas", "Con Interfaz Web (Streamlit)", "Solo Consola (CLI)"],
        )
        busqueda = st.sidebar.text_input("🔍 Buscar por texto / palabra clave:", value="").strip().lower()

        # Filtrar catálogo
        herramientas_filtradas = []
        for h in CATALOGO:
            if filtro_cat != "Todas" and h.categoria != filtro_cat:
                continue
            if filtro_interfaz == "Con Interfaz Web (Streamlit)" and not h.soporta_web:
                continue
            if filtro_interfaz == "Solo Consola (CLI)" and h.soporta_web:
                continue
            if busqueda:
                match = (busqueda in h.nombre.lower() or busqueda in h.descripcion.lower() or busqueda in h.archivo.lower())
                if not match:
                    continue
            herramientas_filtradas.append(h)

        st.subheader(f"Catálogo de Herramientas ({len(herramientas_filtradas)} encontradas)")

        # Renderizar en 2 columnas
        col_izq, col_der = st.columns(2)
        for i, h in enumerate(herramientas_filtradas):
            target_col = col_izq if i % 2 == 0 else col_der
            faltantes = h.obtener_dependencias_faltantes()
            arch_ok = h.existe_archivo()

            with target_col:
                with st.container(border=True):
                    c_titulo, c_badge = st.columns([3, 1])
                    with c_titulo:
                        st.markdown(f"### {h.id_num}. {h.nombre}")
                    with c_badge:
                        if h.soporta_web:
                            st.markdown('<span class="badge-web">CLI + Web</span>', unsafe_allow_html=True)
                        else:
                            st.markdown('<span class="badge-cli">Solo CLI</span>', unsafe_allow_html=True)

                    st.caption(f"📁 **Ruta:** `{h.archivo}` | **Categoría:** {h.categoria}")
                    st.write(h.descripcion)

                    if not arch_ok:
                        st.error("❌ Archivo del programa no encontrado en disco.")
                    elif not faltantes:
                        st.markdown('<span class="badge-ok">✅ Dependencias Completas</span>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<span class="badge-warn">⚠️ Faltan: {", ".join(faltantes)}</span>', unsafe_allow_html=True)

                    st.markdown("")
                    col_b1, col_b2 = st.columns(2)
                    with col_b1:
                        if h.soporta_web:
                            if st.button(f"🌐 Iniciar Web UI", key=f"btn_web_{h.id_num}"):
                                st.info(f"Lanzando servidor Streamlit para `{h.nombre}`...")
                                subprocess.Popen([sys.executable, "-m", "streamlit", "run", str(h.ruta_absoluta)], cwd=str(h.ruta_absoluta.parent))
                                st.success("✅ Servidor web iniciado en segundo plano. Se abrirá una nueva pestaña en tu navegador.")
                        else:
                            st.code(f"python {h.archivo}", language="bash")

                    with col_b2:
                        if faltantes:
                            if st.button(f"📥 Instalar ({', '.join(faltantes)})", key=f"btn_inst_{h.id_num}"):
                                with st.spinner(f"Instalando {', '.join(faltantes)}..."):
                                    res = instalar_paquetes(faltantes)
                                    if res:
                                        st.success("¡Instalación completada!")
                                        st.rerun()
                                    else:
                                        st.error("Ocurrió un error en pip.")
                        elif h.soporta_web:
                            st.code(f"streamlit run {h.archivo}", language="bash")

    elif seccion == "🩺 Diagnóstico de Integridad":
        st.subheader("Diagnóstico Integral de Salud del Repositorio")
        st.write("Verificación de la existencia de archivos fuente y librerías externas de Python en el entorno activo.")

        filas = []
        for h in CATALOGO:
            arch_ok = "✅ Presente" if h.existe_archivo() else "❌ Falta"
            faltantes = h.obtener_dependencias_faltantes()
            if not h.dependencias:
                deps_estado = "Librería Estándar (0 deps)"
            elif not faltantes:
                deps_estado = "✅ 100% Instaladas"
            else:
                deps_estado = f"⚠️ Faltan: {', '.join(faltantes)}"

            filas.append({
                "#": h.id_num,
                "Herramienta": h.nombre,
                "Categoría": h.categoria,
                "Archivo": h.archivo,
                "Estado Archivo": arch_ok,
                "Dependencias": deps_estado,
                "Interfaz Web": "Sí (Streamlit)" if h.soporta_web else "No (CLI)",
            })

        try:
            import pandas as pd
            df_diag = pd.DataFrame(filas)
            st.dataframe(df_diag, use_container_width=True, hide_index=True)
        except Exception:
            for f in filas:
                st.write(f)

        st.info(f"**Intérprete Python Activo:** `{sys.executable}`\n\n**Directorio Raíz:** `{PROYECTO_ROOT}`")

    elif seccion == "📦 Gestor de Dependencias":
        st.subheader("Gestión e Instalación de Dependencias")
        st.write("Administra los paquetes requeridos por las herramientas del proyecto definidos en `requirements.txt`.")

        req_path = PROYECTO_ROOT / "requirements.txt"
        if req_path.is_file():
            with open(req_path, "r", encoding="utf-8") as fp:
                req_content = fp.read()

            with st.expander("📄 Ver contenido de requirements.txt"):
                st.code(req_content, language="text")

            col_inst_all, _ = st.columns([1, 2])
            with col_inst_all:
                if st.button("🚀 Instalar TODAS las dependencias del proyecto (pip install -r requirements.txt)"):
                    with st.spinner("Instalando dependencias globales..."):
                        cmd = [sys.executable, "-m", "pip", "install", "-r", str(req_path)]
                        res = subprocess.run(cmd, capture_output=True, text=True)
                        if res.returncode == 0:
                            st.success("✅ ¡Todas las dependencias se instalaron correctamente!")
                            st.rerun()
                        else:
                            st.error(f"Error al ejecutar pip:\n{res.stderr}")


def main():
    if is_running_in_streamlit():
        run_streamlit_dashboard()
        return

    # Soporte para argumentos de línea de comandos directos:
    # Ejemplos:
    #   python main.py web / --web
    #   python main.py --check / --diagnostico
    #   python main.py --list
    #   python main.py 1
    #   python main.py metadatos
    if len(sys.argv) > 1:
        arg = sys.argv[1].strip().lower()
        if arg in ("web", "--web", "-w"):
            lanzar_streamlit_dashboard()
            sys.exit(0)
        elif arg in ("--check", "-c", "check", "diagnostico", "--diagnostico"):
            diagnostico_repositorio(pausar=False)
            sys.exit(0)
        elif arg in ("--list", "-l", "list"):
            for h in CATALOGO:
                badge = "[CLI + Web]" if h.soporta_web else "[CLI]"
                print(f"[{h.id_num:2d}] {h.nombre} ({h.archivo}) {badge}")
            sys.exit(0)
        elif arg.isdigit():
            id_arg = int(arg)
            for h in CATALOGO:
                if h.id_num == id_arg:
                    ejecutar_herramienta(h)
                    sys.exit(0)
            print(f"[!] No existe herramienta con ID: {id_arg}")
            sys.exit(1)
        else:
            # Buscar por coincidencia en nombre o archivo
            for h in CATALOGO:
                if arg in h.archivo.lower() or arg in h.nombre.lower():
                    ejecutar_herramienta(h)
                    sys.exit(0)

    # Modo interactivo por defecto
    # Modo interactivo de consola por defecto
    try:
        while True:
            mostrar_menu_principal()
            eleccion = solicitar_entrada(f"{VERDE}{NEGRITA}Seleccione una opción (1-18, W, B, D, I, 0): {RESET}").strip().upper()

            if eleccion in ("0", "Q", "SALIR", "EXIT", ""):
                print("\nSaliendo del Centro de Control. ¡Hasta luego!\n")
                sys.exit(0)
            elif eleccion == "W":
                lanzar_streamlit_dashboard()
            elif eleccion == "B":
                buscar_herramientas()
            elif eleccion == "D":
                diagnostico_repositorio()
            elif eleccion == "I":
                inst_script = PROYECTO_ROOT / "instalar_dependencias.py"
                if inst_script.is_file():
                    subprocess.run([sys.executable, str(inst_script)], cwd=str(PROYECTO_ROOT))
                else:
                    print(f"[!] No se encontró '{inst_script}'.")
                    esperar_enter("Presione Enter...")
            elif eleccion.isdigit():
                id_sel = int(eleccion)
                herramienta_encontrada = None
                for h in CATALOGO:
                    if h.id_num == id_sel:
                        herramienta_encontrada = h
                        break

                if herramienta_encontrada:
                    ejecutar_herramienta(herramienta_encontrada)
                else:
                    print("\n[!] Número de opción no válido.")
                    esperar_enter("Presione Enter para continuar...")
            else:
                print("\n[!] Opción no reconocida. Intente de nuevo.")
                esperar_enter("Presione Enter para continuar...")
    except KeyboardInterrupt:
        print("\n\nSaliendo del Centro de Control. ¡Hasta luego!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
