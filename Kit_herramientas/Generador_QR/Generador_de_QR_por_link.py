import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

try:
    import qrcode
except ImportError:
    qrcode = None

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

CARPETA_QR = Path(__file__).resolve().parent

TEMAS_COLOR = {
    "1": ("Clásico (Negro / Blanco)", "#000000", "#FFFFFF"),
    "2": ("Ámbar Dorado (#FFA300 / Blanco)", "#FFA300", "#FFFFFF"),
    "3": ("Azul Tecnológico (#0D47A1 / Blanco)", "#0D47A1", "#FFFFFF"),
    "4": ("Verde Matrix / Hacker (#00FF66 / Negro)", "#00FF66", "#111111"),
    "5": ("Púrpura Neón (#8E24AA / Blanco)", "#8E24AA", "#FFFFFF"),
}


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


def generar_qr(url: str, fill_color: str = "#000000", back_color: str = "#FFFFFF", nombre_archivo: str = ""):
    if qrcode is None:
        print(f"\n{ROJO}❌ Error: La librería 'qrcode' no está instalada. Ejecute: pip install qrcode pillow{RESET}")
        return None

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=12,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color=fill_color, back_color=back_color)

        if not nombre_archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"qr_{timestamp}.png"
        elif not nombre_archivo.lower().endswith(".png"):
            nombre_archivo += ".png"

        ruta_destino = CARPETA_QR / nombre_archivo
        img.save(str(ruta_destino))

        print(f"\n{VERDE}{NEGRITA}✓ [ÉXITO] Código QR generado y guardado correctamente:{RESET}")
        print(f"  {CYAN}📁 Ruta:{RESET} {ruta_destino}")
        print(f"  {AMARILLO}🎨 Colores:{RESET} {fill_color} sobre {back_color}")

        abrir = input(f"\n{BLANCO}¿Desea abrir y previsualizar la imagen generada? (S/n): {RESET}").strip().lower()
        if abrir not in ("n", "no"):
            abrir_archivo_o_carpeta(ruta_destino)

        return ruta_destino
    except Exception as e:
        print(f"\n{ROJO}❌ Error al generar el código QR: {e}{RESET}")
        return None


def main():
    while True:
        print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{AZUL}{NEGRITA}║                   📱 GENERADOR PROFESIONAL DE CÓDIGOS QR                           ║{RESET}")
        print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"  {CYAN}📁 Carpeta de guardado:{RESET} {CARPETA_QR}")
        print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"║  {VERDE}[1]{RESET} {BLANCO}⚡ Generar código QR estándar (Negro sobre Blanco){RESET}                     ║")
        print(f"║  {VERDE}[2]{RESET} {BLANCO}🎨 Generar código QR estilizado (Elegir paleta de color){RESET}                ║")
        print(f"║  {CYAN}[3]{RESET} {BLANCO}📂 Abrir carpeta de códigos QR en el Explorador{RESET}                         ║")
        print(f"║  {ROJO}[0]{RESET} {BLANCO}🚪 Salir del programa{RESET}                                                 ║")
        print(f"{AZUL}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

        opcion = input(f"{VERDE}{NEGRITA}Seleccione una opción (0-3): {RESET}").strip()

        if opcion == "1":
            link = input(f"\n{CYAN}Ingrese la URL o texto a codificar en el QR: {RESET}").strip()
            if not link:
                print(f"{ROJO}❌ Debe ingresar un enlace o texto válido.{RESET}")
                continue
            nombre = input(f"{AMARILLO}Nombre de archivo (Enter para automático): {RESET}").strip()
            generar_qr(link, "#000000", "#FFFFFF", nombre)
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "2":
            link = input(f"\n{CYAN}Ingrese la URL o texto a codificar en el QR: {RESET}").strip()
            if not link:
                print(f"{ROJO}❌ Debe ingresar un enlace o texto válido.{RESET}")
                continue

            print(f"\n{CYAN}Paletas de color disponibles:{RESET}")
            for k, (nom, _, _) in TEMAS_COLOR.items():
                print(f"  {VERDE}[{k}]{RESET} {BLANCO}{nom}{RESET}")
            print(f"  {MAGENTA}[6]{RESET} {BLANCO}Personalizado (Escribir códigos Hexadecimales){RESET}")

            sel_col = input(f"\n{VERDE}Seleccione paleta de color (1-6): {RESET}").strip()
            if sel_col in TEMAS_COLOR:
                _, fc, bc = TEMAS_COLOR[sel_col]
            elif sel_col == "6":
                fc = input(f"{CYAN}Código Hex del QR (ej. #FF5722): {RESET}").strip() or "#000000"
                bc = input(f"{CYAN}Código Hex del Fondo (ej. #FFFFFF): {RESET}").strip() or "#FFFFFF"
            else:
                fc, bc = "#000000", "#FFFFFF"

            nombre = input(f"{AMARILLO}Nombre de archivo (Enter para automático): {RESET}").strip()
            generar_qr(link, fc, bc, nombre)
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "3":
            abrir_archivo_o_carpeta(CARPETA_QR)

        elif opcion in ("0", "q", "exit", "salir"):
            print(f"\n{CYAN}Saliendo del generador de QR. ¡Hasta luego!{RESET}\n")
            break
        else:
            print(f"\n{ROJO}[!] Opción inválida. Intente de nuevo.{RESET}")


if __name__ == "__main__":
    main()
