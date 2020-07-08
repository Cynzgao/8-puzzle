class puzzleSolver(object):
    def __init__(self, initial_state, algorithm):
        self.initial_state = initial_state
        self.alg = algorithm
        self.path_to_goal = []
        self.cost_of_path = 0
        self.nodes_expanded = 0
        self.search_depth = 0
        self.max_search_depth = 0


    def path_finding(self, end_state):
        """pass in the PuzzleState object; use its parent to find path"""
        path = []
        state = end_state
        while(state.parent):
            path.append(state.action)
            state = state.parent
        return path[::-1]

    def solve(self):
        start_time = time.time()
        if   self.alg == "bfs":
            res, self.cost_of_path, self.search_depth, self.nodes_expanded, \
            self.max_search_depth= bfs_search(self.initial_state)
        elif self.alg == "dfs":
            res, self.cost_of_path, self.search_depth, self.nodes_expanded, \
            self.max_search_depth= dfs_search(self.initial_state)
        elif self.alg == "ast":
            res, self.cost_of_path, self.search_depth, self.nodes_expanded, \
            self.max_search_depth= A_star_search(self.initial_state)
        else:
            print("Enter valid command arguments !")
        running_time = time.time() - start_time
        end_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        max_ram = float(end_ram/1024e3)
        self.writeOutput(res, running_time, max_ram)


    def writeOutput(self, result, running_time, ram_usage):
        self.path_to_goal = self.path_finding(result)
        file = open('output.txt', 'w')
        file.write("path_to_goal: " + str(self.path_to_goal) + '\n')
        file.write("cost_of_path: " + str(self.cost_of_path) + '\n')
        file.write("nodes_expanded: " + str(self.nodes_expanded) + '\n')
        file.write("search_depth: " + str(self.search_depth) + '\n')
        file.write("max_search_depth: " + str(self.max_search_depth) + '\n')
        file.write("running_time: " + str(running_time) + '\n')
        file.write("max_ram_usage: " + str(ram_usage) + '\n')
        file.close()


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    solver = puzzleSolver(hard_state, search_mode)
    solver.solve()

if __name__ == '__main__':
    main()
