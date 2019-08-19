import os

gitignore = ("__init__.py", "目录.md", "get_directory.py", ".git", ".idea")

class AutoDirectoty:
    def __init__(self):
        self.directoty_txt = ""

    def writefile(self):
        with open("README.md", "w") as f:
            f.write(self.directoty_txt)

    def get_list(self, level, file_path):
        dir = False
        indent_flag = " " * (level - 1) * 4
        for file in os.listdir(file_path):
            if file not in gitignore:
                new_file = file_path + "/" + file
                file_name = file if os.path.isfile(new_file) else "[" + file + "]"
                self.directoty_txt = self.directoty_txt + indent_flag + file_name + "\n"
                if not os.path.isfile(new_file):
                    dir = True
                    new_level = level + 1
                    new_path = file_path + "/" + file
                    self.get_list(new_level, new_path)
        if not dir:
            return


def main():
    level = 1
    path = "."
    ad = AutoDirectoty()
    ad.get_list(level, path)
    ad.writefile()


if __name__ == '__main__':
    main()
