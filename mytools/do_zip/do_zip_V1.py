#conding:utf8
import os

# 解压文件
def unpack(file,suffix):
    dir = os.path.dirname(file)
    if suffix == 'rar':
        new_dir = ''.join(file.split('.rar')[:-1]).replace('.','')
        command = 'unrar e -o- {} {}'
    elif suffix == 'zip':
        new_dir = ''.join(file.split('.zip')[:-1]).replace('.','')
        command = 'unzip -o {} -d {}'
    elif suffix == 'tar':
        new_dir = ''.join(file.split('.tar')[:-1]).replace('.','')
        command = 'tar -xvf {} {}'
    elif suffix == 'bz2':
        new_dir = ''.join(file.split('.tar.bz2')[:-1]).replace('.', '')
        command = 'tar -xjvf {} {}'
    elif suffix == 'gz':
        new_dir = ''.join(file.split('.tar.gz')[:-1]).replace('.', '')
        command = 'tar -xzvf {} -C {}'
    elif suffix == 'Z':
        new_dir = ''.join(file.split('.tar.Z')[:-1]).replace('.', '')
        command = 'tar -xZvf {} {}'

    if not os.path.exists(new_dir):
        os.makedirs(new_dir)

    command = command.format(file,new_dir)
    os.system(command)
    # command = 'rm -fr {}'.format(file)
    # os.system(command)

def do_zip(file):
    if '.' in file:
        suffix = file.split('.')[-1]
        if suffix in ('zip', 'rar','tar','bz2','gz','Z'):
            unpack(file,suffix)
            return

    try:
        for file_ in os.listdir(file):
            file_path = os.path.join(file, file_)
            do_zip(file_path)
    except:
        pass


dir = '/home/tarena/1905/AIDCode/aid1905_01'
do_zip(dir)


# for a,b,c in os.walk(dir):
#     print(a,c)