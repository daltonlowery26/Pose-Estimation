import ffmpeg
import os
# conversion extension
ffmpeg_exe = "C:/ffmpeg/bin/ffmpeg.exe"

def convert_to_h264(input_file, output_file):
    try:
        (
            ffmpeg
            .input(input_file)
            .filter('scale', w=-2, h='trunc(ih/2)*2')
            .output(output_file, vcodec='libx264', acodec='aac')
            .run(cmd=ffmpeg_exe, overwrite_output=True, capture_stderr=True)
        )
        print(f"Successfully converted {input_file} to {output_file}")
    except ffmpeg.Error as e:
        print("Error during conversion:")
        print(e.stderr.decode())

if __name__ == "__main__":
    detected_folder = "C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Pose Estimation/video/detected/"

    for filename in os.listdir(detected_folder):
        if "h264" in filename:
            continue
        input_video = os.path.join(detected_folder, filename)
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_h264{ext}"
        output_video = os.path.join(detected_folder, output_filename)
        convert_to_h264(input_video, output_video)
    
    # remove files without h264        
    for filename in os.listdir(detected_folder):
        if "h264" not in filename:
            file_path = os.path.join(detected_folder, filename)
            try:
                os.remove(file_path)
                print(f"Deleted {filename}")
            except OSError as e:
                print(f"Error deleting {filename}: {e}")

    # split the video into jpeg taking 5 frames every second from video, save this in the frames folder
    frames_folder_b = "C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Pose Estimation/video/frames/batter/"
    frames_folder_p = "C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Pose Estimation/video/frames/pitcher/"
    os.makedirs(frames_folder_b, exist_ok=True)
    os.makedirs(frames_folder_p, exist_ok=True)
    
    for filename in os.listdir(detected_folder):
        if "h264" in filename:
            input_video = os.path.join(detected_folder, filename)
            name, ext = os.path.splitext(filename)
            
            # to seperate folders
            if "batter" in filename:
                output_pattern = os.path.join(frames_folder_b, f"{name}_frame_%03d.jpg")
            elif "pitcher" in filename:
                output_pattern = os.path.join(frames_folder_p, f"{name}_frame_%03d.jpg")
            else:
                continue 
            
            # take 5 frames a second
            (
                ffmpeg
                .input(input_video)
                .filter('fps', 5)
                .output(output_pattern)
                .run(cmd=ffmpeg_exe, overwrite_output=True, capture_stderr=True)
            )
            print(f"Successfully extracted frames from {filename}")
    

    
