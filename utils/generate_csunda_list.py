import os.path as osp
import os

if __name__ == '__main__':
    # mode: obda, pda, opda
    mode = 'opda'
    domains = ["AID", "CLRS", "MLRSN", "OPTIMAL-31"]

    # 写到这里了
    path = osp.join('data', domains[1])
    dir_list = os.listdir(path)
    dir_list = sorted(dir_list, key=lambda x: x.lower())
    print(dir_list)
    print('total {} classes'.format(len(dir_list)))

    if mode == 'obda':
        public_classes = [
            'airport', 'beach', 'farmland', 'forest', 'industrial', 'parking',
            'residential'
        ]
        source_private_classes = []
        target_private_classes = [
            'bridge', 'commercial', 'desert', 'meadow', 'mountain', 'overpass',
            'playground', 'port'
        ]
    elif mode == 'pda':
        public_classes = [
            'airport', 'beach', 'farmland', 'forest', 'industrial', 'parking',
            'residential'
        ]
        source_private_classes = [
            'bridge', 'commercial', 'desert', 'meadow', 'mountain', 'overpass',
            'playground', 'port'
        ]
        target_private_classes = []
    elif mode == 'opda':
        public_classes = [
            'airport', 'beach', 'farmland', 'forest', 'industrial', 'parking',
            'residential'
        ]
        source_private_classes = ['bridge', 'commercial', 'desert', 'meadow']
        target_private_classes = ['mountain', 'overpass', 'playground', 'port']
    else:
        raise NotImplementedError
    
    print('public_classes', public_classes)
    print('source_private_classes:', source_private_classes)
    print('target_private_classes:', target_private_classes)

    source_list = public_classes + source_private_classes
    target_list = public_classes + target_private_classes

    print('source classes', source_list)
    print('target classes', target_list)


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