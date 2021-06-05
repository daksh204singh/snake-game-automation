import tensorflow.compat.v1 as tf
from tensorflow.python.keras.backend import set_session
from snake import *
from keras.models import model_from_json
from tqdm import tqdm

''' Configure the session '''
config = tf.ConfigProto()

''' Dynamically grow the memory used on the GPU '''
config.gpu_options.allow_growth = True

''' To log device placement (on which device the operation ran) '''
config.log_device_placement = True

''' Initialize the session object with the custom config created '''
sess = tf.Session(config=config)

''' Pass the session object to the tensorflow set_session '''
set_session(sess)


json_file = open('model.json', 'r')
loaded_json_model = json_file.read()
model = model_from_json(loaded_json_model)
model.load_weights('model.h5')

def run_game_with_automation(model, display, clock, apple):
	max_score = 3
	avg_score = 0
	test_games = 1000
	steps_per_game = 2000

	for _ in tqdm(range(test_games)):
		snake_start, \
			snake_position, \
			apple_position, \
			score = starting_positions()

		for _ in range(steps_per_game):
			current_direction_vector, \
				is_front_blocked, \
				is_left_blocked, \
				is_right_blocked = blocked_directions(snake_position)

			angle, \
				snake_direction_vector, \
				apple_direction_vector_normalized, \
				snake_direction_vector_normalized = \
					angle_with_apple(snake_position, apple_position)


			predicted_direction = np.argmax(np.array(model.predict(np.array( \
												[ \
													is_left_blocked, \
													is_front_blocked, \
													is_right_blocked, \
													apple_direction_vector_normalized[0], \
													snake_direction_vector_normalized[0], \
													apple_direction_vector_normalized[1], \
													snake_direction_vector_normalized[1] \
												]).reshape(-1, 7) \
												) \
											) \
										) - 1

			new_direction = np.array(snake_position[0]) - np.array(snake_position[1])

			if predicted_direction == -1:
				'''
					Non-standard orientation of coordinate axis where
					y increases down and x increases right
					anti-clockwise -> clockwise in conventional plane
					Rotate point to left
					(x, y) -> (y, -x)
				'''
				new_direction = np.array([new_direction[1], -new_direction[0]])
			elif predicted_direction == 1:
				'''
					Non-standard orientation of coordinate axis where
					y increases down and x increases right
					clockwise -> anti-clockwise in conventional plane
					Rotate point to right
					(x, y) -> (-y, x)
				'''
				new_direction = np.array([-new_direction[1], new_direction[0]])
			else:
				''' Same direction '''
				pass

			button_direction = generate_button_direction(new_direction)
			next_step = snake_position[0] + current_direction_vector

			if collision_with_boundaries(snake_position[0]) == 1 \
				or collision_with_self(next_step.tolist(), snake_position) == 1:
				break

			snake_position, apple_position, score = play_game_training( \
														snake_start, \
														snake_position, \
														apple_position, \
														button_direction, \
														score, \
														display, \
														clock,\
														apple)

			if score > max_score:
				max_score = score

		avg_score += score

	return max_score, avg_score/1000



if __name__ == '__main__':
	display_width = 500
	display_height = 500
	pygame.init()
	display = pygame.display.set_mode((display_width, display_height))
	clock = pygame.time.Clock()
	clock.tick(100)
	apple = pygame.image.load('apple.png')
	max_score, avg_score = run_game_with_automation(model, display, clock, apple)
	print("Maximum score achieved is: ", max_score)
	print("Average score achieved is: ", avg_score)
