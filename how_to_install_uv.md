To install uv, the recommended approach is to use the official standalone installer. 

Because uv is written in Rust, it downloads as a fast, self-contained binary—meaning you do not even need Python installed on your computer first. 

uv can download and manage Python versions for you later. [1, 2, 3] 

Choose the terminal command that matches your operating system:
## 1. The Official Standalone Method (Recommended)
Open your computer's terminal and paste the appropriate command: [1] 


* macOS / Linux:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```
* Windows (PowerShell):
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```


⚠️ Important Step: After the installer finishes, close your terminal window and open a brand new one. This forces the terminal to refresh its system path (PATH) and realize that the new uv command is ready to use. [1] 


## 2. Alternative Methods (Package Managers)
If you prefer managing your system apps through traditional package managers, you can use these instead: [1, 4] 

 
* macOS (Homebrew):
```
brew install uv
```
* Windows (WinGet):
```
winget install --id=astral-sh.uv -e
```
* Any System (via pip): If you already have standard Python installed globally, you can download it like a normal library:
```
pip install uv
```


## 3. Verify the Installation
To confirm that everything was configured correctly, type this command into your new terminal window: [1] 
```
uv --version
```
If installed correctly, it will instantly print out your active version number (e.g., uv 0.12.17). [1, 6] 
## What to do next?
Now that uv is installed, you can create a brand new Python project instantly by navigating to an empty folder and running: [7] 
```
uv init
```
This single step handles everything—it writes a starter script, sets up configuration files, and initializes a local .venv environment for you automatically. [7] 

Would you like help with initializing your first project using uv, or would you like to see how to download a specific version of Python (like Python 3.12 or 3.13) directly through uv?
