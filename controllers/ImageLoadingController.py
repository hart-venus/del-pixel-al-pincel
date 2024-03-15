import cv2 
import tkinter as tk 
import numpy as np
from tkinter import filedialog # Este módulo permite abrir un cuadro de diálogo para seleccionar un archivo

class ImageLoadingController:

    def __init__(self):
        pass 

    def load_image(self) -> np.ndarray:
        filename = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png"),("All Files","*.*")])
        if filename:
            return cv2.imread(filename)
        return None 
