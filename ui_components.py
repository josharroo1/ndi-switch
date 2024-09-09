import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def load_background_image(image_path, window_width, window_height):
    try:
        image = Image.open(image_path)
        image_width = int(window_width * 1.5)
        image_height = int(image_width / image.width * image.height)
        image = image.resize((image_width, image_height), Image.LANCZOS)
        
        image_with_opacity = Image.new("RGBA", image.size, (0, 0, 0, 0))
        image_with_opacity.paste(image, (0, 0), image)
        
        data = image_with_opacity.getdata()
        new_data = [(d[0], d[1], d[2], int(d[3] * 0.15)) for d in data]
        image_with_opacity.putdata(new_data)
        
        return ImageTk.PhotoImage(image_with_opacity)
    except Exception as e:
        print(f"Error loading background image: {e}")
        return None

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def create_button(parent, text, command, **kwargs):
    return tk.Button(parent, text=text, command=command, **kwargs)

# Other UI component functions...