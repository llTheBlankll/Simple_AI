import json
import dotenv
import prettytable

config = dotenv.dotenv_values(dotenv_path="../config.env")

class ToDoList:
    def __init__(self):
        self.todolist_file = config["TODOLIST_FILE"]
        self.todolist_category_file = config["TODOLIST_CATEGORY_FILE"]

    def categories(self) -> str:
        categories_table = prettytable.PrettyTable(field_names=["Category Name", "Description"], title="Categories")
        with open(self.todolist_category_file) as cfile:
            categories: dict = json.load(cfile)
            for dictionary in categories:
                categories_table.add_row([dictionary["category_name"], dictionary["category_description"]])

        return categories_table

    def does_category_exist(self, name):
        """
        Check if the category exist in the json file (todolist_category_file.json).

        Parameters
        ----------
        name - name of the category to check if it exists in the file.

        Returns
        -------
        True - if the category exists.
        False - if the category doesn't exist.
        """
        with open(self.todolist_category_file) as cfile:
            for dictionary in json.load(cfile):
                if dictionary["category_name"] == name:
                    return True
        return False


todolist = ToDoList()
print(todolist.categories())
