import os.path as osp
import os

if __name__ == '__main__':
    # mode: univ or obda
    mode = 'obda'
    domains =  ["AID", "Merced", "NWPU"]

    path = osp.join('data', domains[0])
    dir_list = os.listdir(path)
    dir_list = sorted(dir_list, key=lambda x: x.lower())
    print(dir_list)
    print(len(dir_list))

    if mode == 'obda':
        n_share = 9
        n_source_private = 0
    else:
        raise NotImplementedError

    n_source = n_share + n_source_private
    source_list = dir_list[:n_source]
    target_list = dir_list[:n_share] + dir_list[n_source:]

    print(source_list)
    print(len(source_list))
    print(target_list)
    print(len(target_list))

    for domain in domains:
        source_path = f"data/{domain}"
        target_path = f"data/{domain}"

        source_txt = f"txt/source_{domain}_{mode}.txt"
        target_txt = f"txt/target_{domain}_{mode}.txt"

        with open(source_txt, "w") as f:
            for direc in source_list:
                if not '.txt' in direc:
                    files = os.listdir(os.path.join(source_path, direc))
                    files.sort()
                    for i, file in enumerate(files):
                        file_name = os.path.join(source_path, direc, file)
                        class_name = direc
                        f.write('%s %s\n' %
                                (file_name, source_list.index(class_name)))

        with open(target_txt, "w") as f:
            for direc in target_list:
                if not '.txt' in direc:
                    files = os.listdir(os.path.join(target_path, direc))
                    files.sort()
                    for i, file in enumerate(files):
                        file_name = os.path.join(target_path, direc, file)
                        if direc in source_list:
                            class_name = direc
                            f.write('%s %s\n' %
                                    (file_name, source_list.index(class_name)))
                        elif direc in target_list:
                            f.write('%s %s\n' % (file_name, len(source_list)))