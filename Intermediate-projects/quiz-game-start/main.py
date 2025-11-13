from question_model import Question
from data import question_data
from quiz_brain import QuizBrain

data = question_data
question_bank = []

for question in data:
    question_text = question["text"]
    question_answer = question["answer"]
    question_object = Question(question_text, question_answer)
    question_bank.append(question_object)


quiz = QuizBrain(question_bank)


while quiz.still_has_questions():
    quiz.next_question()
print("You've completedthe quiz!")
print(f"Your final score is {quiz.score}/{quiz.question_number}")