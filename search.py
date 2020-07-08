# goal test for each state
def test_goal(puzzle_state):
   """test the state is the goal state or not"""
   for i in range(9):
      if puzzle_state.config[i] != i:
          return False
   return True



def bfs_search(initial_state):
    """BFS search"""
    nodes_expanded = cost_of_path = search_depth = max_search_depth = 0
    frontier = [initial_state]
    explored = set()
    f_set = set()
    config = tuple(initial_state.config)
    f_set.add(config)


    while len(frontier) > 0:
        state = frontier[0]
        if len(frontier) == 1:
            frontier = []
        frontier = frontier[1:]
        explored.add(tuple(state.config))
        f_set.remove(tuple(state.config))

        ## goal test
        if test_goal(state):
            cost_of_path = state.cost
            search_depth = state.cost
            nodes_expanded = len(explored) - 1
            return state, cost_of_path, search_depth, nodes_expanded, \
                                                    max_search_depth

        ## expand node and check children
        neighbors = state.expand()
        for neighbor in neighbors:
            config = tuple(neighbor.config)
            if config not in explored and config not in f_set:
                frontier.append(neighbor)
                f_set.add(config)
                max_search_depth = max(max_search_depth, neighbor.cost)

    print("no path has been found")



def dfs_search(initial_state):
    """DFS search"""
    nodes_expanded = cost_of_path = search_depth = max_search_depth = 0
    explored = set()
    f_set = set()
    frontier = [initial_state]
    config = tuple(initial_state.config)
    f_set.add(config)

    while len(frontier)> 0:
        state = frontier.pop()
        explored.add(tuple(state.config))
        f_set.remove(tuple(state.config))

        # goal test
        if test_goal(state):
            cost_of_path = state.cost
            search_depth = state.cost
            nodes_expanded = len(explored) - 1
            return state, cost_of_path, search_depth, nodes_expanded, \
                                                      max_search_depth

        # expand node and check children
        neighbors = state.expand()
        for neighbor in neighbors[::-1]:
            config = tuple(neighbor.config)
            if config not in explored and config not in f_set:
                frontier.append(neighbor)
                f_set.add(config)
                max_search_depth = max(max_search_depth, neighbor.cost)

    print("No path has been found")



## Heuristic function for A star
def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    current_row = idx // n
    current_col = idx % n
    goal_row = value // n
    goal_col = value % n
    return abs(current_row - goal_row) + abs(current_col - goal_col)


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    cost = 0
    for i in range(8):
        if state.config[i] != 0:
            cost += calculate_manhattan_dist(i, state.config[i], 3)
    cost += state.cost
    return cost



## get weight of the move to break tie
def get_move_order(state):
    """pass in a Puzzle state object - assign value to its previous
      move U-0, D-1, L-2, R-3"""
    move = state.action
    if move == "Up":
        return 0
    if move == "Down":
        return 1
    if move == "Left":
        return 2
    else:
        return 3




def A_star_search(initial_state):
    """A * search"""
    nodes_expanded = cost_of_path = search_depth = max_search_depth = 0
    explored = set()
    f_set = set()
    frontier = []
    config = tuple(initial_state.config)
    cost = calculate_total_cost(initial_state)
    heappush(frontier, (cost, -1, initial_state))
    f_set.add(config)

    while frontier:
        state = heappop(frontier)[2]
        explored.add(tuple(state.config))
        f_set.remove(tuple(state.config))

        if test_goal(state):
            cost_of_path = state.cost
            search_depth = state.cost
            nodes_expanded = len(explored) - 1
            return state, cost_of_path, search_depth, nodes_expanded, max_search_depth

        neighbors = state.expand()
        for neighbor in neighbors:
            config = tuple(neighbor.config)
            if config not in explored and config not in f_set:
                cost = calculate_total_cost(neighbor)
                heappush(frontier, (cost, get_move_order(neighbor), neighbor))
                f_set.add(config)
                max_search_depth = max(max_search_depth, neighbor.cost)

    print("No path has been found")
