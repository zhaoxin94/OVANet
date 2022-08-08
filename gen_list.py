import os
import os.path as osp


def gen_list(data_root, dataset_name, domains, n_share, n_source_private):
    txt_path = osp.join(data_root, dataset_name, 'image_list')
    txt_file = osp.join(txt_path, domains[0] + '.txt')
    classes = []
    with open(txt_file, "r") as f:
        for line in f.readlines():
            path, _ = line.split()
            class_name = path.split('/')[-2]
            if class_name not in classes:
                classes.append(class_name)
    assert len(classes) == 345, 'Wrong DomainNet classes'
    print(classes)

    # class split
    n_total = len(classes)
    n_target_private = n_total - n_share - n_source_private
    print('n_total:', n_total)
    public_classes = classes[:n_share]
    source_private_classes = classes[n_share:n_share + n_source_private]
    target_private_classes = classes[n_share + n_source_private:]
    all_classes = public_classes + source_private_classes + ["unknown"]

    for domain in domains:
        txt_file = osp.join(txt_path, domain + '.txt')
        source_list = []
        target_list = []

        # construct source txt
        with open(txt_file, 'r') as f:
            for line in f.readlines():
                path, _ = line.split()
                class_name = path.split('/')[-2]

                source_classes = public_classes + source_private_classes
                if class_name in source_classes:
                    label = all_classes.index(class_name)
                    assert source_classes.index(
                        class_name) == all_classes.index(
                            class_name), 'someting wrong'
                    source_list.append(path + ' ' + str(label) + '\n')
                else:
                    continue

        with open(osp.join('txt_new',
                           'source_' + domain + '_univ.txt'), 'w') as f_source:
            f_source.writelines(source_list)

        # construct target txt
        with open(txt_file, 'r') as f:
            for line in f.readlines():
                path, _ = line.split()
                class_name = path.split('/')[-2]

                if class_name in public_classes:
                    label = all_classes.index(class_name)
                    target_list.append(path + ' ' + str(label) + '\n')
                elif class_name in target_private_classes:
                    label = all_classes.index("unknown")
                    class_name = "unknown"
                    target_list.append(path + ' ' + str(label) + '\n')
                else:
                    continue

        with open(osp.join('txt_new',
                           'target_' + domain + '_univ.txt'), 'w') as f_target:
            f_target.writelines(target_list)


if __name__ == "__main__":
    data_root = "/home/zhao/data/DA"
    # modify corresponding information
    dataset_name = "domainnet"
    n_share = 150
    n_source_private = 50
    domains = ['painting', 'real', 'sketch']

    gen_list(data_root, dataset_name, domains, n_share, n_source_private)