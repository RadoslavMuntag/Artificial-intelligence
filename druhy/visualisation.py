import tkinter as tk
from PIL import ImageTk, Image
import time

from point import Point
from constants import *
from algorithms import KDTree


def draw_pixel(pixels: Image.Image.load, x: int, y: int, color="black"):
    x, y = (x + SIZE) * WIN_SCALE, (y + SIZE) * WIN_SCALE
    pixels[int(x), int(y)] = color


class Visualization:
    def __init__(self, tree_root: KDTree, point_list: list[Point]):
        '''
        Vizualizácia v tkinteri a s pomocou pillow
        :param tree_root:
        :param point_list:
        '''
        self.root = tk.Tk()

        self.tree_root = tree_root
        self.point_list = point_list

        self.canvas_width, self.canvas_height = int(SIZE * WIN_SCALE * 2), int(SIZE * WIN_SCALE * 2)  # dĺťky strán
        # pillow images pre tkinter
        self.img_org: ImageTk.PhotoImage = None
        self.img_k1: ImageTk.PhotoImage = None
        self.img_k3: ImageTk.PhotoImage = None
        self.img_k7: ImageTk.PhotoImage = None
        self.img_k15: ImageTk.PhotoImage = None

    def start_simulation(self, timer):
        '''
        Pred pripravenie dát na vykreslenie, tu sa klasifikujú prázne body v priestore
        :param timer:
        :return:
        '''
        accuracy = {  # počítanie presnosti klasifikácie
            1: 0,
            3: 0,
            7: 0,
            15: 0,
        }

        # originálny obraz bez klasifikácie
        pillow_image = Image.new("RGB", (self.canvas_width + 1, self.canvas_height + 1), (0, 0, 0))
        pixels = pillow_image.load()

        for point in self.point_list:
            draw_pixel(pixels, point.pos[0], point.pos[1], point.color.value)  # vykreslenie každého bodu na obraz

            # počítanie presnosti klasifikácie
            if K_Values[1]:
                if point.color == point.k1_color:
                    accuracy[1] += 1
            if K_Values[3]:
                if point.color == point.k3_color:
                    accuracy[3] += 1
            if K_Values[7]:
                if point.color == point.k7_color:
                    accuracy[7] += 1
            if K_Values[15]:
                if point.color == point.k15_color:
                    accuracy[15] += 1

        if K_Values[1]:
            print("K1 accuracy is:", accuracy[1]/(POINTS_TO_GENERATE*4) * 100, "%")
        if K_Values[3]:
            print("K3 accuracy is:", accuracy[3]/(POINTS_TO_GENERATE*4) * 100, "%")
        if K_Values[7]:
            print("K7 accuracy is:", accuracy[7]/(POINTS_TO_GENERATE*4) * 100, "%")
        if K_Values[15]:
            print("K15 accuracy is:", accuracy[15]/(POINTS_TO_GENERATE*4) * 100, "%")

        self.img_org = ImageTk.PhotoImage(pillow_image)  # hotový obraz bez klasifikácie

        # klasifikovanie prázdnych miest
        if FILL_EMPTY_SPACE:
            for x in range(self.canvas_width):
                for y in range(self.canvas_height):
                    if pixels[x, y] == (0, 0, 0):
                        new_x, new_y = (x / WIN_SCALE) - SIZE, (y / WIN_SCALE) - SIZE  # redo škálovania pre obraz
                        new_point = Point(Point.Color.RED)
                        new_point.hard_set_position(int(new_x), int(new_y))

                        self.tree_root.insert_and_classify(new_point, K)  # klasifikovanie doplnkových bodov
                        self.point_list.append(new_point)

        self.draw_stuff(timer)

    def draw_stuff(self, timer):
        '''
        Vykreslenie všetkých modulov na tkinter okno
        :param timer:
        :return:
        '''
        self.root.title("Original color Window")

        # inicializácia hlavného okna so scroll barom
        main_canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        main_canvas.config(yscrollcommand=scrollbar.set)

        frame = tk.Frame(main_canvas)

        # modul bez klasifikácie
        org_canvas = tk.Canvas(frame, width=self.canvas_width, height=self.canvas_height, bg="black")

        label_org = tk.Label(frame, text="Generated Points", bg="white")
        label_org.pack(fill="x")
        org_canvas.pack(fill="x", pady=5)
        org_canvas.create_image((SIZE*WIN_SCALE, SIZE*WIN_SCALE), image=self.img_org)

        if K_Values[1]:  # k1 modul
            label_k1 = tk.Label(frame, text="K1 Classified Points", bg="white")
            label_k1.pack(fill="x")
            k1_canvas = tk.Canvas(frame, width=self.canvas_width, height=self.canvas_height, bg="black")
            k1_canvas.pack(fill="x", pady=5)
            k1_pillow_image = Image.new("RGB", (self.canvas_width + 1, self.canvas_height + 1), "black")
            k1_pixels = k1_pillow_image.load()

        if K_Values[3]:  # k3 modul
            label_k3 = tk.Label(frame, text="K3 Classified Points", bg="white")
            label_k3.pack(fill="x")
            k3_canvas = tk.Canvas(frame, width=self.canvas_width, height=self.canvas_height, bg="black")
            k3_canvas.pack(fill="x", pady=5)
            k3_pillow_image = Image.new("RGB", (self.canvas_width + 1, self.canvas_height + 1), "black")
            k3_pixels = k3_pillow_image.load()

        if K_Values[7]:  # k7 modul
            label_k7 = tk.Label(frame, text="K7 Classified Points", bg="white")
            label_k7.pack(fill="x")
            k7_canvas = tk.Canvas(frame, width=self.canvas_width, height=self.canvas_height, bg="black")
            k7_canvas.pack(fill="x", pady=5)
            k7_pillow_image = Image.new("RGB", (self.canvas_width + 1, self.canvas_height + 1), "black")
            k7_pixels = k7_pillow_image.load()

        if K_Values[15]:  # k15 modul
            label_k15 = tk.Label(frame, text="K15 Classified Points", bg="white")
            label_k15.pack(fill="x")
            k15_canvas = tk.Canvas(frame, width=self.canvas_width, height=self.canvas_height, bg="black")
            k15_canvas.pack(fill="x", pady=5)
            k15_pillow_image = Image.new("RGB", (self.canvas_width + 1, self.canvas_height + 1), "black")
            k15_pixels = k15_pillow_image.load()

        for point in self.point_list:  # vykreslenie bodov do jednotlivých obrazov
            if K_Values[1]:
                draw_pixel(k1_pixels, point.pos[0], point.pos[1], point.k1_color.value)

            if K_Values[3]:
                draw_pixel(k3_pixels, point.pos[0], point.pos[1], point.k3_color.value)

            if K_Values[7]:
                draw_pixel(k7_pixels, point.pos[0], point.pos[1], point.k7_color.value)

            if K_Values[15]:
                draw_pixel(k15_pixels, point.pos[0], point.pos[1], point.k15_color.value)

        # priradenie obrazov k modulom
        if K_Values[1]:
            self.img_k1 = ImageTk.PhotoImage(k1_pillow_image)
            k1_canvas.create_image((SIZE * WIN_SCALE, SIZE * WIN_SCALE), image=self.img_k1)

        if K_Values[3]:
            self.img_k3 = ImageTk.PhotoImage(k3_pillow_image)
            k3_canvas.create_image((SIZE * WIN_SCALE, SIZE * WIN_SCALE), image=self.img_k3)

        if K_Values[7]:
            self.img_k7 = ImageTk.PhotoImage(k7_pillow_image)
            k7_canvas.create_image((SIZE * WIN_SCALE, SIZE * WIN_SCALE), image=self.img_k7)

        if K_Values[15]:
            self.img_k15 = ImageTk.PhotoImage(k15_pillow_image)
            k15_canvas.create_image((SIZE * WIN_SCALE, SIZE * WIN_SCALE), image=self.img_k15)

        main_canvas.create_window((0, 0), window=frame, anchor="nw")

        frame.update_idletasks()
        main_canvas.config(scrollregion=main_canvas.bbox("all"))

        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        filename = 'data_whole.txt'  # analýza času
        with open(filename, 'a') as file:
            current_time = time.time() - timer
            file.write(f"{current_time} {POINTS_TO_GENERATE}\n")

        self.root.mainloop()
