# Programa que analiza un texto introducido por el usuario
# Muestra el número total de palabras y la frecuencia de cada una (de mayor a menor)
# Guardamos el analisis en un archivo

import string  # Módulo necesario para acceder a los signos de puntuación estándar
from datetime import datetime  # Para guardar la fecha y hora del análisis


# Pedimos al usuario que introduzca un texto
texto = input('Introduce un texto:\n')

# Eliminamos signos de puntuación usando str.translate y string.punctuation
# str.maketrans('', '', string.punctuation) crea una tabla que elimina todos los signos como . , ; ! etc.
texto_sin_puntuacion = texto.translate(str.maketrans('', '', string.punctuation))

# Convertimos el texto limpio en una lista de palabras
palabras_crudas = texto_sin_puntuacion.split()

# Filtramos palabras: solo dejamos las que están compuestas completamente por letras
palabras = [p.lower() for p in palabras_crudas if p.isalpha()]
n_palabras = len(palabras)
print(f'\nEl texto tiene {n_palabras} palabras válidas (sin contar números ni símbolos).\n')


# Creamos un diccionario para contar cuántas veces aparece cada palabra
# Contamos la frecuencia de cada palabra (todo en minúsculas)
frecuencias = {}
for palabra in palabras:
    palabra = palabra.lower()
    frecuencias[palabra] = frecuencias.get(palabra, 0) + 1

# Ordenamos el diccionario por frecuencia (valor) de mayor a menor

frecuencias_ordenadas = sorted(frecuencias.items(), key=lambda item: item[1], reverse=True)

# Mostramos la frecuencia ordenada
print("Frecuencia de cada palabra (de mayor a menor):")
for palabra, cantidad in frecuencias_ordenadas:
    print(f'{palabra}: {cantidad}')

# Guardamos en archivo (modo "append")
with open('frecuencias_palabras.txt', 'a', encoding='utf-8') as f:
    f.write('==============================\n')
    f.write(f'Nuevo análisis realizado el {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
    f.write('==============================\n')
    f.write(f'Texto analizado:\n{texto}\n\n')
    f.write(f'Número total de palabras válidas: {n_palabras}\n\n')
    f.write('Frecuencia de cada palabra (de mayor a menor):\n')
    for palabra, cantidad in frecuencias_ordenadas:
        f.write(f'{palabra}: {cantidad}\n')
    f.write('\n\n')

print('\nEl análisis se ha guardado en el archivo "frecuencias_palabras.txt".')