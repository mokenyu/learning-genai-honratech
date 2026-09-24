# if-statement, if-else, if-elif-else
# voter
# if-else pair
age = int(input("Enter your age: "))

if age >= 18: # 2+4
    print("You are eligible to vote.")
else:
    print("Take a brake, touch some grass and come back when you're 18")

# if-else code block
if age >= 18:
    print("You are eligible to vote.")
elif age <= 17 and age >=15: # and, or | is, in
    print("You can buy your vote!")
else:
    print("Take a brake, touch some grass and come back when you're 18")