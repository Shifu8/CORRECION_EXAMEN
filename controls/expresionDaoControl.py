from controls.dao.daoAdapter import DaoAdapter
from models.expresion import Expresion
from controls.tda.stack.stack import Stack

class ExpresionDaoControl(DaoAdapter):
    def __init__(self):
        super().__init__(Expresion)
        self.__expresion = None

    @property
    def _expresion(self):
        if self.__expresion == None:
            self.__expresion = Expresion()   
        return self.__expresion
    
    @_expresion.setter
    def _expresion(self, value):
        self.__expresion = value

    def _lista(self):
        return self._list()
    
    @property
    def save(self):
        self._expresion._id = self._lista + 1  # Aquí asignas el ID
        self._save(self._expresion)
    
    def merge(self, pos):
        self._merge(self._expresion, pos)
        
    def calcular_expresion(self, expresion):
        operadores = {'+': lambda x, y: x + y,
                      '-': lambda x, y: x - y,
                      '*': lambda x, y: x * y,
                      '/': lambda x, y: x / y,
                      '^': lambda x, y: x ** y}

        pila = Stack()
        elementos = expresion.split()

        for elemento in elementos:
            if elemento.isdigit():
                pila.push(float(elemento))
            elif elemento in operadores:
                operand2 = pila.pop()
                operand1 = pila.pop()
                resultado = operadores[elemento](operand1, operand2)
                pila.push(resultado)

        return pila.pop()
        
    def guardar_expresion(self, expresion):
        resultado = self.calcular_expresion(expresion)
        self._expresion.expresion = expresion
        self._expresion.resultado = resultado
        self.save
        