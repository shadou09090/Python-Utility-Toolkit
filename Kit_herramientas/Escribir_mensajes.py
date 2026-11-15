import os
import sys
import time
import ctypes
from ctypes import wintypes

try:
    import keyboard
except ImportError:
    keyboard = None

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

user32 = ctypes.WinDLL("user32", use_last_error=True)

INPUT_KEYBOARD = 1
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_KEYUP = 0x0002
VK_RETURN = 0x0D


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.c_ulonglong),
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [("ki", KEYBDINPUT), ("padding", ctypes.c_byte * 32)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("u", INPUT_UNION)]


def construir_lote_memoria_c(texto_bloque):
    eventos = []
    for char in texto_bloque:
        if char == "\n":
            eventos.append(
                INPUT(
                    type=INPUT_KEYBOARD,
                    u=INPUT_UNION(
                        ki=KEYBDINPUT(
                            wVk=VK_RETURN,
                            wScan=0,
                            dwFlags=0,
                            time=0,
                            dwExtraInfo=0,
                        )
                    ),
                )
            )
            eventos.append(
                INPUT(
                    type=INPUT_KEYBOARD,
                    u=INPUT_UNION(
                        ki=KEYBDINPUT(
                            wVk=VK_RETURN,
                            wScan=0,
                            dwFlags=KEYEVENTF_KEYUP,
                            time=0,
                            dwExtraInfo=0,
                        )
                    ),
                )
            )
        else:
            code = ord(char)
            eventos.append(
                INPUT(
                    type=INPUT_KEYBOARD,
                    u=INPUT_UNION(
                        ki=KEYBDINPUT(
                            wVk=0,
                            wScan=code,
                            dwFlags=KEYEVENTF_UNICODE,
                            time=0,
                            dwExtraInfo=0,
                        )
                    ),
                )
            )
            eventos.append(
                INPUT(
                    type=INPUT_KEYBOARD,
                    u=INPUT_UNION(
                        ki=KEYBDINPUT(
                            wVk=0,
                            wScan=code,
                            dwFlags=KEYEVENTF_UNICODE | KEYEVENTF_KEYUP,
                            time=0,
                            dwExtraInfo=0,
                        )
                    ),
                )
            )

    ArrayType = INPUT * len(eventos)
    return ArrayType(*eventos), len(eventos)


def iniciar_escritura():
    CANTIDAD_MAXIMA = 100000

    print(f"\n{CYAN}{NEGRITA}╔══ CONFIGURACIÓN DE LA RÁFAGA DE TECLAS ══{RESET}")
    frase = input(f"  {CYAN}¿Qué frase deseas escribir?: {RESET}").strip()
    if not frase:
        frase = "prueba de escritura"
        print(f"  {AMARILLO}→ Usando frase predeterminada: '{frase}'{RESET}")

    cantidad_str = input(f"  {CYAN}¿Cuántas veces repetirla? (Enter para 50, máx {CANTIDAD_MAXIMA}): {RESET}").strip()
    try:
        total_lineas = int(cantidad_str) if cantidad_str else 50
        if total_lineas <= 0 or total_lineas > CANTIDAD_MAXIMA:
            total_lineas = 50
    except ValueError:
        total_lineas = 50

    tiempo_str = input(f"  {CYAN}¿Segundos de espera para posicionar el cursor? (Enter para 5s): {RESET}").strip()
    try:
        tiempo_espera = float(tiempo_str) if tiempo_str else 5.0
    except ValueError:
        tiempo_espera = 5.0

    resp_num = input(f"  {CYAN}¿Añadir números consecutivos antes de la frase? (s/N): {RESET}").strip().lower()
    incluir_numeros = resp_num in ("s", "si", "sí", "y", "yes")

    tamano_rafaga = 100
    print(f"\n{AMARILLO}[*] Pre-compilando {total_lineas:,} eventos en estructuras de memoria C Win32...{RESET}")

    lotes_preparados = []
    for inicio_lote in range(1, total_lineas + 1, tamano_rafaga):
        fin_lote = min(inicio_lote + tamano_rafaga, total_lineas + 1)
        if incluir_numeros:
            texto_rafaga = "".join(f"{i} {frase}\n" for i in range(inicio_lote, fin_lote))
        else:
            texto_rafaga = "".join(f"{frase}\n" for _ in range(inicio_lote, fin_lote))
        arreglo_c, num_eventos = construir_lote_memoria_c(texto_rafaga)
        lotes_preparados.append((arreglo_c, num_eventos))

    print(f"{VERDE}✓ Memoria C reservada exitosamente.{RESET}")
    print(f"\n{ROJO}{NEGRITA}⚠️  ATENCIÓN:{RESET}")
    print(f"  {BLANCO}Coloca el cursor en la ventana o campo de texto objetivo.{RESET}")
    print(f"  {BLANCO}La inyección iniciará automáticamente en {tiempo_espera} segundos.{RESET}")
    print(f"  {AMARILLO}Puedes presionar 'ESC' en cualquier momento para abortar la ráfaga.{RESET}")

    # Cuenta regresiva
    segundos_int = int(tiempo_espera)
    for seg in range(segundos_int, 0, -1):
        print(f"  ⏱️  Iniciando en {seg}... ", end="\r", flush=True)
        time.sleep(1)
    if tiempo_espera > segundos_int:
        time.sleep(tiempo_espera - segundos_int)

    print(f"\n{VERDE}{NEGRITA}🚀 ¡INICIANDO INYECCIÓN A TRAVÉS DE WIN32 SendInput!{RESET}")

    t0 = time.perf_counter()
    tamano_struct = ctypes.sizeof(INPUT)
    abortado = False

    for idx, (arreglo_c, num_eventos) in enumerate(lotes_preparados):
        if keyboard is not None and keyboard.is_pressed("esc"):
            print(f"\n{AMARILLO}[!] Inyección cancelada por el usuario con tecla ESC en el lote {idx + 1}.{RESET}")
            abortado = True
            break
        user32.SendInput(num_eventos, ctypes.byref(arreglo_c), tamano_struct)

    t1 = time.perf_counter()
    ms_total = (t1 - t0) * 1000

    print(f"{AZUL}{'─' * 70}{RESET}")
    if not abortado:
        print(f"{VERDE}{NEGRITA}✓ Inyección completada exitosamente al subsistema de ventanas Win32.{RESET}")
    print(f"  {CYAN}📊 Líneas enviadas :{RESET} {total_lineas:,}")
    print(f"  {CYAN}⏱️  Tiempo de kernel:{RESET} {ms_total:.2f} milisegundos ({ms_total / 1000:.4f} s)")
    print(f"{AZUL}{'─' * 70}{RESET}")


def mostrar_info_tecnica():
    print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{AZUL}{NEGRITA}║                   ℹ️ INFORMACIÓN TÉCNICA - MOTOR SENDINPUT C                       ║{RESET}")
    print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"""
  {BLANCO}{NEGRITA}¿Cómo funciona este inyector?{RESET}
  A diferencia de bibliotecas de simulación de teclado tradicionales como pyautogui
  que añaden retardos intencionales de 10 a 50 milisegundos por pulsación, este script:

  {CYAN}1.{RESET} {BLANCO}Pre-compila toda la ráfaga de texto directamente en estructuras nativas de
     memoria de Windows ({CYAN}ctypes.Structure KEYBDINPUT / INPUT{RESET}).{RESET}
  {CYAN}2.{RESET} {BLANCO}Entrega los lotes en masa llamando a la API de bajo nivel {CYAN}user32.SendInput{RESET}.{RESET}
  {CYAN}3.{RESET} {BLANCO}Permite velocidades de hasta decenas de miles de caracteres por segundo,
     siendo ideal para benchmarks de entrada, pruebas de carga de interfaces o
     automatización ultrarrápida.{RESET}
  {CYAN}4.{RESET} {BLANCO}Monitoreo por interrupción de teclado global ({CYAN}ESC{RESET}) para frenar la ráfaga.{RESET}
    """)
    print(f"{AZUL}{'═' * 84}{RESET}")


def main():
    while True:
        print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{AZUL}{NEGRITA}║                   ⌨️ ESCRITOR AUTOMATIZADO DE MENSAJES (AUTO-TYPER C)             ║{RESET}")
        print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"  {CYAN}⚡ Motor:{RESET} Windows user32.dll (SendInput Nativo C) | {CYAN}Freno de emergencia:{RESET} [ESC]")
        print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"║  {VERDE}[1]{RESET} {BLANCO}⚡ Configurar e iniciar ráfaga de escritura ultrarrápida{RESET}                 ║")
        print(f"║  {CYAN}[2]{RESET} {BLANCO}ℹ️  Ver información técnica de arquitectura del inyector C{RESET}               ║")
        print(f"║  {ROJO}[0]{RESET} {BLANCO}🚪 Salir del programa{RESET}                                                 ║")
        print(f"{AZUL}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

        opcion = input(f"{VERDE}{NEGRITA}Seleccione una opción (0-2): {RESET}").strip()

        if opcion == "1":
            iniciar_escritura()
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")
        elif opcion == "2":
            mostrar_info_tecnica()
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")
        elif opcion in ("0", "q", "exit", "salir"):
            print(f"\n{CYAN}Saliendo del auto-typer. ¡Hasta luego!{RESET}\n")
            break
        else:
            print(f"\n{ROJO}[!] Opción no válida. Intente de nuevo.{RESET}")


if __name__ == "__main__":
    main()
