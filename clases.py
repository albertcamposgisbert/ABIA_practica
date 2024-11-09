from abia_azamon import *
from main import *

class Operator(object):
    pass

class MovePackage(Operator):
    def __init__(self, p: Paquete, of: Oferta):
        self.paq = p
        self.of_dest = of

    def __repr__(self) -> str:
        return f"Cambbiar el paquete {self.p} de la oferta {self.of1} a la oferta {self.of2}"

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

        
        return new_state

    def __repr__(self) -> str:
        return f"v_c={str(self.v_c)} | {self.params}"

    def generate_actions(self):
        # Recorregut per ofertes i paquets per saber quins podem moure:

        for id_oferta in self.ofertas:
            for paquete in self.paquetes:
                # Condició: oferta diferent i té espai per al paquet
                if asignable(paquete, self.ofertas[id_oferta], self.peso_por_oferta[id_oferta]):
                    yield MovePackage(paquete, self.ofertas[id_oferta])

        # Intercanviar paquets
        for paquete1 in self.paquetes:
            for paquete2 in self.paquetes:
                # Condición: son paquetes distintos y son asignables a las ofertas del otro
                if paquete1 != paquete2:
                    id_oferta1 = self.oferta_por_paquete[paquetes.index(paquete1)]
                    id_oferta2 = self.oferta_por_paquete[paquetes.index(paquete2)]
                    if asignable(paquete1, self.ofertas[id_oferta2], self.peso_por_oferta[id_oferta2]) and asignable(paquete2, self.ofertas[id_oferta1], self.peso_por_oferta[id_oferta1]):
                        yield SwapPackages (paquete1, paquete2)
                        

    def apply_action(self, action: Operator):
        new_state = self.copy()
        if isinstance(action, MovePackage):
            paq = action.paq
            of = action.of_dest

            new_state.peso_por_oferta[new_state.oferta_por_paquete[paquetes.index(paq)]] = new_state.peso_por_oferta[new_state.oferta_por_paquete[paquetes.index(paq)]] - paq.peso
            id_oferta = self.ofertas.index(of)
            new_state.oferta_por_paquete[paquetes.index(paq)] = id_oferta
            new_state.peso_por_oferta[id_oferta] = self.peso_por_oferta[id_oferta] + paq.peso
            
            new_state.coste_total_ofertas = self.coste_total_ofertas - self.ofertas[self.oferta_por_paquete[paquetes.index(paq)]].precio * paq.peso + of.precio * paq.peso
            
            # Resta peso y coste de la oferta actual
            id_oferta_actual = new_state.oferta_por_paquete[self.paquetes.index(paq)]
            new_state.peso_por_oferta[id_oferta_actual] -= paq.peso
            new_state.coste_total_ofertas -= self.ofertas[id_oferta_actual].precio * paq.peso

            # Suma el peso y coste de la nueva oferta
            id_oferta_nueva = self.ofertas.index(of)
            new_state.oferta_por_paquete[self.paquetes.index(paq)] = id_oferta_nueva
            new_state.peso_por_oferta[id_oferta_nueva] += paq.peso
            new_state.coste_total_ofertas += self.ofertas[id_oferta_nueva].precio * paq.peso
                
                
            
        
        elif isinstance(action, SwapPackages):
            paq1 = action.p1
            paq2 = action.p2

            id_oferta1 = new_state.oferta_por_paquete[self.paquetes.index(paq1)]
            id_oferta2 = new_state.oferta_por_paquete[self.paquetes.index(paq2)]

            # Resta pesos y costes de las ofertas actuales
            new_state.peso_por_oferta[id_oferta1] -= paq1.peso
            new_state.peso_por_oferta[id_oferta2] -= paq2.peso
            new_state.coste_total_ofertas -= self.ofertas[id_oferta1].precio * paq1.peso
            new_state.coste_total_ofertas -= self.ofertas[id_oferta2].precio * paq2.peso

            # Intercambia ofertas
            new_state.oferta_por_paquete[self.paquetes.index(paq1)] = id_oferta2
            new_state.oferta_por_paquete[self.paquetes.index(paq2)] = id_oferta1
            
            # Suma pesos y costes de las nuevas ofertas
            new_state.peso_por_oferta[id_oferta1] += paq2.peso
            new_state.peso_por_oferta[id_oferta2] += paq1.peso
            new_state.coste_total_ofertas += self.ofertas[id_oferta1].precio * paq2.peso
            new_state.coste_total_ofertas += self.ofertas[id_oferta2].precio * paq1.peso


        return new_state
        
        
    def heuristic(self) -> float:
            pass

# USO AIMA (aún está con los param del BinPacking)
# class Problem(Problem):
#     def __init__(self, initial_state: StateRepresentation):
#         super().__init__(initial_state)

#     def actions(self, state: StateRepresentation) -> Generator[BinPackingOperator, None, None]:
#         return state.generate_actions()

#     def result(self, state: StateRepresentation, action: BinPackingOperator) -> StateRepresentation:
#         return state.apply_action(action)

#     def value(self, state: StateRepresentation) -> float:
#         return -state.heuristic()

#     def goal_test(self, state: StateRepresentation) -> bool:
#         return False
    

######################