import random

import json
from game import current_game
import neuralNetwork


class Snake:
    # Snake class for saving DNA and scoring for each snake
    dna = []
    average = 0
    reward = 0

    def get_random_dna(self):
        # Making random DNA and resetting scores
        self.dna = neuralNetwork.get_random_dna()
        self.average = 0
        self.reward = 0

    def make_mutation(self, parent_dna: []):
        # Making mutation on selected parent and resetting scores
        self.dna = neuralNetwork.make_mutation(parent_dna, self.dna)
        self.average = 0
        self.reward = 0

    def refine_mutation(self, parent_dna: []):
        # Making mutation on selected parent and resetting scores
        self.dna = neuralNetwork.refine_mutation(parent_dna, self.dna)
        self.average = 0
        self.reward = 0

    def make_child(self, parent1_dna: [], parent2_dna: []):
        # Making child on selected parents and resetting scores
        self.dna = neuralNetwork.make_child(parent1_dna, parent2_dna, self.dna)
        self.average = 0
        self.reward = 0


def evolve(total_generations: int, generation_size=100):
    # Set up random generation
    generation = []
    for _ in range(generation_size):
        snake = Snake()
        snake.get_random_dna()
        generation.append(snake)
    # Adapt generation
    dna_list = []
    for generation_iteration in range(total_generations):
        # Test snakes in generation
        for i in range(len(generation)):
            test_snake(generation[i])
        # Sort snakes based on reward
        generation.sort(key=lambda x: x.reward, reverse=True)
        dna_list.append(generation[0].dna)
        # Print results for each generation
        test = []
        for i in range(int(generation_size / 10)):
            test.append(f'A:{generation[i].average} R: {int(generation[i].reward)}')
        print(f'Generation {generation_iteration + 1} = {test}')
        # Make new generation with breeding and mutation
        generation = make_new_generation(generation)[:]
    # Save gameplay of best of each generation in json list txt file for gui
    # database.save_gameplay(dna_list)
    with open('dna_data.json', 'w') as f:
        json.dump(dna_list, f)


def make_new_generation(generation: []) -> []:
    generation_size = len(generation)
    # Amount of parents are 10% of generation_size
    parent_size = int(generation_size * .1)
    # Mutation start is the index at where the breeding stops and mutation begins
    refine_mutation_start = int(parent_size * 2)
    mutation_start = int(parent_size * 3)
    # Create child from parents
    for i in range(parent_size, mutation_start):
        index1 = random.randint(0, parent_size - 1)
        index2 = random.randint(0, parent_size - 1)
        generation[i].make_child(generation[index1].dna, generation[index2].dna)
    for i in range(refine_mutation_start, mutation_start):
        generation[i].refine_mutation(generation[i % parent_size].dna)
    # Create mutations from parents
    for i in range(mutation_start, generation_size):
        generation[i].make_mutation(generation[i % parent_size].dna)
    return generation


def test_snake(snake: Snake, number_of_games=int(5)):
    score = 0
    moves = 0
    # Test each individual snake within number_of_games
    for _ in range(number_of_games):
        # Continue game until won or lost
        while not current_game.won and not current_game.lose:
            # Pass get_move to neural network with the snake's DNA
            current_game.move(neuralNetwork.get_move(snake.dna))
        # Keep track of score and moves
        score += current_game.score
        moves += current_game.total_move_count
        # If snake moves in circles set reward to 0 and end test_snake
        if current_game.move_count > ((current_game.max_y - 2) * (current_game.max_x - 2)):
            snake.reward = 0
            # Reset game
            current_game.reset()
            return
        # Reset game
        current_game.reset()
    # Calculate average
    snake.average = score/number_of_games
    # Calculate moves
    moves = moves/number_of_games
    # Send average and moves for calculating reward
    snake.reward = get_reward(snake.average, moves)


def get_reward(average, moves):
    # Find max moves
    max_moves = (current_game.max_y - 2) * (current_game.max_x - 2)
    # Reward explorations and targets acquired
    reward = (average * max_moves) + moves
    return reward


evolve(1000)
