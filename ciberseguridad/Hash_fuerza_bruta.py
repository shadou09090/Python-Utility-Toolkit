import hashlib
import os
import sys
import time
from typing import Iterable, Optional, Tuple

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

DICCIONARIO_DEFECTO = [
    "123456", "admin", "12345678", "1234", "password", "12345", "123456789",
    "qwerty", "princesa", "dragon", "password123", "queso", "chocolate",
    "master", "superman", "iloveyou", "secret", "seguridad", "colombia", "mexico"
]


def crack_sha256(
    target_hex: str, candidates: Iterable[str]
) -> Tuple[Optional[str], int, float]:
    try:
        target_bytes = bytes.fromhex(target_hex.strip())
    except ValueError:
        raise ValueError("El hash objetivo no tiene un formato hexadecimal válido.")

    if len(target_bytes) != 32:
        raise ValueError("El hash objetivo no corresponde a SHA-256 (debe tener 64 caracteres hex).")

    start_time = time.perf_counter()

    for attempts, word in enumerate(candidates, start=1):
        if hashlib.sha256(word.encode("utf-8")).digest() == target_bytes:
            elapsed = time.perf_counter() - start_time
            return word, attempts, elapsed
    else:
        elapsed = time.perf_counter() - start_time
        return None, attempts, elapsed


def mostrar_resultados_crackeo(hash_objetivo: str, password: Optional[str], attempts: int, elapsed: float):
    rate = attempts / elapsed if elapsed > 0 else 0.0
    print(f"\n{AZUL}{'─' * 70}{RESET}")
    print(f"  {CYAN}🎯 Hash objetivo :{RESET} {BLANCO}{hash_objetivo}{RESET}")
    if password is not None:
        print(f"  {VERDE}{NEGRITA}✓ Contraseña     : '{password}' (¡RECUPERADA!){RESET}")
    else:
        print(f"  {ROJO}✗ Contraseña     : No encontrada en el diccionario de prueba.{RESET}")

    print(f"  {AMARILLO}📊 Intentos       :{RESET} {BLANCO}{attempts:,}{RESET}")
    print(f"  {AMARILLO}⏱️  Tiempo         :{RESET} {BLANCO}{elapsed:.6f} segundos{RESET}")
    print(f"  {MAGENTA}⚡ Velocidad      :{RESET} {BLANCO}{rate:,.2f} H/s (Hashes por segundo){RESET}")
    print(f"{AZUL}{'─' * 70}{RESET}")


def main() -> None:
    while True:
        print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{AZUL}{NEGRITA}║                   ⚡ CRACKER DE HASHES SHA-256 POR DICCIONARIO                      ║{RESET}")
        print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"║  {VERDE}[1]{RESET} {BLANCO}🧪 Demostración de prueba predefinida{RESET}                                  ║")
        print(f"║  {VERDE}[2]{RESET} {BLANCO}🔓 Probar crackeo de un hash SHA-256 personalizado{RESET}                    ║")
        print(f"║  {CYAN}[3]{RESET} {BLANCO}🔑 Generar hash SHA-256 de una palabra o frase{RESET}                         ║")
        print(f"║  {ROJO}[0]{RESET} {BLANCO}🚪 Salir del programa{RESET}                                                 ║")
        print(f"{AZUL}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

        opcion = input(f"{VERDE}{NEGRITA}Seleccione una opción (0-3): {RESET}").strip()

        if opcion == "1":
            hash_demo = "a00d52243f97dba5c7cd716d8a675cb4e1db62ca6f14c25ebee868bd17ec2bfc"
            print(f"\n{CYAN}[*] Ejecutando demo sobre diccionario de prueba ({len(DICCIONARIO_DEFECTO)} palabras)...{RESET}")
            pwd, att, elap = crack_sha256(hash_demo, DICCIONARIO_DEFECTO)
            mostrar_resultados_crackeo(hash_demo, pwd, att, elap)
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "2":
            target = input(f"\n{CYAN}Ingrese el hash SHA-256 a crackear (64 hex chars): {RESET}").strip()
            if not target:
                print(f"{ROJO}❌ Debe ingresar un hash.{RESET}")
                continue
            try:
                print(f"\n{CYAN}[*] Buscando coincidencia en el diccionario...{RESET}")
                pwd, att, elap = crack_sha256(target, DICCIONARIO_DEFECTO)
                mostrar_resultados_crackeo(target, pwd, att, elap)
            except ValueError as ve:
                print(f"{ROJO}❌ Error: {ve}{RESET}")
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "3":
            palabra = input(f"\n{CYAN}Ingrese la palabra o texto a hashear con SHA-256: {RESET}").strip()
            if not palabra:
                print(f"{ROJO}❌ El texto no puede estar vacío.{RESET}")
                continue
            h = hashlib.sha256(palabra.encode("utf-8")).hexdigest()
            print(f"\n{AZUL}{'─' * 70}{RESET}")
            print(f"  {CYAN}Texto original   :{RESET} {BLANCO}{palabra}{RESET}")
            print(f"  {VERDE}{NEGRITA}SHA-256 generado :{RESET} {VERDE}{h}{RESET}")
            print(f"{AZUL}{'─' * 70}{RESET}")
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion in ("0", "q", "exit", "salir"):
            print(f"\n{CYAN}Saliendo del auditor de hashes. ¡Hasta luego!{RESET}\n")
            break
        else:
            print(f"\n{ROJO}[!] Opción no válida. Intente de nuevo.{RESET}")


if __name__ == "__main__":
    main()
