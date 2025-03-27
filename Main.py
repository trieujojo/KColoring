import tkinter as tk
import matplotlib.pyplot as plt

from UILayer import UILayer

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Graph Coloring Visualizer")
    app = UILayer(root)
    def on_closing():
        plt.close('all')
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
