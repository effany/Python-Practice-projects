def add(*args):
    sum = 0
    for i in args:
       sum += i

    return sum 


def calculate(n, **kwargs):
    print(kwargs)

    n += kwargs["add"]
    n *= kwargs["multiply"]
    print(n)



calculate(2, add=3, multiply=5)

class Car:

    def __init__ (self, **kw):
        # if we use get, when we dont provide the value, it'll just default to non
        self.make = kw.get("make")
        # if we use the kw["model"], when there's nothing, it'll give an error
        self.model = kw.get("model")

my_car = Car(make="Nissan")
print(my_car.model)