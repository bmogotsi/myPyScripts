class Dog:
    species = "Canine"  # Class attribute

    def __init__(self, name, age): # Constructor method
        self.name = name  # Instance attribute
        self.age = age  # Instance attribute

    """Self Parameter
            self parameter is a reference to the current instance of class.
            It allows us to access the attributes and methods of the object.
    """
    def bark(self):
        print(f"{self.name} is barking!")
        print(f"{self.name} is {self.age} years old.")
    """" __str__ method
            allows us to define a custom string representation of an object.
            defaualt is: "<__main__.ClassName object at 0x00000123>."
            
            with __Str__ is: "Buddy is 3 years old." for dog1!!!!!!!!!!!!"
                    and      "Charlie is 5 years old. for dog2!!!!!!!!!!!!"
    """
    def __str__(self):
        return f"{self.name} is {self.age} years old!!!!!!!!!!!!"
        
    
    """ Getter and Setter methods 
            provide controlled access to an object's attributes.
    """
    # Getter and Setter methods
    # @property(age) getter
    def age(self):
        return self._age  # Getter

    # @property(age) setter
    def age(self, value):
        if value < 0:
            print("Age cannot be negative!")
        else:
            self._age = value  # Setter

# Creating an object of the Dog class
dog1 = Dog("Buddy", 3)
dog2 = Dog("Charlie", 5)

print(dog1) # <__main__.Dog object at 0x0000019435BCF550> (without __str__ method)
print(dog2) # <__main__.Dog object at 0x0000019435BCF590> (without __str__ method)

dog1.bark()


# print(dog1.name)
# print(dog1.species)
# print(dog1.age)