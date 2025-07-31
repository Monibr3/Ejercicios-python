#Programa que analiza una palabra o frase introducida por el usuario
#y comprueba si es un palindromo(se lee igual al derecho y al revés),
#ignora espacios, mayusculas y signos

import string  # Módulo necesario para acceder a los signos de puntuación estándar
# Pedimos al usuario que introduzca una palabra o un texto

texto = input('Introduce un texto o una palabra y te diré si es o no un palindromo:\n')

## Limpiamos: eliminamos puntuación, espacios y lo pasamos a minúsculas
texto_limpio = texto.translate(str.maketrans('', '', string.punctuation))  # quita signos
texto_limpio = texto_limpio.replace(" ", "")  # quita espacios
texto_limpio = texto_limpio.lower()  # pasa a minúsculas

# NOTA: Este programa considera acentos como letras diferentes (no se eliminan).
#       Por tanto, "mamá" no es igual a "mama" y puede afectar el análisis.

if texto_limpio == texto_limpio[::-1]:# comparamos el texto y su inverso
    print(f'"{texto}" es un palíndromo')
else:
    print(f'"{texto}" no es un palíndromo')
