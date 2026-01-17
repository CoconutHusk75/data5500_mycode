#2.  Create a class called Employee with attributes name and salary. 
# Implement a method within the class that increases the salary of the employee by a given percentage. 
# Instantiate an object of the Employee class with 
# name = "John" and salary = 5000, 
# increase the salary by 10%, and print the updated salary.

#creating class called employee
class Employee:
    def __init__ (self, name, salary):
        self.name = name
        self.salary = salary

    #creating a method to modify employee salary by a cerain percentage
    def modify_salary(self, percentage):
        self.salary += self.salary * (percentage / 100)

#Instantiating employee object John
emp1 = Employee("John", 5000)
emp1.modify_salary(10)
print ("Increased salary: ", emp1.salary)

#I initially tried to set a variable "x" to 1 within the class and use that as a salary modifier 
# outside of the class by setting x = 1.10 or something similar but I asked chatGPT how to better impliment 
# this method in a class and it suggested I use the modifier seen in the code.

