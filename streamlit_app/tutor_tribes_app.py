"""
Streamlit web application for Tutor Tribes analysis.
Allows non-technical users to upload CSV files and generate tutor overlap reports.
"""

import streamlit as st
import pandas as pd
from tutor_tribes_core import (
    load_tutor_data,
    calculate_all_overlaps,
    perform_matching,
    generate_csv_report,
    generate_text_report,
    generate_html_report
)

# Page configuration
st.set_page_config(
    page_title="Tutor Tribes Analysis",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS to ensure proper scrolling
st.markdown("""
    <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stExpander {
            margin-bottom: 1rem;
        }
        iframe {
            border: 1px solid #ccc;
            border-radius: 5px;
        }
    </style>
    """, unsafe_allow_html=True)

# Default configuration
DEFAULT_EXCLUDE_LIST = [
    'Emma', 'Adelaide', 'Regina', 'Anthony', 'Geo', 'Lucy P.',
    'Maya', 'Grace', 'Lydia', 'Meredith', 'Rohan', 'Clive', 'Sophia', 'Noah',
    'Lucy', 'Maria', 'Jacob', 'Gabe', 'Kristie', 'Lukas', 'Pat', 'Sarah', 'Yash'
]

DEFAULT_BONUS_COURSES = [
    'AE 140', 'AE 202', 'AE 311', 'AE 321', 'AE 323', 'AE 352',
    'BIOE 202', 'BIOE 206', 'BIOE 210', 'BIOE 302', 'BIOE 303', 'BIOE 360', 'BIOE 414', 'CS 124',
    'CS 128', 'CS 173', 'CS 225', 'CS 233', 'CS 340', 'CS 361', 'CS 374',
    'ECE 310', 'ECE 313', 'ECE 329', 'ECE 342', 'ECE 374', 'ECE 385',
    'ECE 391', 'IE 300', 'IE 310', 'MATH 347', 'MCB 450', 'ME 170', 'ME 200',
    'ME 270', 'ME 310', 'ME 330', 'ME 340', 'MSE 201', 'MSE 206', 'ME 360', 'ME 370',
    'MSE 280', 'NPRE 200', 'NPRE 247', 'NPRE 321', 'NPRE 330',
    'NPRE 349', 'STAT 400', 'PHYS 326', 'PHYS 370', 'TAM 335',
    'CHEM 312'
]

DEFAULT_SPECIAL_TUTORS = ['Jiya', 'Johail', 'Diego', 'Aman', 'Amy']

def parse_list_input(text: str) -> list:
    """Parse comma or newline-separated list from text input."""
    if not text or not text.strip():
        return []
    # Split by comma or newline, strip whitespace, filter empty strings
    items = [item.strip() for item in text.replace('\n', ',').split(',') if item.strip()]
    return items


def main():
    """Main application function."""
    st.title("📚 Tutor Tribes Analysis")
    st.markdown("Upload a CSV file with tutor data to generate overlap analysis reports.")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.subheader("File Upload")
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=['csv'],
            help="Upload a CSV file with columns: PageTitle, FieldValue"
        )
        
        st.subheader("Analysis Settings")
        max_matches = st.slider(
            "Max matches per tutor",
            min_value=1,
            max_value=10,
            value=4,
            help="Maximum number of matches to assign to each tutor"
        )
        
        min_overlap = st.slider(
            "Minimum overlap threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.5,
            step=0.1,
            format="%.1f",
            help="Minimum overlap score (0.0-1.0) required for a match"
        )
        
        max_assignments = st.slider(
            "Max assignments per tutor",
            min_value=1,
            max_value=10,
            value=5,
            help="Maximum times a tutor can appear in others' match lists"
        )
        
        # Configuration sections that need CSV data will be shown after file upload
        st.info("💡 Upload a CSV file to configure exclude list and bonus courses")
    
    # Main content area
    if uploaded_file is not None:
        try:
            # Load and preview data
            df = pd.read_csv(uploaded_file)
            
            # Validate required columns
            required_columns = ['PageTitle', 'FieldValue']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                st.error(f"❌ Missing required columns: {', '.join(missing_columns)}")
                st.info("Your CSV file must have columns named 'PageTitle' and 'FieldValue'")
                return
            
            # Extract unique values for configuration
            all_tutors = sorted(df['PageTitle'].dropna().unique().tolist())
            all_courses = sorted(df['FieldValue'].dropna().unique().tolist())
            
            # Store in session state so sidebar can access
            st.session_state['all_tutors'] = all_tutors
            st.session_state['all_courses'] = all_courses
            
            # Show data preview
            with st.expander("📊 Preview uploaded data", expanded=False):
                st.dataframe(df.head(20))
                st.caption(f"Total rows: {len(df)} | Unique tutors: {len(all_tutors)} | Unique courses: {len(all_courses)}")
            
            # Configuration sections in sidebar (now that we have data)
            with st.sidebar:
                st.markdown("---")
                st.subheader("📋 Exclude List")
                st.caption("Select tutors to exclude from analysis")
                
                # Initialize default excludes in session state (only once per file)
                exclude_key = f'exclude_list_{uploaded_file.name}'
                if exclude_key not in st.session_state:
                    # Pre-select default excludes that exist in the data
                    default_excludes = [t for t in DEFAULT_EXCLUDE_LIST if t in all_tutors]
                    st.session_state[exclude_key] = default_excludes
                
                exclude_list = st.multiselect(
                    "Select tutors to exclude",
                    options=all_tutors,
                    default=st.session_state.get(exclude_key, []),
                    key="exclude_multiselect",
                    help="Select one or more tutors to exclude from the analysis"
                )
                
                # Update session state when selection changes
                st.session_state[exclude_key] = exclude_list
                
                # Quick select buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Select All", key="exclude_select_all"):
                        st.session_state[exclude_key] = all_tutors
                        st.rerun()
                with col2:
                    if st.button("Clear All", key="exclude_clear_all"):
                        st.session_state[exclude_key] = []
                        st.rerun()
                
                st.markdown("---")
                st.subheader("📚 Core Courses")
                st.caption("Select courses that are considered 'core' (unselected courses will be treated as bonus)")
                
                # Initialize default core courses in session state (only once per file)
                # Default core courses = all courses EXCEPT the default bonus courses
                core_key = f'core_courses_{uploaded_file.name}'
                if core_key not in st.session_state:
                    # Pre-select all courses EXCEPT the default bonus courses
                    default_bonus = [c for c in DEFAULT_BONUS_COURSES if c in all_courses]
                    default_core = [c for c in all_courses if c not in default_bonus]
                    st.session_state[core_key] = default_core
                
                core_courses = st.multiselect(
                    "Select core courses",
                    options=all_courses,
                    default=st.session_state.get(core_key, []),
                    key="core_multiselect",
                    help="Selected courses are core courses. Unselected courses will be treated as bonus/extra courses"
                )
                
                # Update session state when selection changes
                st.session_state[core_key] = core_courses
                
                # Calculate bonus courses (all courses not selected as core)
                bonus_courses = [c for c in all_courses if c not in core_courses]
                
                # Show count of bonus courses
                if bonus_courses:
                    st.info(f"📊 {len(bonus_courses)} course(s) will be treated as bonus: {', '.join(bonus_courses[:5])}{'...' if len(bonus_courses) > 5 else ''}")
                
                # Quick select buttons for core courses
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Select Defaults", key="core_select_defaults"):
                        # Default = all courses except default bonus courses
                        default_bonus = [c for c in DEFAULT_BONUS_COURSES if c in all_courses]
                        default_core = [c for c in all_courses if c not in default_bonus]
                        st.session_state[core_key] = default_core
                        st.rerun()
                with col2:
                    if st.button("Select All", key="core_select_all"):
                        st.session_state[core_key] = all_courses
                        st.rerun()
                
                st.markdown("---")
                st.subheader("🎯 Special Tutors")
                st.caption("Tutors that get special matching treatment")
                
                # Initialize default special tutors in session state (only once per file)
                special_key = f'special_tutors_{uploaded_file.name}'
                if special_key not in st.session_state:
                    # Pre-select default special tutors that exist in the data
                    default_special = [t for t in DEFAULT_SPECIAL_TUTORS if t in all_tutors]
                    st.session_state[special_key] = default_special
                
                special_tutors = st.multiselect(
                    "Select special tutors",
                    options=all_tutors,
                    default=st.session_state.get(special_key, []),
                    key="special_multiselect",
                    help="These tutors will get priority matching if they have few good options"
                )
                
                # Update session state when selection changes
                st.session_state[special_key] = special_tutors
            
            # Generate button
            if st.button("🚀 Generate Analysis", type="primary", use_container_width=True):
                with st.spinner("Processing data..."):
                    try:
                        # Load tutor data
                        person_subjects, person_bonus_subjects = load_tutor_data(
                            df, exclude_list, bonus_courses
                        )
                        
                        if not person_subjects:
                            st.error("❌ No tutors found after applying exclude list. Please check your configuration.")
                            return
                        
                        st.success(f"✅ Loaded {len(person_subjects)} tutors")
                        
                        # Calculate overlaps
                        with st.spinner("Calculating overlaps..."):
                            results = calculate_all_overlaps(person_subjects, person_bonus_subjects)
                        
                        # Perform matching
                        with st.spinner("Performing matching..."):
                            final_results = perform_matching(
                                results,
                                max_matches_per_tutor=max_matches,
                                min_overlap_threshold=min_overlap,
                                max_assignments_per_tutor=max_assignments,
                                special_tutors=special_tutors
                            )
                        
                        # Store results in session state
                        st.session_state['final_results'] = final_results
                        st.session_state['analysis_complete'] = True
                        
                        st.success("✅ Analysis complete!")
                        
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                        st.exception(e)
                        return
            
            # Display results if analysis is complete
            if st.session_state.get('analysis_complete', False):
                final_results = st.session_state.get('final_results')
                
                if final_results:
                    # Summary statistics
                    st.header("📈 Summary Statistics")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    total_tutors = len(final_results)
                    tutors_with_matches = sum(1 for r in final_results.values() if r['match_count'] > 0)
                    total_matches = sum(r['match_count'] for r in final_results.values())
                    avg_matches = total_matches / total_tutors if total_tutors > 0 else 0
                    
                    with col1:
                        st.metric("Total Tutors", total_tutors)
                    with col2:
                        st.metric("Tutors with Matches", tutors_with_matches)
                    with col3:
                        st.metric("Total Matches", total_matches)
                    with col4:
                        st.metric("Avg Matches per Tutor", f"{avg_matches:.1f}")
                    
                    # Generate reports
                    st.header("📄 Generated Reports")
                    st.markdown("---")  # Visual separator
                    
                    # HTML Report
                    st.subheader("🌐 HTML Report")
                    html_content = generate_html_report(final_results)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download HTML Report",
                        data=html_content,
                        file_name="tutor_overlap_report.html",
                        mime="text/html",
                        use_container_width=True
                    )
                    st.caption("💡 Tip: After downloading, you can open the HTML file in any web browser for the best viewing experience")
                    
                    # Preview HTML in expander
                    with st.expander("👁️ Preview HTML Report (Scroll within preview window)", expanded=False):
                        st.info("💡 Tip: Use 'Open in New Tab' button above for better scrolling experience")
                        st.components.v1.html(html_content, height=1000, scrolling=True)
                    
                    st.markdown("---")  # Visual separator
                    
                    # CSV Report
                    st.subheader("📊 CSV Report")
                    csv_df = generate_csv_report(final_results)
                    csv_string = csv_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV Report",
                        data=csv_string,
                        file_name="tutor_overlap_analysis.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                    
                    # Preview CSV - use full dataframe with configurable height
                    with st.expander("👁️ Preview CSV Report", expanded=False):
                        st.dataframe(csv_df, use_container_width=True, height=400)
                    
                    st.markdown("---")  # Visual separator
                    
                    # Text Report
                    st.subheader("📝 Text Report")
                    text_content = generate_text_report(final_results)
                    st.download_button(
                        label="📥 Download Text Report",
                        data=text_content,
                        file_name="tutor_overlap_analysis.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                    
                    # Preview text
                    with st.expander("👁️ Preview Text Report", expanded=False):
                        st.text(text_content[:5000] + "..." if len(text_content) > 5000 else text_content)
                    
                    st.markdown("---")  # Visual separator
                    
                    # Detailed results table
                    st.header("🔍 Detailed Results")
                    
                    # Create a searchable/filterable table
                    results_data = []
                    for person, data in sorted(final_results.items()):
                        results_data.append({
                            'Tutor': person,
                            'Total Subjects': data['total_subjects'],
                            'Bonus Subjects': len(data['bonus_subjects']),
                            'Matches Found': data['match_count']
                        })
                    
                    results_df = pd.DataFrame(results_data)
                    
                    # Search/filter
                    search_term = st.text_input("🔍 Search tutors", "")
                    if search_term:
                        results_df = results_df[results_df['Tutor'].str.contains(search_term, case=False, na=False)]
                    
                    st.dataframe(results_df, use_container_width=True)
                    
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.exception(e)
    else:
        # Instructions when no file is uploaded
        st.info("👆 Please upload a CSV file to get started")
        
        st.markdown("""
        ### 📋 Expected CSV Format
        
        Your CSV file should have the following columns:
        - **PageTitle**: The name of the tutor
        - **FieldValue**: The subject/course code
        
        Example:
        ```
        PageTitle,FieldValue
        John Doe,CS 101
        John Doe,MATH 241
        Jane Smith,CS 101
        Jane Smith,PHYS 211
        ```
        
        ### 🎯 How It Works
        
        1. **Upload** your CSV file using the file uploader in the sidebar
        2. **Configure** the analysis settings (optional - defaults are provided)
        3. **Click** "Generate Analysis" to process the data
        4. **Download** the generated reports (HTML, CSV, or TXT)
        
        ### 💡 Tips
        
        - The exclude list lets you remove certain tutors from the analysis
        - Bonus courses are tracked separately and shown as "extra subjects"
        - Special tutors get priority matching if they have few good options
        - Adjust the overlap threshold to be more or less strict about matches
        """)


if __name__ == "__main__":
    # Initialize session state
    if 'analysis_complete' not in st.session_state:
        st.session_state['analysis_complete'] = False
    if 'final_results' not in st.session_state:
        st.session_state['final_results'] = None
    
    main()

