import random
# numbers = [1,2,3]

# new_numbers = [n+ 1 for n in numbers]

# print(new_numbers)

# new_list = [ i * 2 for i in range(1,5)]
# print(new_list)

names = ["Alex", "Beth", "Caroline", "Dave", "eleanor", "Freddie"]
new_dict = {student:random.randint(0,100) for student in names}
print(new_dict)

passed_student = {student:score for (student,score) in new_dict.items() if score >= 60}
print(passed_student)

# new_names = [name.upper() for name in names if len(name) > 4]

# print(new_names)