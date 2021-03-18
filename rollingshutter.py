import cv2
import glob
import tkinter
import tkinter.filedialog
import os.path 
from PIL import Image
import shutil



def roll_shutter(path, folder, speed_mult = 1):
    frame_dir  = os.path.join(path, folder)
    frame_file = 'png'
    
    files         = glob.glob(os.path.join(frame_dir, f'*.{frame_file}'))
    image         = Image.open(files[0])
    width, height = image.size
    
    current_row = 0
    n_files     = len(files)
    speed       = speed_mult * height / n_files
    
    # Making our blank output frame
    output_image = Image.new('RGB', (width, height))

    # Chech if there are images
    if len(files) == 0:
        print(f'Directory has no {frame_file} files.')
        return False
    
    # Go through the frames one at a time
    for file in files:
        a = int(current_row)
        b = int(current_row + speed)
        new_line = Image.open(file).crop((0, a, width, b))
        output_image.paste(new_line, (0, a))
        current_row += speed

    # Save result
    output_image.save(os.path.join(path, 'result.png'))

    return True



def make_frames(frames_folder, file):
    if not os.path.exists(frames_folder):
        os.makedirs(frames_folder)
    
    video = cv2.VideoCapture(os.path.join(frames_folder, file))
    success, image = video.read()
    frame = 0
    
    while success:
      cv2.imwrite(frames_folder + '/' + str(frame) + '.png', image)
      success, image = video.read()
      frame += 1

    return True



if __name__ == '__main__':
    speed = 3
    
    root = tkinter.Tk()
    root.withdraw()

    path          = os.getcwd()
    video_file    = tkinter.filedialog.askopenfilename(title = 'Select video file', initialdir = path)
    frames_folder = os.path.join(path, 'frames')

    if make_frames(frames_folder, video_file):
        roll_shutter(path, 'frames', speed)
        
        if os.path.exists(frames_folder):
            print(frames_folder)
            shutil.rmtree(frames_folder)
            
    print('Done.')
