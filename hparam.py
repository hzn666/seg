class hparams:
    train_or_test = 'train'
    output_dir = 'logs/'
    aug = None
    latest_checkpoint_file = 'checkpoint_latest.pt'
    total_epochs = 100
    epochs_per_checkpoint = 10
    batch_size = 2
    ckpt = None
    init_lr = 0.002
    scheduer_step_size = 20
    scheduer_gamma = 0.8
    debug = False
    mode = '2d'  # '2d or '3d'
    in_class = 1
    out_class = 1

    crop_or_pad_size = 512, 512, 1  # if 2D: 256,256,1
    patch_size = 512, 512, 1  # if 2D: 128,128,1

    # for test
    patch_overlap = 4, 4, 0  # if 2D: 4,4,0

    fold_arch = '*/*.png'

    save_arch = '.png'

    source_train_dir = 'train/PNG'
    label_train_dir = 'train/LABEL'
    source_test_dir = 'test/PNG'
    label_test_dir = 'test/LABEL'

    output_dir_test = 'results/'
