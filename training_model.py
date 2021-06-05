from snake import *;
from generate_training_data import generate_training_data

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam

display_width = 500
display_height = 500
green = (0,255,0)
red = (255,0,0)
black = (0,0,0)
white = (255,255,255)

pygame.init()
display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
apple_image = pygame.image.load('apple.png')

'''
LEFT -> button_directon = 0
RIGHT -> button_directon = 1
DOWN -> button_direction = 2
UP -> button_directon = 3
'''

training_data_x, training_data_y = generate_training_data(display, clock, apple_image)

model = Sequential([
	Dense(units=9, input_dim=7),
	Dense(units=15, activation='relu'),
	Dense(units=3, activation='softmax')
])

model.compile(loss = 'mean_squared_error', optimizer=Adam(), metrics=['accuracy'])
model.fit(x=np.array(training_data_x).reshape(-1, 7), \
			y=np.array(training_data_y).reshape(-1, 3), \
			validation_split=0.2, \
			batch_size=256, \
			epochs=3, \
			shuffle=True, \
			verbose=2)
model.save_weights('model.h5')
model_json = model.to_json()
with open('model.json', 'w') as json_file:
	json_file.write(model_json)
