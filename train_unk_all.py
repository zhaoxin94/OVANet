import os
import os.path as osp
import argparse
import hashlib


def seed_hash(*args):
    """
    Derive an integer hash from all args, for use as a random seed.
    """
    args_str = str(args)
    return int(hashlib.md5(args_str.encode("utf-8")).hexdigest(), 16) % (2**31)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dataset",
        "-d",
        default="officehome",
        help="Dataset",
        choices=['office31', 'officehome', 'visda', 'domainnet'])
    parser.add_argument("--source", "-s", type=str)
    parser.add_argument("--target", "-t", type=str)
    parser.add_argument("--gpu", "-g", default=0, type=int, help="Gpu ID")
    parser.add_argument('--mode', type=str, default='OPDA')

    # do not need to modify
    parser.add_argument('--exp_name', type=str, default='unk')
    parser.add_argument('--seed', type=int, default=-1)
    parser.add_argument("--n_trials",
                        "-n",
                        default=3,
                        type=int,
                        help="Repeat times")
    parser.add_argument("--method", "-m", default="OVA", help="Method")
    parser.add_argument("--backbone",
                        "-b",
                        default="resnet50",
                        help="Backbone")
    args = parser.parse_args()

    ##################################################################################

    if args.mode == 'OPDA':
        source_template = './txt/source_{}_opda.txt'
        target_template = './txt/target_{}_opda_{}.txt'
    elif args.mode == 'ODA':
        source_template = './txt/source_{}_obda.txt'
        target_template = './txt/target_{}_obda_{}.txt'

    if args.dataset == 'office31':
        domains = ["amazon", "dslr", "webcam"]
        config_file = 'configs/office-train-config_' + args.mode + '.yaml'
    elif args.dataset == 'officehome':
        domains = ['art', 'clipart', 'product', 'real_world']
        config_file = 'configs/officehome-train-config_' + args.mode + '.yaml'
        if args.mode == 'OPDA':
            source_template = './txt/source_{}_univ.txt'
            target_template = './txt/target_{}_univ_{}.txt'
    elif args.dataset == 'visda':
        domains = ["synthetic", "real"]
        config_file = ''
    elif args.dataset == 'domainnet':
        domains = [
            'clipart', 'infograph', 'painting', 'quickdraw', 'real', 'sketch'
        ]
        config_file = ''
    else:
        raise ValueError('Unknown Dataset: {}'.format(args.dataset))

    exp_info = args.exp_name
    if exp_info:
        exp_info = '_' + exp_info

    source = args.source
    target = args.target

    # num_unks = [5, 10, 15, 20, 25, 30, 35, 40, 45]
    if args.mode == 'OPDA':
        num_unks = [10, 15, 20, 25, 30, 35, 40, 45]
    else:
        num_unks = [5, 10, 15, 20, 25, 30, 35]

    for n_unk in num_unks:
        for i in range(args.n_trials):
            base_dir = osp.join(
                'output', args.method,
                args.dataset + '_' + args.mode + '_' + str(n_unk),
                args.backbone + exp_info)
            output_dir = osp.join(base_dir, source + '_to_' + target,
                                  str(i + 1))
            seed = args.seed
            if args.seed < 0:
                seed = seed_hash(args.method, args.backbone, args.dataset,
                                 source, target, i)

            source_txt = source_template.format(source)
            target_txt = target_template.format(target, n_unk)

            os.system(f'python train_amp.py '
                      f'--config  {config_file} '
                      f'--source_data {source_txt} '
                      f'--target_data {target_txt} '
                      f'--gpu {args.gpu} '
                      f'--output-dir {output_dir} '
                      f'--seed {seed}')
