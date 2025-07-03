
import os

project_structure = {
    "FinSentinel": [
        "app/__init__.py",
        "app/models.py",
        "app/api.py",
        "app/rules.py",
        "app/dashboard.py",
        "app/client_profiles.py",
        "data/",
        "requirements.txt",
        "main.py"
    ]
}

def create_project(structure):
    for base, files in structure.items():
        os.makedirs(base, exist_ok=True)
        for file in files:
            file_path = os.path.join(base, file)
            if file.endswith("/"):
                os.makedirs(file_path, exist_ok=True)
            else:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                open(file_path, "a").close()  # create empty file

create_project(project_structure)
print("Project structure created.")
