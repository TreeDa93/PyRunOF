

DIR_NOT_EXIST_TEMPLATE = """The specify directory "{directory}" does not exist! \n
I have returned empty tuple!"""


NOTHING_FOUND_TEMPLATE = """There were no folders in the specified directory '{directory}' that contain the specified word '{word}' in their name. \n
I have returned empty tuple!"""

FILE_MISS_TEMPLATE = """The directory ({dir_path}) exists, but the file to be deleted ({folder_name}) is missing!
"""

MORE_INFO_TO_DELETE = """You have to enter either 
1. the list of explicitly specified paths (full_paths) to be deleted 
or
2. the list consists of words (words) and directory path (directory) or key of directory path (dir_key). 
The specified word is used for seeking folders to be deleted in the path directory """

WORD_TYPE = "The argument (word) must be only string!"
