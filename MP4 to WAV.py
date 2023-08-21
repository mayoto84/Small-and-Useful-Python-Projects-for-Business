import moviepy.editor as mp
from pydub import AudioSegment
import os
import tkinter as tk
from tkinter import filedialog
import sys
sys.stdout = open("output.log", "w")
sys.stderr = open("error.log", "w")



class VideoToWavConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Convert MP4 to WAV")

        # Set the initial window size
        window_width = 400
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

        # Add a label with a message
        message_label = tk.Label(root, text="Browse your files for the MP4 you want to convert to WAV.")
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

        # Create a button to browse for the video file
        browse_button = tk.Button(button_frame, text="Browse Video File", command=self.browse_file)
        browse_button.pack(side="left", padx=(10, 5))  # Adds padding only to the right side

        # Create a Convert button
        self.convert_button = tk.Button(button_frame, text="Convert!", command=self.convert_mp4_to_wav)
        self.convert_button.pack(side="left", padx=(5, 10))  # Adds padding only to the left side

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4")])
        if file_path:
            self.selected_file_path = file_path
            self.selected_file_name.set("Selected File: " + os.path.basename(file_path))
            self.convert_button.config(text="Convert!")  # Reset button text after new selection

    def convert_mp4_to_wav(self):
        if self.selected_file_path:
            file_path = os.path.dirname(self.selected_file_path)
            file_name = os.path.basename(self.selected_file_path)

            # Construct the full path to the video file
            video_path = os.path.join(file_path, file_name)

            # Load the video file
            video = mp.VideoFileClip(video_path)

            # Extract the audio from the video
            audio = video.audio

            # Export the audio to a temporary WAV file
            temp_wav_path = os.path.join(file_path, "temp.wav")
            audio.write_audiofile(temp_wav_path)

            # Load the temporary WAV file
            audio_segment = AudioSegment.from_file(temp_wav_path, format="wav")

            # Set the sample rate to 96000 Hz
            audio_segment = audio_segment.set_frame_rate(96000)

            # Construct the full path to the output WAV file
            output_path = os.path.join(file_path, os.path.splitext(file_name)[0] + ".wav")

            # Export the high-quality WAV audio file
            audio_segment.export(output_path, format="wav")

            # Remove the temporary WAV file
            os.remove(temp_wav_path)

            # Print the output file path
            print("WAV file saved at:", output_path)

            # Update button text to "Done!" after successful conversion
            self.convert_button.config(text="Done!")

             # Open the directory where the converted file is saved
            output_directory = os.path.dirname(output_path)
            os.startfile(output_directory)  # Opens the file explorer


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToWavConverterApp(root)
    root.mainloop()


