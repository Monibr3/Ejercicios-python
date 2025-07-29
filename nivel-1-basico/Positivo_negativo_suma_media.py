#Programa que pide números al usuario hasta que introduzca un cero
#Muestra por pantalla la cantidad de números positivos y negativos introducidos
# y sus respectivas sumas y medias
n=float(input("Introduce un número: "))
neg = 0
pos = 0
suma_neg = 0
suma_pos = 0
while n != 0:
    if n < 0:
        neg += 1
        suma_neg+=n
    else:
        pos += 1
        suma_pos +=n
    n=float(input("Introduce un número(0 para salir): "))
print(f'Positivos {pos}\nNegativos {neg}')
print(f'Suma positivos = {suma_pos}\nSuma negativos = {suma_neg}')

if pos > 0:
    print(f"Media positivos = {suma_pos / pos}")
else:
    print("No se introdujeron números positivos")

if neg > 0:
    print(f"Media negativos = {suma_neg / neg}")
else:
    print("No se introdujeron números negativos")