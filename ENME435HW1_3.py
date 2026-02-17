import numpy as np #idk if i need this rn
import random

count = 0 #this will show how many doubles are rolled 

for i in range(10000):
    Dice1 = random.randint(1,6) #Dice 1 roll
    Dice2 = random.randint(1,6) #Dice 2 roll
    if Dice1==Dice2: #a double
        count+=1
    pass
Doubles = float((count/10000)*100) #get percentage
print(f"The percent of doubles rolled is {Doubles:.2f}%") # f string uses .2f to pick amount of decimals 

#6 possible rolls per dice and 2 die so there is 36 possible combos
#6 possible double rolls so 6/36. Answer should be around 16.67%