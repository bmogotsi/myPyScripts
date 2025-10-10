# https://www.geeksforgeeks.org/python/python-classes-and-objects/
class Animal:
    species = "Animal"
    def sound(self):
        print("Some sound")

    def __init__(self, name, age):
        self.name = name
        self.age = age
        # print(f"Animal created...: {self.name}, {self.age}")

    def age(self): # Getter
        return self._age

    def age(self, value): # Setter
         self._age = value

    def __str__(self):
        return f"Animal __str__ method...: {self.name}, {self.age}"

    def info(self):
        return    f"Animal info...: {self.name}, {self.age}"

class Dog(Animal):
    species1 = "Dog"
    """ Method overriding
            occurs when a subclass provides a specific implementation of a method that is already defined in its superclass.
                This allows subclasses to modify or extend behavior of inherited methods.
    """
    def sound(self):  # Method overriding
        print("Woof")

dog = Dog("Buddy", 3)
print(dog.info())
print(dog.__str__())
dog.sound()
print(dog.species)
print(dog.species1)
dog.age = 4
print(dog.age)
print(dog.name)
print(dog.species)
print(dog)
print(f"Dog sound...: {dog.sound()}")


quit()