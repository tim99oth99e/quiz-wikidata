import warnings
from game import Game
warnings.filterwarnings("ignore")


def quiz_mvp():
    game = Game("serie", 0, n_questions= 5)
    game.run()


if __name__ == '__main__':
    quiz_mvp()
