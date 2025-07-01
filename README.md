 ██████╗ ██████╗ ██╗   ██╗███████╗██████╗ ███████╗██╗   ██╗ ██████╗██╗  ██╗███████╗██████╗     
██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██║   ██║██╔════╝██║ ██╔╝██╔════╝██╔══██╗    
██║     ██║   ██║██║   ██║█████╗  ██████╔╝███████╗██║   ██║██║     █████╔╝ █████╗  ██████╔╝    
██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗    
╚██████╗╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████║╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║    
 ╚═════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    

coversucker 🐙

Un script de Python para descargar todos los datos de tus clientes de CoverManager utilizando su API, ¡y mantenerlos organizados! 🚀
✨ Funcionalidades

Este proyecto te proporciona las herramientas para:

    Descargar todos los clientes: Obtén una lista completa de tus clientes de CoverManager.

    Paginación automática: No te preocupes por los límites de página; el script navegará por todas las páginas disponibles para asegurar que obtienes cada cliente. 🔄

    Guardado incremental en CSV: Los datos se guardan directamente en un archivo CSV a medida que se descargan, lo que es ideal para grandes volúmenes de datos. 💾

    Eliminación de duplicados por email integrada: Una vez que todos los clientes son descargados, el script automáticamente procesa y genera un segundo archivo CSV con entradas únicas por dirección de email. 🧹

🛠️ Requisitos

    Python 3.x

    La librería requests de Python.

🚀 Instalación

    Clona este repositorio (o descarga el archivo coversucker.py directamente):

    git clone https://github.com/tu-usuario/coversucker.git
    cd coversucker

    Instala las dependencias de Python:

    pip install requests

⚙️ Configuración

Antes de ejecutar el script, necesitas configurar tu API Key de CoverManager y el slug de tu restaurante.

    Abre el archivo coversucker.py en tu editor de texto favorito.

    Encuentra y actualiza las siguientes líneas en la sección --- Configuración ---:

    YOUR_API_KEY = "TU_API_KEY_AQUI"  # ¡IMPORTANTE! Reemplaza con tu API Key real
    YOUR_RESTAURANT_SLUG = "tu-restaurante-slug"  # ¡IMPORTANTE! Reemplaza con el slug de tu restaurante

        YOUR_API_KEY: Esta es la clave que CoverManager te proporciona para acceder a su API. Si no la tienes, contacta con el soporte de CoverManager.

        YOUR_RESTAURANT_SLUG: Es el identificador único de tu restaurante en CoverManager (por ejemplo, "casa-carlos" o "restaurante-oliviavalerenoweb").

🏃 Cómo usar

Simplemente ejecuta el script principal desde tu terminal:

python coversucker.py

El script realizará los siguientes pasos automáticamente:

    Comenzará a descargar las páginas de clientes y las guardará en un archivo llamado todos_clientes_covermanager.csv en el mismo directorio. Verás el progreso en tu consola.

    Una vez que la descarga esté completa, procesará automáticamente este archivo para eliminar duplicados por email.

    Creará un segundo archivo llamado clientes_covermanager_unicos_por_email.csv con todas las entradas únicas basadas en la dirección de email.

⚠️ Notas Importantes

    Seguridad de la API Key: ¡Mantén tu API Key segura! No la compartas públicamente ni la subas a repositorios públicos sin protegerla (por ejemplo, usando variables de entorno).

    Tasa de solicitudes (Rate Limiting): El script incluye una pequeña pausa (time.sleep(0.5)) entre cada solicitud para evitar sobrecargar la API de CoverManager y ser bloqueado. Si experimentas errores relacionados con límites de tasa, puedes aumentar este valor.

    Estructura de datos: La API de CoverManager puede evolucionar. Si la estructura de los datos de los clientes cambia, es posible que necesites ajustar la lista FIELDNAMES dentro del script coversucker.py para que coincida con los nuevos campos.

¡Disfruta de tus datos de clientes! 🎉
