import pandas as pd
from collections import defaultdict

# Read the CSV file
df = pd.read_csv('care tutor subject(Sheet1).csv')

# Create a dictionary mapping each person to their set of subjects
person_subjects = defaultdict(set)
for _, row in df.iterrows():
    if pd.notna(row['FieldValue']):  # Skip NULL values
        person_subjects[row['PageTitle']].add(row['FieldValue'])

# Function to calculate overlap score between two people
def calculate_overlap(person1, person2, subjects_dict):
    subjects1 = subjects_dict[person1]
    subjects2 = subjects_dict[person2]
    
    if len(subjects1) == 0:
        return 0.0
    
    intersection = len(subjects1.intersection(subjects2))
    overlap_score = intersection / len(subjects1)
    
    return overlap_score, intersection, subjects1 - subjects2, subjects2 - subjects1

# Calculate overlaps for each person
results = {}

for person in person_subjects:
    overlaps = []
    
    for other_person in person_subjects:
        if person != other_person:
            score, intersection_size, missing_from_other, extra_in_other = calculate_overlap(
                person, other_person, person_subjects
            )
            
            overlaps.append({
                'person': other_person,
                'overlap_score': score,
                'intersection_size': intersection_size,
                'missing_from_other': list(missing_from_other),
                'extra_in_other': list(extra_in_other)
            })
    
    # Sort by overlap score (descending) and get top matches
    overlaps.sort(key=lambda x: x['overlap_score'], reverse=True)
    
    # Handle ties: include all people with the same score as the 5th person
    if len(overlaps) >= 5:
        fifth_score = overlaps[4]['overlap_score']
        # Find all people with the same score as the 5th person
        top_matches = [overlap for overlap in overlaps if overlap['overlap_score'] >= fifth_score]
    else:
        top_matches = overlaps
    
    results[person] = {
        'total_subjects': len(person_subjects[person]),
        'subjects': list(person_subjects[person]),
        'top_matches': top_matches,
        'match_count': len(top_matches)
    }

# Create CSV output for Excel users
csv_rows = []
for person in sorted(results.keys()):
    data = results[person]
    
    # Add main person info
    csv_rows.append({
        'Tutor': person,
        'Total_Subjects': data['total_subjects'],
        'All_Subjects': '; '.join(sorted(data['subjects'])),
        'Number_of_Matches': data['match_count'],
        'Match_Type': 'MAIN_TUTOR'
    })
    
    # Add match info
    for i, match in enumerate(data['top_matches'], 1):
        csv_rows.append({
            'Tutor': f"  {i}. {match['person']}",
            'Total_Subjects': match['intersection_size'],
            'All_Subjects': f"Overlap: {match['overlap_score']:.1%}",
            'Number_of_Matches': '',
            'Match_Type': 'MATCH'
        })
    
    # Add separator row
    csv_rows.append({
        'Tutor': '',
        'Total_Subjects': '',
        'All_Subjects': '',
        'Number_of_Matches': '',
        'Match_Type': 'SEPARATOR'
    })

# Create DataFrame and save to CSV
csv_df = pd.DataFrame(csv_rows)
csv_df.to_csv('tutor_overlap_analysis.csv', index=False)

# Create HTML report with improved tie handling
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tutor Subject Overlap Analysis</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        .person-section {
            margin-bottom: 40px;
            border: 2px solid #ecf0f1;
            border-radius: 8px;
            padding: 20px;
            background-color: #fafafa;
        }
        .person-header {
            background-color: #3498db;
            color: white;
            padding: 15px;
            margin: -20px -20px 20px -20px;
            border-radius: 6px 6px 0 0;
        }
        .person-name {
            font-size: 24px;
            font-weight: bold;
            margin: 0;
        }
        .person-stats {
            font-size: 16px;
            margin: 5px 0 0 0;
            opacity: 0.9;
        }
        .subjects-list {
            background-color: #e8f4fd;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .subjects-title {
            font-weight: bold;
            color: #2980b9;
            margin-bottom: 10px;
        }
        .match-item {
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .match-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .match-name {
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        }
        .overlap-score {
            background-color: #27ae60;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
        }
        .match-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 10px;
        }
        .detail-box {
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }
        .detail-title {
            font-weight: bold;
            color: #34495e;
            margin-bottom: 5px;
        }
        .classes-list {
            color: #555;
            font-size: 14px;
        }
        .no-classes {
            color: #95a5a6;
            font-style: italic;
        }
        .toc {
            background-color: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .toc-title {
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
        }
        .toc-list {
            list-style: none;
            padding: 0;
            margin: 0;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 10px;
        }
        .toc-item a {
            color: #3498db;
            text-decoration: none;
            padding: 5px 10px;
            display: block;
            border-radius: 3px;
            transition: background-color 0.2s;
        }
        .toc-item a:hover {
            background-color: #d5e8f7;
        }
        .tie-note {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
            font-style: italic;
        }
        .download-links {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        .download-links a {
            color: #155724;
            font-weight: bold;
            text-decoration: none;
            margin: 0 10px;
        }
        .download-links a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Tutor Subject Overlap Analysis</h1>
        
        <div class="download-links">
            <strong>📥 Download Options:</strong>
            <a href="tutor_overlap_analysis.csv">📊 Excel/CSV Version</a>
            <a href="tutor_overlap_summary.txt">📝 Text Summary</a>
        </div>
        
        <div class="toc">
            <div class="toc-title">📋 Table of Contents</div>
            <ul class="toc-list">
"""

# Add table of contents
for person in sorted(results.keys()):
    html_content += f'                <li class="toc-item"><a href="#{person.replace(" ", "-")}">{person}</a></li>\n'

html_content += """
            </ul>
        </div>
"""

# Add each person's section
for person in sorted(results.keys()):
    data = results[person]
    
    html_content += f"""
        <div class="person-section" id="{person.replace(' ', '-')}">
            <div class="person-header">
                <h2 class="person-name">{person}</h2>
                <p class="person-stats">Total Subjects: {data['total_subjects']} | Matches Found: {data['match_count']}</p>
            </div>
            
            <div class="subjects-list">
                <div class="subjects-title">📚 All Subjects:</div>
                {', '.join(sorted(data['subjects']))}
            </div>
            
            <h3>🔗 Top Matches (Including Ties):</h3>
    """
    
    # Add tie note if there are more than 5 matches
    if data['match_count'] > 5:
        html_content += f"""
            <div class="tie-note">
                ⚠️ Note: {data['match_count']} tutors have the same overlap score as the 5th match. 
                All are shown below as they provide equally good coverage.
            </div>
        """
    
    for i, match in enumerate(data['top_matches'], 1):
        html_content += f"""
            <div class="match-item">
                <div class="match-header">
                    <span class="match-name">{i}. {match['person']}</span>
                    <span class="overlap-score">{match['overlap_score']:.1%}</span>
                </div>
                <p><strong>Classes in Common:</strong> {match['intersection_size']}</p>
                
                <div class="match-details">
                    <div class="detail-box">
                        <div class="detail-title">Classes {person} has that {match['person']} doesn't:</div>
                        <div class="classes-list">
                            {', '.join(match['missing_from_other']) if match['missing_from_other'] else '<span class="no-classes">None</span>'}
                        </div>
                    </div>
                    <div class="detail-box">
                        <div class="detail-title">Classes {match['person']} has that {person} doesn't:</div>
                        <div class="classes-list">
                            {', '.join(match['extra_in_other']) if match['extra_in_other'] else '<span class="no-classes">None</span>'}
                        </div>
                    </div>
                </div>
            </div>
        """
    
    html_content += """
        </div>
    """

html_content += """
    </div>
</body>
</html>
"""

# Save the improved HTML report
with open('tutor_overlap_report_v2.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Improved analysis completed!")
print("📁 Files generated:")
print("   • tutor_overlap_analysis.csv (Excel-friendly)")
print("   • tutor_overlap_report_v2.html (Improved HTML)")
print("\nKey improvements:")
print("• Handles ties properly - shows all people with same overlap score")
print("• CSV output for Excel users")
print("• Download links in HTML report")
print("• Better tie explanations")
print("• Fixed linter issues")
