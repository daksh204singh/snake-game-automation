from snake import *
import pygame
import random
import time
import math
from tqdm import tqdm
import numpy as np


def generate_training_data(display, clock, apple):
	training_data_x = []
	training_data_y = []
	training_games = 1000
	steps_per_game = 2000

	for _ in tqdm(range(training_games)):
		snake_start, snake_position, apple_position, score = starting_positions()
		prev_apple_distance = apple_distance_from_snake(apple_position, snake_position)

		for _ in range(steps_per_game):
			angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized = angle_with_apple(snake_position, apple_position)
			direction, button_direction = generate_random_direction(snake_position, angle)
			current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked = blocked_directions(
				snake_position)

			direction, button_direction, training_data_y = generate_training_data_y(snake_position, angle_with_apple,
																					button_direction, direction,
																					training_data_y, is_front_blocked,
																					is_left_blocked, is_right_blocked)

			if is_front_blocked == 1 and is_left_blocked == 1 and is_right_blocked == 1:
				break

			training_data_x.append(
				[is_left_blocked, is_front_blocked, is_right_blocked, apple_direction_vector_normalized[0], \
				 snake_direction_vector_normalized[0], apple_direction_vector_normalized[1], \
				 snake_direction_vector_normalized[1]])

			snake_position, apple_position, score = play_game_training(snake_start, snake_position, apple_position,
															  button_direction, score, display, clock, apple)

	return training_data_x, training_data_y


def generate_training_data_y(snake_position, angle_with_apple, button_direction, direction, training_data_y,
							 is_front_blocked, is_left_blocked, is_right_blocked):
	if direction == -1:
		if is_left_blocked == 1:
			if is_front_blocked == 1 and is_right_blocked == 0:
				direction, button_direction = direction_vector(snake_position, angle_with_apple, 1)
				training_data_y.append([0, 0, 1])
			elif is_front_blocked == 0 and is_right_blocked == 1:
				direction, button_direction = direction_vector(snake_position, angle_with_apple, 0)
				training_data_y.append([0, 1, 0])
			elif is_front_blocked == 0 and is_right_blocked == 0:
				direction, button_direction = direction_vector(snake_position, angle_with_apple, 1)
				training_data_y.append([0, 0, 1])

		else:
			training_data_y.append([1, 0, 0])

	elif direction == 0:
		if is_front_blocked == 1:
			if is_left_blocked == 1 and is_right_blocked == 0:
				direction, button_direction = direction_vector(snake_position, angle_with_apple, 1)
				training_data_y.append([0, 0, 1])
			elif is_left_blocked == 0 and is_right_blocked == 1:
				direction, button_direction = direction_vector(snake_position, angle_with_apple, -1)
				training_data_y.append([1, 0, 0])
			elif is_left_blocked == 0 and is_right_blocked == 0:
				training_data_y.append([0, 0, 1])
				direction, button_direction = direction_vector(snake_position, angle_with_apple, 1)
		else:
			training_data_y.append([0, 1, 0])
	else:
		if is_right_blocked == 1:
			if is_left_blocked == 1 and is_front_blocked == 0:
				direction, button_direction = direction_vector(snake_position, angle_with_apple, 0)
				training_data_y.append([0, 1, 0])
			elif is_left_blocked == 0 and is_front_blocked == 1:
				direction, button_direction = direction_vector(snake_position, angle_with_apple, -1)
				training_data_y.append([1, 0, 0])
			elif is_left_blocked == 0 and is_front_blocked == 0:
				direction, button_direction = direction_vector(snake_position, angle_with_apple, -1)
				training_data_y.append([1, 0, 0])
		else:
			training_data_y.append([0, 0, 1])

	return direction, button_direction, training_data_y

if __name__ == '__main__':
	display_width = 500
	display_height = 500
	green = (0, 255, 0)
	red = (255, 0, 0)
	bright_green = (0, 200, 0)
	bright_red = (200, 0, 0)
	white = (255,255,255)
	black = (0, 0, 0)
	window_color = black
	apple_image = pygame.image.load('apple.png')
	clock = pygame.time.Clock()
	clock.tick(100)
	snake_head = [250, 250]
	snake_position = [[250,250],[240,250],[230,250]]
	apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
	score = 0
	pygame.init()
	display = pygame.display.set_mode((display_width, display_height))
	display.fill(window_color)
	pygame.display.update()
	training_data_x, training_data_y = generate_training_data(display, clock, apple_image)
	# DEBUG ONLY
	# with open('training_data.dat', 'w') as f:
	   # for item in list(zip(training_data_x, training_data_y)):
			# f.write("%s\n" % str(item))
