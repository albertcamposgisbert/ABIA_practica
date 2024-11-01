from abia_azamon import *

paquetes = []  # Atr: peso, prioridad
ofertas = []  # Atr: preciomax, peso, dias
peso_por_oferta = []
lista_paquetes_ofertas = []  # Cada elemento es la oferta y el indice el id del paquete

def asignable(paquete, oferta, peso_acumulado):
    
    if paquete.peso + peso_acumulado > oferta.pesomax:
        return False
    
    if paquete.prioridad == 0 and oferta.dias != 1:
        return False
    if paquete.prioridad == 1 and oferta.dias not in [2, 3]:
        return False
    if paquete.prioridad == 2 and oferta.dias not in [4, 5]:
        return False
    
    return True

def crear_asignacion_por_prioridad(paquetes, ofertas):
    oferta_por_paquete = [None] * len(paquetes)
    peso_por_oferta = [0.0] * len(ofertas)

    # Agrupar paquetes por prioridad
    paquetes_por_prioridad = [
        [p for p in paquetes if p.prioridad == 0],
        [p for p in paquetes if p.prioridad == 1],
        [p for p in paquetes if p.prioridad == 2]
    ]

    ofertas_ordenadas = sorted(ofertas, key=lambda o: (o.dias, o.pesomax))

    # Asignar paquetes a ofertas por prioridad
    for paquetes_prioridad in paquetes_por_prioridad:
        for paquete in paquetes_prioridad:
            asignado = False
            for id_oferta, oferta in enumerate(ofertas_ordenadas):
                if asignable(paquete, oferta, peso_por_oferta[id_oferta]):
                    peso_por_oferta[id_oferta] += paquete.peso
                    oferta_por_paquete[paquetes.index(paquete)] = id_oferta
                    asignado = True
                    print(f"Paquete {paquete} asignado a oferta {id_oferta} (peso acumulado: {peso_por_oferta[id_oferta]} / {oferta.pesomax})")
                    break
            if not asignado:
                print(f"Paquete {paquete} no pudo ser asignado a ninguna oferta")
                return [], []

    return oferta_por_paquete, peso_por_oferta


def estado_inicial_por_prioridad(semilla, n_paq):
    global paquetes, ofertas, lista_paquetes_ofertas
    paquetes = random_paquetes(n_paq, semilla)
    ofertas = random_ofertas(paquetes, 1.2, semilla) 

    #inspeccionar_paquetes(paquetes)
    #inspeccionar_ofertas(ofertas)
    lista_paquetes_ofertas = crear_asignacion_por_prioridad(paquetes, ofertas)
    
    if not lista_paquetes_ofertas:
        print("No se pudo encontrar una solución válida")
    else:
        print("Solución válida encontrada")



# Operador; por implementar
def set_peso_por_oferta(paquete, id_oferta):
    peso_por_oferta[id_oferta] += paquete.peso

# Heurísticas
def puntuación_felicidad():
    pass

def puntuación_coste():
    pass

# lambda*coste + beta*felicidad
def puntuación_total():
    pass


if __name__ == "__main__":
    estado_inicial_por_prioridad(1234, 20)

    oferta_por_paquete, peso_por_oferta = crear_asignacion_por_prioridad(paquetes, ofertas)

    print("Pesos acumulados finales por oferta:")
    for id_oferta, peso in enumerate(peso_por_oferta):
        print(f"Oferta {id_oferta} -> Peso acumulado: {peso} / {ofertas[id_oferta].pesomax}")