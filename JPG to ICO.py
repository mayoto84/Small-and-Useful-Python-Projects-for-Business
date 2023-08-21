import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image

class ImageToIconConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convert JPG to ICO")

        # Set the initial window size
        window_width = 400
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        # Add a label with a message
        message_label = tk.Label(root, text="Browse your files for the JPG image you want to convert to ICO.")
        message_label.pack(pady=20)

        # Initialize variables to store file information
        self.selected_file_path = None
        self.selected_file_name = tk.StringVar()

        # Create a label to display the selected file name
        self.file_label = tk.Label(root, textvariable=self.selected_file_name)
        self.file_label.pack(pady=10)

        # Create a Frame to contain the buttons
        button_frame = tk.Frame(root)
        button_frame.pack()

        # Create a button to browse for the image file
        browse_button = tk.Button(button_frame, text="Browse Image File", command=self.browse_file)
        browse_button.pack(side="left", padx=(10, 5))  # Adds padding only to the right side

        # Create a Convert button
        self.convert_button = tk.Button(button_frame, text="Convert to ICO", command=self.convert_to_ico)
        self.convert_button.pack(side="left", padx=(5, 10))  # Adds padding only to the left side

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg")])
        if file_path:
            self.selected_file_path = file_path
            self.selected_file_name.set("Selected File: " + os.path.basename(file_path))
            self.convert_button.config(text="Convert to ICO!")  # Reset button text after new selection

    def convert_to_ico(self):
        if self.selected_file_path:
            input_image_path = self.selected_file_path
            output_icon_path = os.path.splitext(input_image_path)[0] + ".ico"
            sizes = [(256, 256), (128, 128), (64, 64)]  # List of sizes for the icon

            try:
                img = Image.open(input_image_path)
                img = img.convert("RGBA")
                img.save(output_icon_path, sizes=sizes)
                print(f"Conversion successful. Icon saved as '{output_icon_path}'.")
            except Exception as e:
                print(f"Error: {e}")

            self.convert_button.config(text="Converted!")  # Update button text after conversion

            # Open the directory where the converted ICO file is saved
            output_directory = os.path.dirname(output_icon_path)
            os.startfile(output_directory)  # Opens the file explorer

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToIconConverterApp(root)
    root.mainloop()
