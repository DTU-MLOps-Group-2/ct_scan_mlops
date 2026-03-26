"""Post-generation hook to clean up files based on cookiecutter choices."""

import os
import shutil


def remove_file(filepath):
    """Remove a file if it exists."""
    if os.path.exists(filepath):
        os.remove(filepath)


def remove_dir(dirpath):
    """Remove a directory if it exists."""
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)


# Remove Docker files if not using Docker
if "{{ cookiecutter.use_docker }}" != "yes":
    remove_dir("dockerfiles")
    remove_file("tasks/docker.py")
    remove_file(".github/workflows/docker.yaml")

# Remove DVC references if not using DVC
if "{{ cookiecutter.use_dvc }}" != "yes":
    pass  # DVC tasks are inline in data.py, handled by Jinja conditionals

# Remove sweep config if not using W&B
if "{{ cookiecutter.use_wandb }}" != "yes":
    remove_dir("configs/sweeps")

# Remove GitHub Actions if not requested
if "{{ cookiecutter.use_github_actions }}" != "yes":
    remove_dir(".github")

# Remove API file if not using FastAPI
if "{{ cookiecutter.use_fastapi }}" != "yes":
    remove_file("src/{{ cookiecutter.project_slug }}/api.py")

# Initialize git repo
os.system("git init")
os.system("git add .")
os.system('git commit -m "Initial project from ml-project-template"')

print("")
print("=" * 60)
print("Project {{ cookiecutter.project_name }} created!")
print("=" * 60)
print("")
print("Next steps:")
print("  cd {{ cookiecutter.project_slug }}")
print("  invoke core.setup-dev")
print("  source .venv/bin/activate")
print("")
