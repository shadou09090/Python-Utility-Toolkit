import os
import sys
import time
import random

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

FILAS = 22
COLUMNAS = 40


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def crear_universo_vacio(filas=FILAS, columnas=COLUMNAS):
    return [[0 for _ in range(columnas)] for _ in range(filas)]


def contar_vecinos(tablero, x, y, filas, columnas):
    vecinos = 0
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if i == 0 and j == 0:
                continue
            ni = (x + i) % filas
            nj = (y + j) % columnas
            vecinos += tablero[ni][nj]
    return vecinos


def siguiente_generacion(tablero, filas, columnas):
    nuevo_tablero = [[0 for _ in range(columnas)] for _ in range(filas)]
    for i in range(filas):
        for j in range(columnas):
            vecinos = contar_vecinos(tablero, i, j, filas, columnas)
            if tablero[i][j] == 1 and (vecinos == 2 or vecinos == 3):
                nuevo_tablero[i][j] = 1
            elif tablero[i][j] == 0 and vecinos == 3:
                nuevo_tablero[i][j] = 1
    return nuevo_tablero


def imprimir_tablero(tablero, generacion, filas, columnas, celda_color=VERDE):
    limpiar_pantalla()
    vivas = sum(sum(fila) for fila in tablero)
    densidad = (vivas / (filas * columnas)) * 100

    print(f"{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{AZUL}{NEGRITA}║                   🧬 SIMULADOR DEL JUEGO DE LA VIDA DE CONWAY                      ║{RESET}")
    print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print(
        f"  {CYAN}Generación:{RESET} {BLANCO}{generacion:<6}{RESET} | "
        f"{CYAN}Células vivas:{RESET} {VERDE}{vivas:<5}{RESET} | "
        f"{CYAN}Densidad:{RESET} {AMARILLO}{densidad:.1f}%{RESET} | "
        f"{MAGENTA}[Ctrl+C para pausar/salir]{RESET}"
    )

    ancho_borde = columnas * 2
    print(f"  {AZUL}┌{'─' * ancho_borde}┐{RESET}")
    for fila in tablero:
        linea_str = "".join([f"{celda_color}██{RESET}" if celda else "  " for celda in fila])
        print(f"  {AZUL}│{RESET}{linea_str}{AZUL}│{RESET}")
    print(f"  {AZUL}└{'─' * ancho_borde}┘{RESET}")


def ejecutar_simulacion(universo_inicial, celda_color=VERDE, delay=0.12):
    universo = [fila[:] for fila in universo_inicial]
    generacion = 0
    try:
        while True:
            imprimir_tablero(universo, generacion, FILAS, COLUMNAS, celda_color=celda_color)
            universo = siguiente_generacion(universo, FILAS, COLUMNAS)
            generacion += 1
            time.sleep(delay)
    except KeyboardInterrupt:
        print(f"\n{AMARILLO}[*] Simulación pausada en la generación {generacion}.{RESET}")
        time.sleep(1)


def patron_aleatorio():
    return [[random.choice([0, 1]) if random.random() < 0.28 else 0 for _ in range(COLUMNAS)] for _ in range(FILAS)]


def patron_glider():
    u = crear_universo_vacio()
    glider_coords = [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
    for r, c in glider_coords:
        if r < FILAS and c < COLUMNAS:
            u[r][c] = 1
    return u


def patron_pulsar():
    u = crear_universo_vacio()
    mid_r = FILAS // 2
    mid_c = COLUMNAS // 2
    offsets = [
        (-6, -4), (-6, -3), (-6, -2), (-6, 2), (-6, 3), (-6, 4),
        (-1, -4), (-1, -3), (-1, -2), (-1, 2), (-1, 3), (-1, 4),
        (1, -4), (1, -3), (1, -2), (1, 2), (1, 3), (1, 4),
        (6, -4), (6, -3), (6, -2), (6, 2), (6, 3), (6, 4),
        (-4, -6), (-3, -6), (-2, -6), (2, -6), (3, -6), (4, -6),
        (-4, -1), (-3, -1), (-2, -1), (2, -1), (3, -1), (4, -1),
        (-4, 1), (-3, 1), (-2, 1), (2, 1), (3, 1), (4, 1),
        (-4, 6), (-3, 6), (-2, 6), (2, 6), (3, 6), (4, 6),
    ]
    for dr, dc in offsets:
        r, c = mid_r + dr, mid_c + dc
        if 0 <= r < FILAS and 0 <= c < COLUMNAS:
            u[r][c] = 1
    return u


def patron_gosper_gun():
    u = crear_universo_vacio()
    gun_coords = [
        (5, 1), (5, 2), (6, 1), (6, 2),
        (5, 11), (6, 11), (7, 11), (4, 12), (8, 12), (3, 13), (9, 13), (3, 14), (9, 14),
        (6, 15), (4, 16), (8, 16), (5, 17), (6, 17), (7, 17), (6, 18),
        (3, 21), (4, 21), (5, 21), (3, 22), (4, 22), (5, 22), (2, 23), (6, 23),
        (1, 25), (2, 25), (6, 25), (7, 25),
        (3, 35), (4, 35), (3, 36), (4, 36)
    ]
    for r, c in gun_coords:
        if r < FILAS and c < COLUMNAS:
            u[r][c] = 1
    return u


def main():
    while True:
        limpiar_pantalla()
        print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{AZUL}{NEGRITA}║                   🧬 SIMULADOR DEL JUEGO DE LA VIDA DE CONWAY                      ║{RESET}")
        print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"  {CYAN}Matriz universal:{RESET} {FILAS} Filas x {COLUMNAS} Columnas (Toroidal)")
        print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"║  {VERDE}[1]{RESET} {BLANCO}🎲 Sopa primordial aleatoria (Caos y auto-organización){RESET}                 ║")
        print(f"║  {CYAN}[2]{RESET} {BLANCO}🚀 Planeador / Glider (Nave espacial autónoma en movimiento){RESET}           ║")
        print(f"║  {MAGENTA}[3]{RESET} {BLANCO}🌟 Oscilador Pulsar (Estructura periódica de 3 fases){RESET}                   ║")
        print(f"║  {AMARILLO}[4]{RESET} {BLANCO}💥 Cañón de planeadores de Gosper (Fábrica infinita de naves){RESET}           ║")
        print(f"║  {ROJO}[0]{RESET} {BLANCO}🚪 Salir del programa{RESET}                                                 ║")
        print(f"{AZUL}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

        opcion = input(f"{VERDE}{NEGRITA}Seleccione un patrón para iniciar (0-4): {RESET}").strip()

        if opcion == "1":
            ejecutar_simulacion(patron_aleatorio(), celda_color=VERDE, delay=0.10)
        elif opcion == "2":
            ejecutar_simulacion(patron_glider(), celda_color=CYAN, delay=0.15)
        elif opcion == "3":
            ejecutar_simulacion(patron_pulsar(), celda_color=MAGENTA, delay=0.18)
        elif opcion == "4":
            ejecutar_simulacion(patron_gosper_gun(), celda_color=AMARILLO, delay=0.10)
        elif opcion in ("0", "q", "exit", "salir"):
            print(f"\n{CYAN}Saliendo de la simulación. ¡Hasta luego!{RESET}\n")
            break
        else:
            print(f"\n{ROJO}[!] Opción no reconocida.{RESET}")
            time.sleep(1)


if __name__ == "__main__":
    main()
