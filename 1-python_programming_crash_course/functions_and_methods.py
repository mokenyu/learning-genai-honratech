def sum_num(a: int, b: int, numList, c=8) -> int:
    summation = a+b # a+b=15
    for number in numList:
        summation+=number # summation = 18 + 3
    return summation

num1 = 6
num2 = 9

listNum = [1,2,3,4,5,6,7,8,9]
sum2 = sum_num(num1, num2, listNum)
print(sum2)

listNum.append(10)

name = "Dixey" # name[0]
name_lower = name.lower()
name_higher = name.upper()
print(name_lower, name_higher)

# sum1 = sum_num(num1, num2) # positional/keyword argument
# sum2 = sum_num(b=num2, a=num1)
