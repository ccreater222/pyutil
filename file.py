import os
def walk_directory(path: str, func):
    print(path)
    for root, dirs, files in os.walk(path):
        path = root.split(os.sep)
        for file in files:
            p = os.path.join(root, file)
            with open(p, "r") as f:
                yield func(f.read())