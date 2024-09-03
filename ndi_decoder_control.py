import configparser
import tkinter as tk
from tkinter import messagebox
import requests
import hashlib
import urllib.parse
import math

class AdminPanel(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg='#2e2e2e')
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self, text="Close Application", command=self.close_app, bg='#333333', fg='white').pack(pady=10)
        
        tk.Label(self, text="Edit Sources (comma-separated):", bg='#2e2e2e', fg='white').pack(pady=5)
        self.sources_entry = tk.Entry(self, width=50, bg='#333333', fg='white')
        self.sources_entry.pack(pady=5)
        self.sources_entry.insert(0, ','.join(self.app.sources))
        tk.Button(self, text="Update Sources", command=self.update_sources, bg='#333333', fg='white').pack(pady=5)

        tk.Label(self, text="Edit Button Names (comma-separated):", bg='#2e2e2e', fg='white').pack(pady=5)
        self.names_entry = tk.Entry(self, width=50, bg='#333333', fg='white')
        self.names_entry.pack(pady=5)
        self.names_entry.insert(0, ','.join(self.app.user_friendly_names))
        tk.Button(self, text="Update Button Names", command=self.update_button_names, bg='#333333', fg='white').pack(pady=5)

        tk.Button(self, text="Close Admin Panel", command=self.close_panel, bg='#333333', fg='white').pack(pady=10)

    def close_app(self):
        self.master.quit()

    def update_sources(self):
        new_sources = [s.strip() for s in self.sources_entry.get().split(',')]
        self.app.update_sources(new_sources)

    def update_button_names(self):
        new_names = [n.strip() for n in self.names_entry.get().split(',')]
        self.app.update_button_names(new_names)

    def close_panel(self):
        self.pack_forget()
        self.app.show_main_interface()

class NDIDecoderControl:
    def __init__(self, master):
        self.master = master
        master.title("NDI Decoder Control")
        master.geometry("1920x1080")
        master.configure(bg='#1e1e1e')  # Dark mode background

        # Make the window borderless
        master.overrideredirect(True)
        master.attributes('-topmost', True)

        # Initialize components
        self.initialize_components()

        # Bind click event to the entire window
        master.bind('<Button-1>', self.on_window_click)

    def initialize_components(self):
        # Read configuration
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        # Decoder settings
        self.decoder_ip = self.config['Decoder']['ip']
        self.username = self.config['Decoder']['username']
        self.password = self.config['Decoder']['password']

        # NDI Sources
        self.sources = [value for key, value in self.config['NDI_Sources'].items() if key.startswith('source')]
        self.user_friendly_names = [value for key, value in self.config['User_Friendly_Names'].items() if key.startswith('source')]
        self.active_source = self.config['NDI_Sources'].get('active_source', self.sources[0])
        self.active_source_name = self.user_friendly_names[self.sources.index(self.active_source)]

        # Session for maintaining login
        self.session = requests.Session()

        # Main interface frame
        self.main_frame = tk.Frame(self.master, bg='#1e1e1e')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Active source label
        self.active_source_label = tk.Label(self.main_frame, text=f"Active Source: {self.active_source_name}", bg='#1e1e1e', fg='white', font=("Helvetica", 24))
        self.active_source_label.pack(pady=20)

        # Frame for buttons
        self.button_frame = tk.Frame(self.main_frame, bg='#1e1e1e')
        self.button_frame.pack(expand=True, fill='both')

        # Admin panel
        self.admin_panel = AdminPanel(self.master, self)

        # Login first
        if self.login():
            self.create_buttons()
            self.update_buttons()
        else:
            tk.Label(self.main_frame, text="Login failed. Please check your credentials.", bg='#1e1e1e', fg='white').pack()

        # Initialize click counter for admin panel functionality
        self.admin_click_count = 0
        self.last_click_time = 0

    def login(self):
        url = f"http://{self.decoder_ip}/mwapi"
        md5_password = hashlib.md5(self.password.encode()).hexdigest()
        params = {
            "method": "login",
            "id": self.username,
            "pass": md5_password
        }
        try:
            response = self.session.get(url, params=params)
            print(f"Request URL: {response.url}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
            if response.status_code == 200 and response.json().get("status") == 0:
                sid = response.cookies.get('sid')
                if sid:
                    self.session.cookies.set('sid', sid)
                    print("Successfully logged in")
                    return True
                else:
                    print("Login failed: Session ID not found in cookies")
                    return False
            else:
                print(f"Login failed. Status code: {response.status_code}")
                print(f"Response content: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Login error occurred: {e}")
            return False

    def create_buttons(self):
        self.buttons = []
        button_width = 30
        button_height = 10
        font_size = 24  # Increase font size

        num_sources = len(self.sources)
        num_cols = math.ceil(math.sqrt(num_sources))
        num_rows = math.ceil(num_sources / num_cols)

        for i in range(num_rows):
            row_buttons = []
            for j in range(num_cols):
                index = i * num_cols + j
                if index < num_sources:
                    btn = tk.Button(self.button_frame, text=self.user_friendly_names[index], 
                                    command=lambda x=self.sources[index]: self.change_source(x),
                                    bg='#333333', fg='white', relief='flat',
                                    width=button_width, height=button_height, font=("Helvetica", font_size),
                                    bd=2)  # Border width for all buttons
                    btn.grid(row=i, column=j, padx=20, pady=20, sticky="nsew")
                    row_buttons.append(btn)
            self.buttons.append(row_buttons)

        for i in range(num_rows):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for j in range(num_cols):
            self.button_frame.grid_columnconfigure(j, weight=1)

    def update_buttons(self):
        for row in self.buttons:
            for btn in row:
                source = btn.cget('text')
                if source == self.active_source_name:
                    btn.config(highlightbackground='white', highlightthickness=4, bd=4)  # Active button border
                else:
                    btn.config(highlightbackground='#333333', highlightthickness=0, bd=2)  # Reset other buttons

    def change_source(self, source):
        url = f"http://{self.decoder_ip}/mwapi"
        params = {
            "method": "set-channel",
            "ndi-name": "true",
            "name": source
        }
        try:
            response = self.session.get(url, params=params)
            print(f"Request URL: {response.url}")
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Content: {response.text}")
            if response.status_code == 200 and response.json().get("status") == 0:
                print(f"Successfully changed source to: {source}")
                self.active_source = source
                self.active_source_name = self.user_friendly_names[self.sources.index(source)]
                self.config['NDI_Sources']['active_source'] = source
                with open('config.ini', 'w') as configfile:
                    self.config.write(configfile)
                self.active_source_label.config(text=f"Active Source: {self.active_source_name}")
                self.update_buttons()
            else:
                print(f"Failed to change source. Status code: {response.status_code}")
                print(f"Response content: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")

    def on_window_click(self, event):
        current_time = self.master.winfo_pointerxy()[0]  # Use x-coordinate as a timestamp
        if current_time - self.last_click_time > 2000:  # Reset if more than 2 seconds between clicks
            self.admin_click_count = 0
        self.last_click_time = current_time

        if 0 <= event.x <= 100 and self.master.winfo_height() - 100 <= event.y <= self.master.winfo_height():
            self.admin_click_count += 1
            if self.admin_click_count >= 6:
                self.open_admin_panel()

    def open_admin_panel(self):
        self.main_frame.pack_forget()
        self.admin_panel.pack(fill=tk.BOTH, expand=True)

    def show_main_interface(self):
        self.admin_panel.pack_forget()
        self.update_from_admin_panel()
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # Reset the admin click counter
        self.admin_click_count = 0
        self.last_click_time = 0

    def update_from_admin_panel(self):
        # Re-read the configuration
        self.config.read('config.ini')
        
        # Update sources and user-friendly names
        self.sources = [value for key, value in self.config['NDI_Sources'].items() if key.startswith('source')]
        self.user_friendly_names = [value for key, value in self.config['User_Friendly_Names'].items() if key.startswith('source')]
        
        # Update active source
        self.active_source = self.config['NDI_Sources'].get('active_source', self.sources[0])
        self.active_source_name = self.user_friendly_names[self.sources.index(self.active_source)]
        
        # Update the active source label
        self.active_source_label.config(text=f"Active Source: {self.active_source_name}")
        
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        # Recreate and update buttons
        self.create_buttons()
        self.update_buttons()

    def update_sources(self, new_sources):
        self.sources = new_sources
        # Ensure user_friendly_names matches the number of sources
        self.user_friendly_names = self.user_friendly_names[:len(new_sources)]
        while len(self.user_friendly_names) < len(new_sources):
            self.user_friendly_names.append(f"Source {len(self.user_friendly_names) + 1}")

        self.config['NDI_Sources'] = {f'source{i+1}': source for i, source in enumerate(new_sources)}
        self.config['User_Friendly_Names'] = {f'source{i+1}': name for i, name in enumerate(self.user_friendly_names)}
        self.save_config()
        self.create_buttons()
        self.update_buttons()

    def update_button_names(self, new_names):
        # Ensure new_names matches the number of sources
        new_names = new_names[:len(self.sources)]
        while len(new_names) < len(self.sources):
            new_names.append(f"Source {len(new_names) + 1}")

        self.user_friendly_names = new_names
        self.config['User_Friendly_Names'] = {f'source{i+1}': name for i, name in enumerate(new_names)}
        self.save_config()
        self.create_buttons()
        self.update_buttons()

    def save_config(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)

if __name__ == "__main__":
    root = tk.Tk()
    app = NDIDecoderControl(root)
    root.mainloop()