#1. Given an array of integers, write a function to calculate the sum of all 
# elements in the array.
#Analyze the time complexity of your solution using Big O notation, 
# especially what is the Big O notation of the code you wrote, 
# and include it in the comments of your program.

def sum_array(arr):
    total = 0 
    #This loop runs once for every instance in the array and keeps a running tally of the total
    for num in arr:
        total += num
    return total

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f'The sum of the array is: {sum_array(numbers)}')

# The time complexity in terms of Big O notation is O(n) 
#I iterate through the array once and n is the number of elements in the array.