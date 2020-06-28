import os


def generate_markdown():
    with open('整合.md', 'w+') as f:
        for root, dirs, files in os.walk('.', topdown=True):
            if '.git' in root or '.idea' in root:
                continue
            files = filter(lambda x: '.md' in x and 'total' not in x and 'README.md' not in x, files)
            for file in files:
                with open(os.path.join(root, file), 'r') as read:
                    f.write(read.read())


if __name__ == '__main__':
    generate_markdown()
