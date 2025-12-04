import random

iter=0
while iter <= 25:
    # prints a random value from the list
    list1 = [4,6,7,8,9,12,13,14,15,16,17]
    num1=random.choice(list1)

    # prints a random value from the list
    list2 = [2,3,4,5,6,7,8,9]
    num2=random.choice(list2)

    print(num1, 'X', num2, '=')

    iter+=1

