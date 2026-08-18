
class Information:
 
    # def __new__(cls):
    #     print('I run __new__')
    
    def __init__(self) -> None:
        self.information = 'General info!!!'
        print('I run __init__')


    def my_print(self):
        print('I run my prin function!!!')


class Constant:

    def __init__(self):
        print('Hi!')
        class_info = Information.__new__(Information) # initialize class
        class_info.__init__()
        instance_info = Information.__init__(self)
        info = Information()

    Information().my_print()

def main():
    # info = Information()
    # info.my_print()
    Constant()
    # info.my_print()

def merge_dict():
    dict1 = {'h': 2, 'e':5}
    dict2 = {'hell': 10, 'ooo': 10}
    dict3 = {'uuu': 19, 'iii': 'hello'}
    lists = [dict1, dict2, dict3]
    merged_dict = {}
    for cur_dict in lists:
        merged_dict.update(cur_dict)
    # merged_dict = {key: val for key, val in [cur_dict.items() for cur_dict in lists]}
    print(merged_dict)


def fun_to_wrap():
    print('hello')

def test():
    print('hhh')

def set_items(file, *lists: dict, **options):

    print(file)
    for list_cur in lists:
        print(list_cur)


if __name__ == '__main__':
    
    # print('hi', __file__)
    # print(__doc__)

    # foam_items = {'startTime' : 5, 
    #               'dictName': 'fast'}
    # string_values = ''
    # for key, val in foam_items.items():
    #     string_values += f'{key}={val}, '
    # command = f'foamDictionary -set "{string_values[:-2]}" ssss'
    # print(command)
    merge_dict()
    set_items('hello', {1: 5}, {'hi': 5})