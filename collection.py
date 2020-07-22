import os


def generate_markdown(filename):
    ignore_files = _get_ignore_dirs_files(['.git', '.idea'])
    with open(filename, 'w+') as f:
        for root, dirs, files in os.walk('.', topdown=True):
            if is_ignored(ignore_files, root):
                continue
            files = filter(lambda x: '.md' in x and filename not in x and
                                     'README.md' not in x, files)
            for file in files:
                with open(os.path.join(root, file), 'r') as read:
                    f.write(read.read())
                    f.write('\n')


def _get_ignore_dirs_files(special=None):
    """
    获取被忽略的文件夹，用于过滤无效的文件
    :param special: 自定义的过滤文件
    :return:
    """
    ignore_files = []
    with open('.gitignore', 'r') as f:
        while True:
            res = f.readline()
            if not res:
                break
            else:
                ignore_files.append(res[:-1])
    if special:
        ignore_files.extend(special)
    return ignore_files


def is_ignored(ignore_files, file):
    return file in ignore_files


if __name__ == '__main__':
    generate_markdown('整合.md')
