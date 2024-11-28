import tkinter

import ttkbootstrap as ttkb
from ttkbootstrap import Style
from PIL import Image,ImageTk


class ImageReview(ttkb.Toplevel):
    def __init__(self,parent,image:str):
        super().__init__(parent)
        screen_width = int(self.winfo_screenwidth())
        screen_height = int(self.winfo_screenheight())
        picture_size = self.__get_window_size(image)
        self.geometry(f"{picture_size[0]+20}x{picture_size[1]+20}+{screen_width//2-picture_size[0]//2}+{screen_height//2-picture_size[1]//2}")
        Style("superhero")
        self.resizable(False, False)
        self.title("Recipe Image Review")
        self.attributes('-topmost', 2)
        self.__load_picture()
        self.mainloop()

    def __get_window_size(self,image)->tuple:
        image_object = Image.open(image)
        picture_width: int = image_object.width
        if 500 < picture_width <= 1000:
            picture_width = int(image_object.width//2)
            picture_height = int(image_object.height//2)
            image_object = Image.open(image).resize((picture_width,picture_height))
        elif 1000 < picture_width <= 1600:
            picture_width = int(image_object.width // 3)
            picture_height = int(image_object.height // 3)
            image_object = Image.open(image).resize((picture_width, picture_height))
        elif 1600 < picture_width <= 2500:
            picture_width = int(image_object.width // 4)
            picture_height = int(image_object.height // 4)
            image_object = Image.open(image).resize((picture_width, picture_height))
        elif  picture_width > 2500:
            picture_width = int(image_object.width // 5)
            picture_height = int(image_object.height // 5)
            image_object = Image.open(image).resize((picture_width, picture_height))
        else:
            picture_width = int(image_object.width)
            picture_height = int(image_object.height)
        self.image = ImageTk.PhotoImage(image_object)
        picture_size = (picture_width,picture_height)
        return picture_size

    def __load_picture(self):
        self.picture_label = ttkb.Label(self, image=self.image,relief="groove", borderwidth=2, background="white")
        self.picture_label.pack(fill=tkinter.BOTH, expand=True,padx=10, pady=10)

