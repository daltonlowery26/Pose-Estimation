from roboflow import Roboflow
import os

# api key
robo_api = os.getenv("ROBO_API")

# load data
rf = Roboflow(api_key=robo_api)
project = rf.workspace("fracture-pcnbk").project("player-detection-wr4ch")
version = project.version(6)
dataset = version.download("yolov8")