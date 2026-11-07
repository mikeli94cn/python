# How to Install Python on Ubuntu

Python is a popular programming language used for **automation, web scraping, backend development, data analysis, and artificial intelligence**.

Since you are learning Java backend development and are also interested in browser automation with Playwright, I recommend installing **Python 3, pip, and venv** on Ubuntu.

Unlike Java, Python is usually preinstalled on Ubuntu. However, you may need to install additional development tools.

## 1. Check whether Python is already installed

Open a terminal (`Ctrl + Alt + T`) and execute:

```bash
python3 --version
```

Example output:

```text
Python 3.12.3
```

If you see a version number, Python is already installed.

You can also check its location:

```bash
which python3
```

Typical output:

```text
/usr/bin/python3
```

**Important:** On modern Ubuntu, the standard command is `python3`, not necessarily `python`.

---

## 2. Install Python 3 (Recommended)

Ubuntu provides Python through its APT package manager.

### Step 1: Update the package index

```bash
sudo apt update
```

### Step 2: Install Python

```bash
sudo apt install python3
```

This installs Ubuntu's default Python 3 version if it is not already installed.

### Step 3: Install additional development tools

I recommend installing these packages:

```bash
sudo apt install python3-pip python3-venv python3-dev
```

Their purposes are:

| Package | Purpose |
|---|---|
| `python3` | Python interpreter |
| `python3-pip` | Python package installer |
| `python3-venv` | Creates isolated Python environments |
| `python3-dev` | Development headers for compiling Python extensions |

For your automation projects, the first three packages are particularly useful.

### Step 4: Verify installation

Check Python:

```bash
python3 --version
```

Check pip:

```bash
python3 -m pip --version
```

Expected output will resemble:

```text
pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.12)
```

The exact version depends on your Ubuntu release.

---

## 3. Understand Python vs pip vs venv

These three tools have different responsibilities.

| Tool | Purpose | Similar concept in Java |
|---|---|---|
| Python | Executes Python programs | Java runtime |
| pip | Installs Python libraries | Maven dependency management |
| venv | Creates isolated Python environments | Project-specific dependency environments |

For example, suppose you develop two projects:

```text
Python Projects
│
├── Project A: Web Scraping
│   ├── Python
│   ├── requests
│   └── beautifulsoup4
│
└── Project B: Browser Automation
    ├── Python
    └── playwright
```

Each project may need different library versions.

Using `venv`, you can keep their dependencies separate.

This is particularly useful when working on multiple Python projects.

---

## 4. Create a Python Virtual Environment (Important)

On modern Ubuntu versions, installing third-party packages directly into the system Python environment is generally discouraged.

Ubuntu protects its system-managed Python environment to prevent conflicts with operating-system packages.

**The recommended solution is to use `venv`.**

### Step 1: Create a project directory

```bash
mkdir -p ~/PythonProjects/hello-python
```

Enter the directory:

```bash
cd ~/PythonProjects/hello-python
```

### Step 2: Create a virtual environment

```bash
python3 -m venv .venv
```

This creates a directory:

```text
hello-python/
└── .venv/
    ├── bin/
    ├── include/
    ├── lib/
    └── pyvenv.cfg
```

The `.venv` directory contains an isolated Python environment.

### Step 3: Activate the virtual environment

```bash
source .venv/bin/activate
```

Your terminal prompt should change:

```text
(.venv) user@ubuntu:~/PythonProjects/hello-python$
```

Now you can use:

```bash
python --version
```

And:

```bash
pip --version
```

Notice that inside the virtual environment, you can normally use `python` instead of `python3`.

### Step 4: Install Python libraries

For example:

```bash
pip install requests
```

This installs the `requests` library inside your virtual environment.

You can check installed packages:

```bash
pip list
```

### Step 5: Deactivate the environment

When finished:

```bash
deactivate
```

Your terminal returns to the normal system environment.

**Recommendation:** Create a separate `.venv` for each Python project.

---

## 5. Test Python with a Hello World program

Create a Python file:

```bash
nano hello.py
```

Enter:

```python
print("Hello, Ubuntu!")

name = input("What is your name? ")

print(f"Hello, {name}! Welcome to Python.")
```

Save the file and execute:

```bash
python3 hello.py
```

Example output:

```text
Hello, Ubuntu!
What is your name? Mike
Hello, Mike! Welcome to Python.
```

Unlike Java, Python does not require a separate compilation command such as `javac`.

You can also start Python's interactive interpreter:

```bash
python3
```

Try:

```python
>>> 10 + 20
30

>>> print("Hello Python")
Hello Python
```

Exit with:

```python
exit()
```

---

## 6. Install multiple Python versions (Optional)

You may eventually need different Python versions for different projects.

For example:

```text
Project A → Python 3.12
Project B → Python 3.13
Project C → Python 3.14
```

A useful tool for managing multiple versions is **pyenv**.

The distinction is:

- `pyenv` manages Python interpreter versions.
- `venv` manages isolated environments and dependencies for individual projects.

You can use both together.

Ubuntu's official documentation explains how to install and configure pyenv without modifying the system Python installation. [Ubuntu](https://ubuntu.com/developers/docs/howto/python-setup/?utm_source=chatgpt.com)

**Important:** Do not remove or replace Ubuntu's system Python. Some operating-system utilities depend on it.

---

## 7. My recommendation for your Ubuntu development environment

For your Java backend learning and Python automation projects, I recommend:

| Purpose | Software |
|---|---|
| Java development | OpenJDK 21 |
| Python development | Ubuntu's default Python 3 |
| Python package management | pip |
| Python virtual environments | venv |
| Java IDE | IntelliJ IDEA |
| Python IDE | VS Code or PyCharm |
| Browser automation | Playwright |
| HTTP requests | requests |
| HTML parsing | Beautiful Soup |

For a complete Python development installation, you can also use Ubuntu's `python3-full` package:

```bash
sudo apt update
sudo apt install python3-full python3-pip python3-dev
```

This is consistent with [Ubuntu's official Python setup guide](https://ubuntu.com/developers/docs/howto/python-setup/?utm_source=chatgpt.com).

### Next step: Install Playwright

Once you have Python working, you can create a browser automation project:

```bash
mkdir -p ~/PythonProjects/browser-automation
cd ~/PythonProjects/browser-automation

python3 -m venv .venv
source .venv/bin/activate

python -m pip install playwright
python -m playwright install chromium
```

This prepares Python Playwright and downloads its Chromium browser. Depending on your Ubuntu installation, additional browser system dependencies may be needed.

You can then begin writing scripts to automate browser interactions.

**My suggestion:** Start with Python 3 + pip + venv. You do not need pyenv immediately. Learn it later when a project requires a different Python version.
