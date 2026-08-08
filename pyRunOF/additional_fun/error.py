from pyRunOF.exceptions import ConfigurationError


def error_create_folder():
    error_message = """
        ------------------------------------------
        The folder is already exist and your moder
        of writing is available to make copy.
        Above information can help you find where is it.
        ------------------------------------------
        """
    raise FileExistsError(error_message)


def raise_error_run():
    raise ConfigurationError("The number of OpenFOAM cores must be configured")


def _raise_error_no_correct_mode_run(self):
    raise ConfigurationError("Run mode must be 'common', 'parallel', or 'EOF'")


def raise_error_initialize(error_code, **kwargs):
    """ """
    raise ConfigurationError(generate_error_msg(error_code, **kwargs))


def raise_error_priority(error_code, **kwargs):
    """ """
    raise ConfigurationError(generate_error_msg_priority(error_code, **kwargs))


def generate_error_msg(error_code, **kwargs):

    match error_code:
        case "INFO_DICT_TYPE":
            from .error_message import INFO_DICT_TYPE_ERROR_MSG_TEMPLATE

            ERROR_MESSAGE = INFO_DICT_TYPE_ERROR_MSG_TEMPLATE.format(**kwargs)
        case _:
            from .error_message import UNKNOWN_ERROR_MSG

            ERROR_MESSAGE = UNKNOWN_ERROR_MSG

    return ERROR_MESSAGE


def generate_error_msg_priority(error_code, **kwargs):

    match error_code:
        case "INCORRECT_MODE_TO_SELECT":  # +
            from .error_message import INCORRECT_MODE_TO_SELECT_MSG as TEMPLATE

            ERROR_MESSAGE = TEMPLATE.format(**kwargs)
        case "INFO_KEY_ERROR":  # +
            from .error_message import PRIORITY_INFO_KEY_ERROR_MSG as TEMPLATE

            ERROR_MESSAGE = TEMPLATE.format(**kwargs)
        case "INFO:INCORRECT_KEY_TYPE":  # +
            from .error_message import PRIORITY_INCORRECT_KEY_TYPE_MSG as TEMPLATE

            ERROR_MESSAGE = TEMPLATE.format(**kwargs)
        case "INFO:IS_NOT_DICT":  # +
            from .error_message import INFO_IS_NOT_DICT as TEMPLATE

            ERROR_MESSAGE = TEMPLATE.format(**kwargs)
        case "PATH:INCCORECT_PATH_TYPE":
            from .error_message import PRIORITY_INCCORECT_PATH_TYPE_MSG as TEMPLATE

            ERROR_MESSAGE = TEMPLATE.format(**kwargs)
        case "PRIORITY:NO_CORRECT_ARGS":
            from .error_message import PRIORITY_NO_ARGS as TEMPLATE

            ERROR_MESSAGE = TEMPLATE.format(**kwargs)
        case "NAME:INCCORECT_TYPE":
            from .error_message import PRIORITY_NO_ARGS as TEMPLATE

            ERROR_MESSAGE = TEMPLATE.format(**kwargs)
        case "CHECK_PATH_EXIST_1":
            from .error_message import CHECK_PATH_EXIST_1 as TEMPLATE

            ERROR_MESSAGE = TEMPLATE.format(**kwargs)
        case "CHECK_PATH_EXIST_2":
            from .error_message import CHECK_PATH_EXIST_2 as TEMPLATE

            ERROR_MESSAGE = TEMPLATE.format(**kwargs)

        case _:
            from .error_message import UNKNOWN_ERROR_MSG

            ERROR_MESSAGE = UNKNOWN_ERROR_MSG

    return ERROR_MESSAGE
