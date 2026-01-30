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
def calculate_overlap(person1, person2, person_subjects):
    subjects1 = person_subjects[person1]
    subjects2 = person_subjects[person2]
    
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
            overlap_score, intersection_size, missing_from_other, extra_in_other = calculate_overlap(
                person, other_person, person_subjects
            )
            
            overlaps.append({
                'person': other_person,
                'overlap_score': overlap_score,
                'intersection_size': intersection_size,
                'missing_from_other': list(missing_from_other),
                'extra_in_other': list(extra_in_other)
            })
    
    # Sort by overlap score (descending) and get top 5
    overlaps.sort(key=lambda x: x['overlap_score'], reverse=True)
    top_5 = overlaps[:5]
    
    results[person] = {
        'total_subjects': len(person_subjects[person]),
        'subjects': list(person_subjects[person]),
        'top_matches': top_5
    }

# Create HTML report
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
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Tutor Subject Overlap Analysis</h1>
        
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
                <p class="person-stats">Total Subjects: {data['total_subjects']}</p>
            </div>
            
            <div class="subjects-list">
                <div class="subjects-title">📚 All Subjects:</div>
                {', '.join(sorted(data['subjects']))}
            </div>
            
            <h3>🔗 Top 5 Matches:</h3>
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

# Save the HTML report
with open('tutor_overlap_report.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ HTML report generated successfully!")
print("📁 File saved as: tutor_overlap_report.html")
print("🌐 Open this file in any web browser to view the report")
print("\nThe report includes:")
print("• A table of contents for easy navigation")
print("• Clear sections for each tutor")
print("• Color-coded overlap scores")
print("• Easy-to-read formatting")
print("• Professional styling that works on all devices")
