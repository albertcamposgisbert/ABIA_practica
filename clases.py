from abia_azamon import *
from aima.search import Problem
from copy import deepcopy
import random

class Operator(object):
    pass

class MovePackage(Operator):
    def __init__(self, p: Paquete, of: Oferta):
        self.paq = p
        self.of_dest = of

    def __repr__(self) -> str:
        return f"Cambiar el paquete {self.p} de la oferta {self.of1} a la oferta {self.of2}"

class SwapPackages(Operator):
    def __init__(self, p1: Paquete, p2: Paquete):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self) -> str:
        return f"Cambiar dos paquetes {self.p1} y {self.p2} entre les seves ofertes"
    

class StateRepresentation(object):
    def __init__(self, paquetes: List[Paquete], ofertas: List[Oferta]):
        self.paquetes = paquetes
        self.ofertas = ofertas

        self.peso_por_oferta = [0.0] * len(ofertas) # Peso total por cada oferta
        self.oferta_por_paquete = [None] * len(paquetes) # Asignación de oferta para cada paquete
        self.coste_almacenamiento = 0.0
        self.coste_total_ofertas = 0.0
        self.coste_total_clientes = 0.0
        self.coste_por_kg_dia = 0.25
        self.total_dias_avanzados = 0

    def __repr__(self) -> str:
        paquetes_info = "\n".join([f"Paquete {i}: {paquete}" for i, paquete in enumerate(self.paquetes)])
        ofertas_info = "\n".join([f"Oferta {i}: {oferta}" for i, oferta in enumerate(self.ofertas)])
        peso_por_oferta_info = "\n".join([f"Oferta {i}: {peso} kg" for i, peso in enumerate(self.peso_por_oferta)])
        asignaciones_info = "\n".join([f"Paquete {i} -> Oferta {oferta}" for i, oferta in enumerate(self.oferta_por_paquete) if oferta is not None])
        
        return (
            f"--- Solución final ---\n"
            #f"Paquetes:\n{paquetes_info}\n\n"
            #f"Ofertas:\n{ofertas_info}\n\n"
            f"Peso total por oferta:\n{peso_por_oferta_info}\n\n"
            f"Asignación de ofertas por paquete:\n{asignaciones_info}\n\n"
            f"Días avanzados (felicidad):\n{self.total_dias_avanzados}\n\n"
            f"Costes:\n"
            f"  - Coste de almacenamiento: {self.coste_almacenamiento:.2f} €\n"
            f"  - Coste total de ofertas: {self.coste_total_ofertas:.2f} €\n"
            f"  - Coste total clientes: {self.coste_total_clientes:.2f} €\n"
            f"  - Coste por kg/día de almacenamiento: {self.coste_por_kg_dia:.2f} €\n"
            f"--------------------------------------"
        )



    def copy(self):
        """Devuelve una copia profunda del estado actual."""
        # Crea una copia profunda de los paquetes y las ofertas para que no apunten a los mismos objetos
        paquetes_copy = deepcopy(self.paquetes)
        ofertas_copy = deepcopy(self.ofertas)
        
        # Crear una nueva instancia de StateRepresentation con los paquetes y ofertas copiados
        new_state = StateRepresentation(paquetes_copy, ofertas_copy)
        
        # Copia profunda de listas y variables para asegurar independencia
        new_state.peso_por_oferta = self.peso_por_oferta[:]
        new_state.oferta_por_paquete = self.oferta_por_paquete[:]
        new_state.coste_almacenamiento = self.coste_almacenamiento
        new_state.coste_total_ofertas = self.coste_total_ofertas
        new_state.coste_total_clientes = self.coste_total_clientes
        new_state.coste_por_kg_dia = self.coste_por_kg_dia
        new_state.total_dias_avanzados = self.total_dias_avanzados

        
        return new_state


    def generate_actions(self):
        # Recorregut per ofertes i paquets per saber quins podem moure:

        for oferta in self.ofertas:
            for paquete in self.paquetes:
                # Condició: oferta diferent i té espai per al paquet
                if asignable(paquete, oferta, self.peso_por_oferta[self.ofertas.index(oferta)]):
                    yield MovePackage(paquete, oferta)

        # Intercanviar paquets
        for i, paq1 in enumerate(self.paquetes):
            for j, paq2 in enumerate(self.paquetes[i+1:], i+1):
                id_oferta1 = self.oferta_por_paquete[i]
                id_oferta2 = self.oferta_por_paquete[j]
                
                    
                if (id_oferta1 != id_oferta2 and asignable(paq1, self.ofertas[id_oferta2], self.peso_por_oferta[id_oferta2] - paq2.peso) and \
                asignable(paq2, self.ofertas[id_oferta1], self.peso_por_oferta[id_oferta1] - paq1.peso)):
                    yield SwapPackages(paq1, paq2)

    def generate_one_action_sa(self):

        # Recorregut per ofertes i paquets per saber quins podem moure:
        move_parcel_combinations = set()
        for oferta in self.ofertas:
            for paquete in self.paquetes:
                # Condició: oferta diferent i té espai per al paquet
                if asignable(paquete, oferta, self.peso_por_oferta[self.ofertas.index(oferta)]):
                    move_parcel_combinations.add((paquete, oferta))

        # Intercanviar paquets
        swap_parcels_combinations = set()
        for paquete1 in self.paquetes:
                for paquete2 in self.paquetes:
                    # Condición: son paquetes distintos y son asignables a las ofertas del otro
                    if paquete1 != paquete2:
                        id_oferta1 = self.oferta_por_paquete[self.paquetes.index(paquete1)]
                        id_oferta2 = self.oferta_por_paquete[self.paquetes.index(paquete2)]

                        if id_oferta1 != id_oferta2 and asignable(paquete1, self.ofertas[id_oferta2], self.peso_por_oferta[id_oferta2]) and \
                            asignable(paquete2, self.ofertas[id_oferta1], self.peso_por_oferta[id_oferta1]):
                            swap_parcels_combinations.add((paquete1, paquete2))

        n = len(move_parcel_combinations)
        m = len(swap_parcels_combinations)
        random_value = random.random()
        if random_value < (n / (n + m)):
            combination = random.choice(list(move_parcel_combinations))
            yield MovePackage(combination[0], combination[1])
        else:
            combination = random.choice(list(swap_parcels_combinations))
            yield SwapPackages(combination[0], combination[1])
                        

    def apply_action(self, action: Operator):
        new_state = self.copy()
        if isinstance(action, MovePackage):
            paq = action.paq
            of = action.of_dest

            # Resta peso y coste de la oferta actual
            id_oferta_actual = new_state.oferta_por_paquete[self.paquetes.index(paq)]
            new_state.peso_por_oferta[id_oferta_actual] -= paq.peso
            new_state.coste_total_ofertas -= self.ofertas[id_oferta_actual].precio * paq.peso

            # Suma el peso y coste de la nueva oferta
            id_oferta_nueva = self.ofertas.index(of)
            new_state.oferta_por_paquete[self.paquetes.index(paq)] = id_oferta_nueva
            new_state.peso_por_oferta[id_oferta_nueva] += paq.peso
            new_state.coste_total_ofertas += self.ofertas[id_oferta_nueva].precio * paq.peso

            
            # Resta los días avanzados de la oferta actual
            dias_esperados = 1 if paq.prioridad == 0 else 3 if paq.prioridad == 1 else 5
            dias_avanzados_actual = dias_esperados - self.ofertas[id_oferta_actual].dias
            new_state.total_dias_avanzados -= dias_avanzados_actual
                
            # Suma los días avanzados de la nueva oferta
            dias_avanzados_nueva = dias_esperados - self.ofertas[id_oferta_nueva].dias
            new_state.total_dias_avanzados += dias_avanzados_nueva

            
        
        elif isinstance(action, SwapPackages):
            paq1 = action.p1
            paq2 = action.p2
            index_paq1 = self.paquetes.index(paq1)
            index_paq2 = self.paquetes.index(paq2)

            # Obtener las ofertas actuales usando los índices guardados
            id_oferta1 = new_state.oferta_por_paquete[index_paq1]
            id_oferta2 = new_state.oferta_por_paquete[index_paq2]

            # Resta pesos y costes de las ofertas actuales
            new_state.peso_por_oferta[id_oferta1] -= paq1.peso
            new_state.peso_por_oferta[id_oferta2] -= paq2.peso
            new_state.coste_total_ofertas -= new_state.ofertas[id_oferta1].precio * paq1.peso
            new_state.coste_total_ofertas -= new_state.ofertas[id_oferta2].precio * paq2.peso

            # Intercambia ofertas usando los índices guardados
            new_state.oferta_por_paquete[index_paq1] = id_oferta2
            new_state.oferta_por_paquete[index_paq2] = id_oferta1
            
            # Suma pesos y costes de las nuevas ofertas
            new_state.peso_por_oferta[id_oferta1] += paq2.peso
            new_state.peso_por_oferta[id_oferta2] += paq1.peso
            new_state.coste_total_ofertas += new_state.ofertas[id_oferta1].precio * paq2.peso
            new_state.coste_total_ofertas += new_state.ofertas[id_oferta2].precio * paq1.peso

            # Resta la felicidad del cliente antes de intercambiar los paquetes
            dias_esperados1 = 1 if paq1.prioridad == 0 else 3 if paq1.prioridad == 1 else 5
            dias_esperados2 = 1 if paq2.prioridad == 0 else 3 if paq2.prioridad == 1 else 5
            dias_avanzados1_actual = dias_esperados1 - new_state.ofertas[id_oferta1].dias
            dias_avanzados2_actual = dias_esperados2 - new_state.ofertas[id_oferta2].dias
            new_state.total_dias_avanzados -= dias_avanzados1_actual
            new_state.total_dias_avanzados -= dias_avanzados2_actual
            
            # Suma la felicidad del cliente después de intercambiar los paquetes
            dias_avanzados1_nueva = dias_esperados1 - new_state.ofertas[id_oferta2].dias
            dias_avanzados2_nueva = dias_esperados2 - new_state.ofertas[id_oferta1].dias
            new_state.total_dias_avanzados += dias_avanzados1_nueva
            new_state.total_dias_avanzados += dias_avanzados2_nueva

        return new_state
    
    def heuristic_cost(self) -> float:
        coste_total = self.coste_total_ofertas + self.coste_almacenamiento
        return 1*coste_total
    
    def heuristic_con_felicidad(self) -> float:
        coste_total = self.coste_total_ofertas + self.coste_almacenamiento
        return 1*coste_total - 2 * self.total_dias_avanzados
  
    
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


class Problema(Problem):
    def __init__(self, initial_state: StateRepresentation):
        super().__init__(initial_state)

    def actions(self, state: StateRepresentation):
        return state.generate_actions()

    def result(self, state: StateRepresentation, action: Operator) -> StateRepresentation:
        return state.apply_action(action)

    def value(self, state: StateRepresentation) -> float:
        return -state.heuristic_cost()

    def goal_test(self, state: StateRepresentation) -> bool:
        return False
    
