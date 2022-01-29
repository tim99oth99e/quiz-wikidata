class Question():
    def __init__(self, question, answer, options = [], level = 'hard'):
        self.question = question
        self.answer = answer
        self.options = options
        self.level = level