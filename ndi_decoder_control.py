import configparser
import tkinter as tk
from tkinter import messagebox
import requests
import hashlib
import urllib.parse
import math
import time
import tkinter.ttk as ttk
from PIL import Image, ImageTk  # Make sure to install pillow: pip install pillow
import datetime
import os

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = tk.Canvas(self, bg='#1c1c1e')
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

class AdminPanel(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg='#1c1c1e')
        self.app = app
        
        # Initialize attributes
        self.welcome_entry = None
        self.select_source_entry = None
        self.select_decoder_entry = None
        self.sources_entry = None
        self.names_entry = None
        self.num_decoders_entry = None
        
        # Create and configure style
        self.style = ttk.Style()
        self.style.configure('Dark.TFrame', background='#1c1c1e')
        self.style.configure('Dark.TLabelframe', background='#1c1c1e')
        self.style.configure('Dark.TLabelframe.Label', background='#1c1c1e', foreground='white')
        
        self.log_text = None
        self.create_widgets()

    def create_widgets(self):
        self.scrollable_frame = ScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True)

        frame = self.scrollable_frame.scrollable_frame
        frame.configure(style='Dark.TFrame')  # Use the custom style

        # Create a grid layout
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)

        # General Settings Section
        general_frame = self.create_section(frame, "General Settings", [
            ("Edit Welcome Message:", 'welcome_entry', self.update_welcome_message),
            ("Edit 'Select Source' Text:", 'select_source_entry', self.update_select_source_text),
            ("Edit 'Select Decoder' Text:", 'select_decoder_entry', self.update_select_decoder_text)
        ])
        general_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Sources Section
        sources_frame = self.create_section(frame, "Sources", [
            ("Edit Sources (comma-separated):", 'sources_entry', self.update_sources),
            ("Edit Button Names (comma-separated):", 'names_entry', self.update_button_names)
        ])
        sources_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Decoders Section
        decoders_frame = self.create_section(frame, "Decoders", [
            ("Number of Decoders:", 'num_decoders_entry', None)
        ])
        decoders_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        update_decoders_btn = tk.Button(frame, text="Update Decoders", command=self.update_decoders, 
                                        bg='#333333', fg='white', font=("Roboto", 14))
        update_decoders_btn.grid(row=1, column=1, pady=10)

        # Decoder Fields
        decoder_fields_frame = ttk.Frame(frame, style='Dark.TFrame')
        decoder_fields_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        
        self.decoder_entries = []
        self.decoder_name_entries = []  # New list for decoder name entries
        for i in range(len(self.app.decoders)):
            self.add_decoder_fields(decoder_fields_frame, i)

        # Control Buttons
        close_panel_btn = tk.Button(frame, text="Close Admin Panel", command=self.close_panel, 
                                    bg='#333333', fg='white', font=("Roboto", 14))
        close_panel_btn.grid(row=3, column=0, pady=10)

        close_app_btn = tk.Button(frame, text="Close Application", command=self.close_app, 
                                  bg='#333333', fg='white', font=("Roboto", 14))
        close_app_btn.grid(row=3, column=2, pady=10)

        # Add Log Display
        log_frame = ttk.LabelFrame(frame, text="Log", style='Dark.TLabelframe')
        log_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        
        self.log_text = tk.Text(log_frame, bg='#333333', fg='white', font=("Roboto", 12), height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Make the log frame expandable
        frame.grid_rowconfigure(4, weight=1)

    def create_section(self, parent, title, fields):
        section_frame = ttk.LabelFrame(parent, text=title, style='Dark.TLabelframe')
        
        for i, (label_text, entry_var, command) in enumerate(fields):
            label = tk.Label(section_frame, text=label_text, bg='#1c1c1e', fg='white', font=("Roboto", 14))
            label.grid(row=i*2, column=0, sticky="w", pady=(5,0))

            entry = tk.Entry(section_frame, width=30, bg='#333333', fg='white', font=("Roboto", 12))
            entry.grid(row=i*2+1, column=0, sticky="ew", pady=(0,5))
            
            if entry_var == 'welcome_entry':
                entry.insert(0, self.app.welcome_message)
            elif entry_var == 'select_source_entry':
                entry.insert(0, self.app.config['Messages'].get('select_source', 'Select Source'))
            elif entry_var == 'select_decoder_entry':
                entry.insert(0, self.app.config['Messages'].get('select_decoder', 'Select Decoder'))
            elif entry_var == 'sources_entry':
                entry.insert(0, ','.join(self.app.sources))
            elif entry_var == 'names_entry':
                entry.insert(0, ','.join(self.app.user_friendly_names))
            elif entry_var == 'num_decoders_entry':
                entry.insert(0, str(len(self.app.decoders)))

            setattr(self, entry_var, entry)

            if command:
                btn = tk.Button(section_frame, text=f"Update {label_text.split(':')[0]}", command=command, 
                                bg='#333333', fg='white', font=("Roboto", 12))
                btn.grid(row=i*2+1, column=1, padx=(5,0), pady=(0,5))

        section_frame.columnconfigure(0, weight=1)
        return section_frame

    def add_decoder_fields(self, parent, index):
        decoder_frame = ttk.LabelFrame(parent, text=f"Decoder {index + 1}", style='Dark.TLabelframe')
        decoder_frame.grid(row=index // 3, column=index % 3, sticky="nsew", padx=5, pady=5)

        fields = [("Name:", 'name'), ("IP:", 'ip'), ("Username:", 'username'), ("Password:", 'password')]
        for i, (label_text, key) in enumerate(fields):
            label = tk.Label(decoder_frame, text=label_text, bg='#1c1c1e', fg='white', font=("Roboto", 14))
            label.grid(row=i*2, column=0, sticky="w", pady=(5,0))

            entry = tk.Entry(decoder_frame, width=20, bg='#333333', fg='white', font=("Roboto", 12))
            entry.grid(row=i*2+1, column=0, sticky="ew", pady=(0,5))
            if key == 'name':
                entry.insert(0, self.app.decoders[index].get('name', f"Decoder {index + 1}"))
                self.decoder_name_entries.append(entry)
            else:
                entry.insert(0, self.app.decoders[index][key])
                self.decoder_entries.append(entry)

        decoder_frame.columnconfigure(0, weight=1)

    def update_sources(self):
        new_sources = [s.strip() for s in self.sources_entry.get().split(',')]
        self.app.update_sources(new_sources)

    def update_button_names(self):
        new_names = [n.strip() for n in self.names_entry.get().split(',')]
        self.app.update_button_names(new_names)

    def update_welcome_message(self):
        new_message = self.welcome_entry.get()
        self.app.config['Messages']['welcome'] = new_message
        self.app.save_config()
        self.app.welcome_message = new_message
        self.app.welcome_label.config(text=new_message)

    def update_decoders(self):
        num_decoders = int(self.num_decoders_entry.get())
        self.app.decoders = []
        
        for i in range(num_decoders):
            name = self.decoder_name_entries[i].get() if i < len(self.decoder_name_entries) else f"Decoder {i + 1}"
            ip = self.decoder_entries[i * 3].get() if i < len(self.decoder_entries) // 3 else ''
            username = self.decoder_entries[i * 3 + 1].get() if i < len(self.decoder_entries) // 3 else ''
            password = self.decoder_entries[i * 3 + 2].get() if i < len(self.decoder_entries) // 3 else ''
            self.app.decoders.append({'name': name, 'ip': ip, 'username': username, 'password': password})
        
        self.app.update_decoders()
        
        # Refresh the decoder entries
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def update_select_source_text(self):
        new_text = self.select_source_entry.get()
        self.app.config['Messages']['select_source'] = new_text
        self.app.save_config()

    def update_select_decoder_text(self):
        new_text = self.select_decoder_entry.get()
        self.app.config['Messages']['select_decoder'] = new_text
        self.app.save_config()

    def close_app(self):
        self.master.quit()

    def close_panel(self):
        self.pack_forget()
        self.app.show_main_interface()

    def add_log(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)  # Scroll to the end

class NDIDecoderControl:
    def __init__(self, master):
        self.master = master
        master.title("NDI Decoder Control")
        master.geometry("1920x1080")
        master.configure(bg='#1c1c1e')

        # Make the window borderless
        master.overrideredirect(True)
        master.attributes('-topmost', True)

        # Configure ttk styles
        style = ttk.Style()
        style.configure('TLabelframe', background='#1c1c1e')
        style.configure('TLabelframe.Label', background='#1c1c1e', foreground='white', font=("Roboto", 16))

        # Initialize components
        self.initialize_components()

        # Start in Admin Panel
        self.open_admin_panel()

    def initialize_components(self):
        # Read configuration
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Ensure Messages section exists
        if 'Messages' not in self.config:
            self.config['Messages'] = {'welcome': 'Welcome to NDI Decoder Control!'}
            self.save_config()

        # Decoder settings
        self.decoders = []
        for section in self.config.sections():
            if section.startswith('NDIDecoder'):
                decoder = {
                    'ip': self.config[section].get('ip', ''),
                    'username': self.config[section].get('username', ''),
                    'password': self.config[section].get('password', ''),
                    'name': self.config[section].get('name', f"Decoder {len(self.decoders) + 1}")
                }
                self.decoders.append(decoder)

        # Remember last selected decoder
        self.current_decoder_index = int(self.config.get('Settings', 'last_decoder', fallback='0'))
        self.set_decoder(self.current_decoder_index)

        # NDI Sources
        self.sources = [value for key, value in self.config['NDI_Sources'].items() if key.startswith('source')]
        self.user_friendly_names = [value for key, value in self.config['User_Friendly_Names'].items() if key.startswith('source')]
        self.active_source = self.config['NDI_Sources'].get('active_source', self.sources[0])
        self.active_source_name = self.user_friendly_names[self.sources.index(self.active_source)]

        # Session for maintaining login
        self.session = requests.Session()

        # Main interface frame
        self.main_frame = tk.Frame(self.master, bg='#1c1c1e')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Decoder selection frame (left side)
        self.decoder_selection_frame = tk.Frame(self.main_frame, bg='#2a2a2a', width=220)
        
        # Content frame (right side)
        self.content_frame = tk.Frame(self.main_frame, bg='#1c1c1e')
        
        # Pack the decoder selection frame if there's more than one decoder
        if len(self.decoders) > 1:
            self.decoder_selection_frame.pack(side=tk.LEFT, fill=tk.Y)
            self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        else:
            self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Load and prepare the background image
        self.load_background_image()

        # Create a canvas for the background image and content
        self.canvas = tk.Canvas(self.content_frame, bg='#1c1c1e', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Add the background image to the canvas if it was loaded successfully
        if self.background_image:
            self.canvas.create_image(self.master.winfo_screenwidth(), 0, anchor=tk.NE, image=self.background_image)

        # Welcome message label (left-justified and 10% larger)
        self.welcome_message = self.config['Messages'].get('welcome', 'Welcome to NDI Decoder Control!')
        self.welcome_label = self.canvas.create_text(20, 20, text=self.welcome_message, fill='white', font=("Roboto", 31), anchor='nw')

        # Frame for buttons
        self.button_frame = tk.Frame(self.canvas, bg='#1c1c1e')
        self.button_frame_window = self.canvas.create_window(20, 70, anchor='nw', window=self.button_frame)

        # Bind the Configure event to update button frame size
        self.content_frame.bind('<Configure>', self.update_button_frame_size)

        # Active source label (at the bottom, half the original size)
        self.active_source_label = self.canvas.create_text(
            20, self.master.winfo_screenheight() - 20,
            text="", fill='#808080', font=("Roboto", 12), anchor='sw'  # Font size changed to 12 (half of 24)
        )
        self.canvas.tag_bind(self.active_source_label, '<Button-1>', self.on_active_source_tap)

        # Admin panel
        self.admin_panel = AdminPanel(self.master, self)

        # Create decoder selection buttons
        self.create_decoder_selection()

        # Login first
        if self.login():
            self.create_buttons()
            self.update_buttons()

    def load_background_image(self):
        try:
            # Load the image from the same directory as the script
            image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ERDCLogo.png")
            image = Image.open(image_path)
            
            # Calculate the new size (assuming the window is 1920x1080)
            window_width = 1920
            window_height = 1080
            image_width = int(window_width * 1.5)  # Make the image 1.5 times wider than the window
            image_height = int(image_width / image.width * image.height)
            
            # Resize the image
            image = image.resize((image_width, image_height), Image.LANCZOS)
            
            # Create a new image with an alpha channel
            image_with_opacity = Image.new("RGBA", image.size, (0, 0, 0, 0))
            
            # Paste the original image onto the new image, using the original as a mask
            image_with_opacity.paste(image, (0, 0), image)
            
            # Apply 15% opacity
            data = image_with_opacity.getdata()
            new_data = [(d[0], d[1], d[2], int(d[3] * 0.15)) for d in data]
            image_with_opacity.putdata(new_data)
            
            # Convert to PhotoImage
            self.background_image = ImageTk.PhotoImage(image_with_opacity)
        except FileNotFoundError:
            print(f"Warning: Background image '{image_path}' not found. Using a solid color background instead.")
            # Create a solid color image as a fallback
            self.background_image = None
        except Exception as e:
            print(f"Error loading background image: {e}")
            self.background_image = None

    def create_decoder_selection(self):
        for widget in self.decoder_selection_frame.winfo_children():
            widget.destroy()

        if len(self.decoders) > 1:
            select_decoder_text = self.config['Messages'].get('select_decoder', 'Select Decoder')
            tk.Label(self.decoder_selection_frame, text=select_decoder_text, bg='#2a2a2a', fg='white', font=("Roboto", 16)).pack(pady=(10, 2), fill=tk.X)

            num_decoders = len(self.decoders)
            button_height = (self.master.winfo_height() - 50) // num_decoders  # 50 pixels for the "Select Decoder" label

            for i, decoder in enumerate(self.decoders):
                btn = tk.Button(self.decoder_selection_frame, 
                                text=decoder.get('name', f"Decoder {i+1}"),  # Use custom name if available
                                command=lambda x=i: self.select_decoder(x),
                                bg='#333333' if i != self.current_decoder_index else '#3b3b3d',
                                fg='white', 
                                relief='flat',
                                activebackground='#555555',
                                activeforeground='white',
                                font=("Roboto", 14),
                                bd=0, 
                                highlightthickness=0)
                btn.pack(fill=tk.BOTH, expand=True)

    def select_decoder(self, index):
        self.current_decoder_index = index
        self.set_decoder(index)
        self.config['Settings']['last_decoder'] = str(index)
        self.save_config()
        self.create_decoder_selection()  # Refresh decoder selection buttons
        self.login()  # Re-login with new decoder
        self.create_buttons()  # Recreate source buttons
        self.update_buttons()
        self.update_active_source_label()  # Update the active source label

    def set_decoder(self, index):
        if self.decoders and 0 <= index < len(self.decoders):
            self.current_decoder_index = index
            self.decoder_ip = self.decoders[index]['ip']
            self.username = self.decoders[index]['username']
            self.password = self.decoders[index]['password']
        else:
            self.current_decoder_index = -1
            self.decoder_ip = ''
            self.username = ''
            self.password = ''

    def login(self):
        if not self.decoder_ip:
            self.admin_panel.add_log("No decoder IP set. Please add a decoder in the admin panel.")
            return False
        
        url = f"http://{self.decoder_ip}/mwapi"
        md5_password = hashlib.md5(self.password.encode()).hexdigest()
        params = {
            "method": "login",
            "id": self.username,
            "pass": md5_password
        }
        try:
            response = self.session.get(url, params=params)
            self.admin_panel.add_log(f"Request URL: {response.url}")
            self.admin_panel.add_log(f"Response Status Code: {response.status_code}")
            self.admin_panel.add_log(f"Response Content: {response.text}")
            if response.status_code == 200 and response.json().get("status") == 0:
                sid = response.cookies.get('sid')
                if sid:
                    self.session.cookies.set('sid', sid)
                    self.admin_panel.add_log("Successfully logged in")
                    return True
                else:
                    self.admin_panel.add_log("Login failed: Session ID not found in cookies")
                    return False
            else:
                self.admin_panel.add_log(f"Login failed. Status code: {response.status_code}")
                self.admin_panel.add_log(f"Response content: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            self.admin_panel.add_log(f"Login error occurred: {e}")
            return False

    def create_buttons(self):
        self.buttons = []
        font_size = 20
        background_color = '#1c1c1e'  # Dark gray (modern Tesla-like background)

        num_sources = len(self.sources)
        num_cols = math.ceil(math.sqrt(num_sources))
        num_rows = math.ceil(num_sources / num_cols)

        # Set background color of button_frame
        self.button_frame.configure(bg=background_color)

        # Clear existing widgets in button_frame
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # Add "Select Source" label at the top of button_frame
        select_source_text = self.config['Messages'].get('select_source', 'Select Source')
        select_source_label = tk.Label(self.button_frame, text=select_source_text, bg='#1c1c1e', fg='white', font=("Roboto", 24), anchor='w')
        select_source_label.pack(pady=(0, 2), fill=tk.X)

        # Add white line below "Select Source" spanning the window width
        white_line = tk.Frame(self.button_frame, bg='white', height=1)
        white_line.pack(fill=tk.X, pady=(0, 10))

        # Create a frame for the source buttons
        source_buttons_frame = tk.Frame(self.button_frame, bg=background_color)
        source_buttons_frame.pack(expand=True, fill='both')

        for i in range(num_rows):
            source_buttons_frame.grid_rowconfigure(i, weight=1)
        for j in range(num_cols):
            source_buttons_frame.grid_columnconfigure(j, weight=1)

        for i in range(num_rows):
            row_buttons = []
            for j in range(num_cols):
                index = i * num_cols + j
                if index < num_sources:
                    btn = tk.Button(source_buttons_frame, text=self.user_friendly_names[index], 
                                    command=lambda x=self.sources[index]: self.change_source(x),
                                    bg='#333333' if self.sources[index] != self.active_source else '#3b3b3d',
                                    fg='white', relief='flat',
                                    activebackground='#555555',
                                    activeforeground='white',
                                    font=("Roboto", font_size))
                    btn.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
                    row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Update the button_frame size
        self.button_frame.update_idletasks()
        self.canvas.itemconfig(self.button_frame_window, width=self.content_frame.winfo_width() - 40, height=self.content_frame.winfo_height() - 150)

    def update_buttons(self):
        for row in self.buttons:
            for btn in row:
                source = btn.cget('text')
                if source == self.active_source_name:
                    btn.config(bg='#3b3b3d')  # Slightly lighter background for active button
                else:
                    btn.config(bg='#333333')  # Reset other buttons

    def change_source(self, source):
        url = f"http://{self.decoder_ip}/mwapi"
        params = {
            "method": "set-channel",
            "ndi-name": "true",
            "name": source
        }
        try:
            response = self.session.get(url, params=params)
            self.admin_panel.add_log(f"Request URL: {response.url}")
            self.admin_panel.add_log(f"Response Status Code: {response.status_code}")
            self.admin_panel.add_log(f"Response Content: {response.text}")
            if response.status_code == 200 and response.json().get("status") == 0:
                self.admin_panel.add_log(f"Successfully changed source to: {source}")
                self.active_source = source
                self.active_source_name = self.user_friendly_names[self.sources.index(source)]
                self.config['NDI_Sources']['active_source'] = source
                with open('config.ini', 'w') as configfile:
                    self.config.write(configfile)
                self.update_active_source_label()
                self.update_buttons()
            else:
                self.admin_panel.add_log(f"Failed to change source. Status code: {response.status_code}")
                self.admin_panel.add_log(f"Response content: {response.text}")
        except requests.exceptions.RequestException as e:
            self.admin_panel.add_log(f"Error occurred: {e}")

    def show_main_interface(self):
        self.admin_panel.pack_forget()
        self.update_from_admin_panel()
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_decoder_selection()  # Recreate decoder selection buttons
        # Reset the admin tap counter
        self.admin_tap_count = 0
        self.last_tap_time = 0

    def update_from_admin_panel(self):
        # Re-read the configuration
        self.config.read('config.ini')
        
        # Update sources and user-friendly names
        self.sources = [value for key, value in self.config['NDI_Sources'].items() if key.startswith('source')]
        self.user_friendly_names = [value for key, value in self.config['User_Friendly_Names'].items() if key.startswith('source')]
        self.active_source = self.config['NDI_Sources'].get('active_source', self.sources[0])
        self.active_source_name = self.user_friendly_names[self.sources.index(self.active_source)]

        # Update decoders
        self.decoders = []
        for section in self.config.sections():
            if section.startswith('NDIDecoder'):
                decoder = {
                    'ip': self.config[section].get('ip', ''),
                    'username': self.config[section].get('username', ''),
                    'password': self.config[section].get('password', ''),
                    'name': self.config[section].get('name', f"Decoder {len(self.decoders) + 1}")
                }
                self.decoders.append(decoder)

        # Update welcome message
        self.welcome_message = self.config['Messages'].get('welcome', 'Welcome to NDI Decoder Control!')
        self.canvas.itemconfig(self.welcome_label, text=self.welcome_message)

        # Update active source label
        self.update_active_source_label()

        # Update buttons
        self.create_buttons()
        self.update_buttons()

        # Refresh decoder selection buttons
        self.create_decoder_selection()

    def update_decoders(self):
        # Update the config file with the new decoder information
        for i, decoder in enumerate(self.decoders, 1):
            section = f'NDIDecoder{i}'
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config[section]['ip'] = decoder['ip']
            self.config[section]['username'] = decoder['username']
            self.config[section]['password'] = decoder['password']
            self.config[section]['name'] = decoder['name']
        
        # Remove any excess decoder sections
        sections_to_remove = []
        for section in self.config.sections():
            if section.startswith('NDIDecoder'):
                try:
                    decoder_number = int(section[10:])
                    if decoder_number > len(self.decoders):
                        sections_to_remove.append(section)
                except ValueError:
                    # If we can't parse the number, it's not a valid decoder section
                    sections_to_remove.append(section)
        
        for section in sections_to_remove:
            self.config.remove_section(section)
        
        self.save_config()
        if self.decoders:
            self.current_decoder_index = min(self.current_decoder_index, len(self.decoders) - 1)
        else:
            self.current_decoder_index = -1  # No decoders available
        self.config['Settings']['last_decoder'] = str(self.current_decoder_index)
        self.save_config()
        self.set_decoder(self.current_decoder_index)
        self.create_decoder_selection()  # Refresh decoder selection buttons

    def save_config(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

    def on_active_source_tap(self, event):
        current_time = time.time()
        if current_time - getattr(self, 'last_tap_time', 0) > 4:  # Reset if more than 4 seconds between taps
            self.admin_tap_count = 0
        self.last_tap_time = current_time

        self.admin_tap_count = getattr(self, 'admin_tap_count', 0) + 1
        print(f"Admin tap count: {self.admin_tap_count}")  # Debug print
        if self.admin_tap_count >= 6:
            print("Opening admin panel")  # Debug print
            self.open_admin_panel()
            self.admin_tap_count = 0

    def open_admin_panel(self):
        self.main_frame.pack_forget()
        self.admin_panel.pack(fill=tk.BOTH, expand=True)

    def update_active_source_label(self):
        decoder_name = self.decoders[self.current_decoder_index].get('name', f"Decoder {self.current_decoder_index + 1}")
        self.canvas.itemconfig(self.active_source_label, text=f"Active Source: {self.active_source_name} on {decoder_name}")

    def update_button_frame_size(self, event=None):
        self.canvas.itemconfig(self.button_frame_window, width=self.content_frame.winfo_width() - 40, height=self.content_frame.winfo_height() - 150)
        self.create_buttons()  # Recreate buttons to fit the new size

# Update the config.ini file to include a Settings section
def update_config_file():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    if 'Settings' not in config:
        config['Settings'] = {'last_decoder': '0'}
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

# Call this function before creating the NDIDecoderControl instance
update_config_file()

if __name__ == "__main__":
    root = tk.Tk()
    app = NDIDecoderControl(root)
    root.mainloop()