import json
import sys

import dotenv
import prettytable
import pyttsx3

from prettytable import PrettyTable

# Load Text to Speech module.
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# Load configuration file.
config = dotenv.dotenv_values(dotenv_path="../config.env")


def speak(sentence: str):
    engine.say(sentence)
    engine.runAndWait()


class ToDoList:
    def __init__(self):
        self.todolist_file = config["TODOLIST_FILE"]
        self.todolist_category_file = config["TODOLIST_CATEGORY_FILE"]

    def categories(self) -> PrettyTable or str:
        """
        Read the list of categories file in assets.

        Returns
        -------
        PrettyTable -> a whole table, to display the table use print()
        str -> This can be string as well, but I don't know.
        """
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

    def create_category(self, name: str, description: str) -> bool or None:
        """
        Add new Category

        Parameters
        ----------
        name: str - Name of the category.
        description: str - Description of the category.

        Returns
        -------
        True - if the category was added successfully
        False = if the category already exists.
        """
        form: dict = {
            "category_name": name,
            "category_description": description
        }

        if self.does_category_exist(name):
            speak("Category already exists.")
            return

        # Read and assign the file to the 'categories' variable.
        with open(self.todolist_category_file) as cfile:
            try:
                categories = json.load(cfile)
            except json.JSONDecodeError:
                print(f"You have a problem in your json file ({self.todolist_category_file})")
                sys.exit(1)

        # Append the data
        categories.append(form)

        # Save the file
        with open(self.todolist_category_file, "w") as cfile:
            if json.dump(categories, cfile, indent=2, separators=(",", ": ")):
                speak("Category was saved successfully.")
                return True
            else:
                return False

# todolist = ToDoList()
# todolist.create_category("test", "test description")
