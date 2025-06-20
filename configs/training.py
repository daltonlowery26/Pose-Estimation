# inheret runtime for mmpose
_base_ = [
    'mmpose::rtmpose/rtmpose-s_8xb256-420e_coco-256x192.py', 
    './_base_/datasets/pose_photos.py' 
]

data_root = 'C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Pose Estimation/datasets/pose_photo/'

# 14 key points to predict
model = dict(
    head=dict(
        out_channels=14),
    )

# data loader
train_dataloader = dict(
    batch_size=4,
    dataset=dict(
        data_root=data_root,
        ann_file='annotations/train.json',
        data_prefix=dict(img='train/'),
    ))

val_dataloader = dict(
    batch_size=4,
    dataset=dict(
        data_root=data_root,
        ann_file='annotations/val.json',
        data_prefix=dict(img='valid/'),
    ))

test_dataloader = dict(
    batch_size=4,
    dataset=dict(
        data_root=data_root,
        ann_file='annotations/test.json',
        data_prefix=dict(img='test/'),
    ))

val_evaluator = dict(ann_file=data_root + 'annotations/val.json')
test_evaluator = val_evaluator