log_level = 'INFO'
stack_frame = 1
num_heads = 4

agent = dict(
    type='BC',
    batch_size=64,
    policy_cfg=dict(
        type='ContinuousPolicy',
        policy_head_cfg=dict(
            type='DeterministicHead',
            noise_std=1e-5,
        ),
        nn_cfg=dict(
            type='PAConvPointnet2ManiV0',
            stack_frame=stack_frame,
            num_objs='num_objs',
            num_sym_matrix=0,
            matrix_index=-1,
            obj_residual=True,
            pcd_pn_cfg=dict(
                type='PointNet2SSGSeg',
                c='agent_shape + pcd_xyz_rgb_channel', #3,
                use_xyz=True,
                mask_type='*',
                sa_cfg=dict(
                    type='PointNet2SAModule',
                    nsamples=[32, 32, 32, 32],
                    npoints=[None, None, None, None],
                    sa_mlps=[['agent_shape + pcd_xyz_rgb_channel', 32, 32, 64], [64, 64, 64, 128], [128, 128, 128, 256], [256, 256, 256, 256]],
                    pointnet2_paconv=[True, True, True, True, False, False, False, False],
                    cuda=True,
                    # norm_cfg=None,
                    # mlp_spec=['agent_shape + pcd_xyz_rgb_channel', 256, 256],
                    # bias='auto',
                    # inactivated_output=True,
                    # conv_init_cfg=dict(type='xavier_init', gain=1, bias=0),
                ),
                # mlp_cfg=dict(
                #     type='LinearMLP',
                #     norm_cfg=None,
                #     mlp_spec=[256 * stack_frame, 256, 256],
                #     bias='auto',
                #     inactivated_output=True,
                #     linear_init_cfg=dict(type='xavier_init', gain=1, bias=0),
                # ),
                subtract_mean_coords=True,
                # max_mean_mix_aggregation=True
            ),
            state_mlp_cfg=dict(
                type='LinearMLP',
                norm_cfg=None,
                mlp_spec=['agent_shape', 256, 256],
                bias='auto',
                inactivated_output=True,
                linear_init_cfg=dict(type='xavier_init', gain=1, bias=0),
            ),                        
            transformer_cfg=None,
            final_mlp_cfg=dict(
                type='LinearMLP',
                dropout=0.15,
                norm_cfg=None,
                mlp_spec=['256 * (num_objs + 3)', 256, 'action_shape'],
                bias='auto',
                inactivated_output=True,
                linear_init_cfg=dict(type='xavier_init', gain=1, bias=0),
            ),
        ),
        optim_cfg=dict(type='Adam', lr=1e-4, weight_decay=5e-6),
    ),
)

eval_cfg = dict(
    type='Evaluation',
    num=10,
    num_procs=1,
    use_hidden_state=False,
    start_state=None,
    save_traj=True,
    save_video=True,
    use_log=False,
)

train_mfrl_cfg = dict(
    on_policy=False,
)

env_cfg = dict(
    type='gym',
    unwrapped=False,
    stack_frame=stack_frame,
    obs_mode='pointcloud',
    reward_type='dense',
)
