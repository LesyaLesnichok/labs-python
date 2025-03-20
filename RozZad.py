from abc import ABC, abstractmethod

class Balwan(ABC):
    @abstractmethod
    def tworzenie_balwana(self):
        pass

    @abstractmethod
    def eliminacja_balwana(self):
        pass

class CyrkNaKolkach(Balwan):

    def tworzenie_balwana(self):
        return "Balwan powstal"

    def eliminacja_balwana(self):
        return "Balwan umarl"

class Cyrk(CyrkNaKolkach):
    pass


person = Cyrk()

print(person.tworzenie_balwana())
print(person.eliminacja_balwana())