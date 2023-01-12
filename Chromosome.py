import math
from geopy.distance import great_circle
import sys

dataset = []


def getdata(file_name):

    with open(file_name, "r") as f:
        for line in f:  # check each line
            # remove spaces at the beginning and the end if they are available
            new_line = line.strip()
            new_line = new_line.split(" ")  # split a string into a list
            # check dataset file to see why id,x,y = 0,1,2
            id, x, y = new_line[1], new_line[2], new_line[3]
            # Create a Node object with id, x, y and add to the data list
            print(id, x, y)
            dataset.append(Node(id=id, x=x, y=y))
    return dataset


class Node:  # Node = Location = Point
    def __init__(self, id, x, y):
        self.x = float(x)
        self.y = float(y)
        self.id = int(id)


def getdataset(filename):
    dataset = getdata(filename)
    return dataset


# N = int(len(dataset))
# Total number of unique points, including starting point


# This function will be run once at the beginning of the program to create a distance matrix
def create_distance_matrix(node_list, N):
    matrix = [[0 for _ in range(N)] for _ in range(N)]

    # classical matrix creation with two for loops
    for i in range(0, len(matrix)-1):
        # print(i, len(matrix))
        for j in range(0, len(matrix)-1):
            print(j, i, len(node_list), node_list[i], len(
                matrix), node_list[len(matrix)-1])
            matrix[node_list[i].id][node_list[j].id] = great_circle((float(node_list[i].x), float(
                node_list[i].y)), (float(node_list[j].x), float(node_list[j].y))).km
    return matrix


def creatematrixe(dataset):
    matrix = create_distance_matrix(dataset, int(len(dataset)))
    return matrix


# matrix =  creatematrixe(getdataset("training_datasett.txt"))
matrix = []

# calculate all distances among all points and create a matrix

# This matrix is needed to decrease the runtime and complexity of general flow.


class Chromosome:
    def __init__(self, node_list):

        self.chromosome = node_list

        chr_representation = []
        for i in range(0, len(node_list)):
            chr_representation.append(self.chromosome[i].id)
        self.chr_representation = chr_representation

        distance = 0
        for j in range(1, len(self.chr_representation) - 1):  # get distances from the matrix
            distance += matrix[self.chr_representation[j] -
                               1][self.chr_representation[j + 1]-1]
        self.cost = distance
        if self.cost > 0:
            self.fitness_value = 1 / self.cost+0.001
        else:
            print(self.cost)
            print("the cost is going to here we have to stop The algorithm fails because each new generation goes badly ")
            sys.exit()
