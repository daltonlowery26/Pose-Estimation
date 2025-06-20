# file Directory
_base_ = [
    './_base_/default_runtime.py',
    './_base_/datasets/pose_photo.py'
]

# "global" vars
channel_cfg = dict(
    num_output_channels=14,
    dataset_joints=15,
    dataset_channel=[0, 1, 2, 3, 4, 5, 6, 7 , 8, 9, 10, 11, 12, 13],
    inference_channel=[0, 1, 2, 3, 4, 5 , 6 , 7, 8 ,9, 10, 11, 12, 13, 14]
)

# data info
data_cfg = dict(
    image_size=[640, 640],    
    heatmap_size=[160, 160],    
    num_output_channels=channel_cfg['num_output_channels'],
    num_joints=channel_cfg['dataset_joints'],
    dataset_channel=channel_cfg['dataset_channel'],
    inference_channel=channel_cfg['inference_channel'],
)


# model loop
model = dict(
    pretrained='https://download.openmmlab.com/mmpose/top_down/hrnet/hrnet_w48_coco_256x192-b9e0b3ab_20200708.pth',
    backbone=dict(
        type='HRNet',
        in_channels=3,
        extra=dict(
            stage2=dict(num_channels=(48, 96)),
            stage3=dict(num_channels=(48, 96, 192)),
            stage4=dict(num_channels=(48, 96, 192, 384)))),
    head=dict(
        type='TopdownHeatmapSimpleHead',
        in_channels=48,
        out_channels=channel_cfg['num_output_channels'],
        loss_keypoint=dict(type='JointsMSELoss', use_target_weight=True)),
    train_cfg=dict(),
    test_cfg=dict(
        flip_test=True,
        post_process='default',
        shift_heatmap=True,
        modulate_kernel=11)
)


# data pipelines
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='TopDownGetBboxCenterScale', padding=1.25),
    dict(type='TopDownRandomShiftBboxCenter', shift_factor=0.16, prob=0.3),
    dict(type='TopDownRandomFlip', flip_prob=0.5),
    dict(type='TopDownHalfBodyTransform', num_joints_half_body=2, prob_half_body=0.3),
    dict(type='TopDownGetRandomScaleRotation', rot_factor=40, scale_factor=0.5),
    dict(type='TopDownAffine'),
    dict(type='ToTensor'),
    dict(type='NormalizeTensor', mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    dict(type='TopDownGenerateTarget', sigma=3),
    dict(type='Collect', keys=['img', 'target', 'target_weight'], meta_keys=['image_file', 'center', 'scale', 'rotation']),
]

val_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='TopDownGetBboxCenterScale', padding=1.25),
    dict(type='TopDownAffine'),
    dict(type='ToTensor'),
    dict(type='NormalizeTensor', mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    dict(type='Collect', keys=['img'], meta_keys=['image_file', 'center', 'scale', 'rotation']),
]

test_pipeline = val_pipeline

# wrpper and training configs
optim_wrapper = dict(
    optimizer=dict(type='AdamW', lr=5e-4)
)

train_cfg = dict(
    by_epoch=True,
    max_epochs=210,
    val_interval=10
)

param_scheduler = [
    dict(
        type='MultiStepLR',
        begin=0,
        end=210,
        by_epoch=True,
        milestones=[170, 200],
        gamma=0.1
    )
]

# root and name
data_root = 'C:/Users/dalto/OneDrive/Pictures/Documents/Projects/Coding Projects/Pose Estimation/datasets/pose_photo/'
dataset_type = 'pose_photo'

# dataloaders
train_dataset = dict(
    type=dataset_type,
    data_root=data_root,
    ann_file='annotations/train.json',
    data_prefix=dict(img='train/'),
    pipeline=train_pipeline,
    dataset_info={{_base_.dataset_info}}
)

train_dataloader = dict(
    batch_size=8,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=train_dataset
)

val_dataloader = dict(
    batch_size=8,
    num_workers=4,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type=dataset_type,
        data_root=data_root,
        ann_file='annotations/val.json',
        data_prefix=dict(img='valid/'),
        pipeline=val_pipeline,
        dataset_info={{_base_.dataset_info}}
    )
)

test_dataloader = val_dataloader

# validation 
val_cfg = dict()

# metrics and config
val_evaluator = dict(
    type='PoseMetric',
    ann_file=data_root + 'annotations/val.json',
    metric=['PCKAccuracy', 'AUC', 'EPE'],
    metric_mode='topDown'
)

test_cfg = dict()

# same config for eval
test_evaluator = val_evaluator