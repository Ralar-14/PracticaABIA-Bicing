import timeit
from aima.search import hill_climbing, simulated_annealing
from Bicing_problem_parameters import ProblemParameters
from BicingState import generate_initial_state
from bicing_problem import BicingProblem

for i in range(10):
    params = ProblemParameters(1250, 5, 25, i)
    initial_state = generate_initial_state(params)
    print(initial_state)
    #n = simulated_annealing(BicingProblem(initial_state)) 
    n = hill_climbing(BicingProblem(initial_state))
    print(f"Dinero ganado: {n.heuristic()}")