import os
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Progressbar
from moviepy.editor import VideoFileClip

class VideoSizeReducerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Size Reducer")

        # Set the initial window size
        window_width = 400
        window_height = 380  # Increased height for progress bar and status message
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        # Add a label with the steps
        message_label = Label(root, text="1. Browse to the folder of the videos you want to reduce.", wraplength=350, pady=10)
        message_label.pack()

        step2_label = Label(root, text="2. Input the percentage you want to reduce the videos by.", wraplength=350, pady=10)
        step2_label.pack()

        step3_label = Label(root, text="3. Click Reduce Videos!", wraplength=350, pady=10)
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
        self.reduce_button = Button(control_frame, text="Reduce Videos", command=self.reduce_videos)
        self.reduce_button.pack()

        # Create a progress text
        self.progress_text = Label(root, text="Progress")
        self.progress_text.pack()

        # Create a progress bar
        self.progress_bar = Progressbar(root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.selected_folder_path = folder_path
            self.selected_folder_name.set("Selected Folder: " + os.path.basename(folder_path))

    def reduce_videos(self):
        if self.selected_folder_path:
            input_folder = self.selected_folder_path
            output_folder = os.path.join(input_folder, "resized_videos")
            percentage = int(self.percentage_entry.get())  # Get percentage from input field

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            video_files = [filename for filename in os.listdir(input_folder)
                           if filename.lower().endswith((".mp4", ".avi", ".mov"))]

            total_videos = len(video_files)
            self.progress_bar["maximum"] = total_videos

            for index, filename in enumerate(video_files):
                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, filename)
                self.reduce_video_size(input_path, output_path, percentage)

                # Update progress bar and progress text
                self.progress_bar["value"] = index + 1
                self.progress_text.config(text=f"Progress: {index + 1}/{total_videos}")
                self.root.update_idletasks()

            print("Video reduction completed.")
            self.progress_text.config(text="Video Reduction Completed")
            # Open the directory where the reduced files are saved
            os.startfile(output_folder)  # Opens the file explorer

    @staticmethod
    def reduce_video_size(input_path, output_path, percentage):
        video = VideoFileClip(input_path)
        new_duration = video.duration * (percentage / 100)
        resized_video = video.subclip(0, new_duration)
        resized_video.write_videofile(output_path)

if __name__ == "__main__":
    root = Tk()
    app = VideoSizeReducerApp(root)
    root.mainloop()

