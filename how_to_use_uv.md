Using uv is incredibly simple because it automates the tedious steps of traditional Python setups. You do not need to manually manage virtual environments, install Python versions separately, or continuously activate sandboxes. [1, 2] 

The tool divides day-to-day Python tasks into three clear workflows: [3] 

## Workflow 1: Managing a Project (Most Common)
When you are building a specific application or data science script, uv tracks everything seamlessly inside your pyproject.toml file. [1, 2] 
### 1. Initialize a new project
Navigate to an empty directory on your computer and run:
```
uv init my-project
cd my-project
```
This automatically sets up a project structure, a baseline pyproject.toml, and a sample hello.py file. [4, 5] 
### 2. Add dependencies
To install libraries (like pandas or requests), run uv add: [1, 6] 
```
uv add pandas requests
```


* What happens behind the scenes: uv instantly checks if you have a local .venv environment. If you don't, it creates one. It then downloads the libraries, saves them into .venv, and automatically logs them in your pyproject.toml. [1, 2] 


### 3. Run your code
Instead of manually typing source .venv/bin/activate every time you open a terminal, let uv handle execution dynamically: [2, 7] 
```
uv run hello.py
```
This forces Python to safely execute your code inside the project's sandboxed environment without any manual activation required. [7] 

## Workflow 2: Managing Python Versions
Because uv can handle raw Python distributions, you do not need to download Python from a website installer or use external version tools. [5, 8, 9] 

* Install the latest Python:
```
uv python install
```
* Install a specific version (e.g., Python 3.12):
```
uv python install 3.12
```
* Pin a project to a specific version: If a project specifically requires a legacy runtime, run:
```
uv init --python 3.11
```
uv will lock that project to Python 3.11, automatically downloading it if your machine doesn't have it yet. [8, 10, 11] 



## Workflow 3: Running Global Tools (uvx)
If you want to run a standalone Python tool (like the ruff linter, a code formatter, or the Jupyter interface) without cluttering your local project environment, use uvx (or uv tool run). [1, 3] 
```
uvx jupyter lab
```
This tells uv to pull down Jupyter into a temporary, isolated global cache, run it instantly, and tear it down cleanly when you close the browser—leaving zero footprint on your project files. [1] 

## Summary Cheat Sheet

| Intent | Command | Traditional Alternative |
|---|---|---|
| Create project | uv init | Manual folder creation |
| Download package | uv add <package> | pip install + manual text updates |
| Execute code | uv run <script> | source activate + python <script> |
| Pull down Python | uv python install <version> | Installing from Python.org or Homebrew |
| Run temporary tools | uvx <tool> | pipx run <tool> |

Would you like to initialize your very first project folder using uv right now, or are you ready to configure VS Code to automatically read your newly created uv environment?
