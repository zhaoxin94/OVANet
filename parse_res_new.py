import os.path as osp
import argparse
from collections import defaultdict, OrderedDict
import re
import numpy as np
import os
import warnings

def listdir_nohidden(path, sort=False):
    """List non-hidden items in a directory.

    Args:
         path (str): directory path.
         sort (bool): sort the items.
    """
    items = [f for f in os.listdir(path) if not f.startswith(".")]
    if sort:
        items.sort()
    return items

def check_isfile(fpath):
    """Check if the given path is a file.

    Args:
        fpath (str): file path.

    Returns:
       bool
    """
    isfile = osp.isfile(fpath)
    if not isfile:
        warnings.warn('No file found at "{}"'.format(fpath))
    return isfile


def write_now(row, colwidth=10):
    sep = "  "

    def format_val(x):
        if np.issubdtype(type(x), np.floating):
            x = "{:.4f}".format(x)
        return str(x).ljust(colwidth)[:colwidth]

    return sep.join([format_val(x) for x in row]) + "\n"


# compute results across different seeds
def parse_function(*metrics, directory="", end_signal=None):
    print(f"Parsing files in {directory}")
    subdirs = listdir_nohidden(directory, sort=True)

    outputs = []

    for subdir in subdirs:
        fpath = osp.join(directory, subdir, "log.txt")
        assert check_isfile(fpath)
        good_to_go = False
        output = OrderedDict()

        with open(fpath, "r") as f:
            lines = f.readlines()

            for line in lines:
                line = line.strip()

                if end_signal in line:
                    good_to_go = True

                for metric in metrics:
                    match = metric["regex"].search(line)
                    if match and good_to_go:
                        if "file" not in output:
                            output["file"] = fpath
                        num = float(match.group(1))
                        name = metric["name"]
                        output[name] = num

        if output:
            outputs.append(output)

    assert len(outputs) > 0, f"Nothing found in {directory}"

    metrics_results = defaultdict(list)

    for output in outputs:
        msg = ""
        for key, value in output.items():
            if isinstance(value, float):
                msg += f"{key}: {value:.2f}%. "
            else:
                msg += f"{key}: {value}. "
            if key != "file":
                metrics_results[key].append(value)
        print(msg)

    output_results = OrderedDict()

    print("===")
    print(f"Summary of directory: {directory}")
    for key, values in metrics_results.items():
        avg = np.mean(values)
        std = np.std(values)
        print(f"* {key}: {avg:.2f}% +- {std:.2f}%")
        output_results[key] = avg
    print("===")

    return output_results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", "-m", default="OVA", help="Method")
    parser.add_argument("--dataset",
                        "-d",
                        default="officehome",
                        help="Dataset",
                        choices=['office31', 'officehome'])
    parser.add_argument("--backbone",
                        "-b",
                        default="resnet50",
                        help="Backbone")
    parser.add_argument('--exp_name', type=str, default='')
    parser.add_argument('--mode', type=str, default='ODA')
    parser.add_argument("--amp-type",
                        type=str,
                        default='torch',
                        choices=['torch'])

    args = parser.parse_args()

    ###############################################################################
    exp_info = args.exp_name
    if exp_info:
        exp_info = '_' + exp_info

    amp_type = '_' + args.amp_type
    base_dir = osp.join('output', args.method, args.dataset + '_' + args.mode,
                        args.backbone + exp_info + amp_type)

    print('*****************************************************************')
    print(f'Extract results from {base_dir}')
    print(
        '*****************************************************************\n')

    # parse results
    end_signal = "step 10000"

    metrics = []
    metric_names = ["h score", "acc per class", "acc close all", "acc", "roc"]
    for metric_name in metric_names:
        regex_str = re.compile(fr"{metric_name} ([\.\deE+-]+)")
        metric = {"name": metric_name, "regex": regex_str}
        metrics.append(metric)

    final_results = defaultdict(list)
    tasks = ['Avg']

    for directory in listdir_nohidden(base_dir, sort=True):
        directory = osp.join(base_dir, directory)
        if osp.isdir(directory):
            results = parse_function(*metrics,
                                     directory=directory,
                                     end_signal=end_signal)

            for key, value in results.items():
                final_results[key].append(value)

            dir_name = osp.basename(directory)
            split_names = dir_name.split('_')
            source = split_names[0].capitalize()[0]
            find_to = split_names.index('to')
            target = split_names[find_to + 1].capitalize()[0]
            task = source + '2' + target

            tasks.append(task)

    print("Average performance")
    for key, values in final_results.items():
        avg = np.mean(values)
        print(f"* {key}: {avg:.2f}%")
        final_results[key].insert(0, avg)

    results_path = osp.join(base_dir, 'collect_results.txt')
    with open(results_path, 'w') as f:
        f.write(write_now([args.method] + tasks))
        for key in metric_names:
            row = [key]
            row += list(final_results[key])
            f.write(write_now(row))