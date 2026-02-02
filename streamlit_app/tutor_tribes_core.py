"""
Core module for Tutor Tribes analysis.
Contains all the logic for analyzing tutor subject overlaps and generating reports.
"""

import pandas as pd
from collections import defaultdict
from typing import Dict, List, Set, Tuple, Optional


def load_tutor_data(
    csv_data: pd.DataFrame,
    exclude_list: List[str],
    bonus_courses: List[str]
) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Load and process tutor data from CSV.
    
    Args:
        csv_data: DataFrame with columns 'PageTitle' and 'FieldValue'
        exclude_list: List of tutor names to exclude
        bonus_courses: List of course codes that are bonus/extra courses
    
    Returns:
        Tuple of (person_subjects, person_bonus_subjects) dictionaries
    """
    person_subjects = defaultdict(set)
    person_bonus_subjects = defaultdict(set)
    
    for _, row in csv_data.iterrows():
        if pd.notna(row['FieldValue']) and row['PageTitle'] not in exclude_list:
            if row['FieldValue'] not in bonus_courses:
                person_subjects[row['PageTitle']].add(row['FieldValue'])
            else:
                person_bonus_subjects[row['PageTitle']].add(row['FieldValue'])
    
    return dict(person_subjects), dict(person_bonus_subjects)


def calculate_overlap(
    person1: str,
    person2: str,
    subjects_dict: Dict[str, Set[str]],
    bonus_subjects_dict: Dict[str, Set[str]]
) -> Tuple[float, int, List[str], List[str], List[str], List[str]]:
    """
    Calculate overlap score between two tutors.
    
    Args:
        person1: Name of first tutor
        person2: Name of second tutor
        subjects_dict: Dictionary mapping tutor names to sets of subjects
        bonus_subjects_dict: Dictionary mapping tutor names to sets of bonus subjects
    
    Returns:
        Tuple of (overlap_score, intersection_count, common_classes, 
                 missing_from_other, extra_in_other, bonus_in_common)
    """
    subjects1 = subjects_dict.get(person1, set())
    subjects2 = subjects_dict.get(person2, set())
    bonus1 = bonus_subjects_dict.get(person1, set())
    bonus2 = bonus_subjects_dict.get(person2, set())
    
    if len(subjects1) == 0:
        return 0.0, 0, [], [], [], []
    
    intersection = subjects1.intersection(subjects2)
    intersection_count = len(intersection)
    overlap_score = intersection_count / len(subjects1)
    
    # Calculate bonus subjects in common
    bonus_intersection = bonus1.intersection(bonus2)
    
    return (
        overlap_score,
        intersection_count,
        sorted(list(intersection)),
        sorted(list(subjects1 - subjects2)),
        sorted(list(subjects2 - subjects1)),
        sorted(list(bonus_intersection))
    )


def calculate_all_overlaps(
    person_subjects: Dict[str, Set[str]],
    person_bonus_subjects: Dict[str, Set[str]]
) -> Dict[str, Dict]:
    """
    Calculate overlaps for all tutors.
    
    Args:
        person_subjects: Dictionary mapping tutor names to sets of subjects
        person_bonus_subjects: Dictionary mapping tutor names to sets of bonus subjects
    
    Returns:
        Dictionary with tutor names as keys and overlap data as values
    """
    results = {}
    
    for person in person_subjects:
        overlaps = []
        
        for other_person in person_subjects:
            if person != other_person:
                score, intersection_count, common_classes, missing_from_other, extra_in_other, bonus_in_common = calculate_overlap(
                    person, other_person, person_subjects, person_bonus_subjects
                )
                
                overlaps.append({
                    'person': other_person,
                    'overlap_score': score,
                    'intersection_size': intersection_count,
                    'common_classes': common_classes,
                    'missing_from_other': missing_from_other,
                    'extra_in_other': extra_in_other,
                    'bonus_in_common': bonus_in_common
                })
        
        # Sort by overlap score (descending)
        overlaps.sort(key=lambda x: x['overlap_score'], reverse=True)
        
        results[person] = {
            'total_subjects': len(person_subjects[person]),
            'subjects': sorted(list(person_subjects[person])),
            'bonus_subjects': sorted(list(person_bonus_subjects[person])) if person in person_bonus_subjects else [],
            'all_overlaps': overlaps
        }
    
    return results


def perform_matching(
    results: Dict[str, Dict],
    max_matches_per_tutor: int = 4,
    min_overlap_threshold: float = 0.5,
    max_assignments_per_tutor: int = 5,
    special_tutors: Optional[List[str]] = None,
    tutor_majors: Optional[Dict[str, str]] = None,
    tutor_ece_courses: Optional[Dict[str, Set[str]]] = None,
    tutor_cs_courses: Optional[Dict[str, Set[str]]] = None
) -> Dict[str, Dict]:
    """
    Perform iterative matching with "weakest first" strategy.
    Prioritizes matches based on same ECE/CS courses for ECE/CS majors.
    
    Args:
        results: Dictionary from calculate_all_overlaps
        max_matches_per_tutor: Maximum number of matches to assign per tutor
        min_overlap_threshold: Minimum overlap score (0.0-1.0) to consider
        max_assignments_per_tutor: Maximum times a tutor can appear in others' match lists
        special_tutors: List of tutor names that get special handling
        tutor_majors: Dictionary mapping tutor name -> 'ECE', 'CS', or None
        tutor_ece_courses: Dictionary mapping tutor name -> set of ECE courses they teach
        tutor_cs_courses: Dictionary mapping tutor name -> set of CS courses they teach
    
    Returns:
        Dictionary with final match assignments
    """
    if special_tutors is None:
        special_tutors = []
    if tutor_majors is None:
        tutor_majors = {}
    if tutor_ece_courses is None:
        tutor_ece_courses = {}
    if tutor_cs_courses is None:
        tutor_cs_courses = {}
    
    tutor_assignments = defaultdict(int)
    final_results = {}
    
    # Calculate tutor priorities using "weakest first" strategy
    tutor_priorities = []
    for person in results:
        if results[person]['all_overlaps']:
            # Filter to only overlaps above threshold
            good_overlaps = [
                overlap for overlap in results[person]['all_overlaps']
                if overlap['overlap_score'] > min_overlap_threshold
            ]
            
            if good_overlaps:
                # Get the best score among good overlaps
                best_score = good_overlaps[0]['overlap_score']
                # Count how many good options they have
                good_options_count = len(good_overlaps)
                # Priority score: lower best score = higher priority (weaker tutors first)
                # Secondary: fewer good options = higher priority
                if person in special_tutors:
                    priority_score = 0.0
                else:
                    priority_score = (1.0 - best_score) + (1.0 / good_options_count)
                tutor_priorities.append((person, priority_score, best_score, good_options_count))
            else:
                # No good overlaps, lowest priority
                tutor_priorities.append((person, 999.0, 0.0, 0))
        else:
            tutor_priorities.append((person, 999.0, 0.0, 0))
    
    # Sort by priority score (ascending) - weakest tutors first
    tutor_priorities.sort(key=lambda x: x[1])
    
    # Initialize all tutors with empty match lists
    for person, _, _, _ in tutor_priorities:
        final_results[person] = {
            'total_subjects': results[person]['total_subjects'],
            'subjects': results[person]['subjects'],
            'bonus_subjects': results[person]['bonus_subjects'],
            'top_matches': [],
            'match_count': 0
        }
    
    # Pre-sort all_overlaps with boost applied for each tutor
    # This ensures same-course matches are prioritized from the start
    for person in results:
        current_tutor_major = tutor_majors.get(person, None)
        current_tutor_ece_courses = tutor_ece_courses.get(person, set())
        current_tutor_cs_courses = tutor_cs_courses.get(person, set())
        
        # Apply boost to all overlaps and re-sort
        boosted_overlaps = []
        for overlap in results[person]['all_overlaps']:
            priority_boost = 0.0
            potential_match = overlap['person']
            
            # For ECE tutors: boost if potential match teaches any of the same ECE courses
            if current_tutor_major == 'ECE' and current_tutor_ece_courses:
                potential_match_ece_courses = tutor_ece_courses.get(potential_match, set())
                if current_tutor_ece_courses.intersection(potential_match_ece_courses):
                    priority_boost = 100.0
            
            # For CS tutors: boost if potential match teaches any of the same CS courses
            elif current_tutor_major == 'CS' and current_tutor_cs_courses:
                potential_match_cs_courses = tutor_cs_courses.get(potential_match, set())
                if current_tutor_cs_courses.intersection(potential_match_cs_courses):
                    priority_boost = 100.0
            
            # Create boosted overlap
            boosted_overlap = overlap.copy()
            boosted_overlap['boosted_score'] = overlap['overlap_score'] + priority_boost
            boosted_overlaps.append(boosted_overlap)
        
        # Sort by boosted score (descending), then by original overlap score
        boosted_overlaps.sort(key=lambda x: (x['boosted_score'], x['overlap_score']), reverse=True)
        
        # Replace all_overlaps with the boosted and sorted version
        results[person]['all_overlaps'] = boosted_overlaps
    
    # Special handling for special tutors
    # Note: all_overlaps is already pre-sorted by boosted_score, so same-course matches come first
    for person in special_tutors:
        if person in results:
            data = results[person]
            
            good_overlaps = []
            for overlap in data['all_overlaps']:
                # Get the boosted score (set during pre-sorting)
                boosted_score = overlap.get('boosted_score', overlap['overlap_score'])
                
                # For same-course matches (boosted), allow slightly lower overlap scores
                # This ensures ECE/CS tutors can match with others who teach the same courses
                is_boosted = boosted_score > overlap['overlap_score']
                threshold_to_use = min_overlap_threshold * 0.5 if is_boosted else min_overlap_threshold
                
                if overlap['overlap_score'] > threshold_to_use:
                    # Use the pre-calculated boosted_score (set during pre-sorting)
                    boosted_overlap = overlap.copy()
                    if 'boosted_score' not in boosted_overlap:
                        boosted_overlap['boosted_score'] = overlap['overlap_score']
                    good_overlaps.append(boosted_overlap)
            
            # Sort by boosted score, then by original overlap score
            # (This maintains the pre-sorted order but ensures consistency)
            good_overlaps.sort(key=lambda x: (x['boosted_score'], x['overlap_score']), reverse=True)
            
            if good_overlaps:
                # Assign ALL good matches immediately (prioritizing same-course matches)
                for match in good_overlaps:
                    if (tutor_assignments[match['person']] < max_assignments_per_tutor
                        and len(final_results[person]['top_matches']) < max_matches_per_tutor):
                        final_results[person]['top_matches'].append(match)
                        tutor_assignments[match['person']] += 1
                
                # Update final results
                final_results[person]['match_count'] = len(final_results[person]['top_matches'])
    
    # Iterative matching: multiple passes to ensure even distribution
    for pass_num in range(1, max_matches_per_tutor + 1):
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
            
            # Get current tutor's major and courses
            current_tutor_major = tutor_majors.get(person, None)
            current_tutor_ece_courses = tutor_ece_courses.get(person, set())
            current_tutor_cs_courses = tutor_cs_courses.get(person, set())
            
            # Look for available tutors
            # Note: all_overlaps is already pre-sorted by boosted_score from the pre-sorting step
            for overlap in data['all_overlaps']:
                potential_match = overlap['person']
                
                # Get the boosted score (set during pre-sorting)
                boosted_score = overlap.get('boosted_score', overlap['overlap_score'])
                
                # Check if this tutor is available and meets criteria
                # For same-course matches (boosted), allow slightly lower overlap scores
                # This ensures ECE/CS tutors can match with others who teach the same courses
                is_boosted = boosted_score > overlap['overlap_score']
                threshold_to_use = min_overlap_threshold * 0.7 if is_boosted else min_overlap_threshold
                
                if (tutor_assignments[potential_match] < max_assignments_per_tutor and
                    overlap['overlap_score'] > threshold_to_use and
                    potential_match not in [m['person'] for m in current_matches]):
                    
                    # Use the pre-calculated boosted_score
                    boosted_overlap = overlap.copy()
                    if 'boosted_score' not in boosted_overlap:
                        boosted_overlap['boosted_score'] = overlap['overlap_score']
                    available_matches.append(boosted_overlap)
            
            # Sort available matches by boosted score (descending), then by original overlap score
            available_matches.sort(key=lambda x: (x['boosted_score'], x['overlap_score']), reverse=True)
            
            # Take the best available match for this pass
            if available_matches:
                best_match = available_matches[0]
                current_matches.append(best_match)
                
                # Mark this tutor as assigned
                tutor_assignments[best_match['person']] += 1
                
                # Update final results
                final_results[person]['top_matches'] = current_matches
                final_results[person]['match_count'] = len(current_matches)
    
    return final_results


def generate_csv_report(final_results: Dict[str, Dict]) -> pd.DataFrame:
    """
    Generate CSV report from final results.
    
    Args:
        final_results: Dictionary from perform_matching
    
    Returns:
        DataFrame with CSV report data
    """
    csv_rows = []
    
    for person in sorted(final_results.keys()):
        data = final_results[person]
        
        # Add main person info
        csv_rows.append({
            'Tutor': person,
            'Total_Subjects': data['total_subjects'],
            'All_Subjects': '; '.join(data['subjects']),
            'Bonus_Subjects': '; '.join(data['bonus_subjects']) if data['bonus_subjects'] else 'None',
            'Number_of_Matches': data['match_count'],
            'Match_Type': 'MAIN_TUTOR',
            'Classes_in_Common': '',
            'Classes_Both_Tutors_Have': '',
            'Extra_Subjects_in_Common': '',
            'Classes_Missing_from_Match': '',
            'Classes_Match_Has_Extra': ''
        })
        
        # Add match info
        for i, match in enumerate(data['top_matches'], 1):
            csv_rows.append({
                'Tutor': f"  {i}. {match['person']}",
                'Total_Subjects': match['intersection_size'],
                'All_Subjects': f"Overlap: {match['overlap_score']:.1%}",
                'Classes_in_Common': match['intersection_size'],
                'Classes_Both_Tutors_Have': '; '.join(match['common_classes']) if match['common_classes'] else 'None',
                'Extra_Subjects_in_Common': '; '.join(match['bonus_in_common']) if match['bonus_in_common'] else 'None',
                'Classes_Missing_from_Match': '; '.join(match['missing_from_other']) if match['missing_from_other'] else 'None',
                'Classes_Match_Has_Extra': '; '.join(match['extra_in_other']) if match['extra_in_other'] else 'None',
                'Bonus_Subjects': '',
                'Number_of_Matches': '',
                'Match_Type': 'MATCH'
            })
        
        # Add separator row
        csv_rows.append({
            'Tutor': '',
            'Total_Subjects': '',
            'All_Subjects': '',
            'Bonus_Subjects': '',
            'Number_of_Matches': '',
            'Match_Type': 'SEPARATOR',
            'Classes_in_Common': '',
            'Classes_Both_Tutors_Have': '',
            'Extra_Subjects_in_Common': '',
            'Classes_Missing_from_Match': '',
            'Classes_Match_Has_Extra': ''
        })
    
    return pd.DataFrame(csv_rows)


def generate_text_report(final_results: Dict[str, Dict]) -> str:
    """
    Generate plain text report from final results.
    
    Args:
        final_results: Dictionary from perform_matching
    
    Returns:
        String containing text report
    """
    text_content = "TUTOR SUBJECT OVERLAP ANALYSIS\n"
    text_content += "=" * 80 + "\n\n"
    text_content += "This analysis shows which tutors can best cover for each other.\n"
    text_content += "Overlap score = (shared subjects) / (total subjects of first tutor)\n\n"
    
    for person in sorted(final_results.keys()):
        data = final_results[person]
        text_content += f"TUTOR: {person}\n"
        text_content += f"Total Subjects: {data['total_subjects']}\n"
        text_content += f"All Subjects: {', '.join(data['subjects'])}\n"
        if data['bonus_subjects']:
            text_content += f"Extra Subjects: {', '.join(data['bonus_subjects'])}\n"
        text_content += f"Number of Matches: {data['match_count']}\n\n"
        
        if data['match_count'] == 0:
            text_content += "NO MATCHES AVAILABLE - All potential matches were at their limit.\n\n"
        else:
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
        
        text_content += "-" * 80 + "\n\n"
    
    return text_content


def generate_html_report(final_results: Dict[str, Dict]) -> str:
    """
    Generate HTML report from final results.
    
    Args:
        final_results: Dictionary from perform_matching
    
    Returns:
        String containing HTML report
    """
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
        .bonus-subjects-list {
            background-color: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #ffc107;
        }
        .bonus-subjects-title {
            font-weight: bold;
            color: #856404;
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
        .common-classes-box {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-left: 4px solid #28a745;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        .common-classes-title {
            font-weight: bold;
            color: #155724;
            margin-bottom: 5px;
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
                <h1>📚 Tutor Subject Overlap Analysis</h1>
                
                <div class="instructions">
                    <h3>📖 How to Use This Report</h3>
                    <ul>
                        <li><strong>Overlap Scores:</strong> Green badges show what percentage of subjects another tutor can cover</li>
                        <li><strong>100% Score:</strong> Means that tutor can cover ALL subjects of the first tutor</li>
                        <li><strong>Core Subjects:</strong> Regular courses used for overlap calculations</li>
                        <li><strong>Extra Subjects:</strong> Specialized courses that tutors have in common</li>
                    </ul>
                </div>
            </div>
"""
    
    # Add each person's section
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
                        <p class="person-stats">Total Subjects: {data['total_subjects']} | Matches Found: {data['match_count']}</p>
                    </div>
                </div>
                
                <div class="person-content">
                    <div class="subjects-list">
                        <div class="subjects-title">📚 Core Subjects:</div>
                        {', '.join(data['subjects'])}
                    </div>
"""
        
        if data['bonus_subjects']:
            html_content += f"""
            <div class="bonus-subjects-list">
                <div class="bonus-subjects-title">⭐ Extra Subjects:</div>
                {', '.join(data['bonus_subjects'])}
            </div>
"""
        
        html_content += f"""
                    <h3>🔗 Top Matches:</h3>
"""
        
        if data['match_count'] == 0:
            html_content += f"""
                        <div class="no-matches">
                            ⚠️ NO MATCHES AVAILABLE - All potential matches were at their limit.
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
                            
                            <div class="common-classes-box">
                                <div class="common-classes-title">🎯 Core Subjects in Common ({match['intersection_size']}):</div>
                                <div class="classes-list">
                                    {', '.join(match['common_classes']) if match['common_classes'] else '<span class="no-classes">None</span>'}
                                </div>
                            </div>
"""
                
                if match['bonus_in_common']:
                    html_content += f"""
                            <div class="bonus-subjects-list">
                                <div class="bonus-subjects-title">⭐ Extra Subjects in Common ({len(match['bonus_in_common'])}):</div>
                                <div class="classes-list">
                                    {', '.join(match['bonus_in_common'])}
                                </div>
                            </div>
"""
                
                html_content += f"""
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
    
    return html_content

