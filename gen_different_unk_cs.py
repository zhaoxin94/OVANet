import os.path as osp
import os

if __name__ == '__main__':
    domains = ["AID", "Merced", "NWPU"]
    domain_name = {
        "AID": "AID",
        "Merced": "Merced",
        "NWPU": "NWPU",
    }
    # mode: univ or obda
    mode = 'obda'

    path = osp.join('data', domains[0])
    dir_list = os.listdir(path)
    dir_list.sort()

    # category
    if mode == 'univ':
        raise NotImplementedError
    if mode == 'obda':
        unknown_nums = [3, 4, 5, 6, 7, 8, 9]
        n_source_private = 0
    else:
        raise NotImplemented

    for target_domain in domains:
        p_path = os.path.join('data', target_domain)
        for unknown_num in unknown_nums:
            n_share = 12 - n_source_private - unknown_num
            n_source = n_share + n_source_private
            source_list = dir_list[:n_source]
            target_list = dir_list[:n_share] + dir_list[n_source:n_source +
                                                        unknown_num]

            path_source = "txt_unknown/source_{}_{}_{}.txt".format(
                domain_name[target_domain], mode, unknown_num)
            with open(path_source, "w") as f:
                for k, direc in enumerate(source_list):
                    if not '.txt' in direc:
                        files = os.listdir(os.path.join(p_path, direc))
                        files.sort()
                        for i, file in enumerate(files):
                            file_name = os.path.join('data', target_domain,
                                                     direc, file)
                            if direc in source_list:
                                class_name = direc
                                f.write(
                                    '%s %s\n' %
                                    (file_name, source_list.index(class_name)))

            path_target = "txt_unknown/target_{}_{}_{}.txt".format(
                domain_name[target_domain], mode, unknown_num)
            with open(path_target, "w") as f:
                for k, direc in enumerate(target_list):
                    if not '.txt' in direc:
                        files = os.listdir(os.path.join(p_path, direc))
                        files.sort()
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
