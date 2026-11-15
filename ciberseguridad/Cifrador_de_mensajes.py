import os
import sys

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


def xor_cipher(data: bytes, key: bytes) -> bytes:
    """Aplica XOR simétrico byte a byte."""
    key_len = len(key)
    return bytes([b ^ key[i % key_len] for i, b in enumerate(data)])


def cifrar(mensaje_original: str, llave_secreta: str) -> str:
    data = mensaje_original.encode("utf-8")
    key = llave_secreta.encode("utf-8")

    cifrado_bytes = xor_cipher(data, key)
    cifrado_hex = cifrado_bytes.hex()

    print(f"\n{AZUL}{'─' * 65}{RESET}")
    print(f"  {CYAN}📝 Mensaje Original :{RESET} {BLANCO}{mensaje_original}{RESET}")
    print(f"  {AMARILLO}🔑 Llave Secreta    :{RESET} {BLANCO}{llave_secreta}{RESET}")
    print(f"  {VERDE}{NEGRITA}🔒 Cifrado (Hex)    :{RESET} {VERDE}{cifrado_hex}{RESET}")
    print(f"{AZUL}{'─' * 65}{RESET}")
    return cifrado_hex


def descifrar(mensaje_cifrado_hex: str, llave_secreta: str) -> None:
    try:
        cifrado_bytes = bytes.fromhex(mensaje_cifrado_hex.strip())
    except ValueError:
        print(f"\n{ROJO}❌ Error: La cadena ingresada no es un valor hexadecimal válido.{RESET}")
        return

    key = llave_secreta.encode("utf-8")
    descifrado_bytes = xor_cipher(cifrado_bytes, key)

    try:
        mensaje_descifrado = descifrado_bytes.decode("utf-8")
        print(f"\n{AZUL}{'─' * 65}{RESET}")
        print(f"  {CYAN}🔒 Mensaje Hex      :{RESET} {BLANCO}{mensaje_cifrado_hex.strip()}{RESET}")
        print(f"  {AMARILLO}🔑 Llave Utilizada  :{RESET} {BLANCO}{llave_secreta}{RESET}")
        print(f"  {VERDE}{NEGRITA}🔓 Texto Descifrado :{RESET} {VERDE}{mensaje_descifrado}{RESET}")
        print(f"{AZUL}{'─' * 65}{RESET}")
    except UnicodeDecodeError:
        print(f"\n{ROJO}❌ Error de descifrado: La clave es incorrecta o los bytes están dañados.{RESET}")


def main():
    while True:
        print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{AZUL}{NEGRITA}║                   🔐 CIFRADOR Y DESCIFRADOR DE MENSAJES (XOR)                      ║{RESET}")
        print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"║  {VERDE}[1]{RESET} {BLANCO}🧪 Demostración automática (Prueba predefinida){RESET}                         ║")
        print(f"║  {VERDE}[2]{RESET} {BLANCO}🔒 Cifrar texto plano a código Hexadecimal{RESET}                             ║")
        print(f"║  {CYAN}[3]{RESET} {BLANCO}🔓 Descifrar código Hexadecimal a texto plano{RESET}                         ║")
        print(f"║  {ROJO}[0]{RESET} {BLANCO}🚪 Salir del programa{RESET}                                                 ║")
        print(f"{AZUL}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

        opcion = input(f"{VERDE}{NEGRITA}Seleccione una opción (0-3): {RESET}").strip()

        if opcion == "1":
            mensaje = "MensajeDePrueba123_Confidencial"
            llave = "ClaveSecretaSuperSegura"
            cifrado_hex = cifrar(mensaje, llave)
            print(f"\n{CYAN}[*] Probando descifrado automático inmediato con la misma clave...{RESET}")
            descifrar(cifrado_hex, llave)
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "2":
            mensaje = input(f"\n{CYAN}Ingrese el mensaje de texto a cifrar: {RESET}").strip()
            if not mensaje:
                print(f"{ROJO}❌ El mensaje no puede estar vacío.{RESET}")
                continue
            llave = input(f"{AMARILLO}Ingrese la llave secreta para cifrar: {RESET}").strip()
            if not llave:
                print(f"{ROJO}❌ La clave secreta no puede estar vacía.{RESET}")
                continue
            cifrar(mensaje, llave)
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion == "3":
            cifrado_hex = input(f"\n{CYAN}Ingrese el mensaje cifrado en Hexadecimal: {RESET}").strip()
            if not cifrado_hex:
                print(f"{ROJO}❌ Debe ingresar un valor hexadecimal.{RESET}")
                continue
            llave = input(f"{AMARILLO}Ingrese la llave secreta para descifrar: {RESET}").strip()
            if not llave:
                print(f"{ROJO}❌ La clave secreta no puede estar vacía.{RESET}")
                continue
            descifrar(cifrado_hex, llave)
            input(f"\n{BLANCO}Presione Enter para continuar...{RESET}")

        elif opcion in ("0", "q", "exit", "salir"):
            print(f"\n{CYAN}Saliendo del cifrador. ¡Hasta luego!{RESET}\n")
            break
        else:
            print(f"\n{ROJO}[!] Opción no reconocida. Intente de nuevo.{RESET}")


if __name__ == "__main__":
    main()
