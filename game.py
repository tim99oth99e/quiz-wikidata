from request import RequestManager
import random

class Question():
    def __init__(self, element, to_ask, answer, options = []):
        self.element = element
        self.to_ask = to_ask
        self.answer = answer
        self.options = options
        self.options.append(answer)
        random.shuffle(self.options)
        self.question = self.to_ask + " of " + self.element + " ?"

    def ask(self):
        print(self.question)
        for i, option in enumerate(self.options):
            print("Option ", i+1, ": ", option)

    def get_answer(self):
        id = int(input("Write your answer:"))
        return self.options[id-1]

    def check_answer(self, input):
        if input == self.answer:
            return True
        return False

class Game(object):
    def __init__(self, mode, level, n_questions = 10) -> None:
        self.type = mode
        self.level = level
        self.score = 0
        self.status = 0
        self.game_over = False
        self.need_more_questions = False
        self.questions = []     
        self.request_manager =  RequestManager()
        self.n_questions = n_questions

    def start_game(self):
        # for safety
        self.score = 0
        self.game_over = False
        self.need_more_questions = False
        # get questions
        for i in range(self.n_questions):
            element, to_ask, answer, options = self.request_manager.generate_conflict_question()
            question = Question(element, to_ask, answer, options)
            self.questions.append(question)


    def get_more_questions(self):
        for i in range(self.n_questions):
            element, to_ask, answer, options = self.request_manager.generate_conflict_question()
            question = Question(element, to_ask, answer, options)
            self.questions.append(question)
        self.need_more_questions = False

    def step(self):
        if len(self.questions) == 0:
            if self.type == "standard":
                self.game_over = True
            elif self.type == "serie":
                self.get_more_questions()
            return
        question = self.questions.pop()
        question.ask()
        answer = question.get_answer()
        if question.check_answer(answer):
            self.score += 1
            print("Good one!")
        else:
            print("Bad one!")
            if self.type == "serie":
                self.game_over = True
        return self.score

    def run(self):
        self.start_game()
        while not self.game_over:
            self.step()
        print("Final score: ", self.score)
