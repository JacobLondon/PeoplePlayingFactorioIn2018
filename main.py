from display import *
from player import *

def main():
        square = 20
        size = 40

        game = Controller(square=square, size=size)

        p1 = Player(size=size)
        p2 = Player(number=1, size=size)

        game.run(p1, p2)

if __name__ == '__main__':
    main()
