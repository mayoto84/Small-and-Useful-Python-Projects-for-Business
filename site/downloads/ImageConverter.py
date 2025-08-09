import os
from tkinter import *
from tkinter import filedialog
from PIL import Image

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Format Converter")

        # Set the initial window size
        window_width = 400
        window_height = 250
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        # Add a label with a message
        message_label = Label(root, text="Browse your files for the image you want to convert.")
        message_label.pack(pady=10)

        # Initialize variables to store file information
        self.selected_file_path = None
        self.selected_file_name = StringVar()

        # Create a label to display the selected file name
        self.file_label = Label(root, textvariable=self.selected_file_name)
        self.file_label.pack(pady=5)

        # Create a Frame to contain the buttons and dropdown menu
        control_frame = Frame(root)
        control_frame.pack()

        # Create a button to browse for the image file
        browse_button = Button(control_frame, text="Browse Image File", command=self.browse_file)
        browse_button.pack(side="left", padx=(10, 5))  # Adds padding only to the right side

        # Create a Convert button
        convert_button = Button(control_frame, text="Convert!", command=self.convert_image)
        convert_button.pack(side="left", padx=(5, 10))  # Adds padding only to the left side

        # Create a label for the dropdown menu
        format_label = Label(root, text="Select target format:")
        format_label.pack(pady=5)

        # Create a StringVar to store the selected format
        self.selected_format = StringVar(root)
        self.selected_format.set("JPG")  # Default format

        # Create a dropdown menu for selecting the format
        format_menu = OptionMenu(root, self.selected_format, "JPG", "PNG", "GIF", "BMP", "ICO", "TIFF")
        format_menu.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp *.ico *.tiff")])
        if file_path:
            self.selected_file_path = file_path
            self.selected_file_name.set("Selected File: " + os.path.basename(file_path))

    def convert_image(self):
        if self.selected_file_path:
            file_path = os.path.dirname(self.selected_file_path)
            file_name, file_extension = os.path.splitext(os.path.basename(self.selected_file_path))

            input_image_path = self.selected_file_path
            output_extension = self.selected_format.get().lower()  # Get selected format from dropdown
            output_image_path = os.path.join(file_path, f"{file_name}_converted.{output_extension}")

            try:
                img = Image.open(input_image_path)
                img.save(output_image_path)
                print(f"Conversion successful. Image saved as '{output_image_path}'.")

                # Open the directory where the converted file is saved
                output_directory = os.path.dirname(output_image_path)
                os.startfile(output_directory)  # Opens the file explorer

            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    root = Tk()
    app = ImageConverterApp(root)
    root.mainloop()
