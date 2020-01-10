#Maze Game by Patrick Pineda

#Import modules
import cgitb
cgitb.enable()
import turtle
import math
import random
import time

headers = {start_response('200 OK', [('Content-Type', 'text/html')])}

#Initialize game screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Escape the maze!")
wn.setup(700,700)
wn.tracer(0)

#Pen class
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)

#Player class
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)
       
#Moving the player
       
    def go_up(self):
        #Calculate new position
        move_to_x = player.xcor()
        move_to_y = player.ycor() + 24
        #Check barrier
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        #Calculate new position
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 24
        #Check barrier
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        self.shape("square")
        #Calculate new position
        move_to_x = player.xcor() - 24
        move_to_y = player.ycor()
        #Check barrier
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        self.shape("square")
        #Calculate new position
        move_to_x = player.xcor() + 24
        move_to_y = player.ycor()
        #Check barrier
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

#Collision function
    def is_collision(self, other):
        a = self.xcor()-other.xcor()
        b = self.ycor()-other.ycor()
        distance = math.sqrt((a ** 2) + (b ** 2)  )

        if distance < 5:
            return True
        else:
            return False

#Death function
def death():
    #Clearing gameboard
    pen.clear()
    walls.clear()
   
#Levels list
levels = [""]

#Level 1
level_1 = [
"XXXXXXXXXXXX XXXXXXXXXXXXXXXX",
"XXXXXXXXXXXX XXXXXXXXXXXXXXXX",
"XXXXXXXXXXXX            XXXXX",
"XXXXXXXXXXXXXX          XXXXX",
"                XXXXXXXXXX  X",
"                XXXXXXXXXX  X",
"XXXXXXX  XXXXX  XXXXXXXXXX  X",
"XXXXXXX  XXXXX  XX XXXXXXX  X",
"XXXXXXX  XXXXX  XX XXXXXXX  X",
"XXXXXXX  XXXXX  XX XXXXXXX  X",
"XXXXXXX         XX XXXXXXX  X",
"XXXXXXX                     X",
"XXXX      XXXX              X",
"XXXX  XXXXXXXX  XXXXXXXXXX  X",
"XX    XXXXXXXX  XXXXXXXXXX  X",
"XX    XXXXXXXXXXXXXXXXXXXXXXX",
"XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

#Appending Level 1 to Levels list
levels.append(level_1)

#Game map setup function
def setup_maze(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("square")
                pen.stamp()
                #Append coordinates to wall list
                walls.append((screen_x, screen_y))

            if character == "P":
                pen.goto(screen_x, screen_y)
                pen.shape("circle")
                pen.stamp()                

#Create class instances
pen = Pen()

#Create lists
walls = []

#Level setup
setup_maze(levels[1])

#Keyboard Binding
def playermovement():
    turtle.listen()
    turtle.onkey(player.go_left,"Left")
    turtle.onkey(player.go_right,"Right")
    turtle.onkey(player.go_down,"Down")
    turtle.onkey(player.go_up,"Up")

#Turn of screen updates
wn.tracer(0)

#Main loop
while True:

    #Update screen
    wn.update()
    import numpy as np
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


    if __name__ == '__main__':

        level_1 = [ [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                    [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
                    [1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        floor_1 = ["Entry", "Library", "Gym A", "Gym B", "Fitness Room", "Caf", "Office", "Gym Exit", "Caf Exit",
                   "Entry B", "Entry C", "Exit B"]
        coords_1 = [[12, 8], [14, 5], [5, 3], [10, 7], [7, 7], [4, 8], [11, 11], [5, 0], [0, 12], [14, 15], [14, 27], [4, 27]]
        start = 0
        end = 0
        while start not in floor_1:
            start = input("From?\n")
        start = coords_1[floor_1.index(start)]
        while end not in floor_1:
            end = input("To?\n")
        end = coords_1[floor_1.index(end)]
        cost = 1 # cost per movement

        path = search(level_1,cost, start, end)
        print(path)

    level_1 = [
    "XXXXXXXXXXXX XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXX XXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXX            XXXXX",
    "XXXXXXXXXXXXXX          XXXXX",
    "                XXXXXXXXXX  X",
    "                XXXXXXXXXX  X",
    "XXXXXXX  XXXXX  XXXXXXXXXX  X",
    "XXXXXXX  XXXXX  XX XXXXXXX  X",
    "XXXXXXX  XXXXX  XX XXXXXXX  X",
    "XXXXXXX  XXXXX  XX XXXXXXX  X",
    "XXXXXXX         XX XXXXXXX  X",
    "XXXXXXX                     X",
    "XXXX      XXXX              X",
    "XXXX  XXXXXXXX  XXXXXXXXXX  X",
    "XX    XXXXXXXX  XXXXXXXXXX  X",
    "XX    XXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ]
    arr = []
    for p in range(len(level_1)):
        arr.append(list(level_1[p]))
    for q in path:
        arr[q[0]][q[1]] = "P"
    newArr = []
    for z in arr:
        line = "".join(z)
        newArr.append(line)
    setup_maze(newArr)
    wn.update()
    x = input("Would you like to run again? Y/N\n")
    if x == "N":
        break
    else:
        death()
        setup_maze(level_1)
    wn.update()
