import os
import sys
import io
import subprocess
from datetime import datetime
from PIL import Image, ExifTags, PngImagePlugin
from PIL.ExifTags import TAGS, GPSTAGS

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


def lanzar_streamlit_desde_cli():
    """Lanza la interfaz web de Streamlit para este script desde la línea de comandos."""
    print("\n[*] Iniciando servidor de interfaz web con Streamlit...")
    print("[*] Presione Ctrl+C en esta terminal para detener el servidor web.\n")
    cmd = [sys.executable, "-m", "streamlit", "run", str(os.path.abspath(__file__))]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n[*] Interfaz web cerrada. Regresando a la terminal...")


def decimal_a_dms(deg):
    """
    Convierte grados decimales a formato (grados, minutos, segundos) racionales
    para el estándar EXIF GPS.
    """
    deg_abs = abs(float(deg))
    d = int(deg_abs)
    m = int((deg_abs - d) * 60)
    s = (deg_abs - d - m / 60.0) * 3600.0
    return (float(d), float(m), round(s, 4))


def a_grados_decimales(valor):
    """
    Convierte tuplas o listas (grados, minutos, segundos) o racionales a grados decimales.
    """
    try:
        if isinstance(valor, (int, float)):
            return float(valor)
        if isinstance(valor, (list, tuple)):
            if len(valor) >= 3:
                d = float(valor[0])
                m = float(valor[1])
                s = float(valor[2])
                return d + (m / 60.0) + (s / 3600.0)
            elif len(valor) == 2:
                return float(valor[0]) / float(valor[1])
        return float(valor)
    except Exception:
        return 0.0


def extraer_coordenadas(gps_info):
    """
    Extrae latitud y longitud en grados decimales desde el diccionario de GPSInfo.
    """
    try:
        lat_val = gps_info.get("GPSLatitude")
        lon_val = gps_info.get("GPSLongitude")
        if lat_val is None or lon_val is None:
            return None, None

        lat = a_grados_decimales(lat_val)
        lon = a_grados_decimales(lon_val)

        # Referencia de Latitud (Norte / Sur)
        lat_ref = gps_info.get("GPSLatitudeRef", "N")
        if isinstance(lat_ref, bytes):
            lat_ref = lat_ref.decode("utf-8", errors="ignore")
        lat_ref = str(lat_ref).strip().upper()
        if lat_ref.startswith("S"):
            lat = -lat

        # Referencia de Longitud (Este / Oeste)
        lon_ref = gps_info.get("GPSLongitudeRef", "E")
        if isinstance(lon_ref, bytes):
            lon_ref = lon_ref.decode("utf-8", errors="ignore")
        lon_ref = str(lon_ref).strip().upper()
        if lon_ref.startswith("W") or lon_ref.startswith("O"):
            lon = -lon

        return lat, lon
    except Exception:
        return None, None


def obtener_datos_exif(ruta_o_archivo):
    """
    Extrae los metadatos EXIF, sub-IFDs (GPS, Exif) y metadatos textuales de formato
    para cualquier tipo de imagen compatible (JPEG, PNG, WEBP, TIFF, etc.).
    Acepta tanto rutas de archivo como objetos en memoria (BytesIO, UploadedFile).
    """
    try:
        if hasattr(ruta_o_archivo, "seek"):
            try:
                ruta_o_archivo.seek(0)
            except Exception:
                pass

        with Image.open(ruta_o_archivo) as imagen:
            imagen.load()
            datos_exif = {}

            # 1. API estándar y moderna de Pillow (getexif)
            if hasattr(imagen, "getexif"):
                exif_obj = imagen.getexif()
                if exif_obj:
                    for tag_id, valor in exif_obj.items():
                        nombre = TAGS.get(tag_id, tag_id)
                        datos_exif[nombre] = valor

                    # Sub-IFD Exif (fechas originales, comentarios de usuario, etc.)
                    try:
                        exif_ifd = exif_obj.get_ifd(ExifTags.IFD.Exif)
                        if exif_ifd:
                            for tag_id, valor in exif_ifd.items():
                                nombre = TAGS.get(tag_id, tag_id)
                                datos_exif[nombre] = valor
                    except Exception:
                        pass

                    # Sub-IFD GPSInfo
                    try:
                        gps_ifd = exif_obj.get_ifd(ExifTags.IFD.GPSInfo)
                        if gps_ifd:
                            datos_gps = {}
                            for gps_id, valor in gps_ifd.items():
                                nombre_gps = GPSTAGS.get(gps_id, gps_id)
                                datos_gps[nombre_gps] = valor
                            datos_exif["GPSInfo"] = datos_gps
                    except Exception:
                        pass

            # 2. Compatibilidad clásica con _getexif() si aporta datos adicionales
            if hasattr(imagen, "_getexif"):
                try:
                    raw_legacy = imagen._getexif()
                    if raw_legacy:
                        for tag_id, valor in raw_legacy.items():
                            nombre_tag = TAGS.get(tag_id, tag_id)
                            if nombre_tag == "GPSInfo" and isinstance(valor, dict):
                                if "GPSInfo" not in datos_exif or not datos_exif["GPSInfo"]:
                                    datos_gps = {}
                                    for gps_id, gval in valor.items():
                                        nombre_gps = GPSTAGS.get(gps_id, gps_id)
                                        datos_gps[nombre_gps] = gval
                                    datos_exif["GPSInfo"] = datos_gps
                            elif nombre_tag not in datos_exif:
                                datos_exif[nombre_tag] = valor
                except Exception:
                    pass

            # 3. Metadatos textuales de formato (como chunks PNG tEXt o comentarios GIF)
            if hasattr(imagen, "info") and imagen.info:
                ignorar = {
                    "exif", "icc_profile", "photoshop", "xmp", "jfif",
                    "jfif_version", "jfif_unit", "jfif_density", "dpi",
                    "loop", "duration"
                }
                for k, v in imagen.info.items():
                    if k.lower() in ignorar:
                        continue
                    if isinstance(v, bytes):
                        try:
                            v = v.decode("utf-8", errors="ignore")
                        except Exception:
                            pass
                    val_str = str(v).strip()
                    if val_str and k not in datos_exif:
                        datos_exif[k] = val_str

            return datos_exif if datos_exif else None
    except Exception as e:
        print(f"\n[!] Error al leer la imagen: {e}")
        return None


def mostrar_metadatos_sensibles(ruta):
    """
    Muestra un reporte estructurado y amigable de los metadatos más sensibles encontrados:
    cámara, dispositivo, fechas, autoría y geolocalización GPS con enlace a mapas.
    """
    datos = obtener_datos_exif(ruta)
    if not datos:
        print(f"\n{AMARILLO}[-] No se encontraron metadatos en la imagen o el formato no contiene metadatos legibles.{RESET}")
        return

    print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{AZUL}{NEGRITA}║                   🔍 REPORTE DE METADATOS SENSIBLES                                ║{RESET}")
    print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"  {CYAN}📁 Archivo:{RESET} {ruta}")
    print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")

    marca = datos.get("Make", "No registrado")
    modelo = datos.get("Model", "No registrado")
    software = datos.get("Software", "No registrado")
    autor = datos.get("Artist", datos.get("Author", "No registrado"))
    copyright_info = datos.get("Copyright", "No registrado")
    descripcion = datos.get("ImageDescription", datos.get("Description", "No registrada"))
    fecha = datos.get("DateTimeOriginal", datos.get("DateTime", datos.get("DateTimeDigitized", "No registrada")))

    print(f"  {CYAN}📷 Marca del dispositivo  :{RESET} {BLANCO}{marca}{RESET}")
    print(f"  {CYAN}📱 Modelo del dispositivo :{RESET} {BLANCO}{modelo}{RESET}")
    print(f"  {CYAN}💻 Software / OS          :{RESET} {BLANCO}{software}{RESET}")
    print(f"  {CYAN}👤 Autor / Artista        :{RESET} {VERDE}{autor}{RESET}")
    print(f"  {CYAN}⚖️  Derechos de autor      :{RESET} {BLANCO}{copyright_info}{RESET}")
    print(f"  {CYAN}📝 Descripción / Título   :{RESET} {BLANCO}{descripcion}{RESET}")
    print(f"  {CYAN}📅 Fecha de captura       :{RESET} {AMARILLO}{fecha}{RESET}")

    if "UserComment" in datos:
        comentario = datos["UserComment"]
        if isinstance(comentario, bytes):
            try:
                comentario = comentario.decode("utf-8", errors="ignore")
            except Exception:
                pass
        print(f"  {CYAN}💬 Comentario de usuario  :{RESET} {BLANCO}{comentario}{RESET}")

    if "GPSInfo" in datos:
        lat, lon = extraer_coordenadas(datos["GPSInfo"])
        if lat is not None and lon is not None:
            print(f"  {ROJO}{NEGRITA}📍 Coordenadas GPS        :{RESET} {VERDE}{lat:.6f}, {lon:.6f}{RESET}")
            print(f"  {ROJO}{NEGRITA}🗺️  Enlace Google Maps     :{RESET} {CYAN}https://www.google.com/maps?q={lat},{lon}{RESET}")
            if "GPSAltitude" in datos["GPSInfo"]:
                try:
                    alt = float(datos["GPSInfo"]["GPSAltitude"])
                    print(f"  {CYAN}🏔️  Altitud GPS            :{RESET} {BLANCO}{alt:.2f} m{RESET}")
                except Exception:
                    pass
        else:
            print(f"  {AMARILLO}📍 Coordenadas GPS        : Datos GPS incompletos o corruptos{RESET}")
    else:
        print(f"  {AMARILLO}📍 Coordenadas GPS        : No encontradas (Sin geolocalización){RESET}")
    print(f"{AZUL}{'═' * 84}{RESET}")


def mostrar_todos_metadatos(ruta):
    """
    Realiza un volcado completo de todos los metadatos encontrados en la imagen.
    """
    datos = obtener_datos_exif(ruta)
    if not datos:
        print(f"\n{AMARILLO}[-] No se encontraron metadatos en la imagen.{RESET}")
        return

    print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{AZUL}{NEGRITA}║                   📋 VOLCADO COMPLETO DE METADATOS                                 ║{RESET}")
    print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
    for clave, valor in datos.items():
        if clave == "GPSInfo" and isinstance(valor, dict):
            print(f"\n  {MAGENTA}{NEGRITA}── Información GPS Detallada ──{RESET}")
            for k_gps, v_gps in valor.items():
                print(f"    {CYAN}{k_gps:<24}:{RESET} {BLANCO}{v_gps}{RESET}")
        else:
            print(f"  {CYAN}{clave:<28}:{RESET} {BLANCO}{valor}{RESET}")
    print(f"{AZUL}{'═' * 84}{RESET}")


def sanitizar_imagen_bytes(im: Image.Image, formato: str = "PNG") -> bytes:
    """
    Reconstruye una imagen píxel a píxel a partir de sus bytes brutos sin metadatos
    y retorna los bytes listos para guardar o descargar.
    """
    imagen_limpia = Image.frombytes(im.mode, im.size, im.tobytes())
    out_buf = io.BytesIO()
    fmt_upper = formato.upper()
    if fmt_upper in ("JPEG", "JPG"):
        if imagen_limpia.mode in ("RGBA", "LA", "P"):
            imagen_limpia = imagen_limpia.convert("RGB")
        imagen_limpia.save(out_buf, format="JPEG", quality=95)
    elif fmt_upper == "PNG":
        imagen_limpia.save(out_buf, format="PNG", optimize=True)
    elif fmt_upper == "WEBP":
        imagen_limpia.save(out_buf, format="WEBP", quality=95)
    else:
        imagen_limpia.save(out_buf, format=fmt_upper)
    out_buf.seek(0)
    return out_buf.getvalue()


def sanitizar_imagen(ruta):
    """
    Crea una copia limpia de la imagen reconstruyendo únicamente la matriz de píxeles,
    eliminando cualquier rastro de metadatos (EXIF, GPS, autoría, software).
    """
    try:
        with Image.open(ruta) as imagen:
            imagen.load()
            directorio, nombre_archivo = os.path.split(ruta)
            nombre_base, extension = os.path.splitext(nombre_archivo)
            nueva_ruta = os.path.join(directorio, f"{nombre_base}_sanitizada{extension}")

            ext_lower = extension.lower()
            formato = "JPEG" if ext_lower in (".jpg", ".jpeg") else ("WEBP" if ext_lower == ".webp" else "PNG")
            datos_bytes = sanitizar_imagen_bytes(imagen, formato)

            with open(nueva_ruta, "wb") as f_out:
                f_out.write(datos_bytes)

        print(f"\n[+] Imagen sanitizada guardada con éxito en:\n    -> {nueva_ruta}")
        return nueva_ruta
    except Exception as e:
        print(f"\n[!] Error al sanitizar la imagen: {e}")
        return None


def agregar_metadatos(ruta):
    """
    Permite incrustar o modificar metadatos (dispositivo, autor, copyright, descripción,
    fecha/hora, coordenadas GPS y etiquetas personalizadas) en cualquier tipo de imagen
    (JPEG, PNG, WEBP, TIFF, etc.).
    """
    try:
        with Image.open(ruta) as im_orig:
            im_orig.load()
            imagen = im_orig.copy()

        exif = imagen.getexif()
        datos_existentes = obtener_datos_exif(ruta) or {}

        print("\n" + "=" * 55)
        print("       AÑADIR O MODIFICAR METADATOS EN LA IMAGEN")
        print("=" * 55)
        print("Instrucciones:")
        print("- Ingrese el valor deseado para cada campo.")
        print("- Presione [Enter] directamente para omitir o conservar el valor actual.")
        print("=" * 55)

        # 1. Dispositivo y Software
        marca_act = datos_existentes.get("Make", "")
        prompt_marca = f"[*] Marca del dispositivo [Actual: '{marca_act}']: " if marca_act else "[*] Marca del dispositivo (ej. Sony, Apple, Canon, Nikon): "
        marca_in = input(prompt_marca).strip()
        if marca_in:
            exif[ExifTags.Base.Make] = marca_in

        modelo_act = datos_existentes.get("Model", "")
        prompt_modelo = f"[*] Modelo del dispositivo [Actual: '{modelo_act}']: " if modelo_act else "[*] Modelo del dispositivo (ej. iPhone 15 Pro, Alpha 7 IV): "
        modelo_in = input(prompt_modelo).strip()
        if modelo_in:
            exif[ExifTags.Base.Model] = modelo_in

        soft_act = datos_existentes.get("Software", "")
        prompt_soft = f"[*] Software / Programa [Actual: '{soft_act}']: " if soft_act else "[*] Software / Programa (ej. Adobe Photoshop, Script Metadatos): "
        soft_in = input(prompt_soft).strip()
        if soft_in:
            exif[ExifTags.Base.Software] = soft_in

        # 2. Autoría y Descripción
        autor_act = datos_existentes.get("Artist", datos_existentes.get("Author", ""))
        prompt_autor = f"[*] Autor / Artista [Actual: '{autor_act}']: " if autor_act else "[*] Autor / Artista / Creador: "
        autor_in = input(prompt_autor).strip()
        if autor_in:
            exif[ExifTags.Base.Artist] = autor_in

        copy_act = datos_existentes.get("Copyright", "")
        prompt_copy = f"[*] Copyright [Actual: '{copy_act}']: " if copy_act else "[*] Copyright (ej. © 2026 Todos los derechos reservados): "
        copy_in = input(prompt_copy).strip()
        if copy_in:
            exif[ExifTags.Base.Copyright] = copy_in

        desc_act = datos_existentes.get("ImageDescription", datos_existentes.get("Description", ""))
        prompt_desc = f"[*] Descripción / Título [Actual: '{desc_act}']: " if desc_act else "[*] Descripción o título de la imagen: "
        desc_in = input(prompt_desc).strip()
        if desc_in:
            exif[ExifTags.Base.ImageDescription] = desc_in

        comentario_in = input("[*] Comentario adicional (UserComment): ").strip()
        if comentario_in:
            exif_ifd = exif.get_ifd(ExifTags.IFD.Exif)
            exif_ifd[ExifTags.Base.UserComment] = comentario_in

        # 3. Fecha y Hora
        fecha_act = datos_existentes.get("DateTimeOriginal", datos_existentes.get("DateTime", ""))
        ahora_str = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
        print(f"\n[*] Fecha y hora de captura [Actual: '{fecha_act if fecha_act else 'No registrada'}']:")
        print(f"    1. Usar fecha y hora actual ({ahora_str})")
        print("    2. Ingresar fecha manualmente (Formato: AAAA:MM:DD HH:MM:SS)")
        print("    [Enter] Conservar actual o no modificar")
        opc_fecha = input("    Seleccione opción (1/2/Enter): ").strip()

        fecha_val = None
        if opc_fecha == "1":
            fecha_val = ahora_str
        elif opc_fecha == "2":
            fecha_manual = input("    -> Ingrese fecha (AAAA:MM:DD HH:MM:SS): ").strip()
            if fecha_manual:
                fecha_val = fecha_manual

        if fecha_val:
            exif[ExifTags.Base.DateTime] = fecha_val
            exif_ifd = exif.get_ifd(ExifTags.IFD.Exif)
            exif_ifd[ExifTags.Base.DateTimeOriginal] = fecha_val
            exif_ifd[ExifTags.Base.DateTimeDigitized] = fecha_val

        # 4. Coordenadas GPS
        gps_act = datos_existentes.get("GPSInfo")
        if gps_act:
            c_lat, c_lon = extraer_coordenadas(gps_act)
            coords_desc = f"{c_lat:.6f}, {c_lon:.6f}" if c_lat is not None and c_lon is not None else "Presentes"
            print(f"\n[*] Ubicación GPS actual: {coords_desc}")
            preg_gps = input("    ¿Desea modificar o añadir coordenadas GPS? (s/N): ").strip().lower()
        else:
            preg_gps = input("\n[*] ¿Desea añadir coordenadas GPS a la imagen? (s/N): ").strip().lower()

        if preg_gps in ["s", "si", "sí", "y", "yes"]:
            try:
                lat_in = input("    -> Latitud decimal (ej. 40.416775 para Madrid o -34.603722): ").strip()
                lon_in = input("    -> Longitud decimal (ej. -3.703790 o -58.381592): ").strip()
                alt_in = input("    -> Altitud en metros (opcional, ej. 650, Enter para omitir): ").strip()

                lat_num = float(lat_in.replace(",", "."))
                lon_num = float(lon_in.replace(",", "."))

                gps_ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
                gps_ifd[ExifTags.GPS.GPSLatitudeRef] = "N" if lat_num >= 0 else "S"
                gps_ifd[ExifTags.GPS.GPSLatitude] = decimal_a_dms(lat_num)
                gps_ifd[ExifTags.GPS.GPSLongitudeRef] = "E" if lon_num >= 0 else "W"
                gps_ifd[ExifTags.GPS.GPSLongitude] = decimal_a_dms(lon_num)

                if alt_in:
                    alt_num = float(alt_in.replace(",", "."))
                    gps_ifd[ExifTags.GPS.GPSAltitudeRef] = 0 if alt_num >= 0 else 1
                    gps_ifd[ExifTags.GPS.GPSAltitude] = abs(alt_num)

                print("    [+] Coordenadas GPS configuradas correctamente.")
            except ValueError:
                print("    [!] Error: Valores numéricos inválidos para coordenadas GPS. Se omiten datos GPS.")

        # 5. Etiquetas personalizadas adicionales
        preg_custom = input("\n[*] ¿Desea añadir etiquetas o metadatos de texto personalizados? (s/N): ").strip().lower()
        metadatos_personalizados = {}
        if preg_custom in ["s", "si", "sí", "y", "yes"]:
            print("    (Presione Enter con etiqueta vacía para finalizar)")
            while True:
                clave = input("    -> Nombre de la etiqueta: ").strip()
                if not clave:
                    break
                valor = input(f"       Valor para '{clave}': ").strip()
                metadatos_personalizados[clave] = valor

        # 6. Definición de ruta de guardado
        directorio, nombre_archivo = os.path.split(ruta)
        nombre_base, extension = os.path.splitext(nombre_archivo)
        ruta_sugerida = os.path.join(directorio, f"{nombre_base}_con_metadatos{extension}")

        print("\n" + "=" * 50)
        print("[*] Guardado del archivo:")
        print(f"    Ruta sugerida: {ruta_sugerida}")
        ruta_salida = input("    Ingrese nueva ruta (o presione [Enter] para usar la sugerida): ").strip().strip('"').strip("'")
        if not ruta_salida:
            ruta_salida = ruta_sugerida

        # Confirmación si se sobrescribe la imagen original
        if os.path.abspath(ruta_salida) == os.path.abspath(ruta):
            confirma = input("[!] Advertencia: Sobrescribirá la imagen original. ¿Continuar? (s/N): ").strip().lower()
            if confirma not in ["s", "si", "sí", "y", "yes"]:
                print("[-] Operación cancelada por el usuario.")
                return None

        # 7. Guardado según formato
        _, ext_salida = os.path.splitext(ruta_salida)
        ext_salida = ext_salida.lower()

        # Alerta en formatos no estándar para EXIF (BMP, GIF, etc.)
        if ext_salida in [".bmp", ".gif", ".ico"]:
            print(f"\n[!] Aviso: El formato '{ext_salida}' no admite metadatos EXIF estándar en la mayoría de visores.")
            conv = input("    ¿Desea guardarlo como PNG para preservar todos los metadatos sin pérdida? (S/n): ").strip().lower()
            if conv not in ["n", "no"]:
                ruta_salida = os.path.splitext(ruta_salida)[0] + ".png"
                ext_salida = ".png"
                print(f"    [+] Formato de salida actualizado a: {ruta_salida}")

        if ext_salida in [".jpg", ".jpeg"]:
            if imagen.mode in ("RGBA", "LA", "P"):
                img_guardar = imagen.convert("RGB")
            else:
                img_guardar = imagen
            img_guardar.save(ruta_salida, format="JPEG", exif=exif, quality=95)
        elif ext_salida == ".png":
            pnginfo = PngImagePlugin.PngInfo()
            if ExifTags.Base.Artist in exif:
                pnginfo.add_text("Author", str(exif[ExifTags.Base.Artist]))
            if ExifTags.Base.ImageDescription in exif:
                pnginfo.add_text("Description", str(exif[ExifTags.Base.ImageDescription]))
            if ExifTags.Base.Software in exif:
                pnginfo.add_text("Software", str(exif[ExifTags.Base.Software]))
            if ExifTags.Base.Copyright in exif:
                pnginfo.add_text("Copyright", str(exif[ExifTags.Base.Copyright]))
            for k, v in metadatos_personalizados.items():
                pnginfo.add_text(k, str(v))
            imagen.save(ruta_salida, format="PNG", exif=exif, pnginfo=pnginfo, optimize=True)
        elif ext_salida == ".webp":
            imagen.save(ruta_salida, format="WEBP", exif=exif, quality=95)
        elif ext_salida in [".tif", ".tiff"]:
            imagen.save(ruta_salida, format="TIFF", exif=exif)
        elif ext_salida == ".gif":
            comentario = ""
            if ExifTags.Base.ImageDescription in exif:
                comentario = str(exif[ExifTags.Base.ImageDescription])
            elif ExifTags.Base.Artist in exif:
                comentario = f"Autor: {exif[ExifTags.Base.Artist]}"
            imagen.save(ruta_salida, format="GIF", comment=comentario.encode("utf-8", errors="ignore"))
        else:
            try:
                imagen.save(ruta_salida, exif=exif)
            except Exception:
                imagen.save(ruta_salida)

        print(f"\n[+] ¡Metadatos guardados con éxito en:\n    -> {ruta_salida}")
        print("\n[*] Verificando los metadatos recién incrustados...")
        mostrar_metadatos_sensibles(ruta_salida)
        return ruta_salida
    except Exception as e:
        print(f"\n[!] Error al añadir metadatos a la imagen: {e}")
        return None


def verificar_ruta():
    ruta = input("\nIngrese la ruta de la imagen: ").strip().strip('"').strip("'")
    if not os.path.isfile(ruta):
        print("\n[!] Error: El archivo especificado no existe.")
        return None
    return ruta


# ==============================================================================
# INTERFAZ GRÁFICA INTERACTIVA WEB (STREAMLIT)
# ==============================================================================
def run_streamlit_ui():
    """Ejecuta la interfaz gráfica interactiva de Streamlit para Metadatos."""
    import streamlit as st

    st.set_page_config(
        page_title="Gestor de Metadatos EXIF",
        page_icon="📷",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1E88E5;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #666;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background-color: #f8f9fa;
            border-left: 4px solid #1E88E5;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="main-header">📷 Gestor y Modificador de Metadatos EXIF</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Inspecciona geolocalización GPS, añade metadatos forenses y sanitiza imágenes para proteger tu privacidad.</div>',
        unsafe_allow_html=True,
    )

    tab_inspeccionar, tab_modificar, tab_sanitizar = st.tabs([
        "🔍 Inspeccionar y Auditar",
        "✏️ Añadir o Modificar Metadatos",
        "🧼 Sanitizador de Privacidad",
    ])

    # -------------------------------------------------------------------------
    # PESTAÑA 1: INSPECCIONAR Y AUDITAR
    # -------------------------------------------------------------------------
    with tab_inspeccionar:
        st.subheader("Auditoría de Metadatos e Información Oculta")
        subida_ins = st.file_uploader(
            "Selecciona o arrastra una imagen para analizar:",
            type=["jpg", "jpeg", "png", "webp", "tiff", "tif", "bmp", "gif"],
            key="uploader_inspeccionar",
        )

        if subida_ins is not None:
            col_img, col_info = st.columns([1, 1.2])

            with col_img:
                st.image(subida_ins, caption=f"Archivo: {subida_ins.name}", use_container_width=True)
                with Image.open(subida_ins) as im_preview:
                    st.info(f"**Dimensiones:** {im_preview.width} x {im_preview.height} px | **Modo:** {im_preview.mode} | **Formato:** {im_preview.format}")

            with col_info:
                datos = obtener_datos_exif(subida_ins)
                if not datos:
                    st.warning("⚠️ No se encontraron metadatos EXIF en esta imagen (puede estar limpia o no contener datos).")
                else:
                    st.success("✅ Metadatos detectados en la imagen.")
                    st.markdown("### 📋 Datos Sensibles Detectados")

                    marca = datos.get("Make", "No registrada")
                    modelo = datos.get("Model", "No registrado")
                    soft = datos.get("Software", "No registrado")
                    autor = datos.get("Artist", datos.get("Author", "No registrado"))
                    copy_r = datos.get("Copyright", "No registrado")
                    desc = datos.get("ImageDescription", datos.get("Description", "No registrada"))
                    fecha = datos.get("DateTimeOriginal", datos.get("DateTime", datos.get("DateTimeDigitized", "No registrada")))

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown(f"**Dispositivo:** {marca} {modelo}")
                        st.markdown(f"**Software / OS:** {soft}")
                        st.markdown(f"**Fecha Captura:** {fecha}")
                    with col_b:
                        st.markdown(f"**Autor:** {autor}")
                        st.markdown(f"**Copyright:** {copy_r}")
                        st.markdown(f"**Descripción:** {desc}")

                    if "UserComment" in datos:
                        comm = datos["UserComment"]
                        if isinstance(comm, bytes):
                            comm = comm.decode("utf-8", errors="ignore")
                        st.info(f"💬 **Comentario:** {comm}")

                    # Información GPS
                    if "GPSInfo" in datos:
                        lat, lon = extraer_coordenadas(datos["GPSInfo"])
                        if lat is not None and lon is not None:
                            st.markdown("---")
                            st.error(f"📍 **Ubicación GPS Encontrada:** `{lat:.6f}, {lon:.6f}`")
                            st.markdown(f"[🌍 Abrir en Google Maps](https://www.google.com/maps?q={lat},{lon})")

                            try:
                                import pandas as pd
                                df_map = pd.DataFrame([{"lat": lat, "lon": lon}])
                                st.map(df_map, zoom=14)
                            except Exception:
                                pass
                        else:
                            st.warning("📍 Datos GPS presentes pero incompletos o corruptos.")

                    with st.expander("🔎 Ver todos los metadatos crudos"):
                        st.json({str(k): (str(v) if not isinstance(v, dict) else {str(gk): str(gv) for gk, gv in v.items()}) for k, v in datos.items() if not isinstance(v, bytes)})

    # -------------------------------------------------------------------------
    # PESTAÑA 2: AÑADIR O MODIFICAR METADATOS
    # -------------------------------------------------------------------------
    with tab_modificar:
        st.subheader("Inyector de Metadatos Multiformato")
        subida_mod = st.file_uploader(
            "Cargar imagen a la que deseas incrustar metadatos:",
            type=["jpg", "jpeg", "png", "webp", "tiff", "tif", "bmp"],
            key="uploader_modificar",
        )

        if subida_mod is not None:
            datos_prev = obtener_datos_exif(subida_mod) or {}
            with Image.open(subida_mod) as im_edit:
                im_edit.load()
                formato_sug = im_edit.format or "JPEG"

            st.info("Configura los campos a continuación. Los campos en blanco conservarán los valores previos o se omitirán.")

            with st.form("form_metadatos"):
                col_disp, col_aut = st.columns(2)
                with col_disp:
                    st.markdown("#### 📱 Dispositivo y Cámara")
                    in_make = st.text_input("Marca del dispositivo (Make):", value=str(datos_prev.get("Make", "")))
                    in_model = st.text_input("Modelo del dispositivo (Model):", value=str(datos_prev.get("Model", "")))
                    in_soft = st.text_input("Software / Programa:", value=str(datos_prev.get("Software", "Python Metadatos Tool")))

                with col_aut:
                    st.markdown("#### 👤 Autoría y Derechos")
                    in_artist = st.text_input("Autor / Creador (Artist):", value=str(datos_prev.get("Artist", "")))
                    in_copy = st.text_input("Derechos de autor (Copyright):", value=str(datos_prev.get("Copyright", "")))
                    in_desc = st.text_input("Descripción o Título:", value=str(datos_prev.get("ImageDescription", "")))
                    in_comm = st.text_input("Comentario de usuario (UserComment):", value="")

                st.markdown("---")
                col_fec, col_gps = st.columns(2)
                with col_fec:
                    st.markdown("#### 📅 Fecha y Hora")
                    ahora_str = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
                    usar_ahora = st.checkbox(f"Usar fecha y hora actual ({ahora_str})", value=True)
                    in_fecha = st.text_input("O escribe una fecha manual (AAAA:MM:DD HH:MM:SS):", value=str(datos_prev.get("DateTimeOriginal", "")))

                with col_gps:
                    st.markdown("#### 📍 Geolocalización GPS")
                    gps_prev = datos_prev.get("GPSInfo")
                    def_lat, def_lon = extraer_coordenadas(gps_prev) if gps_prev else (None, None)
                    poner_gps = st.checkbox("¿Incrustar coordenadas GPS?", value=(def_lat is not None))
                    in_lat = st.number_input("Latitud decimal (ej. 40.416775 para Madrid):", value=float(def_lat) if def_lat is not None else 40.416775, format="%.6f")
                    in_lon = st.number_input("Longitud decimal (ej. -3.703790):", value=float(def_lon) if def_lon is not None else -3.703790, format="%.6f")
                    in_alt = st.number_input("Altitud en metros (opcional):", value=0.0, format="%.2f")

                st.markdown("---")
                st.markdown("#### 💾 Formato de Descarga")
                formato_salida = st.selectbox(
                    "Seleccione el formato para guardar:",
                    ["Original (" + formato_sug + ")", "JPEG (.jpg)", "PNG (.png)", "WEBP (.webp)"],
                )

                btn_guardar = st.form_submit_button("⚡ Incrustar Metadatos en la Imagen")

            if btn_guardar:
                with Image.open(subida_mod) as im_target:
                    im_target.load()
                    exif_new = im_target.getexif()

                    # Base tags
                    if in_make:
                        exif_new[ExifTags.Base.Make] = in_make
                    if in_model:
                        exif_new[ExifTags.Base.Model] = in_model
                    if in_soft:
                        exif_new[ExifTags.Base.Software] = in_soft
                    if in_artist:
                        exif_new[ExifTags.Base.Artist] = in_artist
                    if in_copy:
                        exif_new[ExifTags.Base.Copyright] = in_copy
                    if in_desc:
                        exif_new[ExifTags.Base.ImageDescription] = in_desc

                    # Exif IFD
                    exif_ifd = exif_new.get_ifd(ExifTags.IFD.Exif)
                    if in_comm:
                        exif_ifd[ExifTags.Base.UserComment] = in_comm

                    f_val = ahora_str if usar_ahora else in_fecha
                    if f_val:
                        exif_new[ExifTags.Base.DateTime] = f_val
                        exif_ifd[ExifTags.Base.DateTimeOriginal] = f_val
                        exif_ifd[ExifTags.Base.DateTimeDigitized] = f_val

                    # GPS IFD
                    if poner_gps:
                        gps_ifd = exif_new.get_ifd(ExifTags.IFD.GPSInfo)
                        gps_ifd[ExifTags.GPS.GPSLatitudeRef] = "N" if in_lat >= 0 else "S"
                        gps_ifd[ExifTags.GPS.GPSLatitude] = decimal_a_dms(in_lat)
                        gps_ifd[ExifTags.GPS.GPSLongitudeRef] = "E" if in_lon >= 0 else "W"
                        gps_ifd[ExifTags.GPS.GPSLongitude] = decimal_a_dms(in_lon)
                        if in_alt != 0.0:
                            gps_ifd[ExifTags.GPS.GPSAltitudeRef] = 0 if in_alt >= 0 else 1
                            gps_ifd[ExifTags.GPS.GPSAltitude] = abs(float(in_alt))

                    # Guardado a buffer
                    out_buf = io.BytesIO()
                    nombre_base, _ = os.path.splitext(subida_mod.name)

                    if "PNG" in formato_salida or (formato_salida.startswith("Original") and formato_sug == "PNG"):
                        pnginfo = PngImagePlugin.PngInfo()
                        if in_artist:
                            pnginfo.add_text("Author", in_artist)
                        if in_desc:
                            pnginfo.add_text("Description", in_desc)
                        if in_soft:
                            pnginfo.add_text("Software", in_soft)
                        if in_copy:
                            pnginfo.add_text("Copyright", in_copy)
                        im_target.save(out_buf, format="PNG", exif=exif_new, pnginfo=pnginfo, optimize=True)
                        mime_t = "image/png"
                        out_name = f"{nombre_base}_con_metadatos.png"
                    elif "WEBP" in formato_salida or (formato_salida.startswith("Original") and formato_sug == "WEBP"):
                        im_target.save(out_buf, format="WEBP", exif=exif_new, quality=95)
                        mime_t = "image/webp"
                        out_name = f"{nombre_base}_con_metadatos.webp"
                    else:
                        img_rgb = im_target.convert("RGB") if im_target.mode in ("RGBA", "LA", "P") else im_target
                        img_rgb.save(out_buf, format="JPEG", exif=exif_new, quality=95)
                        mime_t = "image/jpeg"
                        out_name = f"{nombre_base}_con_metadatos.jpg"

                    out_bytes = out_buf.getvalue()

                st.success("🎉 ¡Metadatos incrustados con éxito en la imagen!")
                st.download_button(
                    label=f"📥 Descargar {out_name}",
                    data=out_bytes,
                    file_name=out_name,
                    mime=mime_t,
                )

    # -------------------------------------------------------------------------
    # PESTAÑA 3: SANITIZADOR DE PRIVACIDAD
    # -------------------------------------------------------------------------
    with tab_sanitizar:
        st.subheader("Sanitización y Eliminación Total de Metadatos")
        st.write(
            "Crea una copia completamente limpia de tu fotografía mediante reconstrucción de píxeles puros. "
            "Se eliminan fabricantes, modelos, números de serie, software de edición y coordenadas de geolocalización GPS."
        )

        subida_san = st.file_uploader(
            "Selecciona la imagen que deseas desinfectar / sanitizar:",
            type=["jpg", "jpeg", "png", "webp", "tiff", "tif", "bmp"],
            key="uploader_sanitizar",
        )

        if subida_san is not None:
            with Image.open(subida_san) as im_san:
                im_san.load()
                fmt_orig = im_san.format or "PNG"

            col_san_prev, col_san_act = st.columns([1, 1])
            with col_san_prev:
                st.image(subida_san, caption="Imagen original", use_container_width=True)

            with col_san_act:
                st.markdown("#### 🛡️ Acciones de Sanitización")
                formato_san = st.selectbox(
                    "Formato de salida sanitizado:",
                    ["Mismo formato (" + fmt_orig + ")", "PNG (Sin pérdida)", "JPEG (.jpg)"],
                    key="fmt_san",
                )

                if st.button("🧼 Limpiar y Eliminar Metadatos Ahora"):
                    if "PNG" in formato_san:
                        target_fmt = "PNG"
                        ext_f = ".png"
                        mime_s = "image/png"
                    elif "JPEG" in formato_san:
                        target_fmt = "JPEG"
                        ext_f = ".jpg"
                        mime_s = "image/jpeg"
                    else:
                        target_fmt = fmt_orig
                        ext_f = f".{fmt_orig.lower()}"
                        mime_s = f"image/{fmt_orig.lower()}"

                    with Image.open(subida_san) as im_proc:
                        limpia_bytes = sanitizar_imagen_bytes(im_proc, target_fmt)

                    nombre_b, _ = os.path.splitext(subida_san.name)
                    nombre_descarga = f"{nombre_b}_sanitizada{ext_f}"

                    st.success("✅ ¡Imagen sanitizada con éxito! Todos los metadatos han sido eliminados.")
                    st.download_button(
                        label=f"📥 Descargar {nombre_descarga}",
                        data=limpia_bytes,
                        file_name=nombre_descarga,
                        mime=mime_s,
                    )


# ==============================================================================
# MENÚ DE CONSOLA (CLI)
# ==============================================================================
def menu():
    while True:
        print(f"\n{AZUL}{NEGRITA}╔════════════════════════════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{AZUL}{NEGRITA}║                   🖼️  GESTOR Y MODIFICADOR DE METADATOS EXIF                       ║{RESET}")
        print(f"{AZUL}{NEGRITA}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}")
        print(f"{AZUL}╠════════════════════════════════════════════════════════════════════════════════════╣{RESET}")
        print(f"║  {VERDE}[1]{RESET} {BLANCO}🔍 Analizar metadatos sensibles (GPS, Cámara, Autor, Fecha){RESET}          ║")
        print(f"║  {VERDE}[2]{RESET} {BLANCO}🧹 Sanitizar imagen (Crear copia limpia sin metadatos){RESET}               ║")
        print(f"║  {VERDE}[3]{RESET} {BLANCO}✍️  Añadir o modificar metadatos a una imagen{RESET}                         ║")
        print(f"║  {VERDE}[4]{RESET} {BLANCO}⚡ Flujo completo (Analizar, Sanitizar y Verificar){RESET}                 ║")
        print(f"║  {CYAN}[5]{RESET} {BLANCO}📋 Ver todos los metadatos crudos (Volcado completo){RESET}                ║")
        print(f"║  {MAGENTA}[6]{RESET} {BLANCO}🌐 Iniciar Interfaz Gráfica Web (Streamlit){RESET}                          ║")
        print(f"║  {ROJO}[7]{RESET} {BLANCO}🚪 Salir del programa{RESET}                                                ║")
        print(f"{AZUL}╚════════════════════════════════════════════════════════════════════════════════════╝{RESET}\n")

        opcion = input(f"{VERDE}{NEGRITA}Seleccione una opción (1-7): {RESET}").strip()

        if opcion == "1":
            ruta = verificar_ruta()
            if ruta:
                mostrar_metadatos_sensibles(ruta)
        elif opcion == "2":
            ruta = verificar_ruta()
            if ruta:
                sanitizar_imagen(ruta)
        elif opcion == "3":
            ruta = verificar_ruta()
            if ruta:
                agregar_metadatos(ruta)
        elif opcion == "4":
            ruta = verificar_ruta()
            if ruta:
                mostrar_metadatos_sensibles(ruta)
                nueva_ruta = sanitizar_imagen(ruta)
                if nueva_ruta:
                    print("\n[*] Verificando el archivo generado...")
                    mostrar_metadatos_sensibles(nueva_ruta)
        elif opcion == "5":
            ruta = verificar_ruta()
            if ruta:
                mostrar_todos_metadatos(ruta)
        elif opcion == "6":
            lanzar_streamlit_desde_cli()
        elif opcion == "7":
            print("\nSaliendo del programa.")
            sys.exit(0)
        else:
            print("\n[!] Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    if is_running_in_streamlit():
        run_streamlit_ui()
    elif len(sys.argv) > 1 and sys.argv[1].lower() in ("web", "--web", "-w"):
        lanzar_streamlit_desde_cli()
    else:
        menu()
