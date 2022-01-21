import random

import numpy as np
import tensorflow as tf
from game import current_game


def get_random_dna() -> []:
    # Randomize for all weights and biases
    layers = get_layer_amount()
    dna = []
    for i in range(len(layers) - 1):
        dna.append([[random.uniform(-1, 1) for _ in range(layers[i + 1])] for _ in range(layers[i])])
        if i < len(layers) - 2:
            dna.append([random.uniform(-1, 1) for _ in range(layers[i + 1])])
    return dna


def make_mutation(parent_dna: [], child_dna):
    # Change weights and biases based on rate_of_change from 1-10%
    rate_of_change = random.uniform(.01, .1)
    range_of_change = 1
    for i in range(len(child_dna)):
        for j in range(len(child_dna[i])):
            if i % 2 == 0:
                for k in range(len(child_dna[i][j])):
                    child_dna[i][j][k] = parent_dna[i][j][k]
                    if random.uniform(0, 1) < rate_of_change:
                        child_dna[i][j][k] = random.uniform(-range_of_change, range_of_change)
            else:
                child_dna[i][j] = parent_dna[i][j]
                if random.uniform(0, 1) < rate_of_change:
                    child_dna[i][j] = random.uniform(-range_of_change, range_of_change)
    return child_dna


def refine_mutation(parent_dna: [], child_dna):
    # Change weights and biases based on rate_of_change from 1-10%
    rate_of_change = 1
    range_of_change = .01
    for i in range(len(child_dna)):
        for j in range(len(child_dna[i])):
            if i % 2 == 0:
                for k in range(len(child_dna[i][j])):
                    child_dna[i][j][k] = parent_dna[i][j][k]
                    if random.uniform(0, 1) < rate_of_change:
                        child_dna[i][j][k] = random.uniform(-range_of_change, range_of_change)
            else:
                child_dna[i][j] = parent_dna[i][j]
                if random.uniform(0, 1) < rate_of_change:
                    child_dna[i][j] = random.uniform(-range_of_change, range_of_change)
    return child_dna


def make_child(parent1_dna: [], parent2_dna: [], child_dna):
    # Combine DNA equally for child_dna
    for i in range(len(child_dna)):
        for j in range(len(child_dna[i])):
            if i % 2 == 0:
                for k in range(len(child_dna[i][j])):
                    if random.randint(0, 1) == 0:
                        child_dna[i][j][k] = parent1_dna[i][j][k]
                    else:
                        child_dna[i][j][k] = parent2_dna[i][j][k]
            else:
                if random.randint(0, 1) == 0:
                    child_dna[i][j] = parent1_dna[i][j]
                else:
                    child_dna[i][j] = parent2_dna[i][j]
    return child_dna


def get_inputs():
    # Inputs are based upon booleans
    inputs = [0, 0, 0, 0]

    # Four quadrants of possible target location
    if current_game.target.get_y() > current_game.head.get_y():
        inputs[0] = 1
    if current_game.target.get_x() > current_game.head.get_x():
        inputs[1] = 1
    if current_game.target.get_y() < current_game.head.get_y():
        inputs[2] = 1
    if current_game.target.get_x() < current_game.head.get_x():
        inputs[3] = 1

    # Quality of four closest choices (0 for wall or body and 1 for apple or open space)
    options = current_game.head.get_four_options()
    for option in options:
        cell = current_game.board[option.get_x()][option.get_y()]
        if cell == 1 or cell == 3:
            inputs.append(0)
        else:
            inputs.append(1)

    return np.array([inputs], dtype=float)


def get_layer_amount():
    # List of neural network layer lengths
    return [len(get_inputs()[0]), 8, 4]


def get_move(dna):
    # Forward pass of current snake's dna for next move
    layer = get_inputs()
    for i in range(0, len(dna) - 1, 2):
        layer = np.array(tf.nn.relu(tf.matmul(layer, np.array(dna[i]))) + dna[i + 1])
    output_layer = tf.matmul(layer, np.array(dna[len(dna) - 1]))
    output_layer = tf.reshape(output_layer, -1)
    return int(tf.math.argmax(output_layer))
