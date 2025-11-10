#Tuples
coordinates = (10.0, 20.0)
person = ("Alice", 25, "Engineer")
single_item = (42,) # note the comma for single item tuple

#Tuple operations
print(coordinates[0]) # Accessing elements
print(len(person))    # Length of tuple
print(person[2])

# Sets
fruits = {"apple", "banana", "orange", "kiwi", "mango"}
numbers = {1, 2, 3, 4, 5}

#Set operations
fruits.add("grape")      # Adding an element
fruits.remove("banana")   # Removing an element
fruits.discard("kiwi")  # Removing an element if it exists
fruits.discard("apple")  # Trying to remove an element that doesn't exist
print(fruits)

# Math Operations
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

print(set1.union(set2))          # Union
print(set1.intersection(set2))   # Intersection
print(set1.difference(set2))     # Difference
print(set1.symmetric_difference(set2)) # Symmetric Difference

print("")
print("Exercise 5")

# Create a tuple to store student information
# Students grade stored as tuples

grades = [
    ("Alice", "Math", 85),
    ("Bob", "Science", 92),
    ("Alice", "Science", 78),
    ("Charlie", "Math", 90),
    ("Bob", "Math", 88),
    ("Alice", "English", 95)
]
#Find all unique students using sets
students = set()
for grade in grades:
    students.add(grade[0]) #grade 0 is student name
print("Unique students:", students)


# Dictionary

student = {
    "name"  : "Alice",
    "age"   : 20,
    "grade" : "A",
    "courses": ["Math", "Science", "English"]
}

#Accessing and modifying dictionary
print(student["name"])  # Alice
print(student.get("age")) # 20
student["age"] = 21  # Update age
student["email"] = "alice@email.com" # Add new key-value

keys = student.keys()
values = student.values()   
items = student.items()

print(keys)
print(values)
print(items)

#Iterating through dictionary
for key in student:
    print(f"{key}: {student[key]}")

for key, value in student.items():
    print(f"{key}: {value}")

#nested dictionary
company = {
        "employees": {
            "john": {"age": 30, "department": "IT"},
            "jane": {"age": 25, "department": "HR"}
        },
        "departments": ["IT", "HR", "Finance"]
    }

print(company["employees"].items())
print(company["departments"])

print("Exercise 6")

# Create a student records dictionary with nested information
student_records = {
    "student_001": {
        "name": "John",
        "age": 19,
        "major": "Computer Science",
        "grades": [85, 92, 78]
    },
    "student_002": {
        "name": "Sarah",
        "age": 20,
        "major": "Biology",
        "grades": [90, 88, 95]
    }
}

# Demonstrate how to access the information
print("\nAll student records:", student_records)

# Access specific student information
print("\nStudent 001's information:")
print("Name:", student_records["student_001"]["name"])
print("Age:", student_records["student_001"]["age"])
print("Major:", student_records["student_001"]["major"])
print("Grades:", student_records["student_001"]["grades"])

# Add student_003 as requested
student_records["student_003"] = {
    "name": "Mike",
    "age": 18,
    "major": "Math",
    "grades": [82, 79, 91]
}

print("Added student_003:", student_records["student_003"])

# Example: compute and print John's and Mike's average grades
def average(grades_list):
    return sum(grades_list) / len(grades_list) if grades_list else 0

john_avg = average(student_records["student_001"]["grades"])
mike_avg = average(student_records["student_003"]["grades"])
print(f"\nJohn's average: {john_avg:.2f}")
print(f"Mike's average: {mike_avg:.2f}")

