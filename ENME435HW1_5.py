values = list(map(int,(input("Enter 10 numbers seperated by a space: ")).split()))
#split splits the string by the spaces and map applies the int to every number
ascending_numbers = sorted(values) #sorts automatically from smallest to largest
print("numbers from smallest to largest",ascending_numbers)
unique_numbers = [] #new list
for i in ascending_numbers: 
    if i not in unique_numbers: #check to see if number is a dupe
        unique_numbers.append(i) #if not add it to the new list
print("numbers with dupes removed: ", unique_numbers)
print("The two smallest numbers entered were: [",unique_numbers[0],",", unique_numbers[1],"]")
    