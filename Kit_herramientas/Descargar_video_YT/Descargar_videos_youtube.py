import glob
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime

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

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_descarga.json")
EXTS_VALIDAS = {".mp4", ".mp3", ".m4a", ".wav", ".webm", ".mkv", ".avi", ".flv"}

FORMATOS_DISPONIBLES = {
    "1": {
        "nombre": "MP4 - Mejor Calidad Disponible",
        "tipo": "video",
        "ext": "mp4",
        "opciones": {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
        },
    },
    "2": {
        "nombre": "MP4 - 1080p Full HD",
        "tipo": "video",
        "ext": "mp4",
        "opciones": {
            "format": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "merge_output_format": "mp4",
        },
    },
    "3": {
        "nombre": "MP4 - 720p HD",
        "tipo": "video",
        "ext": "mp4",
        "opciones": {
            "format": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best[height<=720]",
            "merge_output_format": "mp4",
        },
    },
    "4": {
        "nombre": "MP4 - 480p Calidad Media",
        "tipo": "video",
        "ext": "mp4",
        "opciones": {
            "format": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=480]+bestaudio/best[height<=480]",
            "merge_output_format": "mp4",
        },
    },
    "5": {
        "nombre": "WebM - Mejor Calidad WebM",
        "tipo": "video",
        "ext": "webm",
        "opciones": {
            "format": "bestvideo[ext=webm]+bestaudio[ext=webm]/best[ext=webm]/best",
            "merge_output_format": "webm",
        },
    },
    "6": {
        "nombre": "MP3 - Audio Alta Calidad (320 kbps)",
        "tipo": "audio",
        "ext": "mp3",
        "opciones": {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
        },
    },
    "7": {
        "nombre": "M4A - Audio Nativo AAC",
        "tipo": "audio",
        "ext": "m4a",
        "opciones": {
            "format": "bestaudio[ext=m4a]/bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                    "preferredquality": "192",
                }
            ],
        },
    },
    "8": {
        "nombre": "WAV - Audio Sin Pérdida (Lossless)",
        "tipo": "audio",
        "ext": "wav",
        "opciones": {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                }
            ],
        },
    },
}


def is_running_in_streamlit():
    try:
        from streamlit import runtime
        return runtime.exists()
    except Exception:
        try:
            import streamlit
            return getattr(streamlit, "_is_running_with_streamlit", False)
        except Exception:
            return False


def lanzar_streamlit_desde_cli():
    print(f"\n{CYAN}[*] Iniciando interfaz gráfica web en Streamlit...{RESET}")
    print(f"{BLANCO}[*] Presione Ctrl+C en esta consola para detener el servidor web.{RESET}\n")
    cmd = [sys.executable, "-m", "streamlit", "run", str(os.path.abspath(__file__))]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{VERDE}[*] Interfaz web cerrada. Regresando a la terminal...{RESET}")


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def formatear_tamano(tamano_bytes):
    for unidad in ["B", "KB", "MB", "GB", "TB"]:
        if tamano_bytes < 1024.0:
            return f"{tamano_bytes:.2f} {unidad}"
        tamano_bytes /= 1024.0
    return f"{tamano_bytes:.2f} PB"


def obtener_ruta_predeterminada():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos_descargado")


def obtener_ruta_descargas():
    if os.path.isfile(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                datos = json.load(f)
                ruta = datos.get("ruta_descarga")
                if ruta and os.path.isdir(ruta):
                    return ruta
        except Exception:
            pass
    return obtener_ruta_predeterminada()


def guardar_ruta_descargas(nueva_ruta):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"ruta_descarga": nueva_ruta}, f, indent=4)
        return True
    except Exception:
        return False


def restaurar_ruta_predeterminada():
    if os.path.isfile(CONFIG_FILE):
        try:
            os.remove(CONFIG_FILE)
        except Exception:
            pass
    return obtener_ruta_predeterminada()


def listar_archivos_descargados(carpeta=None):
    if carpeta is None:
        carpeta = obtener_ruta_descargas()
    if not os.path.isdir(carpeta):
        return []
    archivos = []
    for root, _, files in os.walk(carpeta):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in EXTS_VALIDAS:
                ruta_completa = os.path.join(root, f)
                try:
                    stats = os.stat(ruta_completa)
                    tamano = stats.st_size
                    mtime = stats.st_mtime
                    archivos.append({
                        "nombre": f,
                        "ruta": ruta_completa,
                        "relativa": os.path.relpath(ruta_completa, carpeta),
                        "tamano_bytes": tamano,
                        "tamano_str": formatear_tamano(tamano),
                        "extension": ext.upper().replace(".", ""),
                        "es_video": ext in {".mp4", ".webm", ".mkv", ".avi", ".flv"},
                        "fecha": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S"),
                    })
                except Exception:
                    pass
    archivos.sort(key=lambda x: x["fecha"], reverse=True)
    return archivos


def reproducir_archivo(ruta):
    if not os.path.isfile(ruta):
        return False
    try:
        if os.name == "nt":
            os.startfile(ruta)
        elif sys.platform == "darwin":
            subprocess.run(["open", ruta], check=False)
        else:
            subprocess.run(["xdg-open", ruta], check=False)
        return True
    except Exception:
        return False


def abrir_carpeta_en_explorador(ruta):
    if not os.path.isdir(ruta):
        return False
    try:
        if os.name == "nt":
            os.startfile(ruta)
        elif sys.platform == "darwin":
            subprocess.run(["open", ruta], check=False)
        else:
            subprocess.run(["xdg-open", ruta], check=False)
        return True
    except Exception:
        return False


def obtener_ruta_ffmpeg():
    if shutil.which("ffmpeg"):
        return None

    patrones_winget = [
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\yt-dlp.FFmpeg_*\*\bin"),
        os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\*\bin"),
    ]
    for patron in patrones_winget:
        coincidencias = glob.glob(patron)
        if coincidencias and os.path.isdir(coincidencias[0]):
            return coincidencias[0]

    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        pass

    return None


def obtener_js_runtimes():
    if shutil.which("node"):
        return {"node": {}}
    if shutil.which("deno"):
        return {"deno": {}}
    return None


def descargar_contenido(url, clave_formato="1", es_playlist=False, carpeta_destino=None, hook_progreso=None):
    if not carpeta_destino:
        carpeta_destino = obtener_ruta_descargas()
    os.makedirs(carpeta_destino, exist_ok=True)

    formato_info = FORMATOS_DISPONIBLES.get(clave_formato, FORMATOS_DISPONIBLES["1"])

    if es_playlist:
        plantilla_salida = os.path.join(
            carpeta_destino,
            "%(playlist_title)s",
            "%(playlist_index)s - %(title)s.%(ext)s",
        )
    else:
        plantilla_salida = os.path.join(carpeta_destino, "%(title)s.%(ext)s")

    opciones = {
        "outtmpl": plantilla_salida,
        "noplaylist": not es_playlist,
        "ignoreerrors": es_playlist,
        "windowsfilenames": True,
        "quiet": False,
        "no_warnings": False,
    }

    for k, v in formato_info["opciones"].items():
        opciones[k] = v

    if hook_progreso:
        opciones["progress_hooks"] = [hook_progreso]

    ruta_ffmpeg = obtener_ruta_ffmpeg()
    if ruta_ffmpeg:
        opciones["ffmpeg_location"] = ruta_ffmpeg

    js_runtimes = obtener_js_runtimes()
    if js_runtimes:
        opciones["js_runtimes"] = js_runtimes

    try:
        import yt_dlp
    except ImportError:
        return False, "yt-dlp no está instalado. Ejecute: pip install yt-dlp imageio-ffmpeg"

    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        return True, "Descarga completada correctamente."
    except Exception as e:
        return False, str(e)


def mostrar_biblioteca():
    limpiar_pantalla()
    archivos = listar_archivos_descargados()
    ruta_act = obtener_ruta_descargas()

    print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{AZUL}{NEGRITA}║                   📂 BIBLIOTECA DE CONTENIDOS DESCARGADOS                          ║{RESET}")
    print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"{CYAN}📁 Carpeta actual:{RESET} {ruta_act}")
    print(f"{CYAN}📊 Total de archivos encontrados:{RESET} {len(archivos)}\n")

    if not archivos:
        print(f"{AMARILLO}No hay videos ni pistas de audio en la carpeta de descargas actual.{RESET}")
        input(f"\n{BLANCO}Presione Enter para regresar al menú principal...{RESET}")
        return

    print(f"{BLANCO}{NEGRITA}{'#':<4} {'FORMATO':<9} {'TAMAÑO':<12} {'FECHA':<20} {'NOMBRE DEL ARCHIVO'}{RESET}")
    print(f"{AZUL}{'─'*84}{RESET}")

    for idx, arc in enumerate(archivos, start=1):
        color_fmt = VERDE if arc["extension"] in ("MP3", "M4A", "WAV") else MAGENTA
        print(f"{BLANCO}{idx:<4}{RESET} {color_fmt}{arc['extension']:<9}{RESET} {CYAN}{arc['tamano_str']:<12}{RESET} {AMARILLO}{arc['fecha']:<20}{RESET} {BLANCO}{arc['relativa'][:38]}{RESET}")

    print(f"{AZUL}{'─'*84}{RESET}")
    eleccion = input(f"\n{VERDE}{NEGRITA}▶ Ingrese el número del archivo a reproducir (o Enter para volver): {RESET}").strip()
    if eleccion.isdigit():
        num = int(eleccion)
        if 1 <= num <= len(archivos):
            sel = archivos[num - 1]
            print(f"\n{CYAN}Iniciando reproducción de:{RESET} {sel['nombre']}")
            reproducir_archivo(sel["ruta"])
            time.sleep(1)
        else:
            print(f"{ROJO}Número de opción inválido.{RESET}")
            time.sleep(1)


def mostrar_ruta_actual():
    limpiar_pantalla()
    ruta_act = obtener_ruta_descargas()
    ruta_def = obtener_ruta_predeterminada()
    archivos = listar_archivos_descargados(ruta_act)
    total_bytes = sum(a["tamano_bytes"] for a in archivos)

    print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{AZUL}{NEGRITA}║                       📍 RUTA DE DESCARGA ACTIVA                                    ║{RESET}")
    print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"\n{BLANCO}{NEGRITA}Ruta activa actual:{RESET}\n  👉 {VERDE}{ruta_act}{RESET}")
    print(f"\n{BLANCO}{NEGRITA}Ruta predeterminada original:{RESET}\n  👉 {CYAN}{ruta_def}{RESET}")
    print(f"\n{CYAN}Total de archivos en esta carpeta:{RESET} {len(archivos)}")
    print(f"{CYAN}Espacio utilizado en disco:{RESET}         {formatear_tamano(total_bytes)}")

    if os.path.abspath(ruta_act) == os.path.abspath(ruta_def):
        print(f"\n{VERDE}✓ Estado: Utilizando la ruta predeterminada del sistema.{RESET}")
    else:
        print(f"\n{AMARILLO}ℹ Estado: Utilizando una ruta personalizada.{RESET}")

    print(f"\n{AZUL}{'─'*84}{RESET}")
    abrir = input(f"{BLANCO}¿Desea abrir esta carpeta en el Explorador de Archivos? (s/N): {RESET}").strip().lower()
    if abrir in ("s", "si", "y", "yes"):
        abrir_carpeta_en_explorador(ruta_act)


def gestionar_ruta_descarga():
    while True:
        limpiar_pantalla()
        ruta_act = obtener_ruta_descargas()
        ruta_def = obtener_ruta_predeterminada()

        print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{AZUL}{NEGRITA}║                   ⚙️ CONFIGURACIÓN DE RUTA DE DESCARGA                              ║{RESET}")
        print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"\n{CYAN}Ruta activa actual:{RESET} {VERDE}{ruta_act}{RESET}")
        print(f"{CYAN}Ruta predeterminada:{RESET} {BLANCO}{ruta_def}{RESET}\n")
        print(f"  {VERDE}[1]{RESET} {BLANCO}Ingresar nueva ruta de descarga personalizada{RESET}")
        print(f"  {AMARILLO}[2]{RESET} {BLANCO}Restaurar ruta predeterminada de fábrica{RESET}")
        print(f"  {CYAN}[3]{RESET} {BLANCO}Abrir carpeta actual en el Explorador{RESET}")
        print(f"  {ROJO}[0]{RESET} {BLANCO}Regresar al menú principal{RESET}\n")

        opc = input(f"{VERDE}Seleccione una opción: {RESET}").strip()
        if opc == "1":
            nueva = input(f"\n{CYAN}Ingrese la nueva ruta absoluta de destino: {RESET}").strip().strip('"').strip("'")
            if nueva:
                try:
                    os.makedirs(nueva, exist_ok=True)
                    guardar_ruta_descargas(nueva)
                    print(f"\n{VERDE}✓ Ruta guardada exitosamente en:{RESET} {nueva}")
                except Exception as e:
                    print(f"\n{ROJO}Error al crear o validar la ruta indicada: {e}{RESET}")
                time.sleep(1.5)
        elif opc == "2":
            res = restaurar_ruta_predeterminada()
            print(f"\n{VERDE}✓ Ruta predeterminada restaurada:{RESET} {res}")
            time.sleep(1.5)
        elif opc == "3":
            abrir_carpeta_en_explorador(ruta_act)
        elif opc == "0":
            break


def menu():
    while True:
        limpiar_pantalla()
        ruta_act = obtener_ruta_descargas()

        print(f"{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{AZUL}{NEGRITA}║         🎬 DESCARGADOR PROFESIONAL DE YOUTUBE & AUDIO (YT-DLP)                     ║{RESET}")
        print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"  {CYAN}📍 Guardando en:{RESET} {BLANCO}{ruta_act}{RESET}")
        print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"║  {VERDE}[1]{RESET} {BLANCO}{NEGRITA}📥 Descargar Video o Audio Individual (Elegir formato){RESET}                        ║")
        print(f"║  {VERDE}[2]{RESET} {BLANCO}{NEGRITA}📑 Descargar Playlist Completa (Elegir formato){RESET}                                ║")
        print(f"║  {CYAN}[3]{RESET} {BLANCO}📂 Ver y Reproducir Archivos Descargados{RESET}                                      ║")
        print(f"║  {CYAN}[4]{RESET} {BLANCO}📍 Ver Información de la Ruta de Guardado{RESET}                                    ║")
        print(f"║  {AMARILLO}[5]{RESET} {BLANCO}⚙️  Cambiar Ruta de Descarga / Restaurar Predeterminada{RESET}                       ║")
        print(f"║  {MAGENTA}[6]{RESET} {BLANCO}🌐 Iniciar Interfaz Gráfica Web (Streamlit){RESET}                                  ║")
        print(f"║  {ROJO}[0]{RESET} {BLANCO}🚪 Salir del Programa{RESET}                                                       ║")
        print(f"{AZUL}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

        opcion = input(f"{VERDE}{NEGRITA}Seleccione una opción (0-6): {RESET}").strip()

        if opcion in ("1", "2"):
            es_play = (opcion == "2")
            tipo_txt = "Playlist" if es_play else "Video o Audio individual"
            url = input(f"\n{CYAN}Ingrese la URL de YouTube para descargar ({tipo_txt}): {RESET}").strip()
            if not url:
                continue

            print(f"\n{AZUL}{NEGRITA}┌────────────────────────────────────────────────────────────────────────────────────┐{RESET}")
            print(f"{AZUL}{NEGRITA}│                         SELECCIONE EL FORMATO DE DESCARGA                          │{RESET}")
            print(f"{AZUL}{NEGRITA}├────────────────────────────────────────────────────────────────────────────────────┤{RESET}")
            for k, v in FORMATOS_DISPONIBLES.items():
                icono = "🎵" if v["tipo"] == "audio" else "🎥"
                print(f"│  {VERDE}[{k}]{RESET} {icono} {BLANCO}{v['nombre']:<70}{RESET}│")
            print(f"{AZUL}{NEGRITA}└────────────────────────────────────────────────────────────────────────────────────┘{RESET}")

            fmt_sel = input(f"\n{VERDE}Seleccione formato (1-8) [1 por defecto]: {RESET}").strip()
            if not fmt_sel or fmt_sel not in FORMATOS_DISPONIBLES:
                fmt_sel = "1"

            nombre_formato = FORMATOS_DISPONIBLES[fmt_sel]["nombre"]
            print(f"\n{CYAN}[*] Iniciando descarga en formato: {VERDE}{nombre_formato}{RESET}")
            print(f"{CYAN}[*] Carpeta de destino: {BLANCO}{ruta_act}{RESET}\n")

            exito, mensaje = descargar_contenido(url, clave_formato=fmt_sel, es_playlist=es_play)
            if exito:
                print(f"\n{VERDE}{NEGRITA}🎉 ¡Descarga finalizada con éxito!{RESET}")
            else:
                print(f"\n{ROJO}{NEGRITA}❌ Error durante la descarga: {mensaje}{RESET}")

            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "3":
            mostrar_biblioteca()

        elif opcion == "4":
            mostrar_ruta_actual()

        elif opcion == "5":
            gestionar_ruta_descarga()

        elif opcion == "6":
            lanzar_streamlit_desde_cli()

        elif opcion == "0":
            print(f"\n{VERDE}Saliendo del descargador. ¡Hasta pronto!{RESET}\n")
            sys.exit(0)


def run_streamlit_ui():
    import streamlit as st

    st.set_page_config(
        page_title="Descargador de YouTube & Reproductor",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #FF0000;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #666;
            margin-bottom: 1.5rem;
        }
        .card-descarga {
            background-color: #FAFAFA;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="main-header">🎬 Descargador de YouTube & Reproductor Multimedia</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Descarga videos y pistas de audio en múltiples formatos, gestiona tus rutas y reproduce tu biblioteca local.</div>', unsafe_allow_html=True)

    tab_descarga, tab_biblioteca, tab_rutas = st.tabs([
        "📥 Nueva Descarga",
        "🎬 Biblioteca & Reproductor",
        "⚙️ Configuración de Rutas",
    ])

    ruta_act = obtener_ruta_descargas()
    ruta_def = obtener_ruta_predeterminada()

    with tab_descarga:
        st.subheader("Descargar Video o Audio")
        st.info(f"📁 **Ruta de guardado activa:** `{ruta_act}`")

        with st.form("form_descarga"):
            url_in = st.text_input("Enlace del video o playlist de YouTube:", placeholder="https://www.youtube.com/watch?v=...")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                tipo_modo = st.radio("Tipo de contenido:", ["Video / Pista Individual", "Playlist Completa"])
            with col_m2:
                opciones_formato_keys = list(FORMATOS_DISPONIBLES.keys())
                opciones_formato_labels = [FORMATOS_DISPONIBLES[k]["nombre"] for k in opciones_formato_keys]
                formato_label_sel = st.selectbox("Formato y Calidad deseada:", opciones_formato_labels)
                clave_sel = opciones_formato_keys[opciones_formato_labels.index(formato_label_sel)]

            btn_descargar = st.form_submit_button("🚀 Iniciar Descarga")

        if btn_descargar:
            if not url_in.strip():
                st.error("Por favor, ingrese un enlace válido de YouTube.")
            else:
                es_play = (tipo_modo == "Playlist Completa")
                with st.spinner("Descargando y convirtiendo medios..."):
                    exito, msg = descargar_contenido(url_in.strip(), clave_formato=clave_sel, es_playlist=es_play)
                if exito:
                    st.success(f"🎉 ¡Descarga completada con éxito en: `{ruta_act}`!")
                else:
                    st.error(f"❌ Ocurrió un error: {msg}")

    with tab_biblioteca:
        st.subheader("Archivos Descargados")
        archivos = listar_archivos_descargados(ruta_act)

        col_b1, col_b2 = st.columns([3, 1])
        with col_b1:
            st.write(f"Mostrando **{len(archivos)}** archivos disponibles en `{ruta_act}`")
        with col_b2:
            if st.button("🔄 Actualizar Lista"):
                st.rerun()

        if not archivos:
            st.warning("Aún no hay archivos descargados en la carpeta activa.")
        else:
            filtro_tipo = st.selectbox("Filtrar por tipo de medio:", ["Todos", "Solo Videos (MP4, WebM)", "Solo Audio (MP3, M4A, WAV)"])
            for arc in archivos:
                if filtro_tipo == "Solo Videos (MP4, WebM)" and not arc["es_video"]:
                    continue
                if filtro_tipo == "Solo Audio (MP3, M4A, WAV)" and arc["es_video"]:
                    continue

                icono_tipo = "🎥" if arc["es_video"] else "🎵"
                with st.expander(f"{icono_tipo} {arc['nombre']} ({arc['tamano_str']}) - {arc['fecha']}"):
                    st.write(f"**Ubicación completa:** `{arc['ruta']}`")
                    st.write(f"**Formato:** `{arc['extension']}` | **Tamaño:** `{arc['tamano_str']}`")

                    if arc["es_video"]:
                        try:
                            st.video(arc["ruta"])
                        except Exception as e:
                            st.warning(f"No se pudo cargar la vista previa directa: {e}")
                    else:
                        try:
                            st.audio(arc["ruta"])
                        except Exception as e:
                            st.warning(f"No se pudo cargar el reproductor de audio: {e}")

                    col_act1, col_act2 = st.columns(2)
                    with col_act1:
                        if st.button("▶ Abrir en reproductor del sistema", key=f"play_{arc['ruta']}"):
                            reproducir_archivo(arc["ruta"])
                    with col_act2:
                        if st.button("🗑️ Eliminar archivo", key=f"del_{arc['ruta']}"):
                            try:
                                os.remove(arc["ruta"])
                                st.success("Archivo eliminado.")
                                st.rerun()
                            except Exception as e:
                                st.error(f"No se pudo eliminar: {e}")

    with tab_rutas:
        st.subheader("Configuración de Rutas de Descarga")
        st.write(f"**Ruta de descarga activa actualmente:**\n`{ruta_act}`")
        st.write(f"**Ruta predeterminada del repositorio:**\n`{ruta_def}`")

        nueva_ruta_in = st.text_input("Definir nueva carpeta de descargas:", value=ruta_act)
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            if st.button("💾 Guardar Nueva Ruta"):
                if nueva_ruta_in.strip():
                    try:
                        os.makedirs(nueva_ruta_in.strip(), exist_ok=True)
                        guardar_ruta_descargas(nueva_ruta_in.strip())
                        st.success("Ruta actualizada exitosamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar ruta: {e}")
        with col_r2:
            if st.button("🔄 Restaurar Ruta Predeterminada"):
                restaurar_ruta_predeterminada()
                st.success("Ruta predeterminada restaurada.")
                st.rerun()
        with col_r3:
            if st.button("📂 Abrir Carpeta en Explorador"):
                abrir_carpeta_en_explorador(ruta_act)


if __name__ == "__main__":
    if is_running_in_streamlit():
        run_streamlit_ui()
    elif len(sys.argv) > 1 and sys.argv[1].lower() in ("web", "--web", "-w"):
        lanzar_streamlit_desde_cli()
    else:
        menu()
