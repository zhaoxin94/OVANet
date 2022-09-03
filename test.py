from __future__ import print_function
import yaml
import easydict
import os
import argparse
import random
import numpy as np

import torch
from torch import nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.cuda.amp import GradScaler
from torch.cuda.amp import autocast

from utils.utils import log_set, save_model
from utils.loss import ova_loss, open_entropy
from utils.lr_schedule import inv_lr_scheduler
from utils.defaults_new import get_dataloaders, get_models_new
from eval import test

parser = argparse.ArgumentParser(
    description='Pytorch OVANet',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--config',
                    type=str,
                    default='config.yaml',
                    help='/path/to/config/file')

parser.add_argument('--source_data',
                    type=str,
                    default='./utils/source_list.txt',
                    help='path to source list')
parser.add_argument('--target_data',
                    type=str,
                    default='./utils/target_list.txt',
                    help='path to target list')
parser.add_argument('--log-interval',
                    type=int,
                    default=100,
                    help='how many batches before logging training status')
parser.add_argument('--exp_name',
                    type=str,
                    default='office',
                    help='/path/to/config/file')
parser.add_argument('--network',
                    type=str,
                    default='resnet50',
                    help='network name')
parser.add_argument("--gpu_devices",
                    type=int,
                    nargs='+',
                    default=None,
                    help="")
parser.add_argument("--no_adapt", default=False, action='store_true')
parser.add_argument("--save_model", default=False, action='store_true')
parser.add_argument("--save_path",
                    type=str,
                    default="record/ova_model",
                    help='/path/to/save/model')
parser.add_argument('--multi',
                    type=float,
                    default=0.1,
                    help='weight factor for adaptation')
parser.add_argument("--seed",
                    type=int,
                    default=-1,
                    help="only positive value enables a fixed seed")
parser.add_argument("--output-dir",
                    type=str,
                    default="",
                    help="output directory")
args = parser.parse_args()

print(args.source_data)
print(args.target_data)


def set_random_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


# set seed
if args.seed >= 0:
    print("Setting fixed seed: {}".format(args.seed))
    set_random_seed(args.seed)

torch.backends.cudnn.benchmark = False
torch.backends.cudnn.detrministic = True

config_file = args.config
conf = yaml.safe_load(open(config_file))
save_config = yaml.safe_load(open(config_file))
conf = easydict.EasyDict(conf)
gpu_devices = ','.join([str(id) for id in args.gpu_devices])
os.environ["CUDA_VISIBLE_DEVICES"] = gpu_devices
args.cuda = torch.cuda.is_available()

source_data = args.source_data
target_data = args.target_data
evaluation_data = args.target_data
network = args.network
use_gpu = torch.cuda.is_available()
n_share = conf.data.dataset.n_share
n_source_private = conf.data.dataset.n_source_private
n_total = conf.data.dataset.n_total
open = n_total - n_share - n_source_private > 0
num_class = n_share + n_source_private
script_name = os.path.basename(__file__)

inputs = vars(args)
inputs["evaluation_data"] = evaluation_data
inputs["conf"] = conf
inputs["script_name"] = script_name
inputs["num_class"] = num_class
inputs["config_file"] = config_file

source_loader, target_loader, \
test_loader, target_folder = get_dataloaders(inputs)

logname = log_set(inputs)

G, C1, C2, opt_g, opt_c, \
param_lr_g, param_lr_c = get_models_new(inputs)

ndata = target_folder.__len__()

test(10000, test_loader, logname, n_share, G, [C1, C2], open=open)
