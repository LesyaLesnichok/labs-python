# Importujemy moduł abc (Abstract Base Classes)
from abc import ABC, abstractmethod
# Definiujemy klasę abstrakcyjną Shape dziedziczącą po ABC
class Base(ABC):
    # Definiujemy metodę abstrakcyjną area, którą muszą implementować klasy dziedziczące
    @abstractmethod
    def area(self):
        pass

    # Definiujemy inną metodę abstrakcyjną perimeter
    @abstractmethod
    def perimeter(self):
        pass

class Rectangle(Base):
    # Konstruktor przyjmuje długość i szerokość prostokąta
    def __init__(self, length, width):
        # Przypisanie atrybutów instancji
        self.length = length
        self.width = width

    # Implementujemy wymaganą metodę area
    def area(self):
        # Zwracamy pole powierzchni prostokąta
        return self.length * self.width

    # Implementujemy wymaganą metodę perimeter
    def perimeter(self):
        # Zwracamy obwód prostokąta
        return 2 * (self.length + self.width)


rect = Rectangle(4, 5)
print("Pole prostokąta:", rect.area())        # Pole prostokąta: 20
print("Obwód prostokąta:", rect.perimeter())  # Obwód prostokąta: 18