from game import game



if __name__ == "__main__":
    g = game()
	initiate_instance(g)
	for _ in range(10):
	node = solver.find_best_move(node)
	print('------------')
	print(f'color: {node.color} | best score: {node.score()}')    
	print(node.grid)
	print('------------')