import random

def choose_index_for_weights(weights, factor=2.0):
	weighted_sum = 0.0
	for weight in weights:
		weighted_sum += weight ** factor

	rand_pos = random.random() * weighted_sum
	running_sum = 0.0
	for i in range(len(weights)):
		running_sum += weights[i] ** factor
		if rand_pos <= running_sum:
			return i

	return -1123 # should never reach this point

