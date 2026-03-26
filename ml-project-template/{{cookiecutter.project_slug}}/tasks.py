"""
Invoke tasks for {{ cookiecutter.project_name }}.

Tasks are organized into namespaces:
- core:    Environment setup (bootstrap, sync, setup-dev)
- data:    Data management (download, preprocess, stats)
- train:   Training and evaluation (train, evaluate{% if cookiecutter.use_wandb == "yes" %}, sweep{% endif %})
- quality: Code quality (ruff, test, ci, security-check)
{%- if cookiecutter.use_docker == "yes" %}
- docker:  Docker operations (build, run, clean)
{%- endif %}
- utils:   Utilities (clean-all, env-info, check-gpu)

Usage:
    invoke <namespace>.<task> [options]

Examples:
    invoke core.setup-dev
    invoke train.train
    invoke quality.ci
"""

import importlib.util
from pathlib import Path

from invoke import Collection


def load_module_from_file(module_name, file_path):
    """Load a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


tasks_dir = Path(__file__).parent / "tasks"

core = load_module_from_file("core", tasks_dir / "core.py")
data = load_module_from_file("data", tasks_dir / "data.py")
train = load_module_from_file("train", tasks_dir / "train.py")
quality = load_module_from_file("quality", tasks_dir / "quality.py")
utils = load_module_from_file("utils", tasks_dir / "utils.py")
{% if cookiecutter.use_docker == "yes" -%}
docker = load_module_from_file("docker", tasks_dir / "docker.py")
{% endif %}

namespace = Collection()
namespace.add_collection(Collection.from_module(core), name="core")
namespace.add_collection(Collection.from_module(data), name="data")
namespace.add_collection(Collection.from_module(train), name="train")
namespace.add_collection(Collection.from_module(quality), name="quality")
namespace.add_collection(Collection.from_module(utils), name="utils")
{% if cookiecutter.use_docker == "yes" -%}
namespace.add_collection(Collection.from_module(docker), name="docker")
{% endif %}
