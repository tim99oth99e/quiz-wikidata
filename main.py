import warnings
from request import RequestManager
warnings.filterwarnings("ignore")


def quiz_mvp():
    req = RequestManager()
    req.generate_conflict_question()
    #score = 0


if __name__ == '__main__':
    quiz_mvp()
