"""
EXAMPLE of message template:

ERROR_MSG_TEMPLATE = '''ERROR: In {var1} bla bla bla {var2}'''

USAGE the ERROR as template

ERROR_MSG_TEMPLATE.format(var1=1, var2=path)

"""


UNKNOWN_ERROR_MSG_TEPLATE: str = """
The unknown error!
"""

INFO_DICT_TYPE_ERROR_MSG_TEMPLATE: str = """ 
\n ------------------------------------------ \n
Error initializing instance of {class_name}:
The 'info' attribute must be a dictionary. \n
------------------------------------------ \n
"""

###### PRIORIT ERRORS ######


INFO_IS_NOT_DICT =  ''' 
                ------------------------------------------
                The specify info_node ({info_node}) is not
                dictionary! The type of the info_node is 
                {info_type}. Please, check correct building 
                the info node.
                Above information can help you find where is it.
                ------------------------------------------
                '''

PRIORITY_INFO_KEY_ERROR_MSG = ''' 
                ------------------------------------------
                The specify info_node ({info_node}) has not
                sent key ({key}) to get request variable!
                Above information can help you find where is it.
                ------------------------------------------
                '''
PRIORITY_INCCORECT_PATH_TYPE_MSG = ''' 
                ------------------------------------------
                The path is chosen according priority being 
                inccorect path. 
                Above information can help you find where is it.
                ------------------------------------------
                '''
PRIORITY_INCORRECT_KEY_TYPE_MSG = ''' 
                ------------------------------------------
                The specify key ({key}) is incorrect type ({key_type}).
                The key must be hashable type and not None.
                Above information can help you find where is it.
                ------------------------------------------
                '''

PRIORITY_NO_ARGS = ''' 
                ------------------------------------------
                Neither an argument nor a dictionary with 
                information was passed to perform the procedure.
                Above information can help you find where is it.
                ------------------------------------------
                '''

INCORRECT_MODE_TO_SELECT_MSG = ''' 
                ------------------------------------------
                Private error in the library! 
                The mode (mode={mode}) of _select_req_input_args 
                is chose incorrect. 
                Above information can help you find where is it.
                ------------------------------------------
                '''

WRONG_TYPE_NAME = ''' 
                ------------------------------------------
                The type of name is {name_type}. The type is
                wrong. The typy must be only string!
                Above information can help you find where is it.
                ------------------------------------------
                '''

CHECK_PATH_EXIST_1 = ''' 
                ------------------------------------------
                The path {path} is not exist! 
                But directory {dir} is exist! You can create 
                the folder {folder} yourself or set flag make_new 
                as True to make the Folder by the script with name {folder}! 
                Above information can help you find where is it.
                ------------------------------------------
                '''

CHECK_PATH_EXIST_2 = ''' 
                ------------------------------------------
                The given name {path} is not exist and directory 
                {dir} of the folder {folder} is not exist as well.  
                Above information can help you find where is it.
                ------------------------------------------
                '''


# else:
UNKNOWN_ERROR_MSG = ''' 
                ------------------------------------------
                I do not know the error! The developer should it check!
                ------------------------------------------
                '''