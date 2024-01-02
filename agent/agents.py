import numpy as np
from agent.agent import *
from collections import deque

class myAgent(Agent):
    def __init__(self, matrix):
        """
            Initializes the myAgent agent class

            Args:
                matrix (array): Initial game matrix
        """
        # Initializing the parent class
        super().__init__(matrix)
        print(matrix)
    
    ## !Using A* Algo
    def solve_puzzle(self):
        """
            Solves the game using your algorithm

            Returns:
                list: A list of game matrices that represent the solution
        """
        # Initialize the priority queue with the initial state
        initial_node = Node(None, self.empty_tile, self.initial_matrix)
        self.frontier = PriorityQueue()
        self.frontier.push(initial_node, initial_node.f_score)

        # Initialize the explored set
        self.explored = set()

        while not self.frontier.isEmpty():
            # Pop the node with the lowest f_score from the priority queue
            current_node = self.frontier.pop()

            # Check if the current state is the goal state
            if self.checkEqual(current_node.matrix, self.desired_matrix):
                return self.get_moves(current_node)

            # Add the current state to the explored set
            self.explored.add(tuple(map(tuple, current_node.matrix)))

            # Generate successors
            for direction in self.directions:
                new_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])

                if 0 <= new_position[0] < self.game_size and 0 <= new_position[1] < self.game_size:
                    new_matrix = [list(row) for row in current_node.matrix]
                    new_matrix[current_node.position[0]][current_node.position[1]], new_matrix[new_position[0]][new_position[1]] = \
                        new_matrix[new_position[0]][new_position[1]], new_matrix[current_node.position[0]][current_node.position[1]]

                    if tuple(map(tuple, new_matrix)) not in self.explored and not self.frontier.contains(new_matrix):
                        # Calculate g, h, and f scores for the new node
                        g_score = current_node.g_score + 1
                        h_score = self.calculate_heuristic(new_matrix)
                        f_score = g_score + h_score

                        # Create a new node and push it to the priority queue
                        new_node = Node(current_node, new_position, new_matrix, g_score, h_score)
                        self.frontier.push(new_node, f_score)

                        # Update node information
                        self.generated_node += 1
                        self.maximum_node_in_memory = max(self.maximum_node_in_memory, self.frontier.size())

        # If the goal state is not reached, return an empty list
        return []

    def calculate_heuristic(self, matrix):
        """
        Calculates the Manhattan distance heuristic for the given matrix.

        Args:
            matrix (array): Game matrix

        Returns:
            int: Manhattan distance heuristic value
        """
        heuristic = 0
        for i in range(self.game_size):
            for j in range(self.game_size):
                if matrix[i][j] != 0:
                    desired_position = np.where(self.desired_matrix == matrix[i][j])
                    heuristic += abs(i - desired_position[0]) + abs(j - desired_position[1])
        return heuristic


    ## !Using BFS ALGO
    # def solve_puzzle(self):
    #     # Initial state
    #     initial_node = Node(None, self.empty_tile, self.initial_matrix)
    #     self.frontier = deque([initial_node])
    #     self.explored = set()

    #     while self.frontier:
    #         current_node = self.frontier.popleft()
    #         self.explored.add(tuple(map(tuple, current_node.matrix)))  # Convert matrix to tuple for hashability

    #         if self.checkEqual(current_node.matrix, self.desired_matrix):
    #             # Solution found, reconstruct the path
    #             return self.get_moves(current_node)

    #         # Generate child nodes
    #         for direction in self.directions:
    #             new_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])

    #             if 0 <= new_position[0] < self.game_size and 0 <= new_position[1] < self.game_size:
    #                 new_matrix = [list(row) for row in current_node.matrix]
    #                 new_matrix[current_node.position[0]][current_node.position[1]], new_matrix[new_position[0]][new_position[1]] = \
    #                     new_matrix[new_position[0]][new_position[1]], new_matrix[current_node.position[0]][current_node.position[1]]

    #                 if tuple(map(tuple, new_matrix)) not in self.explored and not self.frontier_contains(new_matrix):
    #                     new_node = Node(current_node, new_position, new_matrix)
    #                     self.frontier.append(new_node)
    #                     self.generated_node += 1

    #                     # Update the maximum nodes in memory
    #                     if len(self.frontier) + len(self.explored) > self.maximum_node_in_memory:
    #                         self.maximum_node_in_memory = len(self.frontier) + len(self.explored)

    #     # No solution found
    #     return []

    # def frontier_contains(self, matrix):
    #     """
    #     Checks if the matrix is in the frontier.

    #     Args:
    #         matrix (list): Matrix to be checked

    #     Returns:
    #         bool: True if the matrix is in the frontier, False otherwise
    #     """
    #     for node in self.frontier:
    #         if self.checkEqual(node.matrix, matrix):
    #             return True
    #     return False
        
    
    ## !!Using Iterative Deepening Depth-First Search (IDDFS) 
    # def solve_puzzle(self):
    #     # Initial state
    #     initial_node = Node(None, self.empty_tile, self.initial_matrix)
    #     max_depth = 1

    #     while True:
    #         result = self.dfs(initial_node, max_depth)
    #         if result:
    #             return result
    #         max_depth += 1

    # def dfs(self, node, max_depth):
    #     self.frontier = [node]
    #     self.explored = set()

    #     while self.frontier:
    #         current_node = self.frontier.pop()
    #         self.explored.add(tuple(map(tuple, current_node.matrix)))  # Convert matrix to tuple for hashability

    #         if self.checkEqual(current_node.matrix, self.desired_matrix):
    #             # Solution found, reconstruct the path
    #             return self.get_moves(current_node)

    #         if current_node.g_score < max_depth:
    #             # Generate child nodes
    #             for direction in self.directions:
    #                 new_position = (current_node.position[0] + direction[0], current_node.position[1] + direction[1])

    #                 if 0 <= new_position[0] < self.game_size and 0 <= new_position[1] < self.game_size:
    #                     new_matrix = [list(row) for row in current_node.matrix]
    #                     new_matrix[current_node.position[0]][current_node.position[1]], new_matrix[new_position[0]][new_position[1]] = \
    #                         new_matrix[new_position[0]][new_position[1]], new_matrix[current_node.position[0]][current_node.position[1]]

    #                     if tuple(map(tuple, new_matrix)) not in self.explored:
    #                         new_node = Node(current_node, new_position, new_matrix, current_node.g_score + 1)
    #                         self.frontier.append(new_node)
    #                         self.generated_node += 1

    #                         # Update the maximum nodes in memory
    #                         if len(self.frontier) + len(self.explored) > self.maximum_node_in_memory:
    #                             self.maximum_node_in_memory = len(self.frontier) + len(self.explored)

    #     # No solution found
    #     return []
    