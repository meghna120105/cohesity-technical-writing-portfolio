# Troubleshooting Guide: Windows, Python, VS Code and Git

## 1. Introduction

This guide explains how to identify and solve common technical problems when working with Python projects, Visual Studio Code, PowerShell, and Git on Windows.

It is designed for beginners who are learning programming and documentation automation.

## 2. Python Errors

### Issue 1: Python is not recognized

**Error message:**

`python is not recognized as an internal or external command`

**Possible cause:**

Python may not be installed, or its installation directory may not be added to the Windows PATH environment variable.

**Solution:**

1. Open PowerShell.
2. Run:

   `python --version`

3. If that does not work, try:

   `py --version`

4. If neither command works, install Python from the official Python website.
5. During installation, select the option to add Python to PATH.
6. Restart VS Code and check again.

### Issue 2: Module not found

**Error message:**

`ModuleNotFoundError: No module named 'package_name'`

**Possible cause:**

The required Python package may not be installed in the active Python environment.

**Solution:**

1. Open the VS Code terminal.
2. Activate the correct virtual environment, if one is being used.
3. Install the missing package:

   `python -m pip install package_name`

4. Run the program again.

### Issue 3: Python indentation error

**Error message:**

`IndentationError: unexpected indent`

**Possible cause:**

Python uses indentation to identify code blocks. Incorrect spacing can cause this error.

**Solution:**

1. Open the Python file in VS Code.
2. Locate the line mentioned in the error.
3. Check the indentation.
4. Use consistent indentation, preferably four spaces.
5. Save and run the program again.

## 3. PowerShell Errors

### Issue 4: Virtual environment activation fails

**Error message:**

`Activate.ps1 cannot be loaded because running scripts is disabled on this system.`

**Possible cause:**

PowerShell execution policies may prevent activation scripts from running.

**Solution:**

You can temporarily allow script execution for the current PowerShell session:

`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

Then activate the virtual environment:

`.\.venv\Scripts\Activate.ps1`

This change applies only to the current PowerShell process.

### Issue 5: Command is not recognized

**Possible cause:**

The command may be incorrect, or the required program may not be installed.

**Solution:**

1. Check the spelling of the command.
2. Verify that the required application is installed.
3. Check whether its location is added to PATH.
4. Restart the terminal and try again.

## 4. VS Code Errors

### Issue 6: Python file does not run

**Possible cause:**

VS Code may be using the wrong Python interpreter.

**Solution:**

1. Open the Command Palette using `Ctrl + Shift + P`.
2. Search for `Python: Select Interpreter`.
3. Select the Python interpreter associated with your project.
4. Open a new terminal.
5. Run the Python file again.

### Issue 7: Terminal opens in the wrong folder

**Possible cause:**

The terminal may not be pointing to the project directory.

**Solution:**

Use the `cd` command to navigate to your project folder.

Example:

`cd C:\Users\YourName\cohesity-technical-writing-portfolio`

Replace the example path with your actual project location.

## 5. Git and GitHub Errors

### Issue 8: Git is not recognized

**Error message:**

`git is not recognized as an internal or external command`

**Possible cause:**

Git may not be installed or may not be available in the PATH.

**Solution:**

1. Install Git for Windows.
2. Restart VS Code.
3. Open a new terminal.
4. Run:

   `git --version`

### Issue 9: Git push fails because there is no upstream branch

**Possible cause:**

The local branch may not yet be connected to a remote branch.

**Solution:**

Run:

`git push -u origin branch-name`

Replace `branch-name` with the actual name of your current branch.

### Issue 10: Git reports uncommitted changes

**Possible cause:**

Some files have been modified but not committed.

**Solution:**

1. Check the changed files:

   `git status`

2. Stage the required files:

   `git add .`

3. Create a commit:

   `git commit -m "Update documentation"`

4. Push the changes:

   `git push`

### Issue 11: Merge conflict

**Possible cause:**

Two different changes have been made to the same part of a file.

**Solution:**

1. Open the file showing the conflict.
2. Find the conflict markers.
3. Review both versions.
4. Decide which changes should be kept.
5. Remove the conflict markers.
6. Save the file.
7. Stage and commit the resolved changes.

Do not remove changes without reviewing them.

## 6. Markdown Documentation Errors

### Issue 12: Markdown headings do not display correctly

**Possible cause:**

The required space after the heading symbol may be missing.

**Incorrect:**

`#Introduction`

**Correct:**

`# Introduction`

**Solution:**

Add a space after the Markdown heading symbol.

### Issue 13: Links do not open

**Possible cause:**

The link address may be incorrect, or the linked file may have been moved or deleted.

**Solution:**

1. Check the link destination.
2. Verify that the target file exists.
3. Check the relative file path.
4. Update the link if necessary.

## 7. General Troubleshooting Best Practices

- Read the complete error message before making changes.
- Check file names and paths carefully.
- Verify that the correct Python environment is selected.
- Keep software and dependencies updated.
- Save important changes before modifying files.
- Use Git to maintain a history of changes.
- Test solutions before documenting them.
- Avoid sharing passwords, API keys, or confidential information.

## 8. Conclusion

Troubleshooting is an important skill in software development and technical writing.

A good troubleshooting guide helps users understand problems, identify possible causes, and follow clear instructions to resolve them.

Technical writers should ensure that every solution is accurate, easy to understand, and tested before it is published.