import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

try:
    from gtts import gTTS, gTTSError
except ImportError:
    gTTS, gTTSError = None, None

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

CARPETA_AUDIOS = Path(__file__).resolve().parent

IDIOMAS = {
    "1": ("Español (Estándar / Latam)", "es"),
    "2": ("Español (España)", "es"),
    "3": ("Inglés (Estados Unidos)", "en"),
    "4": ("Inglés (Reino Unido)", "en"),
    "5": ("Francés", "fr"),
    "6": ("Portugués", "pt"),
    "7": ("Italiano", "it"),
    "8": ("Alemán", "de"),
    "9": ("Japonés", "ja"),
}


def reproducir_audio(ruta: Path):
    try:
        if os.name == "nt":
            os.startfile(str(ruta))
        elif sys.platform == "darwin":
            subprocess.run(["afplay", str(ruta)], check=False)
        else:
            subprocess.run(["xdg-open", str(ruta)], check=False)
    except Exception as e:
        print(f"  {AMARILLO}[!] No se pudo iniciar el reproductor automático: {e}{RESET}")


def abrir_carpeta(ruta: Path):
    try:
        if os.name == "nt":
            os.startfile(str(ruta))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(ruta)], check=False)
        else:
            subprocess.run(["xdg-open", str(ruta)], check=False)
    except Exception:
        pass


def generar_audio(texto: str, lang: str = "es", slow: bool = False, nombre_personalizado: str = ""):
    if gTTS is None:
        print(f"\n{ROJO}❌ Error: La librería 'gTTS' no está instalada. Ejecute: pip install gTTS{RESET}")
        return None

    if not texto.strip():
        print(f"\n{AMARILLO}❌ El texto a sintetizar no puede estar vacío.{RESET}")
        return None

    if not nombre_personalizado:
        nombre = f"audio_{datetime.now():%Y%m%d_%H%M%S}.mp3"
    else:
        nombre = nombre_personalizado if nombre_personalizado.lower().endswith(".mp3") else f"{nombre_personalizado}.mp3"

    archivo = CARPETA_AUDIOS / nombre

    try:
        print(f"\n{CYAN}[*] Conectando con el motor de voz y sintetizando audio...{RESET}")
        audio = gTTS(text=texto, lang=lang, slow=slow)
        audio.save(str(archivo))

        tam_kb = round(archivo.stat().st_size / 1024, 1)
        print(f"{AZUL}{'─' * 70}{RESET}")
        print(f"{VERDE}{NEGRITA}✓ [ÉXITO] Audio generado y guardado correctamente:{RESET}")
        print(f"  {CYAN}📄 Archivo  :{RESET} {archivo.name}")
        print(f"  {CYAN}📁 Carpeta  :{RESET} {archivo.parent}")
        print(f"  {AMARILLO}🌐 Idioma   :{RESET} {lang}")
        print(f"  {AMARILLO}📦 Tamaño   :{RESET} {tam_kb} KB")
        print(f"{AZUL}{'─' * 70}{RESET}")

        reproducir = input(f"\n{BLANCO}¿Desea reproducir el audio ahora? (S/n): {RESET}").strip().lower()
        if reproducir not in ("n", "no"):
            reproducir_audio(archivo)

        return archivo
    except Exception as error:
        print(f"\n{ROJO}❌ No se pudo generar el audio: {error}{RESET}")
        return None


def main():
    lang_actual = "es"
    nombre_lang_actual = "Español"

    while True:
        print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{AZUL}{NEGRITA}║                   🎙️ GENERADOR DE AUDIO Y VOZ POR TEXTO (TTS)                      ║{RESET}")
        print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"  {CYAN}🌐 Idioma activo:{RESET} {VERDE}{nombre_lang_actual} ({lang_actual}){RESET} | {CYAN}📁 Guardando en:{RESET} {CARPETA_AUDIOS}")
        print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"║  {VERDE}[1]{RESET} {BLANCO}✍️  Escribir texto y sintetizar a voz en MP3{RESET}                               ║")
        print(f"║  {CYAN}[2]{RESET} {BLANCO}📄 Leer archivo de texto (.txt) y convertir a voz en MP3{RESET}                   ║")
        print(f"║  {MAGENTA}[3]{RESET} {BLANCO}🌐 Cambiar idioma o dialecto de la voz{RESET}                                    ║")
        print(f"║  {AMARILLO}[4]{RESET} {BLANCO}📂 Abrir carpeta de audios en el Explorador{RESET}                             ║")
        print(f"║  {ROJO}[0]{RESET} {BLANCO}🚪 Salir del programa{RESET}                                                 ║")
        print(f"{AZUL}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

        opcion = input(f"{VERDE}{NEGRITA}Seleccione una opción (0-4): {RESET}").strip()

        if opcion == "1":
            texto = input(f"\n{CYAN}Escriba el texto que desea convertir a voz:{RESET}\n👉 ").strip()
            if not texto:
                print(f"{ROJO}❌ No se ingresó ningún texto.{RESET}")
                continue
            nombre = input(f"\n{AMARILLO}Nombre para el archivo MP3 (Enter para automático): {RESET}").strip()
            generar_audio(texto, lang=lang_actual, slow=False, nombre_personalizado=nombre)
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "2":
            ruta_txt = input(f"\n{CYAN}Ingrese la ruta del archivo de texto (.txt): {RESET}").strip().strip('"').strip("'")
            p_txt = Path(ruta_txt).expanduser().resolve()
            if not p_txt.is_file():
                print(f"{ROJO}❌ No se encontró el archivo: {p_txt}{RESET}")
                input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")
                continue

            try:
                contenido = p_txt.read_text(encoding="utf-8").strip()
            except UnicodeDecodeError:
                contenido = p_txt.read_text(encoding="latin-1", errors="ignore").strip()

            print(f"\n{CYAN}Contenido leído ({len(contenido)} caracteres). Iniciando síntesis...{RESET}")
            generar_audio(contenido, lang=lang_actual, slow=False, nombre_personalizado=f"voz_{p_txt.stem}")
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "3":
            print(f"\n{CYAN}Idiomas disponibles:{RESET}")
            for k, (n, code) in IDIOMAS.items():
                print(f"  {VERDE}[{k}]{RESET} {BLANCO}{n} ({code}){RESET}")
            sub = input(f"\n{VERDE}Seleccione un idioma (1-{len(IDIOMAS)}): {RESET}").strip()
            if sub in IDIOMAS:
                nombre_lang_actual, lang_actual = IDIOMAS[sub]
                print(f"\n{VERDE}✓ Idioma cambiado a: {nombre_lang_actual} ({lang_actual}){RESET}")
            else:
                print(f"\n{ROJO}Opción no reconocida.{RESET}")
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "4":
            abrir_carpeta(CARPETA_AUDIOS)

        elif opcion in ("0", "q", "exit", "salir"):
            print(f"\n{CYAN}Saliendo del sintetizador de voz. ¡Hasta luego!{RESET}\n")
            break
        else:
            print(f"\n{ROJO}[!] Opción no válida. Intente de nuevo.{RESET}")


if __name__ == "__main__":
    main()
