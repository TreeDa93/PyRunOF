import pathlib as pl
import shutil
from collections.abc import Iterable
from time import sleep, strftime

from pyRunOF.exceptions import ConfigurationError, UnsafePathError

from ..additional_fun.auxiliary_functions import Files, Priority
from ..additional_fun.information import Information


class ModelConfigurator(Information):
    """
    This class is designed to perform operations on case folders.
    attributes:
    paths is the dictionary consist of paths
    case_names is the dictionary of names of cases

    run_path is the system_path for key run
    new_path is
    name is the name of the class

    Methods:
    *   duplicate_case is the function make copy or duplicate ot existing folder
    *   create_name is the function to create new name of case in cls.case_names
    *   create_path_dir is the function creating system_path from director and folder
                        name in cls.paths
    *   create_path is the method to create new system_path in cls.paths
    *   change_path is the function serving to change existing system_path in cls.system_path
    *   get_path is the function to get system_path by key
    *   get_name is the function to get name by key
    *   create_folder is function create new folder
    """

    def __init__(self, **optional_args):
        """Initializes the manipulation with optional arguments.

            optional arguments:

                info_key (Optional[str]): The main key for the information dictionary. Defaults to 'general'.
                dir_path (Optional[str]): The directory path. Defaults to None.
                set_names (Optional[list]): A list of set names to initialize in the information dictionary. Defaults to ['paths', 'names'].
        Returns:
            None"""

        Information.__init_manipulation__(self, **optional_args)

    def duplicate_case(
        self,
        src_path: str | None = None,
        dist_path: str | None = None,
        src_key: str | None = None,
        dist_key: str | None = None,
        mode: str = "copy",
    ) -> None:
        """Creates a copy of the base case.

        Args:
            src_path (Optional[str]): The source path of the base case to be copied.
            dist_path (Optional[str]): The destination path where the new case will be created.
                   will be deleted by the function and base case folder will be copied to the folder being the same name
            dist_key (Optional[str]): The key for the destination path in the paths dictionary.
            mode (str): Defines how the copying procedure will be done.
                        'rewrite' mode will delete the existing folder at the destination path and copy the base case folder to the new path.
                        'copy' mode will rename the existing folder at the destination path with a prefix of the current time and copy the base case folder to the destination path.

        Returns:
            None
        """
        source = pl.Path(
            Priority.path(src_path, self.info[self.info_key]["paths"], path_key=src_key)
        )
        destination = pl.Path(
            Priority.path(dist_path, self.info[self.info_key]["paths"], path_key=dist_key)
        )
        Priority.check_path_existence(source, make_new=False)
        if mode == "rewrite":
            if Priority.check_path_existence_only(destination) == "full":
                self._remove_directory(destination, allowed_root=destination.parent)
            shutil.copytree(source, destination)
        elif mode == "copy":
            if Priority.check_path_existence_only(destination) == "full":
                old_name = destination.stem + "_old_" + strftime("%d-%m-%Y %H-%M")
                old_path = destination.parent / old_name
                if old_path.exists():
                    sleep(1)
                    old_name = destination.stem + "_old_" + strftime("%d-%m-%Y %H-%M-%S")
                    old_path = destination.parent / old_name
                    destination.rename(old_path)
                else:
                    destination.replace(old_path)
                shutil.copytree(source, destination)
            else:
                shutil.copytree(source, destination)
        else:
            raise ConfigurationError("mode must be either 'copy' or 'rewrite'")

    def create_folder(
        self,
        directory: str | None = None,
        dir_key: str | None = None,
        folder_name: str | None = None,
        name_key: str | None = None,
        rewrite: bool = False,
        info_key=None,
    ) -> None:
        """Creates a new folder.

        Args:
            directory (Optional[str]): The directory path where the new folder will be created.
            dir_key (Optional[str]): The key for the directory path in the paths dictionary.
            folder_name (Optional[str]): The name of the new folder to be created.
            name_key (Optional[str]): The key for the folder name in the case_names dictionary.
            rewrite (Optional[bool]): If True, the existing folder will be deleted and a new one will be created. Defaults to True.
            info_key (Optional[str]): The key for the information dictionary. Defaults to None.

        Returns:
            None
        """
        info_key = self.get_key(info_key)
        directory = Priority.path(directory, self.info[info_key]["paths"], path_key=dir_key)
        folder_name = Priority.name(
            folder_name, self.info[info_key]["case_names"], name_key=name_key
        )

        full_path = pl.Path(directory) / folder_name
        test = Priority.check_path_existence_only(full_path)
        if test == "full":
            if rewrite is True:
                self._remove_directory(full_path, allowed_root=pl.Path(directory))
                full_path.mkdir(parents=True)
            else:
                raise FileExistsError(f"Folder already exists: {full_path}")
        else:
            full_path.mkdir(parents=True)

    def create_folder_by_path(
        self,
        path: str | None = None,
        path_key: str | None = None,
        rewrite: bool = False,
    ) -> None:
        """Creates a new folder by the given path or path key.

        Args:
            path (Optional[str]): The path where the new folder will be created.
            path_key (Optional[str]): The key for the path in the paths dictionary.
            rewrite (Optional[bool]): If True, the existing folder will be deleted and a new one will be created. Defaults to True.

        Returns:
            None
        """
        target_path = pl.Path(
            Priority.path(path, self.info[self.info_key]["paths"], path_key=path_key)
        )
        test = Priority.check_path_existence_only(target_path)
        if test == "full":
            if rewrite is True:
                self._remove_directory(target_path, allowed_root=target_path.parent)
                target_path.mkdir(parents=True)
            else:
                raise FileExistsError(f"Folder already exists: {target_path}")
        else:
            target_path.mkdir(parents=True)

    def delete_folders_by_words(
        self,
        words: Iterable | str,
        directory: str | None = None,
        dir_key: str | None = None,
    ) -> None:
        if isinstance(words, Iterable) and not isinstance(words, str):
            for word in words:
                folder_paths = self.find_folders_by_word(word, directory=directory, dir_key=dir_key)
                self.delete_folders(folder_paths[1], directory=directory, dir_key=dir_key)
        else:
            folder_paths = self.find_folders_by_word(words, directory=directory, dir_key=dir_key)
            self.delete_folders(folder_paths[1], directory=directory, dir_key=dir_key)

    def delete_folders(
        self,
        folders: Iterable[str | pl.Path] | None = None,
        directory: str | None = None,
        dir_key: str | None = None,
    ) -> None:
        """Deletes specified folders.

        Args:
            folders (Optional[list[str]]): A list of folder names to be deleted.
            directory (Optional[str]): The directory path where the folders are located.
            dir_key (Optional[str]): The key for the directory path in the paths dictionary.

        Returns:
            None
        """

        directory_root = pl.Path(
            Priority.path(directory, self.info[self.info_key]["paths"], path_key=dir_key)
        ).resolve()
        if folders is None:
            raise ValueError("folders must be provided")

        for folder_name in folders:
            candidate = pl.Path(folder_name)
            folder_path = candidate if candidate.is_absolute() else directory_root / candidate
            folder_path = folder_path.resolve()
            if folder_path.exists() and folder_path.is_dir():
                self._remove_directory(folder_path, allowed_root=directory_root)

    def find_folders_by_word(
        self,
        word: str,
        directory: str | None = None,
        dir_key: str | None = None,
    ) -> tuple[list[pl.Path], list[str]]:
        """
        Finds folders in a directory that contain a specific word in their name.

        Args:
            word (str): The word to search for in folder names.
            directory (Optional[str]): The directory path to search in. Defaults to None.
            dir_key (Optional[str]): The key for the directory path in the paths dictionary. Defaults to None.

        Returns:
            tuple: A tuple containing two lists:
                - full_find_path (list): List of full paths to folders containing the word.
                - name_find_file (list): List of folder names containing the word.
        """
        directory_path = pl.Path(
            Priority.path(directory, self.info[self.info_key]["paths"], path_key=dir_key)
        )
        if not directory_path.is_dir():
            raise FileNotFoundError(f"Directory does not exist: {directory_path}")
        if not isinstance(word, str):
            raise TypeError("word must be a string")

        full_find_path = sorted(
            folder for folder in directory_path.iterdir() if folder.is_dir() and word in folder.name
        )
        name_find_file = [folder.name for folder in full_find_path]
        return full_find_path, name_find_file

    @staticmethod
    def _remove_directory(path: pl.Path, *, allowed_root: pl.Path) -> None:
        """Remove a directory only when it is a strict child of ``allowed_root``."""
        target = path.expanduser().resolve()
        root = allowed_root.expanduser().resolve()
        if target == root or not target.is_relative_to(root):
            raise UnsafePathError(f"Refusing to delete path outside {root}: {target}")
        if target.is_symlink():
            raise UnsafePathError(f"Refusing to recursively delete symlink: {target}")
        shutil.rmtree(target)

    @staticmethod
    def change_json_params(
        parameters_path: str,
        changed_parameters: dict,
        save_path: str | pl.Path | None = None,
    ):
        parameters = Files.open_json(parameters_path)
        parameters.update(changed_parameters)
        if save_path is None:
            save_path = parameters_path
        Files.save_json(parameters, str(save_path))

    @staticmethod
    def create_json_params(*parameter_dict: dict, save_path: str | None = None):
        """
        The function creates new json file with parameters and save it in save_path.
        Args:
            *parameter_dict: a number of dictionaries consist of  parameter names as keys and values of parameters as
                                values of the key.
            save_path:      the path in which json file will save.

        Returns:

        """
        collect_dict = dict()
        for dict_i in parameter_dict:
            collect_dict.update(dict_i)

        if save_path is None:
            raise ValueError("save_path must be provided")
        Files.save_json(collect_dict, save_path)

    @staticmethod
    def get_dict_from_json(parameters_path):
        return Files.open_json(parameters_path)

    def __str__(self):
        representation_stirng = ""
        for key, val_info in self.info.items():
            representation_stirng += f"Information of {key} \n"
            for key, data in val_info.items():
                representation_stirng += f"{key} :\n"
                for sub_key, sub_data in data.items():
                    representation_stirng += f"{sub_key} : {sub_data}:\n"
        return representation_stirng

    def __repr__(self):
        representation_stirng = ""
        for key, val_info in self.info.items():
            representation_stirng += f"Information of {key} \n"
            for key, data in val_info.items():
                representation_stirng += f"{key} :\n"
                for sub_key, sub_data in data.items():
                    representation_stirng += f"{sub_key} : {sub_data}:\n"

        return representation_stirng
