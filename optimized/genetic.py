class Genetic:

    def __init__(self, population_size, mutation_rate, max_generations) -> None:
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.current_generation = 0

    def start(self):
        self.start_world()
        while self.current_generation < self.max_generations:
            self.fitness_function()
            self.selection()
        self.fitness_function()
        self.evaluation()

    def start_world(self):
        """Create n-sized array of schedules"""
        pass

    def fitness_function(self):
        pass

    def selection(self):
        pass

    def evaluation(self):
        pass
        
