class Samochod:

    #zmienne klasowe
    marka = None
    color = None
    max_speed = None

    #konstruktor klasy
    #self - like "this" in C++
    def __init__(self):
        pass

    #definicja metody
    def speed(self, currentSpeed):
        if currentSpeed == 10:
            return self.speed
        self.max_speed = currentSpeed
        return currentSpeed


fiat = Samochod()
fiat.max_speed = 10
fiat.color = 'rozowy'
fiat.marka = 'BMW'
fiat.speed(400)

print(fiat.color)