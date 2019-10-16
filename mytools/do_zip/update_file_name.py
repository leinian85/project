#conding:utf8
import os

# 解压文件
def update_name(file):
    dir = os.path.dirname(file)
    file = os.path.join(dir,file)
    new_file = file.replace('、','').replace('：','_')
    print(file)
    if file != new_file:
        command = 'mv {} {}'.format(file,new_file)
        os.system(command)

def update_file_name(file):
    if file.endswith('.mp4'):
        update_name(file)
        return

    if os.path.isfile(file):
        return

    for file_ in os.listdir(file):
        file_path = os.path.join(file, file_)
        update_file_name(file_path)



dir = '/home/tarena/1905/TSD1906'
update_file_name(dir)


# for a,b,c in os.walk(dir):
#     print(a,c)