import tkinter as tk

class Visualization:
    def __init__(self, map_config):
        self.map_config = map_config

        self.root = tk.Tk()
        self.canvas = None
        self.grid_size = None
        self.cell_size = 0
        self.treasures = None
        self.position = None
        self.movement = "HHDPL"

    def set_position(self, position: tuple[int, int]):
        self.position = position

    def check_for_treasures(self):
        for i, treasure in enumerate(self.treasures):
            if self.position == treasure:
                self.treasures.pop(i)

    def handle_movement(self):
        if self.movement == "":
            return

        step = self.movement[0]
        self.movement = self.movement[1:]

        if step == "H":
            self.set_position((self.position[0], self.position[1] - 1))
        elif step == "D":
            self.set_position((self.position[0], self.position[1] + 1))
        elif step == "P":
            self.set_position((self.position[0] + 1, self.position[1]))
        elif step == "L":
            self.set_position((self.position[0] - 1, self.position[1]))
        else:
            return

        self.check_for_treasures()

    def draw_grid(self):
        # Pri tejto funkci mi pomohla umelá inteligencia.
        # Je to jednoduchý kód ale je to časť kódu, ktorá je nepodstatná pre zadanie
        # (viac menej som to implementoval pre debug aj tak)
        self.canvas.delete("all")
        rows, cols = self.grid_size

        # Draw grid
        for row in range(rows):
            for col in range(cols):
                x1 = row * self.cell_size
                y1 = col * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                # Fill the cell with color if it's in the highlight positions
                if (row, col) in self.treasures:
                    self.canvas.create_rectangle(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="gold")
                if (row, col) == self.position:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="blue")
        self.handle_movement()
        self.root.after(500, self.draw_grid)

    def start_simulation(self, movement):
        self.root.title("2D Grid with Rectangles")

        canvas_width = 400
        canvas_height = 400

        self.movement = movement
        self.grid_size = self.map_config["size"]
        self.position = self.map_config["start_position"]
        self.cell_size = min(canvas_width // self.grid_size[0], canvas_height // self.grid_size[1])
        self.treasures = self.map_config["treasure_coordinates"].copy()

        self.canvas = tk.Canvas(self.root, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        self.root.after(50, self.draw_grid)

        self.root.mainloop()


map_config = {
        "size": (7, 7),
        "start_position": (3, 6),
        "treasure_count": 5,
        "treasure_coordinates": [(4, 1), (2, 2), (6, 3), (1, 4), (4, 5)]
    }
