# 🛠️ Programas Útiles (Python Utility Toolkit)

Una colección completa y modular de scripts y herramientas en Python diseñadas para **auditoría de ciberseguridad**, **automatización de tareas cotidianas**, **gestión de procesos y redes**, **procesamiento de medios y documentos**, y **simulaciones algorítmicas**.

Cada herramienta cuenta con una terminal interactiva de consola con menús de opciones o interfaz gráfica web (**Streamlit**) lista para usar. Además, las utilidades que leen y procesan ficheros disponen de carpetas dedicadas para organizar los archivos de entrada y los resultados generados.

---

## 📁 Estructura del Repositorio

```text
Programas_utiles/
├── ciberseguridad/
│   ├── Desbloqueador_pdf_excel/
│   │   ├── por_desbloquear/                   # Carpeta para depositar PDFs o Excels protegidos
│   │   ├── Contraseñas/                       # Diccionarios de claves (ej. rockyou.txt)
│   │   ├── crakeados/                         # Carpeta donde se guardan los archivos desbloqueados
│   │   ├── historial/                         # Registro histórico en formato JSON Lines (historial.jsonl)
│   │   └── Buscador.py                        # Desbloqueador por fuerza bruta acelerado por GPU y CPU
│   ├── Puertos/
│   │   ├── ruta_a_escanear                    # Archivo auxiliar de objetivo para escaneo
│   │   └── SpectraScan.py                     # Escáner de red, puertos y auditoría web
│   ├── encriptador/
│   │   ├── encriptado/                        # Carpeta donde se guardan los archivos cifrados
│   │   └── encriptador.py                     # Cifrador de PDF, Excel y CSV (AES-256 / Fernet + Web UI)
│   ├── Cifrador_de_mensajes.py                # Cifrado y descifrado simétrico por XOR
│   ├── Hash_fuerza_bruta.py                   # Cracker de hashes SHA-256 por diccionario
│   └── metadatos.py                           # Extractor, inyector y sanitizador de metadatos EXIF/Info (GPS, cámara, autor)
├── Kit_herramientas/
│   ├── Auditor_procesos_puertos/
│   │   ├── reportes/                          # Carpeta donde se generan reportes JSON
│   │   └── Auditor_procesos_puertos.py        # Auditor de procesos, puertos y terminación con psutil
│   ├── Compresor_removedor_fondos/
│   │   ├── new images/                        # Carpeta de salida predeterminada
│   │   └── Compresor_removedor_fondos.py      # Optimizador de PDFs/imágenes y recorte de fondos por IA
│   ├── Convertidor_tablas/
│   │   ├── tablas_entrada/                    # Carpeta para colocar archivos CSV, Excel o PDF a leer
│   │   ├── tablas_generadas/                  # Carpeta donde se generan las tablas LaTeX y Markdown
│   │   └── Convertidor_tablas.py              # Conversor de tablas a LaTeX y Markdown
│   ├── Descargar_video_YT/
│   │   ├── videos_descargado/                 # Carpeta de salida de descargas
│   │   └── Descargar_videos_youtube.py        # Descarga de videos individuales y playlists de YouTube
│   ├── Generador_QR/
│   │   └── Generador_de_QR_por_link.py        # Generación de códigos QR personalizados
│   ├── Juntador_pdf/
│   │   └── Juntador_pdfs.py                   # Fusión y unión secuencial de documentos PDF
│   ├── Ping_Logger/
│   │   ├── hosts_entrada/                     # Carpeta de lectura con archivo hosts.txt
│   │   ├── registros/                         # Carpeta donde se generan logs CSV y reportes
│   │   └── Ping_Logger.py                     # Monitor continuo de latencia, pérdidas y microcortes
│   ├── Respaldos_incrementales/
│   │   ├── archivos_a_respaldar/              # Carpeta de lectura para colocar archivos a respaldar
│   │   ├── respaldos/                         # Carpeta donde se generan los respaldos .zip / .tar.gz
│   │   └── Respaldos_incrementales.py         # Copias de seguridad completas e incrementales por mtime
│   ├── Escribir_mensajes.py                   # Automatización de escritura por teclado (Auto-Typer)
│   ├── Genera_y_poner_audio_por_texto.py      # Conversión de texto a voz (TTS) y reproducción automática
│   └── smart_organizer.py                     # Organizador inteligente de directorios (CLI y Web UI)
├── Programas_para_curiosidad/
│   └── Simulador_de_vida_cow.py               # Autómata celular del Juego de la Vida de Conway
├── main.py                                    # 🚀 Centro de control y lanzador interactivo unificado
├── requirements.txt                           # Lista estructurada de dependencias externas
├── instalar_dependencias.py                   # Menú interactivo para instalar dependencias selectivas o totales
├── LICENSE                                    # Licencia del proyecto
└── README.md                                  # Documentación completa y guía de uso
```

---

## 🚀 Centro de Control Unificado (`main.py`)

El repositorio incluye un archivo principal interactivo (`main.py`) diseñado como el punto de entrada unificado para **probar, buscar, diagnosticar y ejecutar cualquiera de las herramientas** desde un único lugar, tanto en **terminal de comandos (CLI)** como mediante un **panel gráfico interactivo en Streamlit**:

```bash
# Iniciar en Consola Interactiva (CLI):
python main.py

# Iniciar en Interfaz Gráfica Web (Streamlit):
python main.py web
# o directamente:
streamlit run main.py
```

### ✨ Características Principales:
- 🧭 **Menú Categórico Interactivo:** Acceso directo con un solo número a cualquiera de las 18 herramientas del proyecto.
- 🌐 **Panel Gráfico Web (Streamlit):** Dashboard interactivo con métricas, tarjetas visuales de cada herramienta, lanzamiento con un clic y visualización en tiempo real.
- 🔍 **Buscador Inteligente (`B`):** Encuentra herramientas al instante por palabra clave (ej. `pdf`, `qr`, `red`, `video`, `wifi`, `cifrar`).
- 🩺 **Diagnóstico de Salud (`D` o `python main.py --check`):** Comprueba automáticamente la integridad de los archivos y qué dependencias están instaladas o faltantes en tu entorno.
- 🛡️ **Pre-flight Check de Dependencias:** Si seleccionas una herramienta que requiere librerías no instaladas, `main.py` te avisa y te ofrece instalarlas automáticamente con `pip` en ese mismo instante.
- 🌐 **Soporte Doble Interfaz (CLI / Web):** Para programas con interfaz gráfica en Streamlit (como el Desbloqueador de PDF/Excel, Encriptador o Smart Organizer), permite elegir con un clic si ejecutarlos en terminal de consola o en el navegador web.
- ⚡ **Atajos por Línea de Comandos:**
  ```bash
  python main.py --list          # Lista rápida de todos los programas disponibles
  python main.py --check         # Ejecuta el diagnóstico del repositorio
  python main.py 1               # Ejecuta directamente la herramienta #1 (Metadatos)
  python main.py metadatos       # Ejecuta por coincidencia de nombre
  ```

---

## ⚙️ Instalación y Gestión de Dependencias

Para preparar el entorno de trabajo, el repositorio incluye un instalador interactivo en Python y el archivo estándar `requirements.txt`.

### Opción 1: Instalador Interactivo (Recomendado)

Ejecuta el script de instalación en la terminal:

```bash
python instalar_dependencias.py
```

Al iniciarse, se desplegará un menú interactivo con detección de estado en tiempo real:
- **Opción `[ F]`**: Detecta qué paquetes faltan en tu entorno Python activo e instala **únicamente las dependencias faltantes**, ahorrando tiempo.
- **Opción `[ 1]`**: Verifica y reinstala o actualiza **todas** las dependencias de todos los programas del repositorio.
- **Opciones `[ 2]` a `[15]`**: Muestran el estado de instalación de cada programa (`[✓ Instalado]` o `[✗ Falta]`) y permiten instalar selectivamente sus librerías.
- **Opciones `[16]` a `[19]`**: Programas que funcionan al 100% con la **biblioteca estándar de Python** sin requerir ninguna descarga externa.

### Opción 2: Instalación Tradicional con Pip

Si prefieres instalar todas las dependencias del proyecto de una sola vez:

```bash
pip install -r requirements.txt
```

---

## 📖 Catálogo Detallado de Programas

---

### 🛡️ Ciberseguridad y Auditoría

#### 1. Desbloqueador de PDF y Excel (Acelerado por GPU y CPU Multi-núcleo)
* **Archivo:** [`ciberseguridad/Desbloqueador_pdf_excel/Buscador.py`](ciberseguridad/Desbloqueador_pdf_excel/Buscador.py)
* **Carpetas del programa:**
  - 📥 **Lectura:** `por_desbloquear/` (donde colocas los PDFs o Excels protegidos) y `Contraseñas/` (diccionarios como `rockyou.txt` o listas de contraseñas en `.txt`).
  - 📤 **Generación:** `crakeados/` (donde se guarda el documento descifrado y, opcionalmente, el archivo `.password.txt` con la clave encontrada).
  - 📋 **Registro:** `historial/historial.jsonl` (historial persistente de operaciones).
* **Dependencias:** `pypdf`, `pycryptodome`, `streamlit` (opcional: `msoffcrypto-tool` para Excel).
* **Aceleración por Hardware y Características:**
  - ⚡ **GPU (OpenCL Nativo en tiempo de ejecución):** Detecta automáticamente cualquier GPU del sistema (NVIDIA RTX/GTX, AMD Radeon, Intel Arc o gráficos integrados) y compila kernels en caliente para evaluar **millones de contraseñas por segundo**.
  - 🧠 **Multiprocesamiento CPU:** En equipos sin GPU o para cifrados complejos (PDF Revision 6 / AES-256 Hardened), activa todos los núcleos del procesador en memoria RAM realizando verificación criptográfica pura (hasta 100x más rápido que parsear el documento).
  - 🔄 **Lector en Streaming:** Carga diccionarios gigantescos (`rockyou.txt` de 14.3 millones de claves) consumiendo menos de 50 MB de memoria RAM y con arranque instantáneo en 0.1 s.
  - 🌐 **Interfaz Web Interactiva (Streamlit):** Panel gráfico completo con 4 pestañas: desbloqueo interactivo, carga por drag-and-drop, visualización destacada de contraseñas encontradas, botón de descarga directa del archivo descifrado, historial persistente y benchmark GPU vs CPU.
  - 🔑 **Historial Detallado:** Almacena y muestra de forma clara la contraseña descubierta en texto plano (`historial.jsonl`) junto con la fecha y las rutas de salida.
  - ⏱️ **Benchmark integrado:** Incluye una prueba de rendimiento en vivo para medir la velocidad de cómputo en claves/segundo de tu GPU vs CPU.
  - 📥 **Descargador de Diccionarios:** Permite descargar directamente el archivo `rockyou.txt` a la carpeta `Contraseñas/` con barra de progreso en vivo desde el menú de consola mediante la biblioteca estándar (`urllib.request`).
* **Ejecución en consola (CLI):**
  ```bash
  # Menú interactivo
  python ciberseguridad/Desbloqueador_pdf_excel/Buscador.py

  # Iniciar interfaz interactiva Web (Streamlit)
  python ciberseguridad/Desbloqueador_pdf_excel/Buscador.py web
  # o directamente:
  streamlit run ciberseguridad/Desbloqueador_pdf_excel/Buscador.py

  # Medir rendimiento GPU vs CPU
  python ciberseguridad/Desbloqueador_pdf_excel/Buscador.py benchmark

  # Desbloquear por línea de comandos
  python ciberseguridad/Desbloqueador_pdf_excel/Buscador.py unlock --file "por_desbloquear/documento.pdf" --password-file "Contraseñas/rockyou.txt" --record-password
  ```

---

#### 2. Encriptador de Archivos (PDF, Excel y CSV)
* **Archivo:** [`ciberseguridad/encriptador/encriptador.py`](ciberseguridad/encriptador/encriptador.py)
* **Carpetas del programa:**
  - 📤 **Generación:** `ciberseguridad/encriptador/encriptado/` (carpeta donde se guardan los archivos protegidos).
* **Dependencias:** `pypdf`, `cryptography`, `msoffcrypto-tool`, `streamlit`
* **¿Qué hace?**  
  Permite proteger y cifrar documentos confidenciales mediante estándares criptográficos de alta seguridad:
  - **PDF:** Cifrado con algoritmo AES-256 y permisos de usuario.
  - **Excel (`.xlsx`, `.xls`):** Protección estándar mediante `msoffcrypto`.
  - **CSV:** Cifrado simétrico autenticado mediante Fernet con derivación de clave PBKDF2-HMAC-SHA256 (480,000 iteraciones y sal criptográfica de 16 bytes).
  - **Doble Interfaz:** Funciona tanto por consola como a través de una interfaz web moderna en **Streamlit** con carga interactiva de archivos.
* **Ejecución en consola (CLI):**
  ```bash
  python ciberseguridad/encriptador/encriptador.py
  ```
* **Ejecución en interfaz web:**
  ```bash
  streamlit run ciberseguridad/encriptador/encriptador.py
  ```

---

#### 3. SpectraScan / NetRecon v3.0 (Escáner de Red y Auditor Web)
* **Archivo:** [`ciberseguridad/Puertos/SpectraScan.py`](ciberseguridad/Puertos/SpectraScan.py)
* **Dependencias:** Ninguna (Biblioteca estándar: `socket`, `ssl`, `concurrent.futures`, `urllib`).
* **¿Qué hace?**  
  Herramienta de reconocimiento de red y auditoría de seguridad perimetral para servidores y sitios web:
  - **Escaneo de Puertos Multihilo:** Comprueba puertos TCP concurrentemente con medición de latencia y captura de banners. Incluye perfiles para infraestructura básica, desarrollo web, bases de datos o rangos manuales.
  - **Auditoría TLS/SSL:** Extrae certificados, SANs, entidad emisora, validez temporal y suites de cifrado.
  - **Auditoría de Cabeceras HTTP:** Revisa cabeceras de protección defensiva (`HSTS`, `CSP`, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, etc.).
  - **Cookies y CORS:** Inspecciona directivas `Secure`, `HttpOnly`, `SameSite` y permisos de orígenes cruzados.
  - **Gobernanza Web:** Valida redirecciones HTTPS y disponibilidad de `robots.txt`, `security.txt` y `sitemap.xml`.
  - **Exportación:** Guarda reportes consolidados en formato JSON estructurado.
* **Ejecución:**
  ```bash
  python ciberseguridad/Puertos/SpectraScan.py
  ```

---

#### 4. Gestor, Inyector y Limpiador de Metadatos EXIF
* **Archivo:** [`ciberseguridad/metadatos.py`](ciberseguridad/metadatos.py)
* **Dependencias:** `Pillow` (opcional: `streamlit` para Web UI)
* **¿Qué hace?**  
  Herramienta integral para auditar, inyectar y sanitizar metadatos en imágenes digitales de cualquier formato (JPEG, PNG, WEBP, TIFF, etc.):
  - **Inspección Sensible:** Extrae fabricante y modelo de cámara, software de edición, autor/artista, derechos de autor, fecha de captura y coordenadas GPS (generando un enlace directo a Google Maps y mapa interactivo en Web UI).
  - **Inyección y Edición de Metadatos:** Permite añadir o modificar metadatos completos en cualquier tipo de imagen: marca, modelo, software, autor, copyright, descripción, fecha/hora (con preset de hora actual), coordenadas GPS con conversión automática de grados decimales a DMS racionales y etiquetas personalizadas libres.
  - **Sanitización de Privacidad:** Crea una copia limpia de la imagen reconstruyendo únicamente la matriz de píxeles, eliminando cualquier rastro de metadatos para evitar doxxing.
  - **Doble Interfaz:** Disponible tanto en consola interactiva como mediante panel gráfico web en **Streamlit** con carga visual de imágenes, mapas interactivos y descarga directa.
* **Ejecución:**
  ```bash
  # Menú interactivo en consola (CLI)
  python ciberseguridad/metadatos.py

  # Iniciar interfaz gráfica Web (Streamlit)
  python ciberseguridad/metadatos.py web
  # o directamente:
  streamlit run ciberseguridad/metadatos.py
  ```

---

#### 5. Cracker de Hashes SHA-256 por Fuerza Bruta / Diccionario
* **Archivo:** [`ciberseguridad/Hash_fuerza_bruta.py`](ciberseguridad/Hash_fuerza_bruta.py)
* **Dependencias:** Ninguna (Biblioteca estándar: `hashlib`, `time`, `typing`).
* **¿Qué hace?**  
  Compara una cadena hash SHA-256 contra un conjunto de contraseñas candidatas calculando el digest en tiempo real. Mide con precisión de microsegundos el tiempo transcurrido, intentos realizados y la tasa de velocidad (*hashrate* en H/s).
* **Ejecución:**
  ```bash
  python ciberseguridad/Hash_fuerza_bruta.py
  ```

---

#### 6. Cifrador de Mensajes (XOR)
* **Archivo:** [`ciberseguridad/Cifrador_de_mensajes.py`](ciberseguridad/Cifrador_de_mensajes.py)
* **Dependencias:** Ninguna (Biblioteca estándar de Python).
* **¿Qué hace?**  
  Cifra y descifra mensajes de texto mediante la operación lógica simétrica XOR byte a byte con una clave secreta arbitraria, codificando la salida en hexadecimal para su transporte seguro.
* **Ejecución:**
  ```bash
  python ciberseguridad/Cifrador_de_mensajes.py
  ```

---

### 🧰 Kit de Herramientas y Productividad

#### 7. Auditor de Procesos y Puertos Locales
* **Archivo:** [`Kit_herramientas/Auditor_procesos_puertos/Auditor_procesos_puertos.py`](Kit_herramientas/Auditor_procesos_puertos/Auditor_procesos_puertos.py)
* **Carpetas del programa:**
  - 📤 **Generación:** `reportes/` (exportación de informes completos en JSON).
* **Dependencias:** `psutil`, `pandas`, `altair`, `streamlit`
* **¿Qué hace?**  
  Diagnóstico de sistema y red local: localiza qué proceso ocupa un puerto específico (ej. 3000, 5432, 8080), escanea puertos de desarrollo típicos (React, Django, Mongo, Redis), muestra rankings Top 15 de consumo de RAM/CPU, permite terminar procesos bloqueadores y ofrece un panel de control interactivo en **Streamlit**.
* **Ejecución en consola (CLI):**
  ```bash
  python Kit_herramientas/Auditor_procesos_puertos/Auditor_procesos_puertos.py
  ```

---

#### 8. Convertidor de Tablas PDF, CSV y Excel a LaTeX o Markdown
* **Archivo:** [`Kit_herramientas/Convertidor_tablas/Convertidor_tablas.py`](Kit_herramientas/Convertidor_tablas/Convertidor_tablas.py)
* **Carpetas del programa:**
  - 📥 **Lectura:** `tablas_entrada/` (para colocar archivos CSV, Excel o PDF).
  - 📤 **Generación:** `tablas_generadas/` (donde se generan los ficheros `.tex` y `.md`).
* **Dependencias:** `pandas`, `openpyxl`, `pymupdf`, `tabulate`, `streamlit`
* **¿Qué hace?**  
  Extrae tablas de hojas de cálculo, archivos delimitados y documentos PDF convirtiéndolas automáticamente a bloques de código LaTeX (con soporte estándar o `booktabs`) y tablas de Markdown listas para GitHub. Incluye previsualización y una aplicación web interactiva.
* **Ejecución:**
  ```bash
  python Kit_herramientas/Convertidor_tablas/Convertidor_tablas.py
  ```

---

#### 9. Automatizador de Respaldos Incrementales
* **Archivo:** [`Kit_herramientas/Respaldos_incrementales/Respaldos_incrementales.py`](Kit_herramientas/Respaldos_incrementales/Respaldos_incrementales.py)
* **Carpetas del programa:**
  - 📥 **Lectura:** `archivos_a_respaldar/` (carpeta predeterminada para colocar datos a respaldar).
  - 📤 **Generación:** `respaldos/` (donde se generan los archivos `.zip` o `.tar.gz` y el manifiesto `.backup_manifest.json`).
* **Dependencias:** `streamlit` (módulos de compresión son estándar).
* **¿Qué hace?**  
  Crea copias de seguridad completas o incrementales detectando archivos modificados o añadidos mediante la marca de tiempo `mtime`. Incluye exclusión de directorios pesados (`node_modules`, `.venv`, `.git`), rotación automática de copias antiguas y panel web para restauración.
* **Ejecución:**
  ```bash
  python Kit_herramientas/Respaldos_incrementales/Respaldos_incrementales.py
  ```

---

#### 10. Monitor de Latencia y Caídas de Red (Ping Logger)
* **Archivo:** [`Kit_herramientas/Ping_Logger/Ping_Logger.py`](Kit_herramientas/Ping_Logger/Ping_Logger.py)
* **Carpetas del programa:**
  - 📥 **Lectura:** `hosts_entrada/hosts.txt` (lista de IPs o dominios a monitorizar).
  - 📤 **Generación:** `registros/` (logs continuos en CSV y reportes de disponibilidad).
* **Dependencias:** `pandas`, `streamlit`
* **¿Qué hace?**  
  Monitorea de forma continua paquetes ICMP registrando latencia y pérdida de paquetes. Incluye detector de microcortes con alertas en terminal, cálculo de estadísticas percentiles (P95) y un panel interactivo web con gráficas en tiempo real.
* **Ejecución:**
  ```bash
  python Kit_herramientas/Ping_Logger/Ping_Logger.py
  ```

---

#### 11. Optimizador de PDFs e Imágenes y Removedor de Fondos por IA
* **Archivo:** [`Kit_herramientas/Compresor_removedor_fondos/Compresor_removedor_fondos.py`](Kit_herramientas/Compresor_removedor_fondos/Compresor_removedor_fondos.py)
* **Carpetas del programa:**
  - 📤 **Generación:** `new images/`
* **Dependencias:** `pymupdf`, `Pillow`, `rembg`, `streamlit`
* **¿Qué hace?**  
  Comprime documentos PDF e imágenes (JPG, PNG, WEBP) reduciendo drásticamente su peso, recorta fondos de fotografías mediante inteligencia artificial con el modelo `u2netp`, permite procesar lotes enteros y ofrece interfaz interactiva en Streamlit.
* **Ejecución:**
  ```bash
  python Kit_herramientas/Compresor_removedor_fondos/Compresor_removedor_fondos.py
  ```

---

#### 12. Juntador de Archivos PDF
* **Archivo:** [`Kit_herramientas/Juntador_pdf/Juntador_pdfs.py`](Kit_herramientas/Juntador_pdf/Juntador_pdfs.py)
* **Dependencias:** `pypdf`
* **¿Qué hace?**  
  Escanea los archivos PDF presentes en el directorio seleccionado, los lista con su tamaño y páginas, y los fusiona en un único documento maestro de salida con nombre personalizable y apertura automática.
* **Ejecución:**
  ```bash
  python Kit_herramientas/Juntador_pdf/Juntador_pdfs.py
  ```

---

#### 13. Descargador de Videos y Playlists de YouTube
* **Archivo:** [`Kit_herramientas/Descargar_video_YT/Descargar_videos_youtube.py`](Kit_herramientas/Descargar_video_YT/Descargar_videos_youtube.py)
* **Carpetas del programa:**
  - 📤 **Generación:** `videos_descargado/` (o ruta personalizada configurable)
* **Dependencias:** `yt-dlp`, `imageio-ffmpeg` (opcional: `streamlit` para Web UI)
* **¿Qué hace?**  
  Herramienta avanzada para descargar y gestionar videos y pistas de audio de YouTube:
  - **Múltiples formatos:** Descarga en MP4 (máxima calidad, 1080p, 720p, 480p), WebM, MP3 (320 kbps), M4A y WAV sin pérdida.
  - **Gestión de rutas:** Permite cambiar la carpeta de descarga a cualquier directorio del sistema y restaurar la predeterminada con un solo comando.
  - **Biblioteca y Reproductor:** Lista los archivos descargados y permite reproducirlos directamente tanto en el reproductor del sistema como en la interfaz web.
  - **Doble Interfaz:** Menú decorado en terminal (CLI) y panel gráfico web interactivo en **Streamlit**.
* **Ejecución:**
  ```bash
  # Menú interactivo en terminal (CLI)
  python Kit_herramientas/Descargar_video_YT/Descargar_videos_youtube.py

  # Iniciar interfaz gráfica Web (Streamlit)
  python Kit_herramientas/Descargar_video_YT/Descargar_videos_youtube.py web
  # o directamente:
  streamlit run Kit_herramientas/Descargar_video_YT/Descargar_videos_youtube.py
  ```

---

#### 14. Generador de Códigos QR Personalizados
* **Archivo:** [`Kit_herramientas/Generador_QR/Generador_de_QR_por_link.py`](Kit_herramientas/Generador_QR/Generador_de_QR_por_link.py)
* **Dependencias:** `qrcode`, `Pillow`
* **¿Qué hace?**  
  Genera imágenes PNG de códigos QR a partir de cualquier enlace web o texto, con paletas de color estilizadas (Negro/Blanco, Ámbar dorado, Azul tecnológico, Verde Matrix/Hacker, Púrpura neón o códigos Hex personalizados) y previsualización automática.
* **Ejecución:**
  ```bash
  python Kit_herramientas/Generador_QR/Generador_de_QR_por_link.py
  ```

---

#### 15. Conversor de Texto a Voz (TTS con gTTS)
* **Archivo:** [`Kit_herramientas/Genera_y_poner_audio_por_texto.py`](Kit_herramientas/Genera_y_poner_audio_por_texto.py)
* **Dependencias:** `gTTS`
* **¿Qué hace?**  
  Transforma texto escrito directo o archivos `.txt` completos a voz sintetizada natural mediante la API de Google TTS, soporta múltiples idiomas y dialectos (Español, Inglés, Francés, Alemán, etc.), genera archivos `.mp3` con marca de tiempo y permite su reproducción inmediata.
* **Ejecución:**
  ```bash
  python Kit_herramientas/Genera_y_poner_audio_por_texto.py
  ```

---

#### 16. Organizador Inteligente de Directorios (Smart Organizer)
* **Archivo:** [`Kit_herramientas/smart_organizer.py`](Kit_herramientas/smart_organizer.py)
* **Dependencias:** `streamlit`
* **¿Qué hace?**  
  Clasifica automáticamente archivos de carpetas caóticas (Descargas, Escritorio) en categorías organizadas. Cuenta con modo simulación (*Dry Run*), modo centinela en tiempo real, función deshacer (*Undo*) e interfaz web en Streamlit.
* **Ejecución:**
  ```bash
  python Kit_herramientas/smart_organizer.py
  ```

---

#### 17. Escritor Automatizado de Mensajes (Auto-Typer Kernel C-Speed)
* **Archivo:** [`Kit_herramientas/Escribir_mensajes.py`](Kit_herramientas/Escribir_mensajes.py)
* **Dependencias:** `keyboard` (utiliza la API nativa de Windows `user32.SendInput` mediante `ctypes`).
* **¿Qué hace?**  
  Inyector de eventos de teclado ultrarrápido a nivel de kernel de Windows mediante estructuras directas en memoria C (`SendInput`). Diseñado para enviar ráfagas masivas de texto sin la lentitud de librerías emuladas:
  - **Inyección por bloques de memoria:** Precompila ráfagas de paquetes de eventos de teclado en arreglos nativos de C antes de transmitirlos.
  - **Parámetros interactivos:** Permite personalizar la frase deseada, la cantidad total de líneas (hasta 100,000 repeticiones) y el tiempo de espera previo para colocar el cursor en la ventana de destino.
  - **Numeración opcional:** Permite activar o desactivar la inserción de números secuenciales al inicio de cada mensaje.
  - **Parada de emergencia:** Monitorea en tiempo real la tecla `ESC` con `keyboard` para abortar la ejecución inmediatamente en cualquier momento.
  - **Métricas de velocidad:** Mide y reporta el tiempo exacto de inyección en milisegundos tras finalizar.
* **Ejecución:**
  ```bash
  python Kit_herramientas/Escribir_mensajes.py
  ```

---

### 🧬 Curiosidades y Algoritmos

#### 18. Simulador del Juego de la Vida de Conway
* **Archivo:** [`Programas_para_curiosidad/Simulador_de_vida_cow.py`](Programas_para_curiosidad/Simulador_de_vida_cow.py)
* **Dependencias:** Ninguna (Biblioteca estándar de Python).
* **¿Qué hace?**  
  Implementación en consola del autómata celular de John Conway sobre una cuadrícula bidimensional animada en tiempo real. Cuenta con menú interactivo para seleccionar patrones clásicos (sopa primordial aleatoria, nave Planeador / Glider, oscilador Pulsar y cañón de planeadores de Gosper) junto a un HUD en vivo con métricas de generaciones y células vivas.
* **Ejecución:**
  ```bash
  python Programas_para_curiosidad/Simulador_de_vida_cow.py
  ```

---

## 📋 Resumen de Dependencias por Programa

| # | Programa | Ubicación | Dependencias Externas |
| :-: | :--- | :--- | :--- |
| **1** | **Desbloqueador de PDF y Excel (GPU & CPU)** | `ciberseguridad/Desbloqueador_pdf_excel/Buscador.py` | `pypdf`, `pycryptodome`, `msoffcrypto-tool`, `streamlit` |
| **2** | **Encriptador de Archivos (PDF, Excel, CSV)** | `ciberseguridad/encriptador/encriptador.py` | `pypdf`, `msoffcrypto-tool`, `cryptography`, `streamlit` |
| **3** | **Convertidor de Tablas** | `Kit_herramientas/Convertidor_tablas/...` | `pandas`, `openpyxl`, `pymupdf`, `tabulate`, `streamlit` |
| **4** | **Auditor de Procesos y Puertos** | `Kit_herramientas/Auditor_procesos_puertos/...` | `psutil`, `pandas`, `altair`, `streamlit` |
| **5** | **Respaldos Incrementales** | `Kit_herramientas/Respaldos_incrementales/...` | `streamlit` |
| **6** | **Monitor de Latencia (Ping Logger)** | `Kit_herramientas/Ping_Logger/...` | `pandas`, `streamlit` |
| **7** | **Descargador de Videos YouTube** | `Kit_herramientas/Descargar_video_YT/...` | `yt-dlp`, `imageio-ffmpeg`, `streamlit` |
| **8** | **Gestor de Metadatos EXIF (Extractor / Inyector / Limpiador)** | `ciberseguridad/metadatos.py` | `Pillow`, `streamlit` |
| **9** | **Escritor de Mensajes (Auto-Typer Kernel C-Speed)** | `Kit_herramientas/Escribir_mensajes.py` | `keyboard` |
| **10** | **Generador de Códigos QR** | `Kit_herramientas/Generador_QR/...` | `qrcode`, `Pillow` |
| **11** | **Generador de Audio (TTS)** | `Kit_herramientas/Genera_y_poner_audio_por_texto.py` | `gTTS` |
| **12** | **Organizador Inteligente** | `Kit_herramientas/smart_organizer.py` | `streamlit` |
| **13** | **Optimizador PDFs / Imágenes** | `Kit_herramientas/Compresor_removedor_fondos/...` | `pymupdf`, `Pillow`, `rembg`, `streamlit` |
| **14** | **Juntador de PDFs** | `Kit_herramientas/Juntador_pdf/Juntador_pdfs.py` | `pypdf` |
| **15** | **Cifrador de Mensajes (XOR)** | `ciberseguridad/Cifrador_de_mensajes.py` | *Ninguna (Estándar)* |
| **16** | **Cracker SHA-256** | `ciberseguridad/Hash_fuerza_bruta.py` | *Ninguna (Estándar)* |
| **17** | **SpectraScan / NetRecon** | `ciberseguridad/Puertos/SpectraScan.py` | *Ninguna (Estándar)* |
| **18** | **Juego de la Vida de Conway** | `Programas_para_curiosidad/Simulador_de_vida_cow.py` | *Ninguna (Estándar)* |

---

## 📄 Licencia

Este repositorio está protegido bajo los términos de la licencia [LICENSE](LICENSE) incluida en la raíz del proyecto.
