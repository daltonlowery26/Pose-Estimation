import roboflow
import os

# api key
robo_api = os.getenv("ROBO_API")

# data and paths
rf = roboflow.Roboflow(api_key=robo_api)
project_h = rf.workspace("fracture-pcnbk")
project_p = rf.workspace("fracture-pcnbk")

hitter_path = "C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Pose Estimation/video/frames/batter/"
pitcher_path = "C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Pose Estimation/video/frames/pitcher/"

# upload data
project_h.upload_dataset(
    dataset_path = hitter_path, 
    project_name= "hitter-pose",
    num_workers=15
)

project_p.upload_dataset(
    dataset_path = pitcher_path, 
    project_name= "pitcher-pose",
    num_workers=15
)

