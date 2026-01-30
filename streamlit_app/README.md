# Tutor Tribes Analysis

A web-based tool for analyzing tutor subject overlaps and generating "Tutor Tribes" - groups of tutors who can cover for each other based on their subject knowledge.

## 🚀 Quick Start

### For Non-Technical Users

1. **Setup** (one-time): Follow the instructions in [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)
2. **Run**: Open Terminal/Command Prompt, navigate to this folder, and type:
   ```bash
   streamlit run tutor_tribes_app.py
   ```
3. **Use**: Your web browser will open automatically. Upload a CSV file and click "Generate Analysis"!

### For Technical Users

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run tutor_tribes_app.py
```

## 📚 Documentation

- **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - Step-by-step setup guide for first-time users
- **[USER_GUIDE.md](USER_GUIDE.md)** - How to use the web application
- **[README_tutor_analysis.md](README_tutor_analysis.md)** - Original documentation for the analysis logic

## 🎯 What It Does

This tool analyzes tutor subject overlaps to help you:

- **Find backup tutors** - Know who can cover for absent tutors
- **Optimize scheduling** - Match tutors to student needs
- **Identify gaps** - See which subject areas need more coverage
- **Plan training** - Focus cross-training on complementary subjects

## 📋 Input Format

Your CSV file needs two columns:
- **PageTitle**: Tutor name
- **FieldValue**: Subject/course code

Example:
```csv
PageTitle,FieldValue
John Doe,CS 101
John Doe,MATH 241
Jane Smith,CS 101
Jane Smith,PHYS 211
```

## 📊 Output Reports

The tool generates three types of reports:

1. **HTML Report** - Interactive web page with navigation (recommended)
2. **CSV Report** - Spreadsheet format for Excel/Google Sheets
3. **Text Report** - Plain text for maximum compatibility

## 🏗️ Project Structure

```
tutor_tribes_app.py          # Main Streamlit web application
tutor_tribes_core.py         # Core analysis logic (reusable)
requirements.txt             # Python dependencies
SETUP_INSTRUCTIONS.md        # Setup guide
USER_GUIDE.md                # User manual
README.md                    # This file
```

## 🔧 Technical Details

### Dependencies
- `pandas` - Data processing
- `streamlit` - Web application framework

### How It Works

1. **Load Data**: Reads CSV and filters based on exclude list
2. **Calculate Overlaps**: Computes overlap scores between all tutor pairs
3. **Match Tutors**: Uses "weakest first" strategy to assign matches fairly
4. **Generate Reports**: Creates HTML, CSV, and text outputs

### Overlap Scoring

- **Formula**: `(Shared subjects) / (Total subjects of first tutor)`
- **Example**: If Tutor A has 10 subjects and Tutor B covers 7, overlap = 70%

### Matching Algorithm

- Prioritizes tutors with fewer good options ("weakest first")
- Ensures even distribution (each tutor can appear in limited match lists)
- Special handling for tutors with very few matches
- Configurable thresholds and limits

## 💡 Features

- **Web-based interface** - No coding required
- **Configurable settings** - Adjust matching parameters
- **Multiple output formats** - HTML, CSV, and text
- **Interactive reports** - Navigate and explore results
- **Preview before download** - See results before saving
- **Search and filter** - Find specific tutors quickly

## 🆘 Troubleshooting

### Application won't start
- Check that Python is installed: `python --version`
- Verify dependencies: `pip install -r requirements.txt`
- See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) for detailed help

### CSV upload errors
- Verify column names: `PageTitle` and `FieldValue`
- Check for empty rows or missing data
- See [USER_GUIDE.md](USER_GUIDE.md) for format requirements

### No matches found
- Lower the "Minimum overlap threshold"
- Check your exclude list isn't too restrictive
- Verify tutors have overlapping subjects

## 🌐 Hosting (Optional)

The app can be hosted online for easy access:

### Streamlit Cloud (Free)
1. Upload project to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Deploy in one click!

### Other Options
- Heroku
- AWS
- Your organization's server

## 📝 Legacy Scripts

The original Python scripts are still available:
- `tutor_overlap_analysis.py` - Original version
- `tutor_overlap_analysis_core_subjects_4_matches_max.py` - Latest script version

These can still be run directly, but the web app is recommended for non-technical users.

## 🤝 Handoff Guide

If you're handing this off to someone:

1. **Share these files**:
   - `tutor_tribes_app.py`
   - `tutor_tribes_core.py`
   - `requirements.txt`
   - `SETUP_INSTRUCTIONS.md`
   - `USER_GUIDE.md`
   - `README.md`

2. **Have them follow** [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)

3. **They can then use** [USER_GUIDE.md](USER_GUIDE.md) to run analyses

4. **Optional**: Set up hosting so they can access it via web browser

## 📄 License

This project is for internal use. Modify as needed for your organization.

---

**Questions?** Check the documentation files or contact your IT support.

