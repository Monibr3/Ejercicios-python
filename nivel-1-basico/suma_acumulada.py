# se introducen por pantalla números hasta que introducimos un cero,
# en ese momento se muentra por pantalla la suma total
n = int(input("introduce un número 2: "))
suma = 0
while n!=0 :
    suma = suma + n
    n = int(input("introduce un otro número:  "))
print(f'la suma es {suma}')
