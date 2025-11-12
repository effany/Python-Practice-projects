student_scores = {
    'Harry': 88,
    'Ron': 78,
    'Hermione': 95,
    'Draco': 75,
    'Neville': 60
}

student_grades = {}

# This is the scoring criteria: 

# - Scores 91 - 100: Grade = "Outstanding" 

# - Scores 81 - 90: Grade = "Exceeds Expectations" 

# - Scores 71 - 80: Grade = "Acceptable" 

# - Scores 70 or lower: Grade = "Fail" 


                                                for name in student_scores:
                                                    score = student_scores[name]
                                                    if 91 <= score <= 100:
                                                        grade = "Outstanding"
                                                    elif 81 <= score <= 90:
                                                        grade = "Exceeds Expectations"
                                                    elif 71 <= score <= 80:
                                                        grade = "Acceptable"
                                                    else:
                                                        grade = "Fail"
                                                    student_grades[name] = grade
print(student_grades) 