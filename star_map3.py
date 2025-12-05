#Star map visualization 
#Name: Nischal Rana
#Student Number: C24392253

import pandas as pd 
import py5
import math

def load_data():
    df = pd.read_csv("data/HabHYG15ly.csv", encoding = "latin -1")

def print_stars():
    global df
    global border
    
    for i, row in df.iterrows():
        xg = row['Xg']
        x = py5.remap(xg, -5, 5, border, py5.width - border)
        yg = row['Yg']
        y = py5.remap(yg, -5, 5, border, py5.height - border)
        py5.no_fill()
        py5.circle(x, y, 10)


def draw_grid():
    py5.stroke(128, 0, 128)
    py5.stroke_weight(1)
    py5.text_size(12)
    border = 50

    for i in range(-5, 6):
        x = py5.remap(i, -5, 5, border, py5.width - border)
        y = py5.remap(i, -5, 5, border, py5.height - border)
        py5.text_align(py5.CENTER, py5.CENTER)
        py5.text(i, x, 25)
        py5.text(i, 25, y)

        py5.line(x, border, x, py5.height - border)
        py5.line(border, y, py5.width - border, y)

    for i, row in df.iterrows():
        print(i)
        display_name = row ['Display Name']
        xg = row['Xg']
        x = py5.remap(xg, -5, 5, 0, py5.width)
        print(display_name)


def setup():
    py5.size(500,500)

def draw():
    py5.background(0)

py5.run_sketch()

