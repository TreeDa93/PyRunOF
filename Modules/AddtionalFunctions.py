import os
import shutil


def change_var_fun(dist_var, sour_var, nameFile=''):
    """Function to find and replace required text part at given file
            dist_var is the depicts finding variables
            sour_var depicts replacing variables
            nameFile is the name of file where the procedure will be done

    """
    if os.path.isfile(nameFile):
        with open(nameFile, 'r') as f:
            oldData = f.read()
        newData = oldData.replace(str(dist_var), str(sour_var))
        with open(nameFile, 'w') as f:
            f.write(newData)
    else:
        print(f'Warning: The file {nameFile} is not exist!')


def changeVariablesFun(distVar, sourVar, nameFile=' '):
    """The fucntion is devoted to change  gotten text part
    dist_var is variable defended text, which should be replaced
    sour_var is variable defended text, which should be entered instead replaced text part
    nameFile is name of file where the procedure will be executed.
    """
    os.system("sed -i 's/{0}/{1}/g' {2}".format(distVar, sourVar, nameFile))


def copy_fun(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


def copy_files(root_src_dir, root_dst_dir):
    for file_ in os.listdir(root_src_dir):
        src_file = os.path.join(root_src_dir, file_)
        dst_file = os.path.join(root_dst_dir, file_)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copy(src_file, dst_file)


def copyFiele(root_src_dir, root_dst_dir, nameFilesOld='', nameFileNew=''):
    src_file = os.path.join(root_src_dir, nameFilesOld)
    dst_file = os.path.join(root_dst_dir, nameFileNew)
    shutil.copy2(src_file, dst_file)


class AddtionalFun:
    """
    Discription of class
    FIXME
    Note:
        Возможны проблемы с кодировкой в Windows

    Attributes
        ----------
        file_path : str
            полный путь до текстового файла
        lines : list
            список строк исходного файла

    Methods
        -------
        change_text(self, dist_var, sour_var, name_file='')
            Разделяет строки списка по указанному разделителю
            и возвращает результат в виде списка
    """

    def __init__(self):
        pass

    def change_text(self, dist_var, sour_var, name_file=''):
        """Function to find and replace required text part at given file
        dist_var is the depicts finding variables
        sour_var depicts replacing variables
        nameFile is the name of file where the procedure will be done

        """

        if os.path.isfile(dist_var):
            with open(sour_var, 'r') as f:
                oldData = f.read()
            newData = oldData.replace(str(dist_var), str(sour_var))
            with open(name_file, 'w') as f:
                f.write(newData)
        else:
            print(f'Warning: The file {name_file} is not exist!')
