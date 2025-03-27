import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import simpledialog, messagebox
import networkx as nx
import random

from Graph import Graph
from ColoringLogic import ColoringLogic

# --- UI Layer Class ---
class UILayer:
    def __init__(self, root):
        self.root = root
        self.graph = Graph()
        self.logic = ColoringLogic()
        self.selected_node = []
        self.dragging_node = None

        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        control_frame = tk.Frame(root)
        control_frame.pack()

        tk.Button(control_frame, text="Add Node", command=self.add_node).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Delete Node", command=self.delete_selected_node).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Color Graph", command=self.color_graph).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Add Edges", command=self.add_edges).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Remove Edges", command=self.remove_edges).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Select random", command=self.select_random).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Unselect", command=self.unselect_all).pack(side=tk.LEFT, padx=5)


        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.canvas.mpl_connect("motion_notify_event", self.on_drag)
        self.canvas.mpl_connect("button_release_event", self.on_release)

        self.root.bind("<Return>", self.color_graph)
        self.draw_graph()

    def add_node(self):
        # Get axis bounds
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()

        x = random.uniform(xlim[0], max(xlim[1],5))
        y = random.uniform(ylim[0], max(ylim[1],5))

        self.graph.add_node(x, y)
        # self.selected_node = None
        self.draw_graph()

    def draw_graph(self, coloring=None):
        self.ax.clear()
        pos = self.graph.get_positions()
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'cyan', 'pink']
        node_colors = []

        for node in self.graph.G.nodes():
            color = coloring[node] if coloring else None
            if node in self.selected_node:
                node_colors.append("lime")
            else:
                node_colors.append(colors[color % len(colors)] if color is not None else 'skyblue')

        nx.draw(self.graph.G, pos, ax=self.ax, with_labels=True,
                node_color=node_colors, node_size=700, font_size=12, edge_color='gray')
        self.canvas.draw()

    def add_edges(self):
        self.graph.add_all_edge(self.selected_node)
        self.draw_graph()

    def remove_edges(self):
        self.graph.remove_all_edges(self.selected_node)
        self.draw_graph()

    def unselect_all(self):
        self.selected_node = []
        self.draw_graph()

    def select_random(self):
        fract = random.uniform(0,1)
        self.selected_node = []
        for i in self.graph.nodes:
            if random.uniform(0,1)>= fract:
                self.selected_node.append(i)
        self.draw_graph()

    def on_click(self, event):
        if event.inaxes != self.ax:
            return

        x, y = event.xdata, event.ydata
        clicked = self.graph.get_node_at(x, y)

        if clicked:
            if clicked in self.selected_node :
                self.selected_node.remove(clicked)
            else:
                self.selected_node.append(clicked)
            self.dragging_node = clicked
        else:
            self.selected_node = []

        self.draw_graph()

    def on_drag(self, event):
        if event.inaxes != self.ax or not self.dragging_node:
            return
        self.graph.move_node(self.dragging_node, event.xdata, event.ydata)
        self.draw_graph()

    def on_release(self, event):
        self.dragging_node = None

    def delete_selected_node(self):
        if self.selected_node:
            for n in self.selected_node:
                self.graph.delete_node(n)
            self.selected_node = []
            self.draw_graph()

    def color_graph(self, event=None):
        self.selected_node = []
        self.draw_graph()
        k = simpledialog.askinteger("Coloring", "Enter number of colors (k):")
        if not k:
            return
        coloring = self.logic.k_color(self.graph, k)
        if coloring:
            self.draw_graph(coloring)
        else:
            messagebox.showerror("Error", f"No valid {k}-coloring found.")
