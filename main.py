from abia_azamon import *

paquetes = []  # Atr: peso, prioridad
ofertas = []  # Atr: preciomax, peso, dias
peso_por_oferta = []
lista_paquetes_ofertas = []  # Cada elemento es la oferta y el indice el id del paquete

def asignable(paquete, oferta):
    return not ((paquete.prioridad != 0 or oferta.dias != 1)
                and (paquete.prioridad != 1 or oferta.dias != 2)
                and (paquete.prioridad != 1 or oferta.dias != 3)
                and (paquete.prioridad != 2 or oferta.dias != 4)
                and (paquete.prioridad != 2 or oferta.dias != 5))

def verifica_solucion(peso_por_oferta, ofertas):
    for id_oferta, peso in enumerate(peso_por_oferta):
        if peso > ofertas[id_oferta].pesomax:
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

    # Ordenar las ofertas por días de entrega y capacidad
    ofertas_ordenadas = sorted(ofertas, key=lambda o: (o.dias, o.pesomax))

    # Asignar paquetes a ofertas por prioridad
    for paquetes_prioridad in paquetes_por_prioridad:
        for paquete in paquetes_prioridad:
            asignado = False
            for id_oferta, oferta in enumerate(ofertas_ordenadas):
                if asignable(paquete, oferta) and paquete.peso + peso_por_oferta[id_oferta] <= oferta.pesomax:
                    peso_por_oferta[id_oferta] += paquete.peso
                    oferta_por_paquete[paquetes.index(paquete)] = id_oferta
                    asignado = True
                    break
            if not asignado:
                return []  # No se pudo asignar el paquete a ninguna oferta

    print("debug:")
    for id_paquete, id_oferta in enumerate(oferta_por_paquete):
        print(f"Paquete {id_paquete} -> Oferta {id_oferta}")
        
    print(peso_por_oferta)

    if not verifica_solucion(peso_por_oferta, ofertas):
        return []

    return oferta_por_paquete

def estado_inicial_por_prioridad(semilla, n_paq):
    global paquetes, ofertas, lista_paquetes_ofertas
    paquetes = random_paquetes(n_paq, semilla)
    ofertas = random_ofertas(paquetes, 1.2, 1234) 
    # Parametros: Lista de paquetes, Proporción, semilla

    inspeccionar_paquetes(paquetes)
    inspeccionar_ofertas(ofertas)
    lista_paquetes_ofertas = crear_asignacion_por_prioridad(paquetes, ofertas)
    if not lista_paquetes_ofertas:
        print("No se pudo encontrar una solución válida")
    else:
        print("Solución válida encontrada")

# Operador
def set_peso_por_oferta(paquete, id_oferta):
    peso_por_oferta[id_oferta] += paquete.peso

# Heurísticas
def puntuación_felicidad():
    pass

def puntuación_coste():
    pass

def puntuación_total():
    pass

if __name__ == "__main__":
    estado_inicial_por_prioridad(1234, 5)
    inspeccionar_paquetes(paquetes)
    inspeccionar_ofertas(ofertas)
    
    print("Lista de paquetes y sus ofertas asignadas:")
    for id_paquete, id_oferta in enumerate(lista_paquetes_ofertas):
        print(f"Paquete {id_paquete} -> Oferta {id_oferta}")
    
    print("Detalles de los paquetes:")
    for paquete in paquetes:
        print(paquete)
    
    print("Detalles de las ofertas:")
    for oferta in ofertas:
        print(oferta)