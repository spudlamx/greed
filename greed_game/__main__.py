import os
import random

from game.casting.actor import Actor
from game.casting.artifact import Artifact
from game.casting.cast import Cast

from game.directing.director import Director

from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService

from game.shared.color import Color
from game.shared.point import Point


FRAME_RATE = 50
MAX_X = 900
MAX_Y = 600
ROB_HEIGHT = 550
CELL_SIZE = 1
FONT_SIZE = 15
COLS = MAX_X / CELL_SIZE
ROWS = MAX_Y / CELL_SIZE
CAPTION = "GREED"
DATA_PATH = os.path.dirname(os.path.abspath(__file__)) + "/data/messages.txt"
WHITE = Color(255, 255, 255)
RAND_COLOR = Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
DEFAULT_ARTIFACTS = 40
GEMS_NUM = random.randint(25, 50)
ROCK_NUM = GEMS_NUM

def main():
    
    # create the cast
    cast = Cast()
    
    # create the banner
    banner = Actor()
    banner.set_text("")
    banner.set_font_size(FONT_SIZE)
    banner.set_color(WHITE)
    banner.set_position(Point(CELL_SIZE, 0))
    cast.add_actor("banners", banner)
    
    # create the robot
    x = int(MAX_X / 2)
    y = int(MAX_Y * 1.95)
    position = Point(x, y)

    robot = Actor()
    robot.set_text("#")
    robot.set_font_size(FONT_SIZE)
    robot.set_color(WHITE)
    robot.set_position(position)
    cast.add_actor("robots", robot)
    # create gem
    for _ in range(GEMS_NUM):
        RAND_COLOR = Color(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        x = random.randint(1, COLS - 1)
        y = random.randint(1, ROWS - 1)
        position = Point(x, y)
        position = position.scale(CELL_SIZE)

        gem = Artifact()
        gem.set_text('o')
        gem.set_font_size(FONT_SIZE)
        gem.set_color(RAND_COLOR)
        gem.set_position(position)
        cast.add_actor('gems', gem)
    # create rock
    for _ in range(ROCK_NUM):
        RAND_COLOR = Color(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

        x = random.randint(1, COLS - 1)
        y = random.randint(1, ROWS - 1)
        position = Point(x, y)
        position = position.scale(CELL_SIZE)

        rock = Artifact()
        rock.set_text('*')
        rock.set_font_size(FONT_SIZE)
        rock.set_color(RAND_COLOR)
        rock.set_position(position)
        cast.add_actor('rocks', rock)
        

    # start the game
    keyboard_service = KeyboardService(CELL_SIZE)
    video_service = VideoService(CAPTION, MAX_X, MAX_Y, CELL_SIZE, FRAME_RATE)
    director = Director(keyboard_service, video_service)
    director.start_game(cast)


if __name__ == "__main__":
    main()