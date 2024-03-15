import numpy as np 
from controllers.ImageLoadingController import ImageLoadingController
import matplotlib.pyplot as plt

def main():
    controller = ImageLoadingController()
    img = controller.load_image()
    # plot image
    plt.imshow(img)
    plt.show()


    print("Hola mundo")

if __name__ == "__main__":
    main()
