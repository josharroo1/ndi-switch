import os
import shutil

def setup_image():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Source image path
    source_image = r"C:\Users\Brandon\Documents\ndi-switch\ERDCLogo.png"
    
    # Destination path (same directory as the script)
    destination_image = os.path.join(current_dir, "ERDCLogo.png")
    
    # Copy the image
    shutil.copy2(source_image, destination_image)
    print(f"Image copied to: {destination_image}")

if __name__ == "__main__":
    setup_image()