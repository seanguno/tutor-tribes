# Tutor Subject Overlap Analysis

This project analyzes how well tutors can cover for each other based on their subject knowledge overlap.

## 📁 Files Generated

### 1. **tutor_overlap_report_v3.html** (RECOMMENDED)
- **Best for**: Sharing via email, messaging apps, or web browsers
- **Features**: 
  - Self-contained HTML (no downloads needed)
  - Mobile-responsive design
  - Clear usage instructions
  - Download links to other formats
  - Handles ties properly
  - Professional styling

### 2. **tutor_overlap_analysis.csv**
- **Best for**: Excel users, data analysis, importing into databases
- **Features**:
  - Structured data format
  - Easy to sort and filter
  - Can be opened in Excel, Google Sheets, etc.
  - Includes all match information

### 3. **tutor_overlap_simple.txt**
- **Best for**: Maximum accessibility, simple text readers, quick reference
- **Features**:
  - Plain text format
  - Works on any device
  - No special software needed
  - Easy to copy/paste

### 4. **tutor_overlap_report.html** (Original)
- **Best for**: Basic HTML viewing
- **Features**: Simple HTML report

## 🎯 How It Works

### Overlap Scoring
- **Formula**: `(Number of shared subjects) / (Total subjects of first tutor)`
- **Example**: If Tutor A has 10 subjects and Tutor B covers 7 of them, overlap = 70%

### Tie Handling
- **Before**: Only showed top 5 matches
- **Now**: Shows ALL tutors with the same overlap score as the 5th match
- **Why**: If 9 tutors all have 100% overlap, they're all equally good backups

## 📱 Accessibility Features

### HTML Reports
- Large, readable fonts (16px minimum)
- High contrast colors
- Mobile-responsive design
- Clear navigation with table of contents
- Hover effects for better usability

### Text Version
- Simple ASCII formatting
- Works with screen readers
- No special software required
- Easy to copy/paste into emails

## 🚀 How to Use

### For Non-Technical Users
1. **Open HTML file**: Double-click any `.html` file
2. **Navigate**: Use the table of contents to jump to specific tutors
3. **Read scores**: Green badges show overlap percentages
4. **Download**: Use the download links for other formats

### For Excel Users
1. **Open CSV file**: Double-click `tutor_overlap_analysis.csv`
2. **Sort/Filter**: Use Excel's built-in tools
3. **Analyze**: Create charts, pivot tables, etc.

### For Sharing
- **Email**: Attach the HTML file (works in most email clients)
- **Messaging**: Share the HTML file link
- **Web**: Upload to any web server
- **Print**: Use browser print function

## 🔧 Technical Details

### Python Scripts
- **tutor_overlap_analysis_v3.py**: Latest version with all improvements
- **tutor_overlap_analysis_v2.py**: Intermediate version
- **tutor_overlap_analysis.py**: Original version

### Dependencies
- pandas (for CSV handling)
- collections.defaultdict (for efficient data structures)

### Data Source
- Reads from `care tutor subject(Sheet1).csv`
- Handles NULL values gracefully
- Processes 67 tutors with various subject combinations

## 💡 Use Cases

### For Tutoring Centers
- **Backup Planning**: Know who can cover for absent tutors
- **Resource Allocation**: Optimize tutor assignments
- **Gap Analysis**: Identify knowledge areas needing more coverage
- **Training Planning**: Focus cross-training on complementary subjects

### For Administrators
- **Scheduling**: Match tutors to student needs
- **Hiring**: Identify subject areas needing more tutors
- **Reporting**: Show coverage statistics to stakeholders

## 🆘 Troubleshooting

### Common Issues
- **File won't open**: Make sure you have a web browser installed
- **Formatting looks wrong**: Try opening in a different browser
- **Mobile issues**: The HTML is mobile-responsive, but some older phones may have issues

### Getting Help
- **HTML issues**: Try opening in Chrome, Firefox, or Safari
- **CSV issues**: Open in Excel or Google Sheets
- **Text issues**: Use any text editor (Notepad, TextEdit, etc.)

## 📊 Sample Output

The analysis shows:
- **67 total tutors** analyzed
- **Subject overlap percentages** from 0% to 100%
- **Top matches** for each tutor (including ties)
- **Detailed breakdowns** of shared and unique subjects
- **Multiple export formats** for different use cases

## 🔄 Future Improvements

Potential enhancements:
- **Interactive charts** showing overlap networks
- **Subject category grouping** (Math, Science, Engineering, etc.)
- **Experience level weighting** (if available)
- **Availability scheduling** integration
- **Student preference matching**

---

**Created by**: AI Assistant  
**Last Updated**: Current session  
**Data Source**: care tutor subject(Sheet1).csv

