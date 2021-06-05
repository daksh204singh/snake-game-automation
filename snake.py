import pygame
import numpy as np
import time
import random
import math

display_width = 500
display_height = 500
green = (0, 255, 0)
red = (255, 0, 0)
bright_green = (0, 200, 0)
bright_red = (200, 0, 0)
white = (255,255,255)
black = (0, 0, 0)
window_color = black

def collision_with_apple(apple_position, score):
	apple_position = [random.randrange(1,50)*10, random.randrange(1,50)*10]
	score += 1
	return apple_position, score

def collision_with_boundaries(snake_head):
	if snake_head[0] >= 500 or snake_head[0] < 0 or snake_head[1] >= 500 or snake_head[1] < 0:
		return 1
	else:
		return 0

def collision_with_self(snake_start, snake_position):
	snake_head = snake_position[0]
	if snake_head in snake_position[1:]:
		return 1
	else:
		return 0

def is_direction_blocked(snake_position, current_direction_vector):
	next_step = snake_position[0] + current_direction_vector
	snake_head = snake_position[0]
	if collision_with_boundaries(next_step) == 1 or collision_with_self(next_step.tolist(), snake_position) == 1:
		return 1
	else:
		return 0

def apple_distance_from_snake(apple_position, snake_position):
	return np.linalg.norm(np.array(apple_position) - np.array(snake_position[0]))

def blocked_directions(snake_position):
	current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

	left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
	right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

	is_front_blocked = is_direction_blocked(snake_position, current_direction_vector)
	is_left_blocked = is_direction_blocked(snake_position, left_direction_vector)
	is_right_blocked = is_direction_blocked(snake_position, right_direction_vector)

	return current_direction_vector, is_front_blocked, is_left_blocked, is_right_blocked

def generate_random_direction(snake_position, angle_with_apple):
	direction = 0
	if angle_with_apple > 0:
		direction = 1
	elif angle_with_apple < 0:
		direction = -1
	else:
		direction = 0

	return direction_vector(snake_position, angle_with_apple, direction)


def direction_vector(snake_position, angle_with_apple, direction):
	current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
	left_direction_vector = np.array([current_direction_vector[1], -current_direction_vector[0]])
	right_direction_vector = np.array([-current_direction_vector[1], current_direction_vector[0]])

	new_direction = current_direction_vector

	if direction == -1:
		new_direction = left_direction_vector
	if direction == 1:
		new_direction = right_direction_vector

	button_direction = generate_button_direction(new_direction)

	return direction, button_direction


'''
	LEFT: [-10, 0] button_direction: 0
	RIGHT: [10, 0] button_directon: 1
	UP: [0, -10] button_directon: 2
	DOWN: [0, 10] button_directon: 3
'''
def generate_button_direction(new_direction):
	button_direction = 0
	if new_direction.tolist() == [10, 0]:
		button_direction = 1
	elif new_direction.tolist() == [-10, 0]:
		button_direction = 0
	elif new_direction.tolist() == [0, 10]:
		button_direction = 2
	else:
		button_direction = 3

	return button_direction


def angle_with_apple(snake_position, apple_position):
	apple_direction_vector = np.array(apple_position) - np.array(snake_position[0])
	snake_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])

	norm_of_apple_direction_vector = np.linalg.norm(apple_direction_vector)
	norm_of_snake_direction_vector = np.linalg.norm(snake_direction_vector)
	if norm_of_apple_direction_vector == 0:
		norm_of_apple_direction_vector = 10
	if norm_of_snake_direction_vector == 0:
		norm_of_snake_direction_vector = 10

	apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
	snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector
	angle = math.atan2(
		apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] - apple_direction_vector_normalized[
			0] * snake_direction_vector_normalized[1],
		apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] + apple_direction_vector_normalized[
			0] * snake_direction_vector_normalized[0]) / math.pi
	return angle, snake_direction_vector, apple_direction_vector_normalized, snake_direction_vector_normalized



def button(msg, x, y, w, h, ic, ac, action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	smallText = pygame.font.Font("freesansbold.ttf", 20)
	display_text1 = msg
	TextSurf = smallText.render(display_text1, True, white)
	if x+w > mouse[0] > x and y+h > mouse[1] > y: # HOver
		pygame.draw.rect(display, ac, (x,y,w,h))
		TextRect = TextSurf.get_rect()
		TextRect.center = ((x+(w/2)),y+(h/2))
		display.blit(TextSurf, TextRect)
		if click[0] == 1 and action != None:
			if action == "play":
				return 3
			elif action == "quit":
				pygame.quit()
	else: # Not hover
		pygame.draw.rect(display, ic, (x,y,w,h))
		TextRect = TextSurf.get_rect()
		TextRect.center = ((x+(w/2)),y+(h/2))
		display.blit(TextSurf, TextRect)

def game_intro():
	intro = True
	button_w = 120
	button_h = 40
	while intro:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		largeText = pygame.font.Font('freesansbold.ttf', 35)
		TextSurf = largeText.render(display_text, True, white) # display_text = MENU
		TextRect = TextSurf.get_rect()
		TextRect.center = ((display_width/2), 40)
		display.blit(TextSurf, TextRect)
		ret = button("PLAY!", 190, 210, button_w, button_h, green, bright_green, "play")
		if ret == 3:
			intro = False
		button("QUIT!", 190, 320, 120, 40, red, bright_red, "quit")
		pygame.display.update()
		clock.tick(20)

def generate_snake(snake_head, snake_position, apple_position, button_direction, score):
	if button_direction == 1:
		snake_head[0] += 10
	elif button_direction == 0:
		snake_head[0] -= 10
	elif button_direction == 2:
		snake_head[1] += 10
	elif button_direction == 3:
		snake_head[1] -= 10

	if snake_head == apple_position:
		apple_position, score = collision_with_apple(apple_position, score) # Line 6
		snake_position.insert(0, list(snake_head))
	else:
		snake_position.insert(0, list(snake_head))
		snake_position.pop()

	return snake_position, apple_position, score

def display_snake(display, snake_position):
	for position in snake_position:
		pygame.draw.rect(display, green, pygame.Rect(position[0], position[1], 10, 10))

def display_apple(display, apple_position, apple):
	display.blit(apple, (apple_position[0], apple_position[1]))

def play_game(snake_head, snake_position, apple_position, button_direction, apple, score):
	crashed = False
	prev_button_direction = 1
	button_direction = 1
	current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])


	while crashed is not True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # Game crashed unexpectadly
				crashed = True
			if event.type == pygame.KEYDOWN: # KEYDOWN is key press
				if event.key == pygame.K_LEFT and prev_button_direction != 1:
					button_direction = 0
				elif event.key == pygame.K_RIGHT and prev_button_direction != 0:
					button_direction = 1
				elif event.key == pygame.K_UP and prev_button_direction != 2:
					button_direction = 3
				elif event.key == pygame.K_DOWN and prev_button_direction != 3:
					button_direction = 2
				else:
					button_direction = button_direction
		display.fill(black)
		# Display -> window object
		# apple_position -> random.randrange
		# apple -> pygame.image.load
		display_apple(display, apple_position, apple)
		# snake_position -> snake list containing positions
		display_snake(display, snake_position)

		# Modify snake
		# Generate apple
		# Generate snake
		snake_position, apple_position, score = generate_snake(snake_head, snake_position, apple_position,
													button_direction, score)

		pygame.display.set_caption("Snake Game  SCORE: " + str(score))
		pygame.display.update()
		prev_button_direction = button_direction
		current_direction_vector = np.array(snake_position[0]) - np.array(snake_position[1])
		if is_direction_blocked(snake_position, current_direction_vector) == 1:
			crashed = True
		clock.tick(15)



	# Out of While loop, crashed = TRUE
	return score

def display_final_score(prev_score_text, final_score):
	largeText = pygame.font.Font('freesansbold.ttf', 35)
	TextSurf = largeText.render(prev_score_text, True, white)
	TextRect = TextSurf.get_rect()
	TextRect.center = ((display_width/2),(display_height/2))
	display.blit(TextSurf, TextRect)
	pygame.display.update()

# main ->
# 	snake -> 3 unit generation
# 	apple -> random position inside canvas
# 	display -> intialize, 500 X 500, black
# 	game_intro
# 		-> MENU DISPLAY
# 		-> BUtton DISPLAY
# 			-> button() "PLAY" "STOP"
# 				-> IF mouse CLICK
# 					-> PLAY
# 						-> play_game()
# 							play game till crashed not True that is all directions are not blocked
# 							-> display_apple()
# 							-> display_snake()
# 							-> generate_snake()
# 					-> QUIT # button or close button
# 						-> pygame.quit()

def play_game_training(snake_start, snake_position, apple_position, button_direction, score, display, clock, apple):
	crashed = False
	while crashed is not True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed = True
		display.fill((0,0,0))

		display_apple(display, apple_position, apple)
		display_snake(display, snake_position)

		snake_position, apple_position, score = generate_snake(snake_start, snake_position, apple_position,
															   button_direction, score)
		pygame.display.set_caption("SCORE: " + str(score))
		pygame.display.update()
		clock.tick(50000)

		return snake_position, apple_position, score

def starting_positions():
	snake_start = [100, 100]
	snake_position = [[100, 100], [90, 100], [80, 100]]
	apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
	score = 3

	return snake_start, snake_position, apple_position, score

if __name__ == "__main__":
	apple_image = pygame.image.load('apple.png')
	clock = pygame.time.Clock()
	clock.tick(10)
	snake_head = [250, 250]
	snake_position = [[250,250],[240,250],[230,250]]
	apple_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
	score = 0
	pygame.init()
	display = pygame.display.set_mode((display_width, display_height))
	display.fill(window_color)
	pygame.display.update()
	display_text="MENU"
	game_intro()
	final_score = play_game(snake_head, snake_position, apple_position, 1, apple_image, score)
	display = pygame.display.set_mode((display_width, display_height))
	display.fill(window_color)
	pygame.display.update()
	prev_score_text = 'Your Score: ' + str(final_score)
	display_final_score(prev_score_text, final_score)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
				pygame.quit()
