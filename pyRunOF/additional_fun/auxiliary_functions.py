import os
import pathlib as pl
import shlex
import subprocess
import traceback
from collections.abc import Sequence
from typing import Any

from pyRunOF.exceptions import CommandExecutionError

from . import files as file_utils
from . import priority as priority_utils


def run_command(
    command: Sequence[str] | str,
    run_path: str | os.PathLike[str],
    *,
    log_path: str | os.PathLike[str] | None = None,
    timeout: float | None = None,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    """Run an external command without invoking a shell.

    A string is parsed with :func:`shlex.split` for backward compatibility. New
    callers should pass a sequence so every argument has an explicit boundary.
    """
    args = shlex.split(command) if isinstance(command, str) else list(command)
    if not args or not all(isinstance(arg, str) and arg for arg in args):
        raise ValueError("command must contain non-empty string arguments")

    cwd = pl.Path(run_path).expanduser().resolve()
    if not cwd.is_dir():
        raise FileNotFoundError(f"Run directory does not exist: {cwd}")

    if capture_output and log_path is not None:
        raise ValueError("capture_output and log_path cannot be used together")

    output = None
    log_file = None
    if log_path is not None:
        log_file = (
            (cwd / log_path).resolve() if not pl.Path(log_path).is_absolute() else pl.Path(log_path)
        )
        log_file.parent.mkdir(parents=True, exist_ok=True)
        output = log_file.open("a", encoding="utf-8")

    try:
        return subprocess.run(
            args,
            cwd=cwd,
            check=True,
            stdout=subprocess.PIPE if capture_output else output,
            stderr=subprocess.PIPE if capture_output else subprocess.STDOUT if output else None,
            start_new_session=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.CalledProcessError as exc:
        raise CommandExecutionError(
            f"Command {args[0]!r} exited with status {exc.returncode}"
        ) from exc
    finally:
        if output is not None:
            output.close()


def merge_dicts(args: Sequence[dict]):
    dct = {}
    for entry in args:
        dct.update(entry)
    return dct


class Files:
    """
    The class is intended to fulfill a number of operations on files, for example, changing text ...

    Note:
        Probably, it is possible problems with coding for OS Windows

    Attributes
        ----------
    Methods
        -------
        change_var_fun is the method to find and replace required text part at given file

        change_text(cls, name_var, value_var, name_file='')
             is the method to find and replace required text part at given file

        change_text_line(var_value, var_name, var_excl_name, path_dict=None, file_name='')
            The method fulfills row searching of the given variable var_name to change it to var_value
            if in the line there are not variable named as var_excl_name
        copy_file is the method to make copy of a file and to move it to new path with new name.
        find_files is
        find_path_by_name
    """

    change_var_fun = staticmethod(file_utils.change_var_fun)
    copy_file = staticmethod(file_utils.copy_file)
    find_files = staticmethod(file_utils.find_files)
    find_folders_by_word = staticmethod(file_utils.find_folders_by_word)
    find_path_by_name = staticmethod(file_utils.find_path_by_name)
    open_json = staticmethod(file_utils.open_json)
    save_json = staticmethod(file_utils.save_json)
    is_executable = staticmethod(file_utils.is_executable)
    merge_dicts = staticmethod(file_utils.merge_dicts)


class Priority:
    """
    The class is designed to choose priority between the sent variable in the executing method and
    its object attributes. The general sense of priority choosing is firstly to check the given variable in
    executing method, if the variable is None then to check the variable in the attributes of the object serving for
    execution of the method.

    Note:
        ---
        In the current version there are attributes. Their appointment is doubtful because highly likely
        the attribute will be deleted in the future.

    Attributes
        ----------
        paths is the dictionary of paths
        name_case is the dictionary of names
        sif_name is the name of elmer file with sif extension
        file is the name of file

    Methods
        -------
        variable(var, key, where)
        path_dict(path_dict, path_key, where)
        path(path_dict, path_key, where)
        name(name, name_key, where)
        check_key(key, where)
        check_name(name, where)
        check_key_path(path_dict, key, where)
        check_key_name
        check_path_existence
        check_path_existence_only
        error_create_folder
    """

    def __init__(
        self, names_cases: str = None, paths: str = None, sif_name: str = ".sif", file: str = None
    ) -> None:
        self.paths = paths
        self.names_cases = names_cases
        self.sif_name = sif_name
        self.file = file

    @classmethod
    def variable(cls, var, where, var_key=None):
        """The method is intended to priority between the sent variable in the executing method and
        its object attributes.
        Input :
            var is the evaluating variable if the var is None then
            key is the key of the dictionary storing value of required variable
            where is the object where the method will be finding required variable by key
        Output:
            return var according priority
        """

        if var is not None:
            return var
        if isinstance(where, dict):
            return priority_utils.select_var(var, where, var_key)
        if where is not None:
            return where
        return priority_utils.select_var(var, {}, var_key)

    @classmethod
    def path(cls, path, where, path_key=None):
        """The method is intended to priority between the sent path_dict in the executing method and
        its object attributes of paths.
        Input :
            path_dict is the evaluating path_dict if the path_dict is None then
            path_key is the key of the dictionary storing value of required variable
            where: dict is the object where the method will be finding required variable by key
        Output:
            return var according priority
        Notice: The method is working as with dictionaries and so variables.
        """
        if path is not None:
            return priority_utils.select_path(path, {}, path_key)
        if isinstance(where, dict):
            return priority_utils.select_path(path, where, path_key)
        return priority_utils.select_path(where, {}, path_key)

    @classmethod
    def name(cls, name, where, name_key=None):
        """The method is used for selection of given name the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
            name is the checking name
            name_key is the key of the dictionary storing value of required name
            where is the object where the method will be finding required name by key
        Output:
            return name according priority
        """
        if name is not None:
            return priority_utils.select_name(name, {}, name_key)
        if isinstance(where, dict):
            return priority_utils.select_name(name, where, name_key)
        return priority_utils.select_name(where, {}, name_key)

    @classmethod
    def check_path_existence(cls, check_path, make_new=False):
        """The method is used for checking existing of given path.
        The method can check one lower level of the path as directory for existing if the directory is existent
        you can create new folder of your path by changing flag mane_new on True.
        FIXME : improve description
        Input :
             check_path is checking path
             make_new is logical variable to define crate new folder if directory of the file exist.

        Output:
            return path or error
        """
        return priority_utils.check_path_existence(check_path, make_new=make_new)

    @classmethod
    def check_path_existence_only(cls, check_path):
        """Check the existence of a given path.

        Parameters:
        check_path (str or Path): The path to check.

        Returns:
        str: 'full' if the path exists,
        'dir' if only the parent directory of the final folder exists.
        'noExist' if the specify directory is not exist

        """
        try:
            return priority_utils.check_path_existence_only(check_path)
        except ValueError:
            return "noExist"

    def sif_file(self, sif_file):
        """The method is used for selection of given name
        the first priority is given name by methods
        the second priority is given name by class constructor
        If both name is None, the program is interupted
        Input :
        basePath, newPath is checkoing pathes
        Output:
        retrunBasePath, returnNewPath is selected pathes acording priority
        """
        if sif_file is None:
            if self.sif_file is not None:
                return self.sif_file
            else:
                raise ValueError("sif_file must be provided")
        else:
            return sif_file

    @classmethod
    def cores(cls, core_OF, where):
        if core_OF is None:
            if where is not None:
                return where
            else:
                cls._raise_error_run()
        else:
            return core_OF

    def _priority(self, var, type_priority="core"):
        """
        Test priority fun
        :param var:
        :return:
        """
        if var is None:
            return self._chose_type_priority(self, type_priority)
        else:
            return var

    def _chose_type_priority(self, type_priority):
        """The function defines priority between attribute variable
        and input variable of the executing method

        Input :
        type_priority is the flag to define for which variables to detirmine the priority
        Now it is avaible following flags
            * core_OF is core OpenFOAM flags
            * file is the file flag
        Output:
        attribute of the required variable or
        error that the required variables was not set

        """
        if type_priority == "core_OF":
            if self.core_OF is not None:
                return self.core_OF
            else:
                raise ValueError("OpenFOAM core count must be configured")
        elif type_priority == "file":
            if self.file is not None:
                return self.file
            else:
                raise ValueError("file must be provided")
        else:
            pass

    @staticmethod
    def _check_path_type(path) -> Any:
        """
        The function checks belonging of input variable to
        path is the checking variable
        return True or False
        """
        return isinstance(path, (str, os.PathLike))

    @staticmethod
    def error_create_folder():
        error_message = """
            ------------------------------------------
            The folder is already exist and your moder
            of writing is available to make copy.
            Above information can help you find where is it.
            ------------------------------------------
            """
        for message in traceback.format_stack():
            print(message)
        # print(repr(traceback.format_stack()))
        raise FileExistsError(error_message)

    @staticmethod
    def _raise_error_run():
        raise ValueError("OpenFOAM core count must be configured")
