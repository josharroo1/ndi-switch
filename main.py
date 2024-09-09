import tkinter as tk
from ndi_decoder_control import NDIDecoderControl
from config_manager import update_config_file

if __name__ == "__main__":
    update_config_file()
    root = tk.Tk()
    app = NDIDecoderControl(root)
    root.mainloop()