# Programa que pide al usuario dos números enteros y devuelve totos los númreos primos que hay entre ellos

# Definimos una función para comprobar si un número es o no primo
def es_primo(n):
    if n <2 :
        return False
    # Comprobamos si el número es divisible por algún número mayor que 2 y menor que su raiz cuadrada
    for i in range(2,int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

#Primero pedimos al usuario que introduzca dos números (inicio y fin)
print('\nIntroduce dos números y te dire los números primos que hay entre ellos:\n')
inicio = int (input("Introduce el primer número del rango:\n"))
fin = int(input("Introduce el segundo número del rango: \n"))

while inicio> fin:# comprobamos que están en el orden correcto, sino ha de introducirlos otra vez
    print('Los números no están en el orden correcto, introducelos otra vez')
    inicio = int (input("Introduce el primer número del rango:\n"))
    fin = int(input("Introduce el segundo número del rango: \n"))   

# buscamos todos los números primos en ese rango
primos = []
for num in range (inicio, fin+1):
    if es_primo(num):
        primos.append(num)

#imprimimos el resultado
if primos:
    print(f"Números primos entre {inicio} y {fin}:")
    print(primos)
else:
    print(f"No hay números primos entre {inicio} y {fin}.")
