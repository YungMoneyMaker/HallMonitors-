#import packages and modules
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.button import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from buttons import ImageButton, LabelButton, ImageButtonSelectable
import turtle
import numpy as np
from itertools import groupby

#Screens
class HomeScreen(Screen):
    pass

class AboutScreen(Screen):
    pass

class ResourceScreen(Screen):
    pass

class ProgramScreen(Screen):
    start = ObjectProperty(None)
    end = ObjectProperty(None)

    #Program Code
    def btn(self):
        #Initialize game screen
        wn = turtle.Screen()
        wn.bgcolor("white")
        wn.title("TLKNAV")
        wn.setup(1100,400)
        wn.tracer(0)
        turtle.register_shape("brick.gif")
        turtle.register_shape("checkpoint.gif")

        #Pen class
        class Pen(turtle.Turtle):
            def __init__(self):
                turtle.Turtle.__init__(self)
                self.shape("square")
                self.color("black")
                self.penup()
                self.speed(0)
                self.shapesize(0.5, 0.5, 1)

        class Node:
            """
                A node class for A* Pathfinding
                parent is parent of the current Node
                position is current position of the Node in the maze
                g is cost from start to current Node
                h is heuristic based estimated cost for current Node to end Node
                f is total cost of present node i.e. :  f = g + h
            """

            def __init__(self, parent=None, position=None):
                self.parent = parent
                self.position = position

                self.g = 0
                self.h = 0
                self.f = 0
            def __eq__(self, other):
                return self.position == other.position

        #This function return the path of the search
        def return_path(current_node,maze):
            path = []
            no_rows, no_columns = np.shape(maze)
            # here we create the initialized result maze with -1 in every position
            result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            # Return reversed path as we need to show from start to end path
            path = path[::-1]
            start_value = 0
            # we update the path of start to end found by A-star serch with every step incremented by 1
            for i in range(len(path)):
                result[path[i][0]][path[i][1]] = start_value
                start_value += 1
            return result


        def search(maze, cost, start, end):
            """
                Returns a list of tuples as a path from the given start to the given end in the given maze
                :param maze:
                :param cost
                :param start:
                :param end:
                :return:
            """

            # Create start and end node with initized values for g, h and f
            start_node = Node(None, tuple(start))
            start_node.g = start_node.h = start_node.f = 0
            end_node = Node(None, tuple(end))
            end_node.g = end_node.h = end_node.f = 0

            # Initialize both yet_to_visit and visited list
            # in this list we will put all node that are yet_to_visit for exploration. 
            # From here we will find the lowest cost node to expand next
            yet_to_visit_list = []  
            # in this list we will put all node those already explored so that we don't explore it again
            visited_list = [] 
            
            # Add the start node
            yet_to_visit_list.append(start_node)
            
            # Adding a stop condition. This is to avoid any infinite loop and stop 
            # execution after some reasonable number of steps
            outer_iterations = 0
            max_iterations = (len(maze) // 2) ** 10

            # what squares do we search . serarch movement is left-right-top-bottom 
            #(4 movements) from every positon

            move  =  [[-1, 0 ], # go up
                      [ 0, -1], # go left
                      [ 1, 0 ], # go down
                      [ 0, 1 ]] # go right


            """
                1) We first get the current node by comparing all f cost and selecting the lowest cost node for further expansion
                2) Check max iteration reached or not . Set a message and stop execution
                3) Remove the selected node from yet_to_visit list and add this node to visited list
                4) Perofmr Goal test and return the path else perform below steps
                5) For selected node find out all children (use move to find children)
                    a) get the current postion for the selected node (this becomes parent node for the children)
                    b) check if a valid position exist (boundary will make few nodes invalid)
                    c) if any node is a wall then ignore that
                    d) add to valid children node list for the selected parent
                    
                    For all the children node
                        a) if child in visited list then ignore it and try next node
                        b) calculate child node g, h and f values
                        c) if child in yet_to_visit list then ignore it
                        d) else move the child to yet_to_visit list
            """
            #find maze has got how many rows and columns 
            no_rows, no_columns = np.shape(maze)
            
            # Loop until you find the end
            
            while len(yet_to_visit_list) > 0:
                
                # Every time any node is referred from yet_to_visit list, counter of limit operation incremented
                outer_iterations += 1    

                
                # Get the current node
                current_node = yet_to_visit_list[0]
                current_index = 0
                for index, item in enumerate(yet_to_visit_list):
                    if item.f < current_node.f:
                        current_node = item
                        current_index = index
                        
                # if we hit this point return the path such as it may be no solution or 
                # computation cost is too high
                if outer_iterations > max_iterations:
                    print ("giving up on pathfinding too many iterations")
                    return return_path(current_node,maze)

                # Pop current node out off yet_to_visit list, add to visited list
                yet_to_visit_list.pop(current_index)
                visited_list.append(current_node)

                # test if goal is reached or not, if yes then return the path
                if current_node == end_node:
                    path = []
                    current = current_node
                    while current is not None:
                        path.append(current.position)
                        current = current.parent
                    return path[::-1]
                    return return_path(current_node,maze) # Return reversed path


                # Generate children from all adjacent squares
                children = []

                for new_position in move: 

                    # Get node position
                    node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                    # Make sure within range (check if within maze boundary)
                    if (node_position[0] > (no_rows - 1) or 
                        node_position[0] < 0 or 
                        node_position[1] > (no_columns -1) or 
                        node_position[1] < 0):
                        continue

                    # Make sure walkable terrain
                    if maze[node_position[0]][node_position[1]] != 0:
                        continue

                    # Create new node
                    new_node = Node(current_node, node_position)

                    # Append
                    children.append(new_node)

                # Loop through children
                for child in children:
                    
                    # Child is on the visited list (search entire visited list)
                    if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                        continue

                    # Create the f, g, and h values
                    child.g = current_node.g + cost
                    ## Heuristic costs calculated here, this is using eucledian distance
                    child.h = (((child.position[0] - end_node.position[0]) ** 2) + 
                               ((child.position[1] - end_node.position[1]) ** 2)) 

                    child.f = child.g + child.h

                    # Child is already in the yet_to_visit list and g cost is already lower
                    if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                        continue

                    # Add the child to the yet_to_visit list
                    yet_to_visit_list.append(child)

        def makedirections(arr):

            moves = []
            for x in arr[1::]:
                if x[0] > arr[(arr.index(x))-1][0]:
                    moves.append("down")
                elif x[0] < arr[(arr.index(x))-1][0]:
                    moves.append("up")
                elif x[0] == arr[(arr.index(x))-1][0]:
                    if x[1] > arr[(arr.index(x))-1][1]:
                        moves.append("right")
                    if x[1] < arr[(arr.index(x))-1][1]:
                        moves.append("left")

            directions = ([(key, len(list(group))) for key, group in groupby(moves)])
            for u in directions:
                print("Move " + str((u[1]*2)) + " meters " + str(u[0]))

        def makearray(path, a):

            arr = []
            for p in range(len(a)):
                arr.append(list(a[p]))
            for q in path:
                arr[q[0]][q[1]] = "P"
            arr[path[0][0]][path[0][1]] = "S"
            arr[path[-1][0]][path[-1][1]] = "E"
            newArr = []
            for z in arr:
                line = "".join(z)
                newArr.append(line)

            setup_maze(newArr, a)
            wn.update()

        def elevate(start, y, z, end, t, v):
            arr0 = []
            arr01 = []
            tests = []
            for x in staircases:
                path0 = search(y, cost, start, x)
                arr0.append(path0)
                path01 = search(z, cost, x, end)
                arr01.append(path01)
            for x in range(len(arr0)):
                test = len(arr0[x]) + len(arr01[x])
                tests.append(test)
            path1 = arr0[tests.index(min(tests))]
            path2 = arr01[tests.index(min(tests))]
            makedirections(path1)
            print("Climb staircase")
            makedirections(path2)
            makearray(path1, t)
            makearray(path2, v)

        #Level 1
        level_1 = [ "XXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXoooooooooooXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXX",
                    "ooooooooooooooooooooXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXoXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXoXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXoXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXoXXXXXXXXoXXXXXXXXXXXXXXXXXXXXoXX",
                    "XXXXXXXXXoXXXXXXXXoXXXXoXXXXXXXXXXXXXXXoXX",
                    "XXXXXXXXXoXXXXXXXXoXXXXoXXXXXXXXXXXXXXXoXX",
                    "XXXXXXXXXoXXXXXXXXoXXXXoXXXXXXXXXXXXXXXoXX",
                    "XXXXXXXXXooooooooooXXXXoXXXXXXXXXXXXXXXoXX",
                    "XXXXXXXXooooXXXXXXoXXoXoXXXXXXXXXXXXXXXoXX",
                    "XXXXXXXXoXXXXXXXXXooooooooooooooooooooooXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXoXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"]

        level_2 = [ "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXooXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXoXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXoXXXXXXXXoXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXoXXXXXXXXoXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXoXXXXXXXXoXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXoXXXXXXXXoXX",
                    "XXXXXXXXXXXXXXXXXXoXXoXXXXXXXXoXXXXXXXXoXX",
                    "XXXXXXXXXXXXXXXXXXooooooooooooooooooooooXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXoXX",
                    "XXXXXXXXXXXXXXXXXXoXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"]

        #Game map setup function
        def setup_maze(level, a):
            for y in range(len(level)):
                for x in range(len(level[y])):
                    character = level[y][x]
                    
                    if a == level_1:
                        screen_x = -525 + (x * 12)
                        screen_y = 140 - (y * 12)
                    if a == level_2:
                        screen_x = 15 + (x * 12)
                        screen_y = 140 - (y * 12)

                    if character == "X":
                        pen.goto(screen_x, screen_y)
                        pen.shape("brick.gif")
                        pen.stamp()

                    if character == "P":
                        pen.goto(screen_x, screen_y)
                        pen.shape("circle")
                        pen.color("#0066ff")
                        pen.stamp()

                    if character == "S":
                        pen.goto(screen_x, screen_y)
                        pen.shape("triangle")
                        pen.color("yellow")
                        pen.stamp()

                    if character == "E":
                        pen.goto(screen_x, screen_y)
                        pen.shape("checkpoint.gif")
                        pen.stamp()               

        #Create class instances
        pen = Pen()

        #Level setup
        setup_maze(level_1, level_1)
        setup_maze(level_2, level_2)

        #Main loop

            #Update screen
        wn.update()

        if __name__ == '__main__':

            level1 = [  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


            level2 = [  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

            staircases = [[17,18], [6, 19], [15, 21], [16, 36], [17, 39], [10, 39]]

            coordinates_1 = {
                "Entry": [15, 10],  
                "Library": [16, 8],
                "Gym A": [6, 4],
                "Gym B": [14, 9],
                "Fitness Room": [8, 9],
                "Caf": [6, 9],
                "Office": [14, 13],
                "Gym Exit": [6, 0],
                "Caf Exit": [0, 15],
                "Entry B": [18, 18],
                "Entry C": [16, 36],
                "Entry D": [17, 39],
                "Exit B": [10, 39]
                }

            coordinates_2 = {
                "Vucic": [16, 21],
                "Math": [14, 39]
            }

            start = None
            end = None
            cost = 1

            while start not in coordinates_1 and start not in coordinates_2:
                start = self.start.text
            if start in coordinates_1:
                start = coordinates_1[start]
                y = level1
                t = level_1
            elif start in coordinates_2:
                start = coordinates_2[start]
                y = level2
                t = level_2
            while end not in coordinates_1 and end not in coordinates_2:
                end = self.end.text
            if end in coordinates_1:
                end = coordinates_1[end]
                z = level1
                v = level_1
            elif end in coordinates_2:
                end = coordinates_2[end]
                z = level2
                v = level_2
            if y != z:
                elevate(start, y, z, end, t, v)
            else:
                path = search(y, cost, start, end)
                makedirections(path)
                makearray(path, t)

        wn.update()
        wn.exitonclick()

#Program Button Class
class ImageButton(ButtonBehavior, Image):
    pass

#Loading Kivy GUI
GUI = Builder.load_file("kv/main.kv")

class MainApp(App):
    def build(self):
        return GUI

    def change_screen(self, screen_name):
        #Finds screen manager from the kv file
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.current = screen_name
MainApp().run()
         
