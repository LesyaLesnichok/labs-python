from abc import ABC, abstractmethod

# Klasa abstrakcyjna
class Base(ABC):
    def __init__(self, name: str, year: int):
        self.name = name
        self.year = year

    @abstractmethod
    def info(self):
        pass

# Klasa Człowiek dziedzicząca po Base
class Czlowiek(Base):
    def __init__(self, name: str, year: int, profession: str):
        super().__init__(name, year)
        self.profession = profession  # Nowe pole - zawód

    def info(self):
        return f"Człowiek: {self.name}, Rok urodzenia: {self.year}, Zawód: {self.profession}"

# Klasa Zwierzę dziedzicząca po Base
class Zwierze(Base):
    def __init__(self, name: str, year: int, species: str):
        super().__init__(name, year)
        self.species = species  # Nowe pole - gatunek

    def info(self):
        return f"Zwierzę: {self.name}, Rok urodzenia: {self.year}, Gatunek: {self.species}"

# Tworzenie obiektów
czlowiek = Czlowiek(name="Jan Kowalski", year=1990, profession="Inżynier")
zwierze = Zwierze(name="Reksio", year=2015, species="Pies")

# Wypisywanie informacji
print(czlowiek.info())
print(zwierze.info())