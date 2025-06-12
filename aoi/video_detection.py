from ultralytics import YOLO
import cv2
import os

os.chdir('C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Pose Estimation/')

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# trained model 
model = YOLO('./runs/detect/train7/weights/best.pt')

# video folder
video_folder = './video/original/' 
video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')] 

# padding 
padding = 5

for video_file in video_files:
    # path for video and video
    video_path = os.path.join(video_folder, video_file)
    save_path = './video/detected/'
    
    # pass 1
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_file}")
        continue

    # dict to store region of intrest cords
    global_rois = {}
    first_detection_frames = {}
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_num = 0
    last_detection_frame = 0
    
    while cap.isOpened():
        # get frame and if it was sucessful
        success, frame = cap.read()
        # error reading, break
        if not success:
            break

        # track ROI with two diff classes
        result = model.track(frame, persist=True, verbose = False)

        # Check if any objects with IDs were detected
        if result[0].boxes.id is not None:
            boxes = result[0].boxes.xyxy.cpu()
            class_ids = result[0].boxes.cls.int().cpu().tolist()
            last_detection_frame = frame_num

            for box, cls_id in zip(boxes, class_ids):
                x1, y1, x2, y2 = box
                class_name = model.names[cls_id]

                # Track first detection of each class
                if class_name not in first_detection_frames:
                    first_detection_frames[class_name] = frame_num

                if class_name not in global_rois:
                    global_rois[class_name] = {'min_x': x1, 'min_y': y1, 'max_x': x2, 'max_y': y2}
                else:
                    # Expand the ROI to include the current detection
                    global_rois[class_name]['min_x'] = min(global_rois[class_name]['min_x'], x1)
                    global_rois[class_name]['min_y'] = min(global_rois[class_name]['min_y'], y1)
                    global_rois[class_name]['max_x'] = max(global_rois[class_name]['max_x'], x2)
                    global_rois[class_name]['max_y'] = max(global_rois[class_name]['max_y'], y2)
        frame_num += 1
    cap.release()
    print("pass 1 done")
        
    # second pass
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    video_writers = {}
    crop_coordinates = {}
    video_base_name = os.path.splitext(video_file)[0]

    for class_name, roi in global_rois.items():
        # Apply padding and ensure coordinates are within frame boundaries
        x1 = max(0, int(roi['min_x'] - padding))
        y1 = max(0, int(roi['min_y'] - padding))
        x2 = min(frame_width, int(roi['max_x'] + padding))
        y2 = min(frame_height, int(roi['max_y'] + padding))
        
        crop_coordinates[class_name] = (x1, y1, x2, y2)
        
        cropped_width = x2 - x1
        cropped_height = y2 - y1
        
        # Create valid output path by joining directory and filename
        output_filename = f"{class_name}_{video_base_name}.mp4"
        roi_output_path = os.path.join(save_path, output_filename)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v') #correct codec for file export
 
            
        video_writers[class_name] = cv2.VideoWriter(roi_output_path, fourcc, fps, (cropped_width, cropped_height))

       
        cap = cv2.VideoCapture(video_path)
    
    frame_num = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
            
        # Only process frames up to the last detection
        if frame_num > last_detection_frame:
            break

        # For each frame, create a cropped version for each ROI
        for class_name, writer in video_writers.items():
            # Only write frames starting 10 frames before first detection of this class
            start_frame = max(0, first_detection_frames[class_name] - 10)
            if frame_num >= start_frame:
                x1, y1, x2, y2 = crop_coordinates[class_name]
                cropped_frame = frame[y1:y2, x1:x2]
                writer.write(cropped_frame)

        frame_num += 1
        
    # release resources
    cap.release()
    for writer in video_writers.values():
        writer.release()
    print(f"Completed: {video_file}")
    
print("Finished processing all videos.")