import os
from tkinter import *
from tkinter import filedialog
from PIL import Image

class ImageSizeReducerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Size Reducer")

        # Set the initial window size
        window_width = 400
        window_height = 300  # Increased height to accommodate spacing
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        # Add a label with the steps
        message_label = Label(root, text="1. Browse to the folder of the images you want to reduce.", wraplength=350, pady=10)
        message_label.pack()

        step2_label = Label(root, text="2. Input the percentage you want to reduce the images by.", wraplength=350, pady=10)
        step2_label.pack()

        step3_label = Label(root, text="3. Click Reduce Images!", wraplength=350, pady=10)
        step3_label.pack()

        # Initialize variables to store folder information
        self.selected_folder_path = None
        self.selected_folder_name = StringVar()

        # Create a label to display the selected folder name
        self.folder_label = Label(root, textvariable=self.selected_folder_name)
        self.folder_label.pack(pady=5)

        # Create a Frame to contain the buttons and input field
        control_frame = Frame(root)
        control_frame.pack()

        # Create a button to browse for the input folder
        browse_button = Button(control_frame, text="Browse Input Folder", command=self.browse_folder)
        browse_button.pack(side="left", padx=(10, 5))  # Adds padding only to the right side

        # Create an input field for specifying the percentage
        self.percentage_entry = Entry(control_frame)
        self.percentage_entry.insert(0, "50")  # Default value
        self.percentage_entry.pack(side="left", padx=(5, 10))  # Adds padding only to the left side

        # Create a Reduce button
        reduce_button = Button(control_frame, text="Reduce Images", command=self.reduce_images)
        reduce_button.pack()

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_folder_path = folder_path
            self.selected_folder_name.set("Selected Folder: " + os.path.basename(folder_path))

    def reduce_images(self):
        if self.selected_folder_path:
            input_folder = self.selected_folder_path
            output_folder = os.path.join(input_folder, "resized")
            percentage = int(self.percentage_entry.get())  # Get percentage from input field

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            for filename in os.listdir(input_folder):
                if filename.lower().endswith((".jpg", ".png")):
                    input_path = os.path.join(input_folder, filename)
                    output_path = os.path.join(output_folder, filename)
                    self.reduce_image_size(input_path, output_path, percentage)

            print("Image reduction completed.")
            # Open the directory where the reduced files are saved
            os.startfile(output_folder)  # Opens the file explorer

    @staticmethod
    def reduce_image_size(input_path, output_path, percentage):
        with Image.open(input_path) as img:
            width, height = img.size
            new_width = int(width * percentage / 100)
            new_height = int(height * percentage / 100)
            img = img.resize((new_width, new_height))
            img.save(output_path)

if __name__ == "__main__":
    root = Tk()
    app = ImageSizeReducerApp(root)
    root.mainloop()