from abia_azamon import *
from clases import *

from aima.search import hill_climbing
import random

class EstadoInicialAleatorio:
    def __init__(self, semilla: int, n_paq: int, factor_ofertas: float = 1.2):
        self.semilla = semilla
        self.n_paq = n_paq
        self.factor_ofertas = factor_ofertas
        self.paquetes = random_paquetes(n_paq, semilla)
        self.ofertas = random_ofertas(self.paquetes, factor_ofertas, semilla)
        self.estado_inicial = self.crear_asignacion_aleatoria()
        self.total_dias_avanzados = 0

    def crear_asignacion_aleatoria(self) -> StateRepresentation:
        random.seed(self.semilla)
        assig = StateRepresentation(self.paquetes, self.ofertas)

        # Ordenar las ofertas por días de entrega y capacidad, manteniendo los índices originales
        ofertas_ordenadas = sorted(enumerate(self.ofertas), key=lambda o: (o[1].dias, o[1].pesomax))

        # Asignar paquetes a ofertas aleatoriamente
        for paquete in self.paquetes:
            asignado = False
            random.shuffle(ofertas_ordenadas)
            for id_oferta, oferta in ofertas_ordenadas:
                if asignable(paquete, oferta, assig.peso_por_oferta[id_oferta]):
                    assig.coste_total_clientes += 5 if paquete.prioridad == 0 else 3 if paquete.prioridad == 1 else 1.5
                    assig.coste_total_ofertas += oferta.precio * paquete.peso
                    assig.peso_por_oferta[id_oferta] += paquete.peso
                    assig.oferta_por_paquete[self.paquetes.index(paquete)] = id_oferta
                    asignado = True
                    
                    # Calcular el coste de almacenamiento
                    if oferta.dias in [3, 4]:
                        assig.coste_almacenamiento += paquete.peso * assig.coste_por_kg_dia * 1
                    elif oferta.dias == 5:
                        assig.coste_almacenamiento += paquete.peso * assig.coste_por_kg_dia * 2

                    # Calcular la felicidad del cliente
                    dias_esperados = 1 if paquete.prioridad == 0 else 3 if paquete.prioridad == 1 else 5
                    dias_avanzados = dias_esperados - oferta.dias
                    assig.total_dias_avanzados += dias_avanzados
                    
                    break
            
            if not asignado:
                print(f"Paquete {paquete} no pudo ser asignado a ninguna oferta")

        
        return assig


class EstadoInicialPorPrioridad:
    def __init__(self, semilla: int, n_paq: int, factor_ofertas: float = 1.2):
        self.semilla = semilla
        self.n_paq = n_paq
        self.factor_ofertas = factor_ofertas
        self.paquetes = random_paquetes(n_paq, semilla)
        self.ofertas = random_ofertas(self.paquetes, factor_ofertas, semilla)
        self.estado_inicial = self.crear_asignacion_por_prioridad()
        self.total_dias_avanzados = 0

    def crear_asignacion_por_prioridad(self) -> StateRepresentation:
        assig = StateRepresentation(self.paquetes, self.ofertas)

        # Agrupar paquetes por prioridad
        paquetes_por_prioridad = [
            [p for p in self.paquetes if p.prioridad == 0],
            [p for p in self.paquetes if p.prioridad == 1],
            [p for p in self.paquetes if p.prioridad == 2]
        ]

        # Ordenar las ofertas por días de entrega y capacidad, manteniendo los índices originales
        ofertas_ordenadas = sorted(enumerate(self.ofertas), key=lambda o: (o[1].dias, o[1].pesomax))

        # Asignar paquetes a ofertas por prioridad
        for paquetes_prioridad in paquetes_por_prioridad:
            for paquete in paquetes_prioridad:
                asignado = False
                for id_oferta, oferta in ofertas_ordenadas:
                    if asignable(paquete, oferta, assig.peso_por_oferta[id_oferta]):
                        assig.coste_total_clientes += 5 if paquete.prioridad == 0 else 3 if paquete.prioridad == 1 else 1.5
                        assig.coste_total_ofertas += oferta.precio * paquete.peso
                        assig.peso_por_oferta[id_oferta] += paquete.peso
                        assig.oferta_por_paquete[self.paquetes.index(paquete)] = id_oferta
                        asignado = True
                        
                        # Calcular el coste de almacenamiento
                        if oferta.dias in [3, 4]:
                            assig.coste_almacenamiento += paquete.peso * assig.coste_por_kg_dia * 1
                        elif oferta.dias == 5:
                            assig.coste_almacenamiento += paquete.peso * assig.coste_por_kg_dia * 2

                        # Calcular la felicidad del cliente
                        dias_esperados = 1 if paquete.prioridad == 0 else 3 if paquete.prioridad == 1 else 5
                        dias_avanzados = dias_esperados - oferta.dias
                        assig.total_dias_avanzados += dias_avanzados
                        
                        break
                
                if not asignado:
                    print(f"Paquete {paquete} no pudo ser asignado a ninguna oferta")
        
        return assig

    def __repr__(self) -> str:
        return (f"EstadoInicialPorPrioridad(\n"
                f"  semilla={self.semilla},\n"
                f"  n_paq={self.n_paq},\n"
                f"  factor_ofertas={self.factor_ofertas},\n"
                #f"  paquetes={self.paquetes},\n"
                f"  ofertas={self.ofertas},\n"
                f"  estado_inicial={self.estado_inicial}\n"
                f")")
    
    

if __name__ == "__main__":
    

    
    """
    estado_inicial_aleatorio = EstadoInicialAleatorio(semilla=222234, n_paq=10)
    estado_actual = estado_inicial_aleatorio.estado_inicial
    
    print(estado_inicial_aleatorio)
    
    problema = Problema(estado_actual)
    
    solucion = hill_climbing(problema)
    
    print("Solución encontrada:")
    print(solucion)
    print("Valor de la heurística de la solución:")
    print(problema.value(solucion))
    """
    
    
    
    estado_inicial_por_prioridad = EstadoInicialPorPrioridad(semilla=777777, n_paq=50)
    estado_actual = estado_inicial_por_prioridad.estado_inicial
    
    print(estado_inicial_por_prioridad)
    
    problema = Problema(estado_actual)
    solucion = hill_climbing (problema)
    
    
    print("Solución encontrada:")
    print(solucion)
    print("Valor de la heurística de la solución:")
    print(-problema.value(solucion))
    


