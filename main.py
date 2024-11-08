from abia_azamon import *


paquetes = []  # Atr: peso, prioridad
ofertas = []  # Atr: preciomax, peso, dias

peso_por_oferta = []
lista_paquetes_ofertas = []  # Cada elemento es la oferta y el indice el id del paquete



almacenaje = []


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
    global coste_almacenamiento
    coste_almacenamiento = 0.0
    coste_por_kg_dia = 0.25

    # Agrupar paquetes por prioridad
    paquetes_por_prioridad = [
        [p for p in paquetes if p.prioridad == 0],
        [p for p in paquetes if p.prioridad == 1],
        [p for p in paquetes if p.prioridad == 2]
    ]

    # Ordenar las ofertas por días de entrega y capacidad, manteniendo los índices originales
    ofertas_ordenadas = sorted(enumerate(ofertas), key=lambda o: (o[1].dias, o[1].pesomax)) # O precio?

    # Asignar paquetes a ofertas por prioridad
    for paquetes_prioridad in paquetes_por_prioridad:
        for paquete in paquetes_prioridad:
            asignado = False
            for id_oferta, oferta in ofertas_ordenadas:
                if asignable(paquete, oferta, peso_por_oferta[id_oferta]):
                    peso_por_oferta[id_oferta] += paquete.peso
                    oferta_por_paquete[paquetes.index(paquete)] = id_oferta
                    asignado = True
                    
                    # Calcular el coste de almacenamiento
                    if oferta.dias in [3, 4]:
                        coste_almacenamiento += paquete.peso * coste_por_kg_dia * 1
                    elif oferta.dias == 5:
                        coste_almacenamiento += paquete.peso * coste_por_kg_dia * 2
                        
                    break
                
            if not asignado:
                print(f"Paquete {paquete} no pudo ser asignado a ninguna oferta")

    return oferta_por_paquete, peso_por_oferta


def estado_inicial_por_prioridad(semilla, n_paq):
    global paquetes, ofertas, lista_paquetes_ofertas
    paquetes = random_paquetes(n_paq, semilla)
    ofertas = random_ofertas(paquetes, 1.2, semilla) 

    #inspeccionar_paquetes(paquetes)
    #inspeccionar_ofertas(ofertas)
    lista_paquetes_ofertas, peso_por_oferta = crear_asignacion_por_prioridad(paquetes, ofertas)
    
    print(peso_por_oferta)
    
    print("Pesos acumulados finales por oferta:")
    for id_oferta, peso in enumerate(peso_por_oferta):
        print(f'{id_oferta} {ofertas[id_oferta]}  -> {peso} / {ofertas[id_oferta].pesomax}')
        print(f"Oferta {id_oferta} -> Peso acumulado: {peso} / {ofertas[id_oferta].pesomax}")
    
    if not lista_paquetes_ofertas:
        print("No se pudo encontrar una solución válida")
    else:
        print("Solución válida encontrada")
        print(f'{coste_almacenamiento} €')



# Operador; por implementar
def set_peso_por_oferta(paquete, id_oferta):
    if peso_por_oferta[id_oferta] + paquete.peso > ofertas[id_oferta].pesomax:
        return False
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
    estado_inicial_por_prioridad(1234, 120)

