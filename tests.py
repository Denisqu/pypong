import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import pygame
from pong import Ball, Gamer, GameField, PongGame, get_random, rgb_colors

class TestBall(unittest.TestCase):
    def test_update_pos(self):
        # Create a Ball instance with predefined values for testing
        ball = Ball(50, 50, 5, (255, 255, 255), 100, 100)
        ball.speed_x = 1
        ball.speed_y = 1

        # Test if update_pos updates ball's position correctly
        ball.update_pos()
        self.assertEqual(ball.center_x, 51)
        self.assertEqual(ball.center_y, 51)

    def test_set_speed(self):
        # Create a Ball instance
        ball = Ball(50, 50, 5, (255, 255, 255), 100, 100)

        # Test if set_speed sets the ball's speed correctly
        ball.set_speed(2, 2)
        self.assertEqual(ball.speed_x, 2)
        self.assertEqual(ball.speed_y, 2)

    def test_invert_move(self):
        # Create a Ball instance
        ball = Ball(50, 50, 5, (255, 255, 255), 100, 100)
        ball.speed_x = 2
        ball.speed_y = 2

        # Test if invert_move inverts ball's movement correctly
        ball.invert_move(invert_x=True, invert_y=True)
        self.assertEqual(ball.speed_x, -2)
        self.assertEqual(ball.speed_y, -2)

   
class TestGamer(unittest.TestCase):
    def test_update_pos(self):
        # Create a Gamer instance with predefined values for testing
        gamer = Gamer(50, 50, 10, 40, (255, 255, 255), "Player 1", 100, 100)
        gamer.speed_y = 1

        # Test if update_pos updates gamer's position correctly
        gamer.update_pos()
        self.assertEqual(gamer.rect.y, 51)
        self.assertNotEquals(gamer.rect.y, 50)

    def test_set_speed(self):
        # Create a Gamer instance
        gamer = Gamer(50, 50, 10, 40, (255, 255, 255), "Player 1", 100, 100)

        # Test if set_speed sets the gamer's speed correctly
        gamer.set_speed(2)
        self.assertEqual(gamer.speed_y, 2)
        self.assertNotEquals(gamer.speed_y, 0)

    def test_reset(self):
        # Create a Gamer instance
        gamer = Gamer(20, 30, 10, 40, (255, 255, 255), "Player", 200, 200)
        
        # Reset the gamer
        gamer.reset()
        
        # Check if gamer attributes are reset
        self.assertEqual(gamer.rect.x, 20)
        self.assertEqual(gamer.rect.y, 30)


class TestGameField(unittest.TestCase):
    def test_get_screen(self):
        # Create a GameField instance
        game_field = GameField(100, 100, "black", (255, 255, 255), "Pong")

        # Test if get_screen returns a pygame Surface
        self.assertIsInstance(game_field.get_screen(), pygame.Surface)


class TestGame(unittest.TestCase):
    def test_check_collision(self):
        screen_width = 320
        screen_height = 240
        fps = 120
        max_score = 10
        color = 'red'
        player_name = 'player'

        game_field = GameField(screen_width, screen_height,
                               "black", rgb_colors[color], "Pong")
        ball = Ball(screen_width / 2, screen_height / 2, 5,
                    rgb_colors[color], screen_width, screen_height)
        player = Gamer(screen_width - 30, (screen_height / 2) - 40,
                       10, 40, rgb_colors[color], player_name, screen_width, screen_height)
        computer = Gamer(20, (screen_height / 2) - 40, 10, 40,
                         rgb_colors[color], "CPU", screen_width, screen_height)
        # no one score a goal
        pong = PongGame(game_field, ball, player, computer, fps=fps, max_score=max_score)
        pong.run_game_once()
        self.assertEqual(pong._stat['cpu_score'], 0)
        self.assertEqual(pong._stat['player_score'], 0)
        # player score goal
        ball.set_pos(pong._computer.get_borders()['left'], 0)
        pong._check_collision()
        self.assertEqual(pong._stat['player_score'], 1)
        # cpu score goal
        ball.set_pos(pong._player.get_borders()['right'], 0)
        pong._check_collision()
        self.assertEqual(pong._stat['cpu_score'], 1)

    def test_check_end_game_cpu(self):
        screen_width = 320
        screen_height = 240
        fps = 120
        max_score = 10
        color = 'red'
        player_name = 'player'
        game_field = GameField(screen_width, screen_height,
                               "black", rgb_colors[color], "Pong")
        ball = Ball(screen_width / 2, screen_height / 2, 5,
                    rgb_colors[color], screen_width, screen_height)
        player = Gamer(screen_width - 30, (screen_height / 2) - 40,
                       10, 40, rgb_colors[color], player_name, screen_width, screen_height)
        computer = Gamer(20, (screen_height / 2) - 40, 10, 40,
                         rgb_colors[color], "CPU", screen_width, screen_height)
        pong = PongGame(game_field, ball, player, computer, fps=fps, max_score=max_score)
        pong.run_game_once()
        pong._stat['cpu_score'] = 5
        pong._check_end_game()
        self.assertTrue(True)
        pong._stat['cpu_score'] = 10
        with self.assertRaises(SystemExit):
            pong._check_end_game()


    def test_check_end_game_player(self):
        screen_width = 320
        screen_height = 240
        fps = 120
        max_score = 10
        color = 'red'
        player_name = 'player'
        game_field = GameField(screen_width, screen_height,
                               "black", rgb_colors[color], "Pong")
        ball = Ball(screen_width / 2, screen_height / 2, 5,
                    rgb_colors[color], screen_width, screen_height)
        player = Gamer(screen_width - 30, (screen_height / 2) - 40,
                       10, 40, rgb_colors[color], player_name, screen_width, screen_height)
        computer = Gamer(20, (screen_height / 2) - 40, 10, 40,
                         rgb_colors[color], "CPU", screen_width, screen_height)
        pong = PongGame(game_field, ball, player, computer, fps=fps, max_score=max_score)
        pong.run_game_once()
        pong._stat['player_score'] = 5
        pong._check_end_game()
        self.assertTrue(True)
        pong._stat['player_score'] = 10
        with self.assertRaises(SystemExit):
            pong._check_end_game()

    def test_move_player(self):
        screen_width = 320
        screen_height = 240
        fps = 120
        max_score = 10
        color = 'red'
        player_name = 'player'
        game_field = GameField(screen_width, screen_height,
                               "black", rgb_colors[color], "Pong")
        ball = Ball(screen_width / 2, screen_height / 2, 5,
                    rgb_colors[color], screen_width, screen_height)
        player = Gamer(screen_width - 30, (screen_height / 2) - 40,
                       10, 40, rgb_colors[color], player_name, screen_width, screen_height)
        computer = Gamer(20, (screen_height / 2) - 40, 10, 40,
                         rgb_colors[color], "CPU", screen_width, screen_height)
        pong = PongGame(game_field, ball, player, computer, fps=fps, max_score=max_score)
        pong.run_game_once()
        event = pygame.event
        event.type = pong._pong_pygame.KEYDOWN
        event.key = pong._pong_pygame.K_UP
        self.assertEqual(pong._player.get_speed(), 0)
        pong._move_player(event)
        self.assertEqual(pong._player.get_speed(), -pong._player_speed)
        self.assertNotEqual(pong._player.get_speed(), 0)
        event.type = pong._pong_pygame.KEYUP
        event.key = pong._pong_pygame.K_UP
        pong._move_player(event)
        self.assertEqual(pong._player.get_speed(), 0)
        self.assertNotEqual(pong._player.get_speed(), -pong._player_speed)
        event.type = pong._pong_pygame.KEYDOWN
        event.key = pong._pong_pygame.K_LEFT
        pong._move_player(event)
        self.assertEqual(pong._player.get_speed(), 0)
        self.assertNotEqual(pong._player.get_speed(), -pong._player_speed)
        event.type = pong._pong_pygame.KEYUP
        event.key = pong._pong_pygame.K_RIGHT
        pong._move_player(event)
        self.assertEqual(pong._player.get_speed(), 0)
        self.assertNotEqual(pong._player.get_speed(), -pong._player_speed)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    
