# First create a file called "first_assignment.py"
# In this file, you will have:
# 4 variables; 3 of them hard-coded and one as a user input
# 1- name, 2- university, 3- hobby, 4- user input: your age
# store all of these in an array
# use a for loop to print out the various information, one by one
# use an f-string as well to print it out
name = "Dixey"
school = "NAHPI"
hobby = "Gaming"

details = [name, school, hobby]

age = int(input("Enter your age: "))

details.append(age)

for item in details:
    print(item)

print(f"My name is {details[0]}, I am {details[3]} years old I school at {details[1]} and I like {details[2]}")