# sentence = "What is the Airspeed Velocity of an Unladen Swallow?"
# sentence_list = list(sentence.split(" "))
# result = {word: len(word) for word in sentence_list}
# print(result)

import pandas
student_dict = {
    "student": ["Angle", "James", "Lily"], 
    "score": [56, 76, 90]
}

student_df = pandas.DataFrame(student_dict)

for (index, row) in student_df.iterrows():
    print(row)