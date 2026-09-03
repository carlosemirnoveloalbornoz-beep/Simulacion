import simpy
import random
from colorama import Fore, Style

TIPOS_VEHICULO = {
    "Moto":       (1, 3),
    "Carro":      (3, 8),
    "Camioneta":  (5, 10),
    "Camion":     (8, 15),
}

estadisticas = []

def tiempo_de_carga(tipo):
    """Devuelve un tiempo de carga aleatorio según el tipo de vehículo."""
    minimo, maximo = TIPOS_VEHICULO.get(tipo, (3, 8))
    return random.randint(minimo, maximo)


def registrar_estadistica(nombre, tipo, llegada, inicio_carga, fin_carga):
    """Guarda los datos de un vehículo para el resumen final."""
    espera = inicio_carga - llegada
    duracion = fin_carga - inicio_carga
    estadisticas.append({
        "nombre": nombre,
        "tipo": tipo,
        "llegada": llegada,
        "espera": espera,
        "duracion": duracion,
        "salida": fin_carga,
    })


def vehiculo(env, nombre, tipo, bombas):
    """Proceso que simula la llegada, espera y carga de combustible de un vehículo."""
    llegada = env.now
    print(f"{env.now:.2f} - {nombre} ({tipo}) llega a la gasolinera")

    with bombas.request() as solicitud:
        yield solicitud
        inicio_carga = env.now
        espera = inicio_carga - llegada

        print(Fore.GREEN + f"{env.now:.2f} - {nombre} empieza a cargar combustible "
              f"(esperó {espera:.2f} min)" + Style.RESET_ALL)

        duracion = tiempo_de_carga(tipo)
        yield env.timeout(duracion)

        fin_carga = env.now
        print(f"{env.now:.2f} - {nombre} termina de cargar combustible "
              f"({duracion} min de carga)")

        registrar_estadistica(nombre, tipo, llegada, inicio_carga, fin_carga)


def generar_vehiculos(env, bombas, intervalo_max=4, cantidad=None):
    """
    Genera vehículos de forma continua con llegadas aleatorias.
    Si 'cantidad' se especifica, deja de generar tras ese número de vehículos.
    """
    contador = 0
    while cantidad is None or contador < cantidad:
        yield env.timeout(random.randint(1, intervalo_max))
        contador += 1
        tipo = random.choice(list(TIPOS_VEHICULO.keys()))
        nombre = f"{tipo}-{contador}"
        env.process(vehiculo(env, nombre, tipo, bombas))


def mostrar_resumen():
    """Imprime un resumen con las estadísticas de todos los vehículos atendidos."""
    if not estadisticas:
        print("No se atendió ningún vehículo.")
        return

    print("\n" + "=" * 55)
    print(Fore.CYAN + "RESUMEN DE LA SIMULACIÓN" + Style.RESET_ALL)
    print("=" * 55)

    total_espera = 0
    for v in estadisticas:
        print(f"{v['nombre']:<12} tipo={v['tipo']:<10} "
              f"llegada={v['llegada']:.2f}  espera={v['espera']:.2f}  "
              f"carga={v['duracion']:.2f}  salida={v['salida']:.2f}")
        total_espera += v["espera"]

    promedio_espera = total_espera / len(estadisticas)
    print("-" * 55)
    print(f"Vehículos atendidos: {len(estadisticas)}")
    print(f"Tiempo de espera promedio: {promedio_espera:.2f} min")
    print("=" * 55)


def main():
    random.seed(42)  
    env = simpy.Environment()
    bombas = simpy.Resource(env, capacity=2)

    env.process(vehiculo(env, "Carro-1", "Carro", bombas))
    env.process(vehiculo(env, "Carro-2", "Carro", bombas))
    env.process(vehiculo(env, "Moto-1", "Moto", bombas))
    env.process(vehiculo(env, "Camioneta-1", "Camioneta", bombas))

    # Generador de vehículos adicionales que llegan aleatoriamente
    env.process(generar_vehiculos(env, bombas, intervalo_max=4, cantidad=6))

    env.run(until=40)
    mostrar_resumen()


if __name__ == "__main__":
    main()
