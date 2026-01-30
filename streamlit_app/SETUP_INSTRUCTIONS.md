# Setup Instructions for Tutor Tribes Analysis

This guide will help you set up the Tutor Tribes Analysis tool on your computer.

## Prerequisites

You need to have Python installed on your computer. If you don't have it yet:

### Installing Python

1. **Windows:**
   - Go to [python.org/downloads](https://www.python.org/downloads/)
   - Download the latest Python 3.x version
   - Run the installer
   - **IMPORTANT:** Check the box that says "Add Python to PATH" during installation
   - Click "Install Now"

2. **Mac:**
   - Python 3 is usually pre-installed
   - To check, open Terminal and type: `python3 --version`
   - If it's not installed, download from [python.org/downloads](https://www.python.org/downloads/)
   - Or install using Homebrew: `brew install python3`

3. **Verify Installation:**
   - Open Terminal (Mac/Linux) or Command Prompt (Windows)
   - Type: `python --version` or `python3 --version`
   - You should see something like "Python 3.11.x"

## Installation Steps

### Step 1: Download the Project Files

Make sure you have all the following files in a folder:
- `tutor_tribes_app.py`
- `tutor_tribes_core.py`
- `requirements.txt`

### Step 2: Open Terminal/Command Prompt

- **Windows:** Press `Win + R`, type `cmd`, press Enter
- **Mac:** Press `Cmd + Space`, type "Terminal", press Enter
- **Linux:** Press `Ctrl + Alt + T`

### Step 3: Navigate to the Project Folder

Use the `cd` command to go to the folder where you saved the files.

Example:
```bash
cd "C:\Users\YourName\Documents\tutor tribe project"
```

Or on Mac/Linux:
```bash
cd ~/Documents/tutor\ tribe\ project
```

### Step 4: Install Required Packages

Type this command and press Enter:

```bash
pip install -r requirements.txt
```

If that doesn't work, try:
```bash
pip3 install -r requirements.txt
```

Or on some systems:
```bash
python -m pip install -r requirements.txt
```

Wait for the installation to complete. You should see messages like "Successfully installed pandas" and "Successfully installed streamlit".

## Running the Application

### Step 5: Start the Web App

Type this command and press Enter:

```bash
streamlit run tutor_tribes_app.py
```

If that doesn't work, try:
```bash
python -m streamlit run tutor_tribes_app.py
```

Or:
```bash
python3 -m streamlit run tutor_tribes_app.py
```

### Step 6: Use the Application

1. Your web browser should automatically open to a page that says "Tutor Tribes Analysis"
2. If it doesn't open automatically, look for a message in the terminal that says:
   ```
   You can now view your Streamlit app in your browser.
   Local URL: http://localhost:8501
   ```
3. Copy that URL and paste it into your web browser

### Step 7: Stop the Application

When you're done:
- Go back to the Terminal/Command Prompt window
- Press `Ctrl + C` (or `Cmd + C` on Mac)
- Type `Y` and press Enter to confirm

## Troubleshooting

### "python: command not found" or "python3: command not found"

- **Windows:** Make sure you checked "Add Python to PATH" during installation. You may need to reinstall Python.
- **Mac/Linux:** Try using `python3` instead of `python`

### "pip: command not found"

- Try `pip3` instead of `pip`
- Or try `python -m pip` or `python3 -m pip`

### "streamlit: command not found"

- Make sure you completed Step 4 (installing requirements)
- Try: `python -m streamlit run tutor_tribes_app.py`

### Port already in use

If you see an error about port 8501 being in use:
- Close any other Streamlit apps that might be running
- Or use a different port: `streamlit run tutor_tribes_app.py --server.port 8502`

### Permission errors

- **Windows:** Try running Command Prompt as Administrator
- **Mac/Linux:** You might need to use `sudo`, but this is usually not necessary

## Optional: Creating a Desktop Shortcut (Windows)

1. Right-click on your desktop
2. Select "New" → "Shortcut"
3. Enter this as the location:
   ```
   cmd /c "cd /d C:\path\to\your\project && streamlit run tutor_tribes_app.py"
   ```
   (Replace `C:\path\to\your\project` with your actual project folder path)
4. Click "Next" and give it a name like "Tutor Tribes"
5. Click "Finish"

Now you can double-click the shortcut to start the app!

## Optional: Hosting Online (Future)

If you want to host this online so others can access it:

### Option 1: Streamlit Cloud (Free)
1. Create a GitHub account
2. Upload your project to GitHub
3. Go to [share.streamlit.io](https://share.streamlit.io)
4. Connect your GitHub account
5. Select your repository
6. Deploy!

### Option 2: Other Hosting Services
- Heroku
- AWS
- Google Cloud Platform
- Your organization's server

Contact your IT department for help with hosting.

## Getting Help

If you run into issues:
1. Check the error message carefully
2. Make sure all files are in the same folder
3. Verify Python is installed correctly
4. Try reinstalling the requirements: `pip install -r requirements.txt --upgrade`

## Next Steps

Once everything is set up, see `USER_GUIDE.md` for instructions on how to use the application!

