# Programa informático Tema 3 - Simulación
# Problema: simular la fila de una caja en una tienda
# Distribución: Exponencial
# Método: Transformada inversa  ->  X = -(1/lambda) * ln(U)

import random
import math


def generar_exponencial(tasa):
    # Genera un valor aleatorio exponencial con el método de transformada inversa
    u = random.random()          # número aleatorio entre 0 y 1
    while u == 0:                # evitamos que sea 0 porque ln(0) no existe
        u = random.random()
    x = -(1 / tasa) * math.log(u)
    return x


def pedir_numero(mensaje):
    # Pide un número al usuario y revisa que sea válido (mayor a 0)
    while True:
        try:
            numero = float(input(mensaje))
            if numero > 0:
                return numero
            else:
                print("El número debe ser mayor a 0. Intenta de nuevo.")
        except ValueError:
            print("Eso no es un número. Intenta de nuevo.")


# ---------------- PROGRAMA PRINCIPAL ----------------

print("=== SIMULACIÓN DE UNA CAJA DE TIENDA ===")
print("El tiempo entre llegadas y el tiempo de atención se generan")
print("con distribución exponencial (transformada inversa).\n")

# 1. Datos de entrada que escribe el usuario
clientes = int(pedir_numero("¿Cuántos clientes quieres simular? "))
llegadas_por_min = pedir_numero("¿Cuántos clientes llegan por minuto en promedio? (ej. 0.5): ")
minutos_atencion = pedir_numero("¿Cuántos minutos tarda en promedio la caja en atender a un cliente? (ej. 1.5): ")

# Convertimos el tiempo promedio de atención a tasa (lambda = 1 / promedio)
tasa_llegada = llegadas_por_min
tasa_servicio = 1 / minutos_atencion

# Aviso si la caja no alcanza a atender a todos
if tasa_llegada >= tasa_servicio:
    print("\nAviso: llegan más clientes de los que la caja puede atender,")
    print("por eso la fila va a crecer mucho.")

# 2. Proceso de simulación
tiempo_llegada = 0          # minuto en que llega el cliente
caja_libre_en = 0           # minuto en que la caja queda libre
suma_esperas = 0
espera_maxima = 0
clientes_que_esperaron = 0
tiempo_total_atencion = 0

print("\nCliente | Llegada | Espera | Atención | Sale")
print("-" * 50)

for i in range(1, clientes + 1):
    # tiempo que pasa desde el cliente anterior hasta este
    tiempo_entre_llegadas = generar_exponencial(tasa_llegada)
    tiempo_llegada = tiempo_llegada + tiempo_entre_llegadas

    # si la caja está ocupada, el cliente espera
    if caja_libre_en > tiempo_llegada:
        inicio_atencion = caja_libre_en
    else:
        inicio_atencion = tiempo_llegada

    espera = inicio_atencion - tiempo_llegada
    tiempo_atencion = generar_exponencial(tasa_servicio)
    salida = inicio_atencion + tiempo_atencion
    caja_libre_en = salida

    # guardamos datos para los resultados
    suma_esperas = suma_esperas + espera
    tiempo_total_atencion = tiempo_total_atencion + tiempo_atencion
    if espera > 0:
        clientes_que_esperaron = clientes_que_esperaron + 1
    if espera > espera_maxima:
        espera_maxima = espera

    print(f"{i:^7} | {tiempo_llegada:7.2f} | {espera:6.2f} | {tiempo_atencion:8.2f} | {salida:6.2f}")

# 3. Resultados (salida del programa)
espera_promedio = suma_esperas / clientes
porcentaje_esperaron = (clientes_que_esperaron / clientes) * 100
porcentaje_caja_ocupada = (tiempo_total_atencion / caja_libre_en) * 100

print("\n=== RESULTADOS DE LA SIMULACIÓN ===")
print(f"Clientes atendidos: {clientes}")
print(f"Tiempo total de la simulación: {caja_libre_en:.2f} minutos")
print(f"Espera promedio por cliente: {espera_promedio:.2f} minutos")
print(f"Espera máxima: {espera_maxima:.2f} minutos")
print(f"Clientes que tuvieron que esperar: {porcentaje_esperaron:.1f}%")
print(f"Porcentaje de tiempo que la caja estuvo ocupada: {porcentaje_caja_ocupada:.1f}%")