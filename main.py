import GeneticAlgorithm as GA
import Chromosome as Ch
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure
import time
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import folium as fm
import webbrowser


class mymain():
    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("800x700")
        self.root.title("short path")
        l = tk.Label(
            self.root, text="select the addresses (the first address is the starting and ending address)")
        l.pack()
        self.filename = "training_datasett.txt"
        self.selecteditemfile = "selected_location.txt"
        self.listbox = self.display_location()
        self.b1 = tk.Button(self.root, text="select location ",
                            command=lambda: self.filelocations(self.listbox))
        self.listbox.pack()
        self.b1.pack()
        self.lable_number_of_generation = tk.Label(
            self.root, text="numbers of generation ")
        self.lable_number_of_generation.pack()
        self.entry_n_of_gen = tk.Entry(self.root)
        self.entry_n_of_gen.pack()
        self.lable_population_size_inisial = tk.Label(
            self.root, text="genarated population size ")
        self.lable_population_size_inisial.pack()
        self.entry_size_pop = tk.Entry(self.root)
        self.entry_size_pop.pack()
        self.label_mutation_rate = tk.Label(
            self.root, text="mutation rate (0==>1)")
        self.entry_mut_rat = tk.Entry(self.root)
        self.label_mutation_rate.pack()
        self.entry_mut_rat.pack()
        btn = tk.Button(self.root, text="get  the shortest path ",
                        command=self.getdateinisial)
        btn.pack()

    def getdateinisial(self):
        # parameters
        numbers_of_generations = int(self.entry_n_of_gen.get())
        self.population_size = int(self.entry_size_pop.get())
        self.mut_rate = float(self.entry_mut_rat.get())
        self.dataset = Ch.getdataset(self.selecteditemfile)
        Ch.matrix = Ch.create_distance_matrix(self.dataset, len(self.dataset))
        last_generation, y_axis = self.genetic_algorithm(
            num_of_generations=numbers_of_generations, pop_size=self.population_size, mutation_rate=self.mut_rate, data_list=self.dataset
        )

        best_solution = GA.find_best(last_generation)
        self.draw_cost_generation(y_axis)
        x_list = []
        y_list = []
        for m in range(0, len(best_solution.chromosome)):
            x_list.append(abs(best_solution.chromosome[m].x))
            y_list.append(abs(best_solution.chromosome[m].y))
        self.fig, self.ax = plt.subplots()
        plt.scatter(x_list, y_list)
        self.line1, = self.ax.plot(
            x_list, y_list, '--', lw=2, color='black', ms=1)
        canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        canvas.get_tk_widget().pack()
        canvas.draw()
        for i in last_generation:
            self.draw_path(i)
        self.draw_path(best_solution)
        time.sleep(5)
        canvas.get_tk_widget().destroy()
        map = fm.Map(
            location=[best_solution.chromosome[0].x, best_solution.chromosome[0].y])
        fg = fm.FeatureGroup(name='short path')
        for m in range(0, len(best_solution.chromosome)):
            x_list.append(best_solution.chromosome[m].x)
            y_list.append(best_solution.chromosome[m].y)
        for i in range(1, len(best_solution.chromosome)):
            fg.add_child(fm.Marker(location=[
                         best_solution.chromosome[i].x, best_solution.chromosome[i].y], popup='tkd', icon=fm.Icon(color='green')))
        map.add_child(fg)
        latlog = []
        for i in range(len(best_solution.chromosome), len(x_list)):
            latlog.append((x_list[i], y_list[i]))
        print(latlog)
        fm.PolyLine(latlog).add_to(map)
        map.save("map.html")
        webbrowser.open_new_tab("map.html")

    def display_location(self):
        listbox = tk.Listbox(self.root, width=40,
                             height=10, selectmode=tk.MULTIPLE)
        locations = []
        file = open(self.filename, 'r')
        for id, i in enumerate(file):
            new_line = i.strip()
            new_line = new_line.split(" ")
            listbox.insert(id, new_line[0])
        return listbox

    def filelocations(self, listbox):
        file = open(self.selecteditemfile, 'r+')
        file.seek(0)
        file.truncate(0)
        file.close()
        file = open(self.selecteditemfile, 'a')
        filedataset = open(self.filename, 'r')
        for id, line in enumerate(filedataset):
            if id in listbox.curselection():
                file.write(line)
        self.filelocations = file
        self.listbox.destroy()
        self.b1.destroy()
        file.close()
        filedataset.close()
    # main function for genetic algorithm

    def genetic_algorithm(self, num_of_generations, pop_size, mutation_rate, data_list):
        # first generation is created with initialization function
        new_gen = GA.initialization(data_list, pop_size)

        # this list is only for Cost-Generations graph. it will constitute y-axis of the graph
        costs_for_plot = []

        for iteration in range(0, num_of_generations):
            # create a new generation in each iteration
            new_gen = GA.create_new_generation(new_gen, mutation_rate)
            # print the cost of first chromosome of each new generation to observe the change over generations
            print(str(iteration) + ". generation --> " +
                  "cost --> " + str(new_gen[0].cost))
            # append the best chromosome's cost of each new generation
            costs_for_plot.append(GA.find_best(new_gen).cost)
            # to the list to plot in the graph

        return new_gen, costs_for_plot

    def draw_cost_generation(self, y_list):
        # create a numpy list from 1 to the numbers of generations
        x_list = np.arange(1, len(y_list)+1)

        plt.plot(x_list, y_list)

        plt.title("Route Cost through Generations")
        plt.xlabel("Generations")
        plt.ylabel("Cost")

        plt.show()

    def draw_path(self, solution):
        x_list = []
        y_list = []
        for m in range(0, len(solution.chromosome)):
            x_list.append(abs(solution.chromosome[m].x))
            y_list.append(abs(solution.chromosome[m].y))
        # fig, ax = plt.subplots()
        # plt.scatter(x_list, y_list)
        # line1, = ax.plot(x_list, y_list, '--', lw=2, color='black', ms=1)

        self.line1.set_xdata(x_list)
        self.line1.set_ydata(y_list)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        time.sleep(0.1)


a = mymain()
a.root.mainloop()
