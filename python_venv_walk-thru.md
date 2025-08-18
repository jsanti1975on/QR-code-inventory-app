# 🐍 Python Virtual Environment Walkthrough

## 1. What is a virtual environment?

>💡 Imagine your computer as a house. Each Python project lives in its own room.
> A virtual environment (venv) is like giving each project its own toolbox of Python packages, so projects don’t fight over versions.

## 2. Check Python is installed

```Bash
Run:
python3 --version
```

**Expected output (something like):**
```Bash
Python 3.10.12
```

## 3. Create a project folder
```Bash
mkdir ~/practice
cd ~/practice
```

## 4. Create the virtual environment
```Bash
python3 -m venv venv
```

> This makes a folder called venv/ that contains its own Python and its own pip.

## 5. Activate the environment
```Bash
source venv/bin/activate
```

### When it works, your shell prompt will show:

```Bash
(venv) username@hostname:~/practice$
```

> The (venv) means you’re inside the toolbox for this project.

## 6. Install requirements

> This project has a file requirements.txt:
> FLASK==2.3.3
> The above syntax shows the only line in the requirments.txt file
> Install it: *pip install -r requirements.txt*
> Check what’s installed:
> *pip list*
> You should see Flask in the list.

## 7. Run the app

> *python app.py* 
> It will start up:
> *Running on http://0.0.0.0:5000*
> Open in browser:
> *http://localhost:5000*

## 8. Deactivate the environment

> When done, exit the toolbox:
> *deactivate*
> Prompt goes back to normal — you’re now in your system Python, not the project’s.


# 9. Why bother with venv?

> Keeps each project’s dependencies separate
> Prevents version conflicts (Project A can use Flask 2.3, Project B Flask 1.1)
> Easy to remove (just delete the venv/ folder)


# 10. Extra: Common issues

> If you forget to activate venv:
> You’ll be using system Python
> pip may install packages globally (bad practice) 
> Easy fix: *source venv/bin/activate*

# That’s the full life cycle of a virtual environment:

> create → activate → install → run → deactivate.
