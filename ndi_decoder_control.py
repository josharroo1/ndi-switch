import tkinter as tk
from tkinter import ttk
import asyncio
from admin_panel import AdminPanel
from config_manager import ConfigManager
from decoder_manager import DecoderManager
from ui_components import ScrollableFrame, create_button, load_background_image

class NDIDecoderControl:
    def __init__(self, master):
        self.master = master
        self.config_manager = ConfigManager('config.ini')
        self.decoder_manager = DecoderManager(self.config_manager)
        self.admin_panel = AdminPanel(self.master, self)
        
        self.initialize_components()
        
    def initialize_components(self):
        # Initialize UI components
        self.master.title("NDI Decoder Control")
        self.master.geometry("1920x1080")
        self.master.configure(bg='#1c1c1e')

        # Load background image
        self.background_image = load_background_image("assets/background.png", 1920, 1080)
        if self.background_image:
            background_label = tk.Label(self.master, image=self.background_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            print("Background image not found. Using solid color.")

        # Create main frame
        self.main_frame = ScrollableFrame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create buttons
        self.create_buttons()

    def create_buttons(self):
        if not hasattr(self, '_buttons'):
            self._buttons = []
            # Create buttons
            for i in range(5):  # Example: creating 5 buttons
                btn = create_button(self.main_frame.scrollable_frame, f"Button {i+1}", lambda i=i: print(f"Button {i+1} clicked"))
                btn.pack(pady=10)
                self._buttons.append(btn)
        return self._buttons

    @property
    def buttons(self):
        return self.create_buttons()

    async def login(self):
        # Implement your login logic here
        print("Logging in...")
        # Simulating an async operation
        await asyncio.sleep(1)
        print("Logged in successfully")
        return await self.decoder_manager.login()

    # Other methods...