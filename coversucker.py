import requests
import json
import csv
import time
import os

banner = """
 ██████╗ ██████╗ ██╗   ██╗███████╗██████╗ ███████╗██╗   ██╗ ██████╗██╗  ██╗███████╗██████╗     
██╔════╝██╔═══██╗██║   ██║██╔════╝██╔══██╗██╔════╝██║   ██║██╔════╝██║ ██╔╝██╔════╝██╔══██╗    
██║     ██║   ██║██║   ██║█████╗  ██████╔╝███████╗██║   ██║██║     █████╔╝ █████╗  ██████╔╝    
██║     ██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗    
╚██████╗╚██████╔╝ ╚████╔╝ ███████╗██║  ██║███████║╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║    
 ╚═════╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    
                                                                                               


"""
print(banner)
print('Exportando  todos tus clientes de Cover Manager...')
                        




# --- Configuración ---
YOUR_API_KEY = "XXXXXXXXXXXX"  # ¡IMPORTANTE! Reemplaza con tu API Key real
YOUR_RESTAURANT_SLUG = "restaurante-XXXXXX"  # ¡IMPORTANTE! Reemplaza con el slug de tu restaurante
INPUT_FILENAME = "todos_clientes_covermanager.csv"  # Nombre del archivo CSV de entrada
OUTPUT_FILENAME_UNIQUE = "clientes_covermanager_unicos_por_email.csv" # Nombre del archivo CSV de salida con duplicados eliminados

API_ENDPOINT = "https://www.covermanager.com/api/clients/clients_list"
OUTPUT_FILENAME = "todos_clientes_covermanager.csv"

# Definir los nombres de las columnas que esperamos en el CSV
# Asegúrate de que estas coincidan exactamente con las claves en tus objetos de cliente
FIELDNAMES = ['first_name', 'last_name', 'int_call_code', 'phone', 'email', 'language', 'subscribe_newsletter', 'id_client', 'date_upd', 'user_birth', 'country', 'membership_number']

# --- Función para obtener una página de clientes ---
def get_clients_page(api_key, restaurant_slug, page_number):
    headers = {
        "Content-Type": "application/json",
        "apikey": api_key
    }
    payload = {
        "restaurant": restaurant_slug,
        "page": str(page_number)
    }

    print(f"Solicitando página {page_number} para el restaurante {restaurant_slug}...")
    try:
        response = requests.post(API_ENDPOINT, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        data = response.json()

        # MODIFICACIÓN CLAVE AQUÍ: Aceptar 'OK' o 1 como respuesta exitosa
        if data.get("resp") in ("OK", 1) and "clients" in data:
            return data["clients"]
        else:
            print(f"Error en la respuesta de la API en la página {page_number}: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API en la página {page_number}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error al decodificar la respuesta JSON en la página {page_number}: {e}")
        print(f"Contenido de la respuesta: {response.text}")
        return None

# --- Bucle principal para obtener y guardar clientes ---
page = 0
total_clients_saved = 0
file_exists = os.path.exists(OUTPUT_FILENAME)

# Lista para guardar todos los nombres de campo encontrados, incluyendo los anidados como 'tag' (si es necesario)
# Por ahora, nos quedamos con los que sabemos de la respuesta
# NOTA: El campo 'tag' es un diccionario, si quieres guardarlo, necesitarás aplanarlo o decidir cómo representarlo en CSV.
# Para simplificar, he añadido los campos que veo directamente en tu ejemplo de cliente,
# excepto 'tag' por su complejidad como diccionario/lista de diccionarios.
# Si necesitas 'tag', deberíamos discutir cómo aplanarlo.

while True:
    clients_on_page = get_clients_page(YOUR_API_KEY, YOUR_RESTAURANT_SLUG, page)

    if clients_on_page is not None:
        if clients_on_page:
            # Abrir el archivo CSV en modo de añadir ('a'), o crear si no existe ('w' en el primer caso)
            with open(OUTPUT_FILENAME, 'a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)

                if not file_exists:
                    writer.writeheader()
                    file_exists = True

                for client in clients_on_page:
                    # Filtrar el cliente para incluir solo las claves que están en FIELDNAMES
                    # y manejar el caso de 'tag' que es un diccionario/lista y no un valor simple
                    processed_client = {}
                    for field in FIELDNAMES:
                        if field == 'tag': # Evitamos el campo 'tag' si es un diccionario complejo
                            processed_client[field] = json.dumps(client.get(field, '')) # Lo guardamos como JSON string
                        else:
                            processed_client[field] = client.get(field, '')

                    writer.writerow(processed_client)

            count_on_page = len(clients_on_page)
            total_clients_saved += count_on_page
            print(f"Página {page} descargada y guardada. Clientes en esta página: {count_on_page}. Total guardados: {total_clients_saved}")
            page += 1
            time.sleep(0.5)
        else:
            print(f"No se encontraron más clientes en la página {page}. Fin de la descarga.")
            break
    else:
        print("Se detuvo la descarga debido a un error en la obtención de una página.")
        break

print(f"\nProceso completado. Se han guardado un total de {total_clients_saved} clientes en '{OUTPUT_FILENAME}'")


def remove_duplicates_by_email(input_csv, output_csv, email_field_name='email'):
    """
    Lee un archivo CSV, elimina las filas duplicadas basándose en la columna de email,
    y escribe los resultados únicos en un nuevo archivo CSV.
    """
    unique_clients = []
    seen_emails = set()
    total_rows = 0
    duplicates_removed = 0

    print(f"Leyendo el archivo: '{input_csv}' para eliminar duplicados por email...")

    try:
        with open(input_csv, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)

            # Verificar que la columna de email exista en el archivo
            if email_field_name not in reader.fieldnames:
                print(f"Error: La columna '{email_field_name}' no se encontró en el archivo CSV de entrada.")
                print(f"Columnas disponibles: {reader.fieldnames}")
                return

            # Si el archivo de entrada tiene un orden de columnas diferente,
            # ajustamos FIELDNAMES para que coincida con el orden real del archivo.
            # Esto es crucial para csv.DictWriter.
            actual_fieldnames = reader.fieldnames

            for row in reader:
                total_rows += 1
                email = row.get(email_field_name, '').strip().lower() # Normalizar email (quitar espacios, minúsculas)

                # Si el email no está vacío y ya lo hemos visto, es un duplicado
                # Si el email está vacío, lo consideramos único a menos que la fila completa sea idéntica
                if email and email in seen_emails:
                    duplicates_removed += 1
                    # print(f"Duplicado encontrado y eliminado (email: '{email}'): {row}") # Opcional: para depuración
                else:
                    unique_clients.append(row)
                    if email: # Solo añadir a 'seen_emails' si no está vacío
                        seen_emails.add(email)

        print(f"Lectura completada. Total de filas leídas: {total_rows}")
        print(f"Total de duplicados eliminados (por email): {duplicates_removed}")
        print(f"Total de filas únicas a escribir: {len(unique_clients)}")

        # Escribir los clientes únicos en el nuevo archivo CSV
        with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=actual_fieldnames)
            writer.writeheader()
            writer.writerows(unique_clients)

        print(f"Archivo de clientes únicos guardado exitosamente en: '{output_csv}'")

    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{input_csv}' no se encontró. Asegúrate de que el nombre sea correcto y esté en el mismo directorio que el script.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

remove_duplicates_by_email(INPUT_FILENAME, OUTPUT_FILENAME_UNIQUE)
