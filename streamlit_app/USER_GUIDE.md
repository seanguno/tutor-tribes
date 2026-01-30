# User Guide: Tutor Tribes Analysis

This guide will help you use the Tutor Tribes Analysis web application to generate tutor overlap reports.

## Getting Started

### Starting the Application

1. Open Terminal (Mac) or Command Prompt (Windows)
2. Navigate to the project folder (see SETUP_INSTRUCTIONS.md if you need help)
3. Type: `streamlit run tutor_tribes_app.py`
4. Your web browser should open automatically

## Preparing Your CSV File

### Required Format

Your CSV file must have these two columns:
- **PageTitle**: The name of the tutor
- **FieldValue**: The subject/course code

### Example CSV Content

```csv
PageTitle,FieldValue
John Doe,CS 101
John Doe,MATH 241
John Doe,PHYS 211
Jane Smith,CS 101
Jane Smith,MATH 241
Bob Johnson,PHYS 211
Bob Johnson,PHYS 212
```

### Tips for Preparing Your CSV

- Each row should represent one tutor-subject combination
- If a tutor teaches multiple subjects, they should have multiple rows
- Make sure column names match exactly: `PageTitle` and `FieldValue`
- You can export from Excel, Google Sheets, or any database
- Save the file as a CSV (Comma Separated Values) format

## Using the Application

### Step 1: Upload Your CSV File

1. Look at the left sidebar
2. Find the "File Upload" section
3. Click "Choose a CSV file" or drag and drop your file
4. Wait for the file to upload (you'll see a preview)

### Step 2: Review Configuration (Optional)

The sidebar has several settings you can adjust:

#### Analysis Settings

- **Max matches per tutor**: How many matches each tutor should get (default: 4)
- **Minimum overlap threshold**: How similar tutors need to be (default: 0.5 = 50%)
  - Lower = more matches, but less similar
  - Higher = fewer matches, but more similar
- **Max assignments per tutor**: How many times a tutor can appear in others' match lists (default: 5)

#### Exclude List

- Enter tutor names you want to exclude from the analysis
- Separate names with commas or put each on a new line
- Example: `John, Jane, Bob`

#### Bonus Courses

- These are courses that are tracked separately as "extra subjects"
- They don't count toward the main overlap calculation
- But they're shown in the reports as additional information
- Example: `CS 124, CS 128, ME 200`

#### Special Tutors

- Tutors who should get priority matching
- Useful if some tutors have very few good options
- They'll get all their good matches upfront
- Example: `Jiya, Sushrut`

**Note:** You can leave all these settings at their defaults if you're not sure what to change!

### Step 3: Generate the Analysis

1. Click the big blue "🚀 Generate Analysis" button
2. Wait for the processing to complete (you'll see progress messages)
3. You'll see a success message when it's done

### Step 4: View and Download Results

Once the analysis is complete, you'll see:

#### Summary Statistics

- Total number of tutors analyzed
- How many tutors found matches
- Total number of matches
- Average matches per tutor

#### Generated Reports

Three types of reports are generated:

1. **HTML Report** (Recommended)
   - Beautiful, interactive web page
   - Best for viewing and sharing
   - Has navigation sidebar
   - Clickable sections
   - Download button at the top

2. **CSV Report**
   - Spreadsheet format
   - Good for Excel/Google Sheets
   - Can be sorted and filtered
   - Download button available

3. **Text Report**
   - Plain text format
   - Works everywhere
   - Easy to copy/paste
   - Download button available

#### Preview Reports

- Click the "👁️ Preview" expanders to see the reports before downloading
- HTML preview shows the full interactive report
- CSV preview shows the first 50 rows
- Text preview shows the first 5000 characters

#### Detailed Results Table

- Scroll down to see a table of all tutors
- Use the search box to find specific tutors
- Shows total subjects, bonus subjects, and matches found

### Step 5: Download Reports

1. Click any of the "📥 Download" buttons
2. Your browser will download the file
3. Save it wherever you want (Desktop, Documents, etc.)

## Understanding the Results

### Overlap Score

The overlap score shows what percentage of subjects one tutor can cover for another.

- **100%** = The matched tutor can cover ALL subjects of the first tutor
- **75%** = The matched tutor can cover 3 out of 4 subjects
- **50%** = The matched tutor can cover half the subjects
- **0%** = No overlap

### Match Details

For each match, you'll see:

- **Core Subjects in Common**: Regular courses both tutors teach
- **Extra Subjects in Common**: Bonus courses both tutors teach
- **Classes [Tutor A] has that [Tutor B] doesn't**: What Tutor A can cover that Tutor B can't
- **Classes [Tutor B] has that [Tutor A] doesn't**: What Tutor B can cover that Tutor A can't

### Reading the HTML Report

1. **Navigation Sidebar**: Click any tutor name to jump to their section
2. **Expand/Collapse**: Click tutor headers to expand or collapse their details
3. **Expand All / Collapse All**: Buttons to show/hide everything at once
4. **Mobile Friendly**: Works on phones and tablets too

## Common Tasks

### Running Analysis for a New Semester

1. Export your new tutor data as CSV
2. Upload the new file
3. (Optional) Update exclude list if needed
4. Click "Generate Analysis"
5. Download the new reports

### Finding Backup Tutors

1. Open the HTML report
2. Find the tutor you need a backup for
3. Look at their "Top Matches" section
4. The tutors with highest overlap scores are the best backups

### Identifying Coverage Gaps

1. Look for tutors with 0 matches
2. These tutors have unique subject combinations
3. Consider hiring more tutors in those subject areas

## Troubleshooting

### "Missing required columns" Error

- Make sure your CSV has columns named exactly: `PageTitle` and `FieldValue`
- Check for typos or extra spaces
- Try opening your CSV in Excel to verify the column names

### "No tutors found" Error

- Check your exclude list - you might have excluded everyone!
- Make sure your CSV file has data
- Verify the PageTitle column has tutor names

### Reports Look Empty

- Check that tutors have overlapping subjects
- Try lowering the "Minimum overlap threshold"
- Make sure your CSV has multiple tutors with some shared subjects

### Application Won't Start

- See SETUP_INSTRUCTIONS.md for setup help
- Make sure Python and Streamlit are installed
- Check that you're in the correct folder

### Browser Won't Open

- Look for a URL in the terminal that starts with `http://localhost:8501`
- Copy and paste that URL into your web browser manually

## Tips and Best Practices

1. **Save Your Configuration**: If you find settings that work well, write them down for next time

2. **Name Your Files**: When downloading reports, add the semester/year to the filename:
   - `tutor_overlap_report_FA25.html`
   - `tutor_overlap_analysis_Spring2024.csv`

3. **Review Before Sharing**: Always preview the HTML report before sharing with others

4. **Keep Originals**: Save your original CSV files for future reference

5. **Regular Updates**: Run the analysis whenever you get new tutor data

## Getting Help

If you need help:
1. Check the error message - it usually tells you what's wrong
2. Review this guide and SETUP_INSTRUCTIONS.md
3. Contact your IT support or the person who set this up

## Advanced Usage

### Customizing Bonus Courses

If you want to change which courses are considered "bonus":
1. Edit the list in the sidebar
2. Add or remove course codes
3. Make sure to separate them with commas

### Adjusting Match Limits

- **More matches**: Increase "Max matches per tutor" and "Max assignments per tutor"
- **Fewer matches**: Decrease these values
- **Stricter matching**: Increase "Minimum overlap threshold"
- **More lenient**: Decrease "Minimum overlap threshold"

### Special Tutor Handling

If certain tutors consistently have trouble finding matches:
1. Add them to the "Special tutors" list
2. They'll get priority in the matching algorithm
3. This ensures they get matches even if they have unique subject combinations

---

**Happy analyzing!** 📚✨

