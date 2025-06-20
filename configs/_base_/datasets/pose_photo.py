dataset_info = dict(
    dataset_name='pose_photo',
    paper_info=dict(
        author='Dalton Lowery',
        title='Joint Angles',
    ),
    keypoint_info={
        0: dict(name='L-Foot', id=0, color=[0, 255, 0], type='lower', swap='R-Foot'),
        1: dict(name='R-Foot', id=1, color=[0, 255, 0], type='lower', swap='L-Foot'),
        2: dict(name='L-Ankle', id=2, color=[0, 255, 0], type='lower', swap='R-Ankle'),
        3: dict(name='R-Ankle', id=3, color=[0, 255, 0], type='lower', swap='L-Ankle'),
        4: dict(name='L-Knee', id=4, color=[0, 255, 0], type='lower', swap='R-Knee'),
        5: dict(name='R-Knee', id=5, color=[0, 255, 0], type='lower', swap='L-Knee'),
        6: dict(name='R-Hip', id=6, color=[255, 128, 0], type='upper', swap='L-Hip'),
        7: dict(name='L-Hip', id=7, color=[255, 128, 0], type='upper', swap='R-Hip'),
        8: dict(name='L-Shoulder', id=8, color=[255, 128, 0], type='upper', swap='R-Shoulder'),
        9: dict(name='R-Shoulder', id=9, color=[255, 128, 0], type='upper', swap='L-Shoulder'),
        10: dict(name='R-Elbow', id=10, color=[51, 153, 255], type='upper', swap='L-Elbow'),
        11: dict(name='R-Wrist', id=11, color=[51, 153, 255], type='upper', swap='L-Wrist'),
        12: dict(name='L-Elbow', id=12, color=[51, 153, 255], type='upper', swap='R-Elbow'),
        13: dict(name='L-Wrist', id=13, color=[51, 153, 255], type='upper', swap='R-Wrist'),
    },
    skeleton_info={
        0: dict(link=(12, 13), id=0, color=[51, 153, 255]),
        1: dict(link=(0, 2), id=1, color=[0, 255, 0]),
        2: dict(link=(2, 4), id=2, color=[0, 255, 0]),
        3: dict(link=(3, 5), id=3, color=[0, 255, 0]),
        4: dict(link=(5, 6), id=4, color=[255, 128, 0]),
        5: dict(link=(4, 7), id=5, color=[255, 128, 0]),
        6: dict(link=(7, 6), id=6, color=[255, 128, 0]),
        7: dict(link=(7, 8), id=7, color=[255, 128, 0]),
        8: dict(link=(8, 12), id=8, color=[51, 153, 255]),
        9: dict(link=(8, 9), id=9, color=[255, 128, 0]),
        10: dict(link=(9, 10), id=10, color=[51, 153, 255]),
        11: dict(link=(10, 11), id=11, color=[51, 153, 255]),
        12: dict(link=(3, 1), id=12, color=[0, 255, 0]),
        13: dict(link=(6, 9), id=13, color=[255, 128, 0]),
    },
    joint_weights=[
        [1.] * 14
    ],
    sigmas=[
        [0.025] * 14
    ])
