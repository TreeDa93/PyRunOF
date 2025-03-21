import traceback
import warnings

def raise_waring_files(warrning_code, **kwargs):
    """ Raises a warning based on the provided warning code and additional keyword arguments.
        Parameters:
        warrning_code (str): The code representing the type of warning to raise. 
                            Possible values are 'DIR_NOT_EXIST', 'NOTHING FOUND', or any other string.
        **kwargs: Additional keyword arguments to format the warning message templates.
        Raises:
        Warning: A warning with a specific message based on the warning code.
        Example:
        raise_warring_files('DIR_NOT_EXIST', directory='/path/to/dir')
    """
    i = 1
    for message in traceback.format_stack():
        print(f'{i}.', message)
        i+=1
    match warrning_code:
        case 'DIR_NOT_EXIST':
            from .waring_message import DIR_NOT_EXIST_TEMPLATE as TEMPLATE
            # directory must be spicfied! 
            MESSAGE = TEMPLATE.format(**kwargs)
            warnings.warn(MESSAGE, stacklevel=1)
        case 'NOTHING FOUND':
            from .waring_message import NOTHING_FOUND_TEMPLATE as TEMPLATE
            MESSAGE = TEMPLATE.format(**kwargs)
            warnings.warn(MESSAGE, stacklevel=1)
        case 'FILE_MISS':
            from .waring_message import FILE_MISS_TEMPLATE as TEMPLATE
            MESSAGE = TEMPLATE.format(**kwargs)
            warnings.warn(MESSAGE, stacklevel=1)
        case 'MORE_INFO_TO_DELETE':
            from .waring_message import MORE_INFO_TO_DELETE as TEMPLATE
            MESSAGE = TEMPLATE.format(**kwargs)
            warnings.warn(MESSAGE, stacklevel=1)
        case 'WORD_TYPE':
            from .waring_message import WORD_TYPE as TEMPLATE
            MESSAGE = TEMPLATE.format(**kwargs)
            warnings.warn(MESSAGE, stacklevel=1)
        case _:
            warnings.warn('The warrning is being developed yet!  ', stacklevel=2)