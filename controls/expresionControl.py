from models.expresion import Expresion
from controls.tda.linked.linkedList import Linked_List

class ExpresionControl:
    def __init__(self):
        self.__expresion = None
        self.__id_counter = 0
        self.__lista = Linked_List()
    
    @property
    def _expresion(self):
        if self.__expresion == None:
            self.__expresion = Expresion()
        return self.__expresion

    @_expresion.setter
    def _expresion(self, value):
        self.__expresion = value

    @property
    def _lista(self):
        return self.__lista

    @_lista.setter
    def _lista(self, value):
        self.__lista = value
        
    
    def save(self):
        self._expresion._id = self.__id_counter
        self._lista.add(self._expresion, self._lista._lenght)
       
    def eliminar(self, expresion_id):
        self._lista.delete(expresion_id)

