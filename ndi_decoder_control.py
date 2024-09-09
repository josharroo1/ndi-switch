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
        
        self.initialize_components()
        
    def initialize_components(self):
        # Initialize UI components
        self.master.title("NDI Decoder Control")
        self.master.geometry("1920x1080")
        self.master.configure(bg='#1c1c1e')

        # Make the window fullscreen
        self.master.attributes('-fullscreen', True)

        # Load background image
        self.background_image = load_background_image("assets/background.png", 1920, 1080)
        if self.background_image:
            background_label = tk.Label(self.master, image=self.background_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create main frame
        self.main_frame = tk.Frame(self.master, bg='#1c1c1e')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create tabs
        self.create_control_tab()
        self.create_admin_tab()

    def create_control_tab(self):
        control_frame = ttk.Frame(self.notebook)
        self.notebook.add(control_frame, text="Control")

        # Welcome message
        welcome_label = tk.Label(control_frame, text="Welcome to NDI Decoder Control", 
                                 font=("Roboto", 24), bg='#1c1c1e', fg='white')
        welcome_label.pack(pady=(20, 10))

        # Create frames for decoders and sources
        decoder_frame = ttk.Frame(control_frame)
        decoder_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        source_frame = ttk.Frame(control_frame)
        source_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Decoder selection
        tk.Label(decoder_frame, text="Select Decoder", font=("Roboto", 18), bg='#1c1c1e', fg='white').pack(pady=(0, 10))
        self.decoder_listbox = tk.Listbox(decoder_frame, font=("Roboto", 14), bg='#333333', fg='white')
        self.decoder_listbox.pack(fill=tk.BOTH, expand=True)
        self.populate_decoder_list()

        # Source selection
        tk.Label(source_frame, text="Select Source", font=("Roboto", 18), bg='#1c1c1e', fg='white').pack(pady=(0, 10))
        self.source_listbox = tk.Listbox(source_frame, font=("Roboto", 14), bg='#333333', fg='white')
        self.source_listbox.pack(fill=tk.BOTH, expand=True)
        self.populate_source_list()

        # Control buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, pady=20)

        apply_button = create_button(button_frame, "Apply", self.apply_changes)
        apply_button.pack(side=tk.LEFT, padx=10)

        refresh_button = create_button(button_frame, "Refresh", self.refresh_lists)
        refresh_button.pack(side=tk.RIGHT, padx=10)

    def create_admin_tab(self):
        self.admin_panel = AdminPanel(self.notebook, self)
        self.notebook.add(self.admin_panel, text="Admin")

    def populate_decoder_list(self):
        self.decoder_listbox.delete(0, tk.END)
        for decoder in self.config_manager.get_decoders():
            self.decoder_listbox.insert(tk.END, decoder['name'])

    def populate_source_list(self):
        self.source_listbox.delete(0, tk.END)
        for source in self.config_manager.get_user_friendly_names():
            self.source_listbox.insert(tk.END, source)

    def apply_changes(self):
        selected_decoder = self.decoder_listbox.curselection()
        selected_source = self.source_listbox.curselection()

        if selected_decoder and selected_source:
            decoder_index = selected_decoder[0]
            source_index = selected_source[0]
            
            # Here you would typically call methods to change the decoder and source
            print(f"Changing to Decoder: {self.config_manager.get_decoders()[decoder_index]['name']}")
            print(f"Changing to Source: {self.config_manager.get_user_friendly_names()[source_index]}")
            
            # Placeholder for actual change implementation
            # self.change_decoder(decoder_index)
            # self.change_source(source_index)

    def refresh_lists(self):
        self.populate_decoder_list()
        self.populate_source_list()

    async def login(self):
        # Implement login logic here
        pass

    async def cleanup(self):
        # Implement cleanup logic here
        pass

# The main execution part remains in main.py