import os

class ContextCreator:
    def __init__(self):
        self.contents = []

    def add_file(self, file_path):
        with open(file_path, 'r') as file:
            self.contents.append(file_path + "\n")
            self.contents.append(file.read())

    def add_folder(self, folder_path):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                self.add_file(file_path)

    def get_contents(self):
        return "\n".join(self.contents)
