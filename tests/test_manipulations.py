import unittest
import os
import shutil
import pathlib as pl
from pyRunOF.modules.manipulations import ModelConfigurator
from pyRunOF.additional_fun.auxiliary_functions import Priority, Files
from pyRunOF.additional_fun.information import Information

class TestModelConfigurator(unittest.TestCase):

    def setUp(self):
        self.test_dir = pl.Path("test_dir")
        self.test_dir.mkdir(exist_ok=True)
        self.src_dir = self.test_dir / "src_case"
        self.src_dir.mkdir(exist_ok=True)
        self.dist_dir = self.test_dir / "dist_case"
        self.info = {
            "general": {
                "paths": {
                    "src": str(self.src_dir),
                    "dist": str(self.dist_dir)
                },
                "case_names": {}
            }
        }
        self.configurator = ModelConfigurator(info=self.info)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_duplicate_case_copy_mode(self):
        (self.src_dir / "test_file.txt").write_text("This is a test file.")
        self.configurator.duplicate_case(src_key="src", dist_key="dist", mode="copy")
        self.assertTrue((self.dist_dir / "test_file.txt").exists())

    def test_duplicate_case_rewrite_mode(self):
        (self.src_dir / "test_file.txt").write_text("This is a test file.")
        self.dist_dir.mkdir(exist_ok=True)
        self.configurator.duplicate_case(src_key="src", dist_key="dist", mode="rewrite")
        self.assertTrue((self.dist_dir / "test_file.txt").exists())

    def test_create_folder(self):
        new_folder_name = "new_folder"
        self.configurator.create_folder(directory=str(self.test_dir), folder_name=new_folder_name)
        self.assertTrue((self.test_dir / new_folder_name).exists())

    def test_create_folder_by_path(self):
        new_folder_path = self.test_dir / "new_folder_by_path"
        self.configurator.create_folder_by_path(path=str(new_folder_path))
        self.assertTrue(new_folder_path.exists())

    def test_delete_cases_by_full_paths(self):
        folder_to_delete = self.test_dir / "folder_to_delete"
        folder_to_delete.mkdir(exist_ok=True)
        self.configurator.delete_cases(full_paths=[str(folder_to_delete)])
        self.assertFalse(folder_to_delete.exists())

    def test_delete_cases_by_words(self):
        folder_to_delete = self.test_dir / "folder_to_delete"
        folder_to_delete.mkdir(exist_ok=True)
        self.configurator.delete_cases(words=["folder_to_delete"], directory=str(self.test_dir))
        self.assertFalse(folder_to_delete.exists())

    def test_find_folders_by_word(self):
        folder_to_find = self.test_dir / "folder_to_find"
        folder_to_find.mkdir(exist_ok=True)
        found_folders, _ = self.configurator.find_folders_by_word(word="folder_to_find", directory=str(self.test_dir))
        self.assertIn(folder_to_find, found_folders)

    def test_change_json_params(self):
        test_json_path = self.test_dir / "test.json"
        Files.save_json({"param1": "value1"}, test_json_path)
        self.configurator.change_json_params(parameters_path=str(test_json_path), changed_parameters={"param2": "value2"})
        updated_params = Files.open_json(test_json_path)
        self.assertIn("param2", updated_params)

    def test_create_json_params(self):
        test_json_path = self.test_dir / "test_create.json"
        self.configurator.create_json_params({"param1": "value1"}, save_path=str(test_json_path))
        created_params = Files.open_json(test_json_path)
        self.assertIn("param1", created_params)

    def test_get_dict_from_json(self):
        test_json_path = self.test_dir / "test_get.json"
        Files.save_json({"param1": "value1"}, test_json_path)
        params = self.configurator.get_dict_from_json(parameters_path=str(test_json_path))
        self.assertIn("param1", params)

if __name__ == "__main__":
    unittest.main()