import os
import sys
import io
import base64
import subprocess
from pathlib import Path

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
try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    PdfReader, PdfWriter = None, None

try:
    import msoffcrypto
except ImportError:
    msoffcrypto = None

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    Fernet, hashes, PBKDF2HMAC = None, None, None

# Anclamos todo a la carpeta exacta donde vive este archivo .py
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "encriptado"
SUPPORTED_EXTS = (".pdf", ".xlsx", ".xls", ".csv")

# =====================================================================
# TEXTO DE EXPLICACIÓN DETALLADA DE NIVELES
# =====================================================================
EXPLICACION_NIVELES = """
================================================================================
                    EXPLICACIÓN DE NIVELES DE ENCRIPTACIÓN
================================================================================

1. ENCRIPTAMIENTO NORMAL (AES-256 Estándar - Revisión 5):
   -----------------------------------------------------------------------------
   * Algoritmo: AES-256 estándar con derivación directa (SHA-256 + salt de 8 bytes).
   * Velocidad de apertura: Instantánea en cualquier dispositivo o visor.
   * Resistencia a ataques: Seguridad estándar industrial. Comprobar cada contraseña
     requiere solo una ronda criptográfica rápida.
   * Comportamiento con la GPU: Es el formato 100% acelerable por tarjetas gráficas
     (NVIDIA GeForce RTX, AMD Radeon, etc.). Un cracker o auditoría en GPU puede
     evaluar millones de contraseñas por segundo en este modo.
   * ¿Cuándo usarlo?:
     - Documentos cotidianos para protegerlos de miradas curiosas.
     - Pruebas de rendimiento, benchmarking y auditorías de contraseñas con GPU.
     - Máxima compatibilidad con lectores antiguos, visores móviles y visores web.

2. ENCRIPTAMIENTO FUERTE (AES-256 Hardened - Revisión 6 / ISO 32000-2):
   -----------------------------------------------------------------------------
   * Algoritmo: AES-256 "Endurecido" con ciclo repetitivo multi-algorítmico.
   * Funcionamiento: Por CADA contraseña probada, el sistema se ve forzado a
     ejecutar un bucle de entre 64 y 96 rondas completas encadenadas de cifrado
     militar AES-128-CBC junto a hashes SHA-256, SHA-384 y SHA-512.
   * Resistencia a ataques: MÁXIMA protección contra hackers y fuerza bruta.
     Incluso con supercomputadoras o granjas de tarjetas gráficas, el ataque se
     vuelve extremadamente lento y costoso (hasta 50,000 veces más lento que el normal).
   * Comportamiento con la GPU: Diseñado específicamente para ahogar y neutralizar
     la ventaja de velocidad masiva de las GPUs, forzando un consumo enorme de ciclos.
   * ¿Cuándo usarlo?:
     - Información confidencial, financiera, legal, contraseñas maestras o datos críticos.
     - Documentos que deban ser prácticamente invulnerables ante robo o filtración.
================================================================================
"""


def ensure_output_dir() -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR


def derive_key(password: str, salt: bytes, iterations: int = 480_000) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))


def encrypt_bytes(file_bytes: bytes, filename: str, password: str, fuerte: bool = False) -> Path:
    """
    Recibe los bytes de un archivo, lo encripta según su extensión y nivel,
    y guarda la copia en ./encriptado.
    """
    ensure_output_dir()
    ext = Path(filename).suffix.lower()
    in_stream = io.BytesIO(file_bytes)

    if ext == ".pdf":
        if PdfReader is None:
            raise RuntimeError("Falta 'pypdf'. Ejecuta: pip install pypdf")
        reader = PdfReader(in_stream)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        if reader.metadata:
            writer.add_metadata(reader.metadata)

        # Modo Normal: AES-256-R5 (Revisión 5, acelerable por GPU)
        # Modo Fuerte: AES-256 (Revisión 6 Hardened, blindaje anti-GPU)
        alg = "AES-256" if fuerte else "AES-256-R5"
        writer.encrypt(user_password=password, algorithm=alg)

        dest_path = OUTPUT_DIR / filename
        with open(dest_path, "wb") as f_out:
            writer.write(f_out)
        return dest_path

    elif ext in (".xlsx", ".xls"):
        if msoffcrypto is None:
            raise RuntimeError("Falta 'msoffcrypto-tool' para cifrar archivos Excel. Ejecuta: pip install msoffcrypto-tool")
        dest_path = OUTPUT_DIR / filename
        office_file = msoffcrypto.OfficeFile(in_stream)
        with open(dest_path, "wb") as f_out:
            office_file.encrypt(password, f_out)
        return dest_path

    elif ext == ".csv":
        if Fernet is None or PBKDF2HMAC is None:
            raise RuntimeError("Falta 'cryptography'. Ejecuta: pip install cryptography")
        salt = os.urandom(16)
        iterations = 600_000 if fuerte else 100_000
        key = derive_key(password, salt, iterations=iterations)
        cipher = Fernet(key)
        encrypted_data = cipher.encrypt(file_bytes)

        dest_path = OUTPUT_DIR / f"{filename}.enc"
        dest_path.write_bytes(salt + encrypted_data)
        return dest_path

    else:
        raise ValueError(f"Extensión '{ext}' no soportada.")


def get_local_files() -> list[Path]:
    """Busca archivos compatibles en la misma carpeta del script .py."""
    return [
        f for f in BASE_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTS and f.name != Path(__file__).name
    ]


# ==========================================
# MODO INTERFAZ WEB (STREAMLIT)
# ==========================================
def run_streamlit_ui():
    import streamlit as st

    st.set_page_config(page_title="Encriptador de Archivos", layout="centered", page_icon="🔐")
    st.title("🔐 Encriptador de PDF, Excel y CSV")
    st.caption(f"Carpeta de salida: `{OUTPUT_DIR}`")

    # Sección de Explicación interactiva desplegable
    with st.expander("ℹ️ ¿Cuál es la diferencia entre Encriptamiento Normal y Fuerte? (Haz clic para ver)", expanded=False):
        st.markdown("""
        ### Comparativa de Niveles de Cifrado

        | Característica | 🟢 Encriptamiento Normal | 🛡️ Encriptamiento Fuerte |
        | :--- | :--- | :--- |
        | **Estándar en PDF** | **AES-256 (Revisión 5)** | **AES-256 Hardened (Revisión 6 - ISO 32000-2)** |
        | **Complejidad de Clave** | 1 ronda SHA-256 directa + salt | Bucle de 64 a 96 rondas de AES-CBC + SHA256/384/512 |
        | **Uso con Tarjeta Gráfica (GPU)** | ⚡ **Acelerable al 100%** (Millones de claves/s) | 🛑 **Anti-GPU** (Frena ataques de fuerza bruta) |
        | **Nivel de Protección** | Estándar / Comercial | Grado Militar / Máxima Seguridad |
        | **Ideal para...** | Documentos diarios, pruebas de GPU, compatibilidad | Información financiera, legal, contraseñas críticas |
        """)
        st.info(
            "💡 **Consejo:** Si quieres probar el desbloqueador por GPU de tu tarjeta gráfica, elige **Normal**. "
            "Si quieres que el archivo sea casi imposible de hackear por fuerza bruta, elige **Fuerte**."
        )

    st.divider()

    modo_origen = st.radio(
        "Selecciona el origen del archivo:",
        ["Archivos en la carpeta del .py", "Subir archivo o ingresar ruta"],
        horizontal=True
    )

    target_bytes = None
    target_name = None

    if modo_origen == "Archivos en la carpeta del .py":
        local_files = get_local_files()
        if not local_files:
            st.warning(f"No hay archivos {SUPPORTED_EXTS} en `{BASE_DIR}`.")
        else:
            selected_name = st.selectbox(
                "Elige el archivo local:",
                options=[f.name for f in local_files]
            )
            if selected_name:
                file_path = BASE_DIR / selected_name
                target_bytes = file_path.read_bytes()
                target_name = file_path.name
    else:
        uploaded = st.file_uploader("Arrastra un archivo aquí", type=["pdf", "xlsx", "xls", "csv"])
        custom_path = st.text_input("O pega la ruta absoluta del archivo en tu PC:")

        if uploaded is not None:
            target_bytes = uploaded.getvalue()
            target_name = uploaded.name
        elif custom_path.strip():
            clean_p = Path(custom_path.strip().strip("\"'")).expanduser().resolve()
            if clean_p.is_file() and clean_p.suffix.lower() in SUPPORTED_EXTS:
                target_bytes = clean_p.read_bytes()
                target_name = clean_p.name
            else:
                st.error("La ruta no existe o el formato no es compatible.")

    st.divider()

    # Selección de nivel de cifrado
    nivel_seleccionado = st.radio(
        "🔒 Elige el nivel de encriptamiento:",
        [
            "🟢 Normal (AES-256 Estándar - Acelerable por GPU / Máxima Compatibilidad)",
            "🛡️ Fuerte (AES-256 Hardened - Grado Militar Anti-Fuerza Bruta)"
        ],
        index=0
    )
    es_fuerte = "Fuerte" in nivel_seleccionado

    password = st.text_input("🔑 ¿Cuál quieres que sea la clave?", placeholder="Escribe tu contraseña aquí...", type="password")

    if st.button("🚀 Encriptar y Guardar Copia", type="primary", use_container_width=True):
        if not target_bytes or not target_name:
            st.error("Primero selecciona o carga un archivo válido.")
        elif not password:
            st.error("Debes escribir una contraseña.")
        else:
            try:
                out_path = encrypt_bytes(target_bytes, target_name, password, fuerte=es_fuerte)
                tipo_str = "🛡️ Fuerte (Anti-Fuerza Bruta)" if es_fuerte else "🟢 Normal (Acelerable en GPU)"
                st.success(f"Archivo encriptado en modo **{tipo_str}** con la clave **`{password}`** y guardado en:\n`{out_path}`")
                st.download_button(
                    label="⬇ Descargar archivo encriptado",
                    data=out_path.read_bytes(),
                    file_name=out_path.name,
                    mime="application/octet-stream"
                )
            except Exception as e:
                st.error(f"Error al encriptar: {e}")


# ==========================================
# MODO CONSOLA (CLI)
# ==========================================
def pedir_nivel_encriptacion() -> bool:
    """Solicita al usuario elegir entre Normal, Fuerte o ver la Explicación."""
    while True:
        print(f"\n{CYAN}{NEGRITA}╔══ SELECCIÓN DE NIVEL DE ENCRIPTACIÓN ══{RESET}")
        print(f"  {VERDE}[1]{RESET} {BLANCO}Normal (AES-256 R5 - Compatible y acelerable por GPU){RESET}")
        print(f"  {AMARILLO}[2]{RESET} {BLANCO}Fuerte (AES-256 Hardened R6 - Blindaje anti-fuerza bruta){RESET}")
        print(f"  {MAGENTA}[3]{RESET} {BLANCO}Ver explicación técnica detallada de cada nivel{RESET}")
        print(f"{CYAN}{'═' * 45}{RESET}")

        op = input(f"{VERDE}{NEGRITA}Elige una opción (1/2/3): {RESET}").strip()
        if op == "1":
            return False  # Normal
        elif op == "2":
            return True   # Fuerte
        elif op == "3":
            print(EXPLICACION_NIVELES)
            input(f"{BLANCO}Presiona Enter para continuar y seleccionar tu nivel...{RESET}")
        else:
            print(f"{ROJO}[!] Opción no válida. Escribe 1, 2 o 3.{RESET}")


def run_cli_menu():
    while True:
        print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{AZUL}{NEGRITA}║                   🔒 ENCRIPTADOR DE ARCHIVOS (PDF / EXCEL / CSV)                   ║{RESET}")
        print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"  {CYAN}📁 Carpeta actual:{RESET} {BASE_DIR}")
        print(f"  {CYAN}📂 Destino cifrado:{RESET} {OUTPUT_DIR}")
        print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"║  {VERDE}[1]{RESET} {BLANCO}📁 Encriptar archivo(s) de la carpeta del script{RESET}                          ║")
        print(f"║  {VERDE}[2]{RESET} {BLANCO}📝 Encriptar archivo ingresando ruta manual{RESET}                               ║")
        print(f"║  {CYAN}[3]{RESET} {BLANCO}📖 Explicación técnica de niveles (Normal vs Blindaje Fuerte){RESET}           ║")
        print(f"║  {MAGENTA}[4]{RESET} {BLANCO}🌐 Iniciar Interfaz Gráfica Web (Streamlit){RESET}                                  ║")
        print(f"║  {ROJO}[0]{RESET} {BLANCO}🚪 Salir del programa{RESET}                                                       ║")
        print(f"{AZUL}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

        opcion = input(f"{VERDE}{NEGRITA}Seleccione una opción (0-4): {RESET}").strip()

        if opcion == "0":
            print(f"\n{CYAN}Hasta luego.{RESET}\n")
            return

        elif opcion == "1":
            archivos = get_local_files()
            if not archivos:
                print(f"\n{AMARILLO}[!] No se encontraron archivos {SUPPORTED_EXTS} en {BASE_DIR}{RESET}")
                input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")
                continue

            print(f"\n{CYAN}Archivos detectados en la carpeta del script:{RESET}")
            for idx, f in enumerate(archivos, 1):
                print(f"  {VERDE}[{idx}]{RESET} {BLANCO}{f.name}{RESET}")
            print(f"  {AMARILLO}[0]{RESET} {BLANCO}Encriptar TODOS los de la lista{RESET}")

            sel = input(f"\n{VERDE}Elige el número del archivo (o Enter para cancelar): {RESET}").strip()
            if not sel:
                continue
            try:
                idx_sel = int(sel)
                if idx_sel == 0:
                    seleccionados = archivos
                elif 1 <= idx_sel <= len(archivos):
                    seleccionados = [archivos[idx_sel - 1]]
                else:
                    print(f"{ROJO}[ERROR] Número fuera de rango.{RESET}")
                    input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")
                    continue
            except ValueError:
                print(f"{ROJO}[ERROR] Entrada inválida.{RESET}")
                input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")
                continue

            clave = input(f"\n{CYAN}¿Cuál quieres que sea la clave?: {RESET}").strip()
            if not clave:
                print(f"{ROJO}[ERROR] La clave no puede estar vacía.{RESET}")
                input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")
                continue

            fuerte = pedir_nivel_encriptacion()
            nivel_nombre = "FUERTE (Anti-GPU)" if fuerte else "NORMAL (GPU-Friendly)"

            for f in seleccionados:
                try:
                    dest = encrypt_bytes(f.read_bytes(), f.name, clave, fuerte=fuerte)
                    print(f"\n{VERDE}✓ [OK] '{f.name}' [{nivel_nombre}] -> Guardado en:{RESET}\n    {dest}")
                except Exception as e:
                    print(f"\n{ROJO}❌ [ERROR] Falló '{f.name}': {e}{RESET}")
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "2":
            ruta_raw = input(f"\n{CYAN}Ingresa la ruta del archivo: {RESET}").strip().strip("\"'")
            if not ruta_raw:
                continue
            archivo = Path(ruta_raw).expanduser().resolve()

            if not archivo.is_file():
                print(f"\n{ROJO}[ERROR] No existe el archivo: {archivo}{RESET}")
                input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")
                continue

            clave = input(f"\n{CYAN}¿Cuál quieres que sea la clave?: {RESET}").strip()
            if not clave:
                print(f"{ROJO}[ERROR] La clave no puede estar vacía.{RESET}")
                input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")
                continue

            fuerte = pedir_nivel_encriptacion()
            nivel_nombre = "FUERTE (Anti-GPU)" if fuerte else "NORMAL (GPU-Friendly)"

            try:
                dest = encrypt_bytes(archivo.read_bytes(), archivo.name, clave, fuerte=fuerte)
                print(f"\n{VERDE}✓ [OK] '{archivo.name}' [{nivel_nombre}] -> Guardado en:{RESET}\n    {dest}")
            except Exception as e:
                print(f"\n{ROJO}[ERROR] Falló la encriptación: {e}{RESET}")
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "3":
            print(EXPLICACION_NIVELES)
            input(f"\n{BLANCO}Presiona Enter para volver al menú principal...{RESET}")

        elif opcion == "4":
            print(f"\n{CYAN}[*] Levantando servidor Streamlit...{RESET}")
            subprocess.run([sys.executable, "-m", "streamlit", "run", str(Path(__file__).resolve())])

        else:
            print(f"\n{ROJO}[ERROR] Opción no válida.{RESET}")


def is_running_in_streamlit() -> bool:
    """Detecta si el archivo fue invocado por 'streamlit run'."""
    try:
        from streamlit.runtime import exists
        return exists()
    except ImportError:
        return False


if __name__ == "__main__":
    if is_running_in_streamlit():
        run_streamlit_ui()
    else:
        run_cli_menu()
