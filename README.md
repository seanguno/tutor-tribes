# Tutor Tribes Project

A web-based tool for analyzing tutor subject overlaps and generating "Tutor Tribes" - groups of tutors who can cover for each other based on their subject knowledge. This helps identify backup tutors and optimize scheduling.

## 📁 Project Structure

```
tutor tribe project/
├── streamlit_app/          # Main application code (web interface)
│   ├── tutor_tribes_app.py      # Streamlit web application
│   ├── tutor_tribes_core.py     # Core analysis logic
│   ├── requirements.txt         # Python dependencies
│   ├── README.md                 # App-specific documentation
│   ├── SETUP_INSTRUCTIONS.md    # Detailed setup guide
│   └── USER_GUIDE.md             # How to use the web app
├── fa25/                   # Fall 2025 semester results
│   ├── Tutor Tribes FA25.csv    # Generated CSV report
│   ├── Tutor Tribes FA25.html   # Generated HTML report
│   └── course lists/            # Source data for FA25
├── sp26/                   # Spring 2026 semester results
│   ├── Tutor Tribes SP26_V*.csv # Generated CSV reports (multiple versions)
│   ├── Tutor Tribes SP26_V*.html # Generated HTML reports
│   └── course lists/            # Source data for SP26
└── scrap/                  # Old/unused files (can be ignored)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher installed on your computer
- Basic familiarity with using Terminal (Mac/Linux) or Command Prompt (Windows)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd "tutor tribe project/streamlit_app"
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```
   
   If that doesn't work, try:
   ```bash
   pip3 install -r requirements.txt
   ```
   or
   ```bash
   python -m pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run tutor_tribes_app.py
   ```

4. **Your web browser should open automatically** to `http://localhost:8501`

   If it doesn't open automatically, copy the URL shown in the terminal and paste it into your browser.

## 📖 How to Use

### Basic Workflow

1. **Prepare your CSV file:**
   - Must have two columns: `PageTitle` (tutor name) and `FieldValue` (course code)
   - Each row = one tutor-subject combination
   - Example:
     ```csv
     PageTitle,FieldValue
     John Doe,CS 101
     John Doe,MATH 241
     Jane Smith,CS 101
     ```

2. **Upload and configure:**
   - Upload your CSV file using the sidebar
   - Adjust settings if needed (defaults work for most cases):
     - **Max matches per tutor**: How many backup tutors to find (default: 4)
     - **Minimum overlap threshold**: How similar tutors need to be (default: 0.5 = 50%)
     - **Max assignments per tutor**: How many times a tutor can appear in others' lists (default: 5)
   - Configure exclude list, bonus courses, and special tutors (optional)

3. **Generate analysis:**
   - Click "🚀 Generate Analysis"
   - Wait for processing to complete

4. **Download reports:**
   - Download HTML report (recommended - interactive and beautiful)
   - Download CSV report (for Excel/Google Sheets)
   - Download text report (plain text format)

### Detailed Documentation

For more detailed instructions, see:
- **Setup help**: `streamlit_app/SETUP_INSTRUCTIONS.md` - Step-by-step installation guide
- **User guide**: `streamlit_app/USER_GUIDE.md` - How to use the web application
- **App README**: `streamlit_app/README.md` - Technical details about the application

## ⚙️ Configuration and Adjustments

### Adjusting Matching Parameters

In the web interface sidebar, you can adjust:

- **Max matches per tutor** (1-10, default: 4)
  - Higher = more backup options per tutor
  - Lower = fewer, more focused matches

- **Minimum overlap threshold** (0.0-1.0, default: 0.5)
  - Higher = stricter matching (tutors must be more similar)
  - Lower = more lenient (more matches, but less similar)

- **Max assignments per tutor** (1-10, default: 5)
  - Controls how many times a tutor can appear in others' match lists
  - Prevents popular tutors from dominating all match lists

### Exclude List

- Select tutors to exclude from the analysis
- Useful for excluding tutors who are no longer available
- Default list is pre-populated but can be customized

### Core vs. Bonus Courses

- **Core courses**: Used for overlap calculations (main matching logic)
- **Bonus courses**: Tracked separately, shown as "extra subjects" in reports
- Default bonus courses are pre-selected, but you can customize
- To mark courses as bonus: unselect them from the "Core Courses" list

### Special Tutors

- Tutors who get priority matching
- Useful for tutors with unique subject combinations who might otherwise get few matches
- They get all their good matches assigned immediately

### Changing Defaults

If you want to change the default values permanently, edit `tutor_tribes_app.py`:

- **Default exclude list** (lines 43-46): Modify `DEFAULT_EXCLUDE_LIST`
- **Default bonus courses** (lines 49-59): Modify `DEFAULT_BONUS_COURSES`
- **Default special tutors** (line 61): Modify `DEFAULT_SPECIAL_TUTORS`

## 📊 Creating Tutor Tribes for a New Semester

### Step-by-Step Process

1. **Prepare your data:**
   - Export tutor-subject data as CSV with `PageTitle` and `FieldValue` columns
   - Save it somewhere accessible (e.g., Desktop)

2. **Run the application:**
   ```bash
   cd streamlit_app
   streamlit run tutor_tribes_app.py
   ```

3. **Upload and configure:**
   - Upload your new CSV file
   - Review/update the exclude list if needed
   - Adjust core/bonus courses if your course list changed
   - Click "Generate Analysis"

4. **Review results:**
   - Check the summary statistics
   - Preview the HTML report
   - Look for tutors with 0 matches (may need attention)

5. **Download and save:**
   - Download all three report formats
   - Save them in a new folder (e.g., `su26/` for Summer 2026)
   - Name files clearly: `Tutor Tribes SU26.csv`, `Tutor Tribes SU26.html`

6. **Optional - Create semester folder:**
   ```bash
   # From project root
   mkdir su26
   mkdir su26/course\ lists
   # Move your source CSV to course lists/
   # Move generated reports to su26/
   ```

## 🗂️ Directory Explanations

### `streamlit_app/`
**Main application code** - This is where you'll spend most of your time.

- Contains the web application that creates the tutor tribes
- Run `streamlit run tutor_tribes_app.py` from this directory
- See `streamlit_app/README.md` for detailed app documentation

### `fa25/` and `sp26/`
**Generated results** - These contain the tutor tribes created for each semester.

- **CSV files**: Spreadsheet format, good for Excel/Google Sheets
- **HTML files**: Interactive web reports (best for viewing)
- **course lists/**: Source data used to generate the tribes
- **old versions/**: Previous iterations (for reference)

When creating tribes for a new semester, you can follow this structure:
- Create a new folder (e.g., `su26/`)
- Save your source CSV in `su26/course lists/`
- Save generated reports in `su26/`

### `scrap/`
**Old/unused files** - Can be ignored. Contains previous versions of scripts and outputs that are no longer used.

## 🔧 Troubleshooting

### Application won't start
- **Check Python installation**: `python --version` or `python3 --version`
- **Verify dependencies**: `pip install -r streamlit_app/requirements.txt`
- **Check you're in the right directory**: Make sure you're in `streamlit_app/` when running the command

### CSV upload errors
- **Verify column names**: Must be exactly `PageTitle` and `FieldValue`
- **Check for empty rows**: Remove any completely empty rows
- **File format**: Make sure it's saved as CSV (not Excel .xlsx)

### No matches found
- **Lower the threshold**: Try reducing "Minimum overlap threshold" to 0.3 or 0.4
- **Check exclude list**: Make sure you haven't excluded too many tutors
- **Verify data**: Ensure tutors have overlapping subjects in your CSV

### Port already in use
If port 8501 is busy:
```bash
streamlit run tutor_tribes_app.py --server.port 8502
```

## 💡 Tips

1. **Save your configuration**: If you find settings that work well, note them down for next semester
2. **Name files clearly**: Include semester/year in filenames (e.g., `Tutor Tribes FA25.html`)
3. **Keep source data**: Always save your original CSV files in the `course lists/` folder
4. **Review before sharing**: Always preview the HTML report before sharing with others
5. **Regular updates**: Re-run the analysis whenever you get new tutor data

## 📝 Notes

- The web application is the recommended way to use this tool
- The old Python scripts in `fa25/` and `scrap/` can still be run directly, but the web app is much easier to use
- All configuration can be done through the web interface - no code editing required
- Reports are generated fresh each time - previous results don't affect new analyses

## 🆘 Getting Help

If you run into issues:

1. Check the error message - it usually tells you what's wrong
2. Review `streamlit_app/SETUP_INSTRUCTIONS.md` for setup help
3. Review `streamlit_app/USER_GUIDE.md` for usage help
4. Check that your CSV format matches the requirements
5. Verify Python and all dependencies are installed correctly

---

**Happy analyzing!** 📚✨
