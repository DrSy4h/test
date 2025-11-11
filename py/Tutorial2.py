single_quote = 'Hello'
double_quote = "World"
triple_quote = """Multi-line string"""

print(single_quote)
print(double_quote)
print(triple_quote)

text = "Python Programming"

print(text[0])
print(text[-2])
print(text[0:6])
print(text[7:])
print(text[:6])
print(text[7:])

name = " bob the builder "

print(len(name))
print(name.strip())
print(name.upper())
print(name.lower())
print(name.title())
print(name.replace("bob", "Dr Syah"))

name = "John Doe"
age = 30

message_1 = f"My name is {name} and I am {age} years old." # f-strings
message_2 = "My name is {} and I amd {} years old.".format(name, age) # str.format()
message_3 = "My name is %s and I am %d years old." % (name, age) # %-formatting

print(message_1)
print(message_2)
print(message_3)

print("") 
print("Exercise 2")

text = """Python is a powerful programming language. It's easy to learn and versatile.
You can use Phython for web development, data analysis, data science, artificial intelligence, and more. The syntax is clean and readable.
This makes Phyton perfect for beginners and experienced programmers alike.
Join me as we take a deep-dive into the world of Python programming!"""

print(len(text)) #count letters
print(len(text.split())) #count words
print(len(text.replace('!', '.').replace('?', '.').split('.'))) #count sentences
print(len(text.splitlines())) #count lines

#IMPORTANT!!! IO Validation

name = input ("Enter your name: ")
height = float(input("Enter your height in cm: ")) #Convert to float

# Input Validation
while True:
    try:
        age = int(input("Enter you age: ")) #Convert to integer
        if age > 0:
            break
        else:
            print("Age must be a positive integer. Please try again.")
    except ValueError:
            print("Sorry. Invalid input. Please try again.")
        
# Output Validation
print(f"Hello, {name}! Welcome to JomHack Cohort 2 app.")
print(f"You are {age} years old and your height is {height} cm.")


print("")
print("Exercise 3(a)")

print("JomHack Calculator")

# Get user input
number_1 = float(input("Enter the first number: ")) #Convert to float
number_2 = float(input("Enter second number: ")) #Convert to float

#Ask for operation
operation = input("Enter operation (+, -, *, /, //, %, **): ")

# Perform calculation based on operation
if operation == "+":
     result = number_1 + number_2
elif operation == "-":
    result = number_1 - number_2
elif operation == "*":
    result = number_1 * number_2
elif operation == "/":
    if number_2 != 0:
        result = number_1 / number_2
    else:
        result = "ERROR!!Division by zero is NOT ALLOWED!"
elif operation == "//":
    result = number_1 // number_2
elif operation == "%":
    result = number_1 % number_2
elif operation == "**":
    result = number_1 ** number_2
else:
    result = "Invalid operation"

#Display result
print(f"The result is: {result}.")
print("Thank you for using JomHack Calculator!")


# Exercise 3(b)
print("Exercise 3(b)")
print('') # New line
print("JomHack Quiz")

#2. Create a simple quiz that asks the user 3 multiple-choice questions.
score = 0

# Question 1
Answer_1 = input("What is the capital of France? ").lower()