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

# Create enhanced CSV output with missing classes
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
    
    # Add match info with missing classes
    for i, match in enumerate(data['top_matches'], 1):
        csv_rows.append({
            'Tutor': f"  {i}. {match['person']}",
            'Total_Subjects': match['intersection_size'],
            'All_Subjects': f"Overlap: {match['overlap_score']:.1%}",
            'Classes_in_Common': match['intersection_size'],
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
        'Classes_Missing_from_Match': '',
        'Classes_Match_Has_Extra': '',
        'Match_Type': 'SEPARATOR'
    })

# Create DataFrame and save to CSV
csv_df = pd.DataFrame(csv_rows)
csv_df.to_csv('tutor_overlap_analysis_enhanced.csv', index=False)

# Create a simple text version for maximum accessibility
text_content = "TUTOR SUBJECT OVERLAP ANALYSIS\n"
text_content += "=" * 50 + "\n\n"
text_content += "This analysis shows which tutors can best cover for each other.\n"
text_content += "Overlap score = (shared subjects) / (total subjects of first tutor)\n\n"

for person in sorted(results.keys()):
    data = results[person]
    text_content += f"TUTOR: {person}\n"
    text_content += f"Total Subjects: {data['total_subjects']}\n"
    text_content += f"All Subjects: {', '.join(sorted(data['subjects']))}\n"
    text_content += f"Number of Matches: {data['match_count']}\n\n"
    
    if data['match_count'] > 5:
        text_content += f"NOTE: {data['match_count']} tutors have the same overlap score.\n"
        text_content += "All are shown below as they provide equally good coverage.\n\n"
    
    text_content += "TOP MATCHES:\n"
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
    
    text_content += "-" * 50 + "\n\n"

# Save the text version
with open('tutor_overlap_simple.txt', 'w', encoding='utf-8') as f:
    f.write(text_content)

# Create HTML report with collapsible sidebar, sections starting closed, and auto-open navigation
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
            position: relative;
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
            padding: 8px 16px;
            background-color: #c3e6cb;
            border-radius: 5px;
            display: inline-block;
            margin-top: 10px;
        }
        .download-links a:hover {
            background-color: #a8e6cf;
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
        .tie-note {
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
            font-style: italic;
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
for person in sorted(results.keys()):
    html_content += f'                <li class="toc-item"><a href="#{person.replace(" ", "-")}" onclick="navigateToSection(\'{person.replace(" ", "-")}\')">{person}</a></li>\n'

html_content += """
            </ul>
        </div>
        
        <div class="main-content" id="main-content">
            <div class="header">
                <h1>📚 Tutor Subject Overlap Analysis</h1>
                
                <div class="instructions">
                    <h3>📖 How to Use This Report</h3>
                    <ul>
                        <li><strong>Sidebar Navigation:</strong> Use the left sidebar to jump to any tutor (automatically opens section)</li>
                        <li><strong>Collapsible Sidebar:</strong> Click the red ◀ button to collapse/expand the sidebar</li>
                        <li><strong>Collapsible Sections:</strong> All sections start closed - click tutor headers to open</li>
                        <li><strong>Expand/Collapse All:</strong> Use buttons in sidebar to control all sections at once</li>
                        <li><strong>Overlap Scores:</strong> Green badges show what percentage of subjects another tutor can cover</li>
                        <li><strong>100% Score:</strong> Means that tutor can cover ALL subjects of the first tutor</li>
                        <li><strong>Ties:</strong> If more than 5 tutors have the same score, all are shown</li>
                    </ul>
                </div>
                
                <div class="download-links">
                    <strong>📥 Download Options:</strong><br>
                    <a href="tutor_overlap_analysis_enhanced.csv">📊 Enhanced Excel/CSV Version</a>
                    <a href="tutor_overlap_simple.txt">📝 Simple Text Version</a>
                </div>
            </div>
"""

# Add each person's section (starting collapsed)
for person in sorted(results.keys()):
    data = results[person]
    
    html_content += f"""
            <div class="person-section" id="{person.replace(' ', '-')}">
                <div class="person-header" onclick="toggleSection(this)">
                    <div>
                        <h2 class="person-name">
                            {person}
                            <span class="collapse-icon">▶</span>
                        </h2>
                        <p class="person-stats">Total Subjects: {data['total_subjects']} | Matches Found: {data['match_count']}</p>
                    </div>
                </div>
                
                <div class="person-content">
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
with open('tutor_overlap_report_v5_fixed.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Fixed version with visible sidebar toggle button completed!")
print("📁 Files generated:")
print("   • tutor_overlap_analysis_enhanced.csv (Enhanced CSV with missing classes)")
print("   • tutor_overlap_simple.txt (Simple text version)")
print("   • tutor_overlap_report_v5_fixed.html (Fixed HTML with visible sidebar toggle)")
print("\nKey fixes:")
print("• Made sidebar toggle button clearly visible (red color)")
print("• Increased button size (50x50px)")
print("• Better positioning and z-index")
print("• Added hover effects and shadows")
print("• Updated instructions to mention the red button")
print("• All other features working as expected")

