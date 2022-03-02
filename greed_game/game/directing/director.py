import random
from game.shared.color import Color
from game.shared.point import Point
from game.casting.artifact import Artifact
class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self.score = 0
        self.start = 0
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)   
        banner = cast.get_first_actor("banners")
        banner.set_text(f"Score: {self.score}") 

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        COLS = 60
        ROWS = 40
        CELL_SIZE = 15

        x = random.randint(1, COLS - 1)
        y = random.randint(1, ROWS - 1)
        position = Point(x, y)
        position = position.scale(CELL_SIZE)

        robot = cast.get_first_actor("robots")
        gems = cast.get_actors('gems')
        down = self._keyboard_service.set_down(random.randint(0, 3))
        rocks = cast.get_actors('rocks')

        
        
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)
        rand_x = random.randint(1, max_x)
        if self.start < 1:
            for gem in gems:
                down = self._keyboard_service.set_down(random.randint(2, 5))
                gem.set_velocity(down)
            for rock in rocks:
                down = self._keyboard_service.set_down(random.randint(2, 5))
                rock.set_velocity(down)
        for gem in gems:
            gem.move_next(max_x, max_y)
            if robot.get_position().close_enough(gem.get_position()):
                position = Point(rand_x, y - y)
                self.score += 1
                gem.set_position(position)
    

                   
        for rock in rocks:
            rock.move_next(max_x, max_y)
            if robot.get_position().close_enough(rock.get_position()):
                position = Point(rand_x, y - y)
                self.score -= 1
                rock.set_position(position)
        self.start += 1
        
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()