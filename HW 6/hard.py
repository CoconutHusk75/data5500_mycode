#3. Write a function that takes an array of integers as input 
# and returns the maximum difference between any two numbers in the array.
#Analyze the time complexity of your solution using Big O notation, 
# especially what is the Big O notation of the code you wrote, 
# and include it in the comments of your program.

def max_difference(arr):
    #sets two varibales equal to the first instance in the array
    min_value = arr[0]
    max_value = arr[0]
    #loops to update the min value variable and max value variable as we iterate through the array
    for num in arr:
        if num < min_value:
            min_value = num
        elif num > max_value:
            max_value = num
    #finds the max difference by subtracting the min value from the max
    return max_value - min_value

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100]
print(f' The max difference between two numbers in the array is: {max_difference(numbers)}')

#The time complexity is still O(n) as we are only iterating through the array once and only comparin two varibales still. 