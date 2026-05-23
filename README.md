# Event Search Agent - Project Setup Guide

This document provides a step-by-step guide to set up the event-search-agent project environment using Visual Studio Code and Python virtual environments.

## Step 0: Create Project Folder

Create a folder named "event-search-agent" on your local machine.

## Step 1: Open the Project in VS Code

Launch Visual Studio Code and navigate to File → Open Folder.

Select the "event-search-agent" folder.

## Step 2: Create the Project Folder Structure

Inside the project workspace, create the folder structure as discussed for the project architecture.

## Step 3: Open a New Terminal

From the VS Code menu, navigate to Terminal → New Terminal to open the integrated terminal window.

## Step 4: Verify Python Installation

Run the following command in the terminal to verify that Python is installed and available in the system path:

python --version

If the command executes successfully, Python is correctly installed.

If you receive an error, Python may either not be installed or not added to the system PATH.

## Step 5: Create a Python Virtual Environment

If Python is installed successfully, create a virtual environment for the project using the following command:

python -m venv Event_Search_Agent_VENV

## Step 6: Configure VS Code to Use the Virtual Environment

a) Press Ctrl + Shift + P (Windows) or Cmd + Shift + P (Mac) to open the Command Palette.

b) Search for Select Interpreter and click on it.

c) Choose the interpreter corresponding to your virtual environment (for example: Event_Search_Agent_VENV).

Once selected, VS Code will use the Python interpreter from the virtual environment.

## Step 7: Activate the Virtual Environment

The virtual environment should activate automatically when opening the VS Code terminal.

If it does not, activate it manually using the following command:

.\Event_Search_Agent_VENV\Scripts\activate

## Step 8: Verify the Virtual Environment Configuration

Run the following command to confirm that the virtual environment is correctly configured:

python --version
