import os.path as osp
import os

if __name__ == '__main__':
    domains = ["Art", "Clipart", "Product", "Real"]
    domain_name = {
        "Art": "art",
        "Clipart": "clipart",
        "Product": "product",
        "Real": "real_world"
    }
    # mode: univ or obda
    mode = 'obda'

    path = osp.join('data', domains[0])
    dir_list = os.listdir(path)
    dir_list.sort()

    # category
    if mode == 'univ':
        n_share = 10
        n_source_private = 5
        unknown_nums = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    elif mode == 'obda':
        n_share = 25
        n_source_private = 0
        unknown_nums = [5, 10, 15, 20, 25, 30, 35, 40]
    else:
        raise NotImplemented

    n_source = n_share + n_source_private
    source_list = dir_list[:n_source]

    for target_domain in domains:
        p_path = os.path.join('data', target_domain)
        for unknown_num in unknown_nums:
            target_list = dir_list[:n_share] + dir_list[n_source:n_source +
                                                        unknown_num]
            path_target = "txt_unknown/target_{}_{}_{}.txt".format(
                domain_name[target_domain], mode, unknown_num)
            with open(path_target, "w") as f:
                for k, direc in enumerate(target_list):
                    if not '.txt' in direc:
                        files = os.listdir(os.path.join(p_path, direc))
                        for i, file in enumerate(files):
                            file_name = os.path.join('data', target_domain,
                                                     direc, file)
                            if direc in source_list:
                                class_name = direc
                                f.write(
                                    '%s %s\n' %
                                    (file_name, source_list.index(class_name)))
                            elif direc in target_list:
                                f.write('%s %s\n' %
                                        (file_name, len(source_list)))
