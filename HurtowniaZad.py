from abc import ABC, abstractmethod

class Sklep(ABC):
    @abstractmethod
    def zamow_material(self, material, ilosc):
        pass


class SklepDrewniany(Sklep):
    def zamow_material(self, material, ilosc):
        return f"Sklep drewniany zamawia {ilosc} jednostek {material}"


class SklepBudowlany(Sklep):
    def zamow_material(self, material, ilosc):
        return f"Sklep budowlany zamawia {ilosc} jednostek {material}"


class HurtowniaMerito:
    def realizuj_zamowienie(self, sklep, material, ilosc):
        print("Przetwarzanie zamówienia...")
        komunikat = sklep.zamow_material(material, ilosc)
        print(komunikat)
        print("Zamówienie zrealizowane")


sklep_drewniany = SklepDrewniany()
sklep_budowlany = SklepBudowlany()
hurtownia = HurtowniaMerito()

hurtownia.realizuj_zamowienie(sklep_drewniany, "deski", 20)
hurtownia.realizuj_zamowienie(sklep_budowlany, "cement", 20)