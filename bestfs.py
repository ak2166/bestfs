#!/usr/bin/env python
"""
.. module:: bestfs
    :platform: Ubuntu
    :synopsis: Module implements best first search in maze. Can run stand-alone.

.. moduleauthor:: Anthony A. Kolodzinski <aak2166@columbia.edu>

"""

import json
import sys
import os
 
class Node :
    '''This class initializes a node data structure and computes a heuristic.'''
    
    g = None
    h = None

    def __init__(self, coordinates, parent, goal):
        '''Initialization method, set attributes and compute h
        
        :param coordinates: The node's coordinates in form (x,y)
        :type coordinates: tuple
        :param parent: Reference to the node's parent node, needed for path reconstruction
        :type parent: Node
        :param goal: The maze's goal coordinates, needed to compute h.
        :type goal: tuple

        '''
        self.coordinates = coordinates
        self.parent = parent
        #Compute heuristic for Best First Search, Manhattan Distance
        dx = coordinates[0] - goal[0]
        dy = coordinates[1] - goal[1]
        self.f = abs(dx)+abs(dy)
       
class BestFirst :
    '''This class contains methods to implement search, import the file, reconstruct the path and get a node's neighbors. 
    '''

    def import_file(self, json_file):
        '''Import the data file to unload json data as a dictionary

        :param json_file: The name of the json file containing maze data.
        :type json_file: str
        :returns environment: The dictionary containing all obstacle, start, and goal positions.
        :type environment: dict
        :raises: IOError

        '''
        try:
            environment = json.loads(open(json_file).read())
        except IOError:
            exit("IOError: Could not read json data")
        return environment

    def get_neighbors(self,parent, goal, obstacles):
        '''Get all neighbors of current node and check if they are walls

        :param parent: The node whose children we are generating.  
        :type parent: tuple
        :param goal: The goal's coordinates.
        :type goal: tuple
        :param obstacles: The set of obstacle coordinates.
        :type obstacles: set
        :returns return_list: List of valid children nodes.
        :type return_list: list

        '''
        return_list = []
        #Generate nodes for each of the parent's adjacent squares
        node_max_x = Node((parent.coordinates[0]+1,parent.coordinates[1]), parent, goal)
        node_max_y = Node((parent.coordinates[0],parent.coordinates[1]+1), parent, goal)
        node_min_x = Node((parent.coordinates[0]-1,parent.coordinates[1]), parent, goal)
        node_min_y = Node((parent.coordinates[0],parent.coordinates[1]-1), parent, goal)
        neighbor_list = [node_max_x, node_max_y, node_min_x, node_min_y]

        #Check if any neighbors are walls and discard where appropriate
        for i in neighbor_list:
            if i.coordinates not in obstacles:
                return_list.append(i)

        return return_list

    def get_path(self, node, obstacles, path_found):
        '''Writes correct path to text file while checking validity
   
        :param node: The node that the search has reached the goal with.
        :type node: Node
        :param obstacles: The set of obstacle coordinates.
        :type obstacles: set
        :param path_found: Tells whether we think we have found a path or no solution
        :type path_found: bool
        :returns int: --return code

        '''
        #List holds the path from start to finish
        file_name, file_extension = os.path.splitext(sys.argv[1])
        text_file = open(str(file_name) + '.txt', 'w')
        if path_found:
             path = []
             while node.parent:

                 if node.coordinates not in obstacles:
                     path.append(node.coordinates)
                     node = node.parent         
                 else:
                     print ("Error: Hit a wall, not a valid path")
                     print node.coordinates
        
             #Add start node
             path.append(node.coordinates)
             path.reverse()
             #Write to file with same name as dataset
             for i in path:
                 text_file.write(str(i[0]) + ',' + str(i[1]) + '\n')
             text_file.close()
             return 0
                 
        else:
            text_file.write("This maze appears to have no solution") 
            text_file.close()
            return 1
     
    def perform_algorithm(self):
        '''Implementation of Best-first Search. Program executes this.

        :returns int: --return  code

        '''
        json_file = sys.argv[1]
        environment = self.import_file(json_file)
        #Cast lists to tuple and set for constant lookup
        obstacles = set(map(tuple, environment['obstacles']))
        start = tuple(environment['robotStart'])
        goal = tuple(environment['robotEnd'])
        #Sets hold open nodes and coordinates
        opened = set()
        visited_coordinates = set()
        opened_coordinates = set()
        #Each node must contain its coordinates and parent
        start_node = Node(start, None, goal)  
        start_node.g = 0
        start_node.f = start_node.h
        opened.add(start_node)
        opened_coordinates.add(start_node.coordinates)

        #Now loop through to implement BFS
        while opened:
            #Set node with lowest h score in opened to current
            current_node = min(opened, key = lambda Node: Node.h)
            opened_coordinates.remove(current_node.coordinates)
            opened.remove(current_node)
            visited_coordinates.add(current_node.coordinates)
            print(current_node.coordinates)
            if current_node.coordinates == goal:
                 return self.get_path(current_node, obstacles, True)

            neighbors = self.get_neighbors(current_node, goal, obstacles)

            for i in neighbors:
                cost = current_node.g + 1
                if i.coordinates in opened_coordinates and cost < i.g:
                    opened_coordinates.remove(i.coordinates)
                    opened.remove(i)
                if i.coordinates in visited_coordinates and cost < i.g:
                    visited_coordinates.remove(i.coordinates)
                if i.coordinates not in visited_coordinates and i.coordinates not in opened_coordinates:
                    i.g = cost
                    i.h = i.g + i.f
                    opened_coordinates.add(i.coordinates)
                    opened.add(i)

        return self.get_path(current_node, obstacles, False)
                            
if __name__ == "__main__":

    search = BestFirst()
    search.perform_algorithm()
                    
