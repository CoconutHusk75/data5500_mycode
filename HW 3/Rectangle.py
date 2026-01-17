# Create a class called Rectangle with attributes length and width. 
# Implement a method within the class to calculate the area of the rectangle. 
# Instantiate an object of the Rectangle class with length = 5 and width = 3, and print its area.

#creating class for the rectangle 
class Rectangle:
    def __init__ (self, length, width):
        self.length = length 
        self.width = width 

    #implementing the method to calculate the area of the rectangle 
    def area(self):
        return self.length * self.width

#instantiate the object 
rect = Rectangle(5, 3)
print("Rectangle Area: ", rect.area())
