from abia_azamon import *
from clases import *
from aima.search import hill_climbing, simulated_annealing


def crear_asignacion_por_prioridad(paquetes, ofertas):

    assig = StateRepresentation(paquetes, ofertas)

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
                if asignable(paquete, oferta, assig.peso_por_oferta[id_oferta]):
                    assig.coste_total_clientes += 5 if paquete.prioridad == 0 else 3 if paquete.prioridad == 1 else 1.5
                    assig.coste_total_ofertas += oferta.precio * paquete.peso
                    assig.peso_por_oferta[id_oferta] += paquete.peso
                    assig.oferta_por_paquete[paquetes.index(paquete)] = id_oferta
                    asignado = True
                    
                    # Calcula el coste de almacenamiento
                    if oferta.dias in [3, 4]:
                        assig.coste_almacenamiento += paquete.peso * assig.coste_por_kg_dia * 1
                    elif oferta.dias == 5:
                        assig.coste_almacenamiento += paquete.peso * assig.coste_por_kg_dia * 2
                        
                        
                    # Calcula la felicidad
                    dias_esperados = 1 if paquete.prioridad == 0 else 3 if paquete.prioridad == 1 else 5
                    dias_avanzados = dias_esperados - oferta.dias
                    assig.total_dias_avanzados += dias_avanzados
                                         
                    break
                
                    
                
            if not asignado:
                print(f"Paquete {paquete} no pudo ser asignado a ninguna oferta")
    
    return assig


def estado_inicial_por_prioridad(semilla, n_paq):
    paquetes = random_paquetes(n_paq, semilla)
    ofertas = random_ofertas(paquetes, 1.2, semilla) 

    inspeccionar_paquetes(paquetes)
    inspeccionar_ofertas(ofertas)
    
    estado_inicial = crear_asignacion_por_prioridad(paquetes, ofertas)
    
    estado_inicial.coste_almacenamiento = round(estado_inicial.coste_almacenamiento, 2)
    estado_inicial.coste_total_ofertas = round(estado_inicial.coste_total_ofertas, 2)
    
    print(estado_inicial.peso_por_oferta)
    
    print("Pesos acumulados finales por oferta:")
    for id_oferta, peso in enumerate(estado_inicial.peso_por_oferta):
        print(f'{id_oferta} {ofertas[id_oferta]}  -> {peso} / {ofertas[id_oferta].pesomax}')
        print(f"Oferta {id_oferta} -> Peso acumulado: {peso} / {ofertas[id_oferta].pesomax}")
    
    if not estado_inicial.oferta_por_paquete:
        print("No se pudo encontrar una solución válida")
    else:
        print('\n')
        print("Solución válida encontrada")
        print(f'Coste de almacenamiento {estado_inicial.coste_almacenamiento} €')
        print(f'Coste total de ofertas {estado_inicial.coste_total_ofertas} €')
        print(f'Coste total clientes {estado_inicial.coste_total_clientes} €')
        print('\n')
        print(f'Beneficio final: {estado_inicial.coste_total_clientes - estado_inicial.coste_total_ofertas - estado_inicial.coste_almacenamiento} €')
        
    return estado_inicial
    


if __name__ == "__main__":
    
    estado_actual = estado_inicial_por_prioridad(222234, 10)
    
    beta = 1.0
    alpha = 1.0
    
    problema = Problema(estado_actual, beta, alpha)
    solucion = simulated_annealing (problema)
    
    
    print("Solución encontrada:")
    print(solucion)
    print("Valor de la heurística de la solución:")
    print(solucion.heuristic(beta, alpha))
    #print(problema.value(solucion))
    
    


