# Programa que pide introducir una lista de números separados por comas
# y devuelve un anlisis donde indica los que son pares, impares, positivos y negativos
# y también cual es mayor y menor junto con la media
numeros =[]
entrada = input('Introduce números separados por coma:')
numeros = [ int(n.strip()) for n in entrada.split(",")]
suma = 0
total = len(numeros)
par = 0
impar = 0
pos =0
neg =0 
media =0 
mayor =numeros[0]
menor =numeros[0]
for m in numeros:
    suma +=m
    if m%2 ==0:
        par += 1
    else:
        impar +=1
    if m > 0:
        pos += 1
    else:
        neg +=1
    if m>mayor:
        mayor = m
    if m< menor:
        menor = m
media = suma/total

print("\n Resultados del análisis:")
print(f'Números introducidos: {numeros}')
print(f'Pares: {par}\nImpares: {impar}\nPositivos: {pos}\nNegativos: {neg}\nMedia: {media}\nMayor: {mayor}\nMenor: {menor}')
