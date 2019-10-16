#!/usr/bin/python3
import os

gitignore = ("__init__.py", "目录.md", "get_directory_txt.py", ".git", ".idea", ".gitignore")


class AutoDirectoty:
    def __init__(self, path):
        self.id = 0
        self.files_dic = {}
        self.base_list = []  # 初始层级列表
        self.base_dir = {}  # 初始层级对应的字典
        self.father_id = {}
        self.directoty_txt = ""
        self.path = path

    def writefile(self, path="."):
        with open(path + "/目录.md", "w", encoding='utf8') as f:
            f.write(str(self.directoty_txt))

    def get_list(self, level, father_id, file_path="."):
        dir = False
        for file in os.listdir(file_path):
            if file not in gitignore:
                self.id += 1
                new_file = file_path + "/" + file
                file_name = file if os.path.isfile(new_file) else "/" + file + "/"
                self.files_dic[self.id] = {"name": file_name, "level": level}
                if father_id in self.father_id.keys():
                    self.father_id[father_id].append(self.id)
                else:
                    self.father_id[father_id] = [self.id]
                if level == 1:
                    self.base_list.append(file_name)
                    self.base_dir[file_name] = self.id

                if not os.path.isfile(new_file):
                    dir = True
                    new_level = level + 1
                    new_path = file_path + "/" + file
                    self.get_list(new_level, self.id, new_path)
        if not dir:
            return

    def edit_dir(self, name):
        if name.startswith("/") and name.endswith("/"):
            return "[" + name[1:-1] + "]"
        else:
            return name

    def get_indent_flag(self, level):
        return " " * (level - 1) * 4 if level > 1 else ""

    def dir_order(self):
        self.base_list.sort()

    def add_text(self, level, name):
        return self.directoty_txt + self.get_indent_flag(level) + name + "\n"

    def get_dir(self):
        for base_dir in self.base_list:
            file_name = self.edit_dir(base_dir)
            base_id = self.base_dir[base_dir]
            level = self.files_dic[base_id]["level"]
            self.directoty_txt = self.add_text(level, file_name)

            if base_dir.startswith("/") and base_dir.endswith("/"):
                self.get_dir_child(base_id)

    def get_dir_child(self, father_id):
        name_list = [[self.files_dic[id]["name"], id] for id in self.father_id[father_id]]
        name_list.sort()

        for name in name_list:
            level = self.files_dic[name[1]]["level"]
            self.directoty_txt = self.add_text(level, self.edit_dir(name[0]))

            if name[0].startswith("/") and name[0].endswith("/"):
                self.get_dir_child(name[1])

    def show_message(self):
        print("文件数:{}".format(self.id))

    def run(self):
        level = 1
        id = 0
        self.get_list(level, id, self.path)
        self.dir_order()
        self.get_dir()
        self.writefile(self.path)
        self.show_message()


def main():
    path = "/home/tarena/1905/TSD1906"
    ad = AutoDirectoty(path)
    ad.run()

main()
