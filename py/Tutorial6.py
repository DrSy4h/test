#OOP
from random import random


class Shape: #parent class
    def __init__(self, name):
        self.name = name

    def area(self):
        return 0
    
class Circle(Shape): #child inherits from Shape
    def __init__(self, radius):
        super().__init__("Circle") #call parent constructor
        self.radius = radius

    def area(self): #override area method
        return 3.14 * self.radius * self.radius
    
class Square(Shape): #child inherits from Shape
    def __init__(self, side):
        super().__init__("Square") #call parent constructor
        self.side = side

    def area(self): #override parent method
        return self.side * self.side

# instantiate and print at module level (outside class definitions)
circle = Circle(5)
square = Square(4)

print(circle.name)
print(square.name)

#Polymorphism
def print_area(shape): #function takes shape object
    print(f"The area of the {shape.name} is {shape.area()}")

print_area(circle) # "The area of the Circle is 78.5"
print_area(square) # "The area of the Square is 16"

shapes = [Circle(3), Square(5), Circle(2)]
for shape in shapes:
    print_area(shape)

    #Shuffle

random_number = random.randint(1, 100)
random_choice = random.choice(['apple', 'banana', 'orange'])
numbers = [1, 2, 3, 4, 5]
random.shuffle(numbers)
  
print(f"Random Number: {random_number}")
print(f"Random Choice: {random_choice}")
print(f"Shuffled List: {numbers}")
