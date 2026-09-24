In PyCharm 2025, JetBrains changed how uv integration works. You no longer change a global dropdown setting from "pip" to "uv" inside the Python Packages window. Instead, PyCharm binds the package manager directly to the type of Python Interpreter you select for the project. [1, 2, 3] 
If your project interpreter is configured as a standard virtualenv, PyCharm defaults to pip. To switch PyCharm's default package management system entirely over to uv, you must re-add the local environment explicitly as a uv environment. [2, 3, 4] 
## How to Switch Package Management to uv

   1. Open PyCharm Settings:
   * 🖥️ Windows / Linux: Go to File -> Settings (or press Ctrl + Alt + S).
      * 🍏 macOS: Go to PyCharm -> Settings (or press Cmd + ,). [4] 
   2. In the left sidebar, navigate to Project: <your_project_name> -> Python Interpreter. [4] 
   3. Click the Add Interpreter dropdown button at the top-right, and select Add Local Interpreter... [3, 4] 
   4. In the left panel of the popup window, select uv from the list of environment types. (Do not click Virtualenv). [3, 4] 
   5. Under the configuration options, select Existing environment. [3] 
   6. PyCharm will automatically locate your system's uv executable and find the .venv folder in your project root. If it doesn't, manually point the Path to uv to your uv binary. [3, 4] 
   7. Click OK. [3, 4] 


## What Changes After Doing This?
Once PyCharm registers the environment specifically as a uv environment rather than a generic virtual environment, the IDE updates its interface behaviors: [1] 

* 
* The "Python Packages" Tool Window: When you search for and click "Install" on packages here, PyCharm will invisibly run uv add or uv pip install instead of traditional pip. [2, 5] 
* Missing Package Popups: If you open a Python script with an unresolved import, PyCharm's yellow warning banner will offer to fix it by running a uv command to sync your pyproject.toml file automatically. [1] 
* 

Are you working on a project that uses a standard pyproject.toml file, or are you managing packages via a requirements.txt file? Let me know so I can ensure PyCharm triggers the exact uv command structure you prefer.
