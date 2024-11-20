import os
import subprocess

# List of folders to create
folders = ["artifacts", "code", "data", "sql"]

# Create each folder and add a .gitkeep file
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, '.gitkeep'), 'w') as f:
        pass
    print(f"Folder '{folder}' and '.gitkeep' created.")