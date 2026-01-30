import pandas as pd
from collections import defaultdict

# Read the CSV file
df = pd.read_csv('care tutor subject(Sheet1).csv')

# List of facilitators to exclude
exclude_list = ['Emma', 'Adelaide', 'Regina', 'Anthony', 'Geo', 'Lucy P.', \
    'Maya', 'Grace', 'Lydia', 'Meredith', 'Rohan', 'Clive', 'Sophia', 'Noah', \
        'Lucy', 'Maria', 'Jacob', 'Zaahi', 'Gabe']

bonus_courses = ['AE 140', 'AE 202', 'AE 311', 'AE 321', 'AE 323', 'AE 352', \
    'BIOE 202', 'BIOE 206', 'BIOE 210', 'BIOE 302', 'BIOE 303', 'CS 124', \
        'CS 128', 'CS 173', 'CS 225', 'CS 233', 'CS 340', 'CS 361', 'CS 374', \
            'ECE 310', 'ECE 313', 'ECE 329', 'ECE 342', 'ECE 374', 'ECE 385', \
                'ECE 391', 'IE 300', 'IE 310', 'MATH 347', 'ME 170', 'ME 200', \
                    'ME 270', 'ME 310', 'ME 330', 'ME 340', 'MSE 201', 'MSE 206', \
                        'MSE 280', 'NPRE 200', 'NPRE 247', 'NPRE 321', 'NPRE 330', \
                            'NPRE 349', 'STAT 400', 'PHYS 326', 'PHYS 370', 'TAM 335', \
                                'CHEM 312']

# all the CS's 124, 128, 173, 124, 225, 233, 340, 361, 374
# IE 310, 300
# ME 170, 200, 270
# Any 300's
# MSE 180, 201, 206, 280
# STAT 400
# NPRE 200, 
# BIOE 202, 206, 210, 302, 303
# AE 140, 202, 3--

# Create a dictionary mapping each person to their set of subjects
person_subjects = defaultdict(set)
person_bonus_subjects = defaultdict(set)
for _, row in df.iterrows():
    if pd.notna(row['FieldValue']) and row['PageTitle'] not in exclude_list and row['FieldValue'] not in bonus_courses:  # Skip NULL values
        person_subjects[row['PageTitle']].add(row['FieldValue'])
    elif pd.notna(row['FieldValue']) and row['PageTitle'] not in exclude_list and row['FieldValue'] in bonus_courses:
        person_bonus_subjects[row['PageTitle']].add(row['FieldValue'])

# Function to calculate overlap score between two people
def calculate_overlap(person1, person2, subjects_dict):
    subjects1 = subjects_dict[person1]
    subjects2 = subjects_dict[person2]
    
    if len(subjects1) == 0:
        return 0.0
    
    intersection = subjects1.intersection(subjects2)
    intersection_size = len(intersection)
    overlap_score = intersection_size / len(subjects1)
    
    return overlap_score, intersection_size, list(intersection), subjects1 - subjects2, subjects2 - subjects1

# Calculate overlaps for each person using filtered subjects (excluding bonus courses)
results = {}

for person in person_subjects:
    overlaps = []
    
    for other_person in person_subjects:
        if person != other_person:
            score, intersection_size, common_classes, missing_from_other, extra_in_other = calculate_overlap(
                person, other_person, person_subjects
            )
            
            overlaps.append({
                'person': other_person,
                'overlap_score': score,
                'intersection_size': intersection_size,
                'common_classes': common_classes,
                'missing_from_other': missing_from_other,
                'extra_in_other': extra_in_other
            })
    
    # Sort by overlap score (descending)
    overlaps.sort(key=lambda x: x['overlap_score'], reverse=True)
    
    results[person] = {
        'total_subjects': len(person_subjects[person]),
        'subjects': list(person_subjects[person]),
        'bonus_subjects': list(person_bonus_subjects[person]) if person in person_bonus_subjects else [],
        'all_overlaps': overlaps
    }

# Now implement the iterative matching system with "weakest first" strategy
# First pass: Give every tutor 1 match, then 2nd, then 3rd
# Priority goes to tutors with the LOWEST best scores (fewer good options)

# Track how many times each tutor has been assigned to match lists
tutor_assignments = defaultdict(int)
final_results = {}

# Calculate tutor priorities using "weakest first" strategy
tutor_priorities = []
for person in results:
    if results[person]['all_overlaps']:
        # Filter to only 50%+ overlaps
        good_overlaps = [overlap for overlap in results[person]['all_overlaps'] if overlap['overlap_score'] >= 0.5]
        if person == 'Jiya' or person == 'Sushrut':
            print(f'on person: {person}\n all overlaps is {results[person]["all_overlaps"]}\n good overlaps are {good_overlaps}')
        
        if good_overlaps:
            # Get the best score among good overlaps
            best_score = good_overlaps[0]['overlap_score']
            # Count how many good options they have
            good_options_count = len(good_overlaps)
            # Priority score: lower best score = higher priority (weaker tutors first)
            # Secondary: fewer good options = higher priority
            priority_score = (1.0 - best_score) + (1.0 / good_options_count)
            if person == 'Jiya' or person == 'Sushrut':
                tutor_priorities.append((person, 0.0, best_score, good_options_count))
            else:
                tutor_priorities.append((person, priority_score, best_score, good_options_count))
        else:
            # No good overlaps, lowest priority
            tutor_priorities.append((person, 999.0, 0.0, 0))
    else:
        tutor_priorities.append((person, 999.0, 0.0, 0))

# Sort by priority score (ascending) - weakest tutors first
tutor_priorities.sort(key=lambda x: x[1])

print("Tutor priorities (weakest first):")
for i, (person, priority, best_score, good_options) in enumerate(tutor_priorities[:10]):
    print(f"  {i+1}. {person}: best={best_score:.1%}, options={good_options}, priority={priority:.3f}")

# Initialize all tutors with empty match lists
for person, _, _, _ in tutor_priorities:
    final_results[person] = {
        'total_subjects': results[person]['total_subjects'],
        'subjects': results[person]['subjects'],
        'bonus_subjects': results[person]['bonus_subjects'],
        'top_matches': [],
        'match_count': 0,
        'total_available': 0,
        'total_potential': len(results[person]['all_overlaps']),
        'assignments_used': 0
    }

# Special handling for tutors with very few good options (like Jiya and Sushrut)
# Give them ALL their good matches upfront before the iterative process
special_tutors = ['Jiya', 'Sushrut']
for person in special_tutors:
    if person in results:
        data = results[person]
        good_overlaps = [overlap for overlap in data['all_overlaps'] if overlap['overlap_score'] >= 0.5]
        
        if good_overlaps:  # Only if they have 3 or fewer good options
            print(f"🎯 SPECIAL CASE: {person} has only {len(good_overlaps)} good options - assigning ALL upfront")
            
            # Assign ALL good matches immediately
            for match in good_overlaps:
                if tutor_assignments[match['person']] < 4:  # Still respect assignment limit
                    final_results[person]['top_matches'].append(match)
                    tutor_assignments[match['person']] += 1
                    print(f"  ✅ {person} got special match: {match['person']} ({match['overlap_score']:.1%})")
            
            # Update final results
            final_results[person]['match_count'] = len(final_results[person]['top_matches'])
            final_results[person]['total_available'] = len(good_overlaps)
            final_results[person]['assignments_used'] = sum(tutor_assignments[m['person']] for m in final_results[person]['top_matches'])

# Iterative matching: 4 passes to ensure even distribution
for pass_num in range(1, 5):  # Pass 1, 2, 3, 4
    print(f"Starting pass {pass_num}...")
    
    # Process tutors in priority order for this pass (weakest first)
    for person, _, _, _ in tutor_priorities:
        # Skip special tutors - they already got their matches
        if person in special_tutors:
            continue
            
        data = results[person]
        current_matches = final_results[person]['top_matches']
        
        # Skip if this tutor already has enough matches for this pass
        if len(current_matches) >= pass_num:
            continue
            
        available_matches = []
        
        # Look for available tutors (assigned less than 5 times) AND has at least 50% overlap
        for overlap in data['all_overlaps']:
            potential_match = overlap['person']
            
            # Check if this tutor is available (assigned less than 5 times) AND has at least 50% overlap
            if (tutor_assignments[potential_match] < 4 and 
                overlap['overlap_score'] >= 0.5 and
                potential_match not in [m['person'] for m in current_matches]):  # Not already matched
                available_matches.append(overlap)
        
        # Sort available matches by overlap score (descending)
        available_matches.sort(key=lambda x: x['overlap_score'], reverse=True)
        
        # Take the best available match for this pass
        if available_matches:
            best_match = available_matches[0]
            current_matches.append(best_match)
            
            # Mark this tutor as assigned
            tutor_assignments[best_match['person']] += 1
            
            # Update final results
            final_results[person]['top_matches'] = current_matches
            final_results[person]['match_count'] = len(current_matches)
            final_results[person]['total_available'] = len(available_matches)
            final_results[person]['assignments_used'] = sum(tutor_assignments[m['person']] for m in current_matches)
            
            print(f"  {person} got match {pass_num}: {best_match['person']} ({best_match['overlap_score']:.1%})")
    
    print(f"Pass {pass_num} complete. Current match distribution:")
    match_counts = [len(final_results[p]['top_matches']) for p in final_results]
    for i in range(5):
        count = match_counts.count(i)
        print(f"  {i} matches: {count} tutors")

# Create enhanced CSV output with missing classes
csv_rows = []
for person in sorted(final_results.keys()):
    data = final_results[person]
    
    # Add main person info
    csv_rows.append({
        'Tutor': person,
        'Total_Subjects': data['total_subjects'],
        'All_Subjects': '; '.join(sorted(data['subjects'])),
        'Number_of_Matches': data['match_count'],
        'Total_Available': data['total_available'],
        'Assignments_Used': data['assignments_used'],
        'Match_Type': 'MAIN_TUTOR'
    })
    
    # Add match info with missing classes
    for i, match in enumerate(data['top_matches'], 1):
        csv_rows.append({
            'Tutor': f"  {i}. {match['person']}",
            'Total_Subjects': match['intersection_size'],
            'All_Subjects': f"Overlap: {match['overlap_score']:.1%}",
            'Classes_in_Common': match['intersection_size'],
            'Classes_Both_Tutors_Have': '; '.join(match['common_classes']) if match['common_classes'] else 'None',
            'Classes_Missing_from_Match': '; '.join(match['missing_from_other']) if match['missing_from_other'] else 'None',
            'Classes_Match_Has_Extra': '; '.join(match['extra_in_other']) if match['extra_in_other'] else 'None',
            'Match_Type': 'MATCH'
        })
    
    # Add separator row
    csv_rows.append({
        'Tutor': '',
        'Total_Subjects': '',
        'All_Subjects': '',
        'Classes_in_Common': '',
        'Classes_Both_Tutors_Have': '',
        'Classes_Missing_from_Match': '',
        'Classes_Match_Has_Extra': '',
        'Match_Type': 'SEPARATOR'
    })

# Create DataFrame and save to CSV
csv_df = pd.DataFrame(csv_rows)
csv_df.to_csv('tutor_overlap_analysis_v7_fixed.csv', index=False)

# Create a simple text version for maximum accessibility
text_content = "TUTOR SUBJECT OVERLAP ANALYSIS (V7 Fixed - Up to 3 Matches Per Tutor)\n"
text_content += "=" * 80 + "\n\n"
text_content += "This analysis shows which tutors can best cover for each other.\n"
text_content += "IMPORTANT: Each tutor can appear in up to 3 other tutors' match lists.\n"
text_content += "Each tutor shows only their top 3 matches.\n"
text_content += "Overlap score = (shared subjects) / (total subjects of first tutor)\n\n"

for person in sorted(final_results.keys()):
    data = final_results[person]
    text_content += f"TUTOR: {person}\n"
    text_content += f"Total Subjects: {data['total_subjects']}\n"
    text_content += f"All Subjects: {', '.join(sorted(data['subjects']))}\n"
    text_content += f"Number of Matches: {data['match_count']}\n"
    text_content += f"Total Available (before assignment): {data['total_available']}\n"
    text_content += f"Assignments Used: {data['assignments_used']}\n\n"
    
    if data['match_count'] == 0:
        text_content += "NO MATCHES AVAILABLE - All potential matches were at their limit (3 assignments).\n\n"
    else:
        text_content += "TOP 3 MATCHES:\n"
        for i, match in enumerate(data['top_matches'], 1):
            text_content += f"{i}. {match['person']} - {match['overlap_score']:.1%} overlap\n"
            text_content += f"   Classes in common: {match['intersection_size']}\n"
            text_content += f"   Classes {person} has that {match['person']} doesn't: "
            if match['missing_from_other']:
                text_content += f"{', '.join(match['missing_from_other'])}\n"
            else:
                text_content += "None\n"
            text_content += f"   Classes {match['person']} has that {person} doesn't: "
            if match['extra_in_other']:
                text_content += f"{', '.join(match['extra_in_other'])}\n"
            else:
                text_content += "None\n"
            text_content += "\n"
    
    text_content += "-" * 80 + "\n\n"

# Save the text version
with open('tutor_overlap_simple_v7_fixed.txt', 'w', encoding='utf-8') as f:
    f.write(text_content)

# Create HTML report with collapsible sidebar, sections starting closed, and auto-open navigation
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tutor Subject Overlap Analysis (V7 Fixed - Up to 3 Matches Per Tutor)</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            font-size: 16px;
        }
        .container {
            display: flex;
            min-height: 100vh;
        }
        .sidebar {
            width: 300px;
            background-color: #2c3e50;
            color: white;
            position: sticky;
            top: 0;
            height: 100vh;
            overflow-y: auto;
            flex-shrink: 0;
            transition: transform 0.3s ease;
        }
        .sidebar.collapsed {
            transform: translateX(-250px);
        }
        .sidebar-toggle {
            position: absolute;
            top: 20px;
            right: -50px;
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 0 8px 8px 0;
            padding: 12px 8px;
            cursor: pointer;
            font-size: 18px;
            width: 50px;
            height: 50px;
            transition: all 0.3s ease;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
            z-index: 1000;
        }
        .sidebar-toggle:hover {
            background-color: #c0392b;
            transform: scale(1.1);
        }
        .sidebar-toggle.collapsed {
            right: -50px;
        }
        .sidebar-header {
            background-color: #34495e;
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid #3498db;
        }
        .sidebar-title {
            margin: 0;
            font-size: 20px;
            color: #ecf0f1;
        }
        .toc-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .toc-item {
            border-bottom: 1px solid #34495e;
        }
        .toc-item a {
            color: #bdc3c7;
            text-decoration: none;
            padding: 15px 20px;
            display: block;
            transition: all 0.3s ease;
        }
        .toc-item a:hover {
            background-color: #3498db;
            color: white;
        }
        .toc-item a.active {
            background-color: #3498db;
            color: white;
            border-left: 4px solid #e74c3c;
        }
        .main-content {
            flex: 1;
            padding: 30px;
            max-width: calc(100vw - 300px);
            transition: max-width 0.3s ease;
        }
        .main-content.sidebar-collapsed {
            max-width: calc(100vw - 50px);
        }
        .header {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            font-size: 28px;
            margin-top: 0;
        }
        .instructions {
            background-color: #e3f2fd;
            border: 1px solid #bbdefb;
            color: #1565c0;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .instructions h3 {
            margin-top: 0;
            color: #0d47a1;
        }
        .instructions ul {
            margin: 10px 0;
            padding-left: 20px;
        }
        .instructions li {
            margin-bottom: 5px;
        }
        .person-section {
            background-color: white;
            border: 2px solid #ecf0f1;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .person-header {
            background-color: #3498db;
            color: white;
            padding: 15px;
            margin: -20px -20px 20px -20px;
            border-radius: 6px 6px 0 0;
            cursor: pointer;
            user-select: none;
        }
        .person-header:hover {
            background-color: #2980b9;
        }
        .person-name {
            font-size: 24px;
            font-weight: bold;
            margin: 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .collapse-icon {
            font-size: 20px;
            transition: transform 0.3s ease;
        }
        .collapsed .collapse-icon {
            transform: rotate(-90deg);
        }
        .person-stats {
            font-size: 16px;
            margin: 5px 0 0 0;
            opacity: 0.9;
        }
        .person-content {
            transition: all 0.3s ease;
            overflow: hidden;
            max-height: 0;
            opacity: 0;
        }
        .person-content.expanded {
            max-height: 2000px;
            opacity: 1;
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
            background-color: #f8f9fa;
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
            flex-wrap: wrap;
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
            font-size: 14px;
        }
        .match-details {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
            margin-top: 10px;
        }
        @media (min-width: 768px) {
            .match-details {
                grid-template-columns: 1fr 1fr;
            }
        }
        .detail-box {
            background-color: white;
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
        .no-matches {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 15px;
            text-align: center;
            font-weight: bold;
        }
        .scroll-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            opacity: 0;
            visibility: hidden;
        }
        .scroll-to-top.visible {
            opacity: 1;
            visibility: visible;
        }
        .scroll-to-top:hover {
            background-color: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(0,0,0,0.4);
        }
        .mobile-toggle {
            display: none;
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1000;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px;
            cursor: pointer;
            font-size: 16px;
        }
        @media (max-width: 768px) {
            .container {
                flex-direction: column;
            }
            .sidebar {
                width: 100%;
                height: auto;
                position: relative;
                display: none;
                transform: none;
                position: sticky;
                top: 0;
            }
            .sidebar.show {
                display: block;
            }
            .main-content {
                max-width: 100%;
                padding: 20px;
            }
            .mobile-toggle {
                display: block;
            }
            .person-header {
                padding: 20px;
            }
            .sidebar-toggle {
                display: none;
            }
        }
        .expand-all-btn {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px 20px;
            font-size: 14px;
            transition: background-color 0.3s ease;
        }
        .expand-all-btn:hover {
            background-color: #229954;
        }
        .collapse-all-btn {
            background-color: #e74c3c;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px 20px;
            font-size: 14px;
            transition: background-color 0.3s ease;
        }
        .collapse-all-btn:hover {
            background-color: #c0392b;
        }
    </style>
</head>
<body>
    <button class="mobile-toggle" onclick="toggleSidebar()">☰ Menu</button>
    
    <div class="container">
        <div class="sidebar" id="sidebar">
            <button class="sidebar-toggle" onclick="toggleSidebarCollapse()" title="Toggle sidebar">◀</button>
            
            <div class="sidebar-header">
                <h2 class="sidebar-title">📋 Navigation</h2>
                <button class="expand-all-btn" onclick="expandAllSections()">Expand All</button>
                <button class="collapse-all-btn" onclick="collapseAllSections()">Collapse All</button>
            </div>
            <ul class="toc-list">
"""

# Add table of contents
for person in sorted(final_results.keys()):
    html_content += f'                <li class="toc-item"><a href="#{person.replace(" ", "-")}" onclick="navigateToSection(\'{person.replace(" ", "-")}\')">{person}</a></li>\n'

html_content += """
            </ul>
        </div>
        
        <div class="main-content" id="main-content">
            <div class="header">
                <h1>📚 Tutor Subject Overlap Analysis (V7 Fixed)</h1>
                
                <div class="instructions">
                    <h3>📖 How to Use This Report</h3>
                    <ul>
                        <li><strong>Sidebar Navigation:</strong> Use the left sidebar to jump to any tutor (automatically opens section)</li>
                        <li><strong>Collapsible Sidebar:</strong> Click the red ◀ button to collapse/expand the sidebar</li>
                        <li><strong>Collapsible Sections:</strong> All sections start closed - click tutor headers to open</li>
                        <li><strong>Expand/Collapse All:</strong> Use buttons in sidebar to control all sections at once</li>
                        <li><strong>Up to 3 Matches Per Tutor:</strong> Each tutor can appear in up to 3 other tutors' match lists</li>
                        <li><strong>Top 3 Matches:</strong> Each tutor shows only their top 3 matches</li>
                        <li><strong>Overlap Scores:</strong> Green badges show what percentage of subjects another tutor can cover</li>
                        <li><strong>100% Score:</strong> Means that tutor can cover ALL subjects of the first tutor</li>
                    </ul>
                </div>
            </div>
"""

# Add each person's section (starting collapsed)
for person in sorted(final_results.keys()):
    data = final_results[person]
    
    html_content += f"""
            <div class="person-section" id="{person.replace(' ', '-')}">
                <div class="person-header" onclick="toggleSection(this)">
                    <div>
                        <h2 class="person-name">
                            {person}
                            <span class="collapse-icon">▶</span>
                        </h2>
                        <p class="person-stats">Total Subjects: {data['total_subjects']} | Matches Found: {data['match_count']} | Available Before Assignment: {data['total_available']} | Assignments Used: {data['assignments_used']}</p>
                    </div>
                </div>
                
                <div class="person-content">
                    <div class="subjects-list">
                        <div class="subjects-title">📚 All Subjects:</div>
                        {', '.join(sorted(data['subjects']))}
                    </div>
                    
                    <h3>🔗 Top 3 Matches (Up to 3 Matches Per Tutor Logic):</h3>
    """
    
    if data['match_count'] == 0:
        html_content += f"""
                        <div class="no-matches">
                            ⚠️ NO MATCHES AVAILABLE - All potential matches were at their limit (3 assignments).
                            This tutor had {data['total_available']} potential matches before the assignment algorithm.
                        </div>
        """
    else:
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
            </div>
        """

html_content += """
        </div>
    </div>
    
    <button class="scroll-to-top" onclick="scrollToTop()" title="Scroll to top">↑</button>
    
    <script>
        // Toggle section collapse/expand
        function toggleSection(header) {
            const section = header.parentElement;
            const content = section.querySelector('.person-content');
            const icon = header.querySelector('.collapse-icon');
            
            if (content.classList.contains('expanded')) {
                content.classList.remove('expanded');
                icon.textContent = '▶';
            } else {
                content.classList.add('expanded');
                icon.textContent = '▼';
            }
        }
        
        // Navigate to section and automatically open it
        function navigateToSection(sectionId) {
            const element = document.getElementById(sectionId);
            if (element) {
                // Scroll to section
                element.scrollIntoView({ behavior: 'smooth' });
                
                // Automatically open the section
                const content = element.querySelector('.person-content');
                const icon = element.querySelector('.collapse-icon');
                
                if (!content.classList.contains('expanded')) {
                    content.classList.add('expanded');
                    icon.textContent = '▼';
                }
                
                // Update active state in sidebar
                updateActiveSection(sectionId);
            }
        }
        
        // Toggle sidebar collapse
        function toggleSidebarCollapse() {
            const sidebar = document.getElementById('sidebar');
            const mainContent = document.getElementById('main-content');
            const toggleBtn = document.querySelector('.sidebar-toggle');
            
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('sidebar-collapsed');
            
            if (sidebar.classList.contains('collapsed')) {
                toggleBtn.textContent = '▶';
                toggleBtn.title = 'Expand sidebar';
            } else {
                toggleBtn.textContent = '◀';
                toggleBtn.title = 'Collapse sidebar';
            }
        }
        
        // Expand all sections
        function expandAllSections() {
            document.querySelectorAll('.person-content').forEach(content => {
                content.classList.add('expanded');
            });
            document.querySelectorAll('.collapse-icon').forEach(icon => {
                icon.textContent = '▼';
            });
        }
        
        // Collapse all sections
        function collapseAllSections() {
            document.querySelectorAll('.person-content').forEach(content => {
                content.classList.remove('expanded');
            });
            document.querySelectorAll('.collapse-icon').forEach(icon => {
                icon.textContent = '▶';
            });
        }
        
        // Update active section in sidebar
        function updateActiveSection(sectionId) {
            // Remove all active classes
            document.querySelectorAll('.toc-item a').forEach(link => {
                link.classList.remove('active');
            });
            
            // Add active class to current section
            const activeLink = document.querySelector(`[href="#${sectionId}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
            }
        }
        
        // Scroll to top
        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        
        // Show/hide scroll to top button
        window.addEventListener('scroll', function() {
            const scrollButton = document.querySelector('.scroll-to-top');
            if (window.pageYOffset > 300) {
                scrollButton.classList.add('visible');
            } else {
                scrollButton.classList.remove('visible');
            }
        });
        
        // Update active section on scroll
        window.addEventListener('scroll', function() {
            const sections = document.querySelectorAll('.person-section');
            let currentSection = '';
            
            sections.forEach(section => {
                const rect = section.getBoundingClientRect();
                if (rect.top <= 100) {
                    currentSection = section.id;
                }
            });
            
            if (currentSection) {
                updateActiveSection(currentSection);
            }
        });
        
        // Mobile sidebar toggle
        function toggleSidebar() {
            const sidebar = document.getElementById('sidebar');
            sidebar.classList.toggle('show');
        }
        
        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', function(event) {
            const sidebar = document.getElementById('sidebar');
            const mobileToggle = document.querySelector('.mobile-toggle');
            
            if (window.innerWidth <= 768) {
                if (!sidebar.contains(event.target) && !mobileToggle.contains(event.target)) {
                    sidebar.classList.remove('show');
                }
            }
        });
        
        // Initialize first section as active
        document.addEventListener('DOMContentLoaded', function() {
            const firstSection = document.querySelector('.person-section');
            if (firstSection) {
                updateActiveSection(firstSection.id);
            }
        });
    </script>
</body>
</html>
"""

# Save the enhanced HTML report
with open('tutor_overlap_report_v7_fixed.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ V7 Fixed analysis completed!")
print("📁 Files generated:")
print("   • tutor_overlap_analysis_v7_fixed.csv (Enhanced CSV with up to 3 matches per tutor)")
print("   • tutor_overlap_simple_v7_fixed.txt (Simple text version)")
print("   • tutor_overlap_report_v7_fixed.html (Fixed HTML with proper sticky sidebar)")
print("\nKey fixes:")
print("• Fixed CSS conflict that was preventing sidebar from being sticky")
print("• Sidebar now stays in place while scrolling (like fa25_no_plt)")
print("• Maintains all V7 functionality (up to 3 matches per tutor)")
print("• Proper mobile responsiveness without breaking desktop sticky behavior")
print("\nCSS fix details:")
print("• Removed duplicate 'position: relative' that was overriding 'position: sticky'")
print("• Mobile media query now properly preserves sticky behavior on desktop")
print("• Sidebar maintains its position during scroll as intended")
