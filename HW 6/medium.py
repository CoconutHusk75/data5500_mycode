#2. Given an array of integers, write a function that finds 
# the second largest number in the array.
#Analyze the time complexity of your solution using Big O notation, 
# especially what is the Big O notation of the code you wrote, and 
# include it in the comments of your program.

def second_largest_number(arr):
    #create two placeholders with the smallest possible value
    first = float('-inf')
    second = float('-inf')
    #loop to see if the current number is bigger than our first variable and update 
    for num in arr:
        if num > first:
            second = first 
            first = num    
        #if the number is between first and second then update the second variable
        elif num > second and num != first:
            second = num
    return second if second != float('-inf') else None

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 120]
print(f"The second largest number is: {second_largest_number(numbers)}")

#The time complexity is O(n) becasue this is a linear algorithym and we iterate through every instance once
