from pyRunOF import Constant
from pyRunOF import Manipulations


mp = Manipulations(info_key='main')

mp.create_name('test', name_base='base', name_key='test_name')
print(mp.info)
