import os
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s:')

def create_project_structure(base_path='.'):
    """
    Create the project structure
    """

    folders = [
        'data/raw',
        'data/Feature_Store',
        'notebooks',
        'src/data',
        'src/features',
        'src/training',
        'src/visualization',
        'src/utils',
        'src/inference',
        'src/logging',
        'src/config',
        'src/exceptions',
        'tests',
        'models',
        'reports',
        'logs',
         'utils' ]
    
    # Create the folders (only if they don't exist)
    for folder in folders:
        folder_path = Path(base_path) / folder
        if not folder_path.exists():
            os.makedirs(folder_path, exist_ok=True)
            logging.info(f"Created folder: {folder_path}")
        else:
            logging.info(f"Folder already exists: {folder_path}")

    #create empty files (optional)
    files = [
        '.env', 
        'src/__init__.py',
        'src/data/__init__.py',
        'src/features/__init__.py',
        'src/training/__init__.py',
        'src/visualization/__init__.py',
        'src/utils/__init__.py',
        'src/inference/__init__.py',
        'src/logging/__init__.py',
        'src/config/__init__.py',
        'src/exceptions/__init__.py',
        'tests/__init__.py' ,
        'utils/__init__.py',
        'Dockerfile'   
    ]

    for file in files:
        file_path = Path(base_path) / file
        if not file_path.exists():
            with open(file_path, 'w') as f:
                logging.info(f"Created file: {file_path}")
        else:
            logging.info(f"File already exists: {file_path}")

    # Elements to add to .gitignore
    gitignore_content = """#Ignore data and logs folders
data/
logs/
.env

# Ignore Python cache and virtual environments
__pycache__/
*.py[cod]
*$py.class
.Python
env/
venv/
.venv
ENV/
env.bak/
venv.bak/

# Ignore IDE-specific files
.idea/
.vscode/
*.swp
*.swo

# Ignore system files
.DS_Store
Thumbs.db
"""

    # Create or update .gitignore file
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content.strip())
        logging.info(f"Created .gitignore file with default content")
    else:
        logging.info(f".gitignore already exists")

if __name__ == '__main__':
    create_project_structure()