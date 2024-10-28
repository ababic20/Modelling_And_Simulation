import random

def simulate_dog_flea_model(n, iterations):
    # Initial state (all fleas on dog 1)
    state = (n, 0)
    print(f"Initial state: {state}")
    
    # Iterate and simulate flea movements
    for i in range(1, iterations + 1):
        fleas_on_dog1 = state[0]
        r = random.randint(1, n)  # Generate random integer between 1 and n
        
        # Determine transition based on r
        if r <= fleas_on_dog1 and fleas_on_dog1 > 0:
            # Flea jumps from dog 1 to dog 2
            state = (fleas_on_dog1 - 1, n - (fleas_on_dog1 - 1))
        elif fleas_on_dog1 < n:
            # Flea jumps from dog 2 to dog 1
            state = (fleas_on_dog1 + 1, n - (fleas_on_dog1 + 1))
        
        print(f"Iteration {i}, Random number: {r}, State: {state}")

def average_iterations_to_initial_state(n, simulations):
    total_iterations = 0
    
    for sim in range(simulations):
        state = (n, 0) 
        iterations = 0
        
        while state != (n, 0) or iterations == 0:
            fleas_on_dog1 = state[0]
            r = random.randint(1, n)  
            
            if r <= fleas_on_dog1 and fleas_on_dog1 > 0:
                state = (fleas_on_dog1 - 1, n - (fleas_on_dog1 - 1))
            elif fleas_on_dog1 < n:
                state = (fleas_on_dog1 + 1, n - (fleas_on_dog1 + 1))
            
            iterations += 1
        
        total_iterations += iterations
        print(f"Simulation {sim + 1}, Return to initial state after {iterations} iterations")
    
    average_iterations = total_iterations / simulations
    print(f"Average iterations to return to initial state: {average_iterations}")

# Parameters
n = 20  # Number of fleas
iterations = 20  
simulations = 20  

simulate_dog_flea_model(n, iterations)

average_iterations_to_initial_state(n, simulations)
