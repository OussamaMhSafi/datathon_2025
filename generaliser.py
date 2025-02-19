import pandas as pd
import re

def clean_degree_name(degree):
    """Clean and standardize degree names"""
    if pd.isna(degree):
        return "Pre-University Diploma"  # Default category for empty values
    return str(degree).strip().lower()

def generalize_degrees(input_file, output_file):
    """
    Generalize degrees using pattern matching to map to standardized categories
    """
    df = pd.read_csv(input_file)
    
    # Clean degree names
    df['degree'] = df['degree'].apply(clean_degree_name)
    
    # Define mapping rules with specific categories
    degree_categories = {
        # Pre-University and Professional Diplomas
        lambda x: any(term in x for term in ['community college', 'emergency & safety', 'aeronautical', 'pre-university']): 'Pre-University Diploma',
        lambda x: ('diploma' in x or 'early childhood' in x or 'jossor institute' in x) and not any(term in x for term in ['pre-university']): 'Professional Diploma',
        
        # Bachelor's level
        lambda x: ('bachelor' in x or 'b.a' in x or 'b.sc' in x) and any(term in x for term in ['art', 'language', 'literature', 'science']) and not any(term in x for term in ['engineering', 'computer', 'health', 'medical', 'business']): 'Bachelor of Arts',
        lambda x: any(term in x for term in ['engineering', 'technology', 'telecommunications', 'mechanical', 'electrical', 'chemical', 'maintenance']): 'Engineering & Technology',
        lambda x: any(term in x for term in ['business', 'economics', 'administration', 'accounting', 'finance', 'marketing', 'management', 'logistics']): 'Business & Economics',
        lambda x: any(term in x for term in ['health', 'medical', 'medicine', 'pharmacy', 'dental', 'nursing', 'radiography', 'respiratory', 'paramedicine', 'biomedical']): 'Medical & Health Sciences',
        lambda x: ('law' in x or 'legal' in x): 'Law & Legal Studies',
        lambda x: 'education' in x: 'Education',
        lambda x: any(term in x for term in ['islamic', 'sharia', 'fiqh', 'quranic', 'religions']): 'Islamic Studies',
        lambda x: any(term in x for term in ['computer', 'computing', 'information', 'cyber']): 'Computer & Information Sciences',
        
        # Master's level
        lambda x: 'master' in x and any(term in x for term in ['business', 'mba', 'economics', 'accounting', 'marketing', 'management']): 'MBA & Economics',
        lambda x: 'master' in x and any(term in x for term in ['engineering', 'mechanical', 'electrical', 'civil']): 'Master of Engineering',
        lambda x: 'master' in x and 'education' in x: 'Master of Education',
        lambda x: 'master' in x and any(term in x for term in ['science', 'biology', 'chemistry', 'physics', 'environmental', 'computing', 'health', 'medical']): 'Master of Science',
        lambda x: 'master' in x and any(term in x for term in ['art', 'language', 'literature', 'gulf']): 'Master of Arts',
        
        # Doctorate level
        lambda x: ('ph.d' in x or 'doctorate' in x) and any(term in x for term in ['engineering', 'mechanical', 'electrical']): 'PhD in Engineering',
        lambda x: ('ph.d' in x or 'doctorate' in x) and any(term in x for term in ['science', 'physics', 'chemistry', 'biology', 'computing', 'computer', 'environmental']): 'PhD in Sciences',
        lambda x: ('ph.d' in x or 'doctorate' in x): 'Other Doctorate Programs'  # Catch remaining doctorates
    }
    
    def map_degree(degree):
        """Maps individual degree names to broader categories"""
        # First try exact matches
        for rule, category in degree_categories.items():
            if rule(degree):
                return category
                
        # If no match found, use education level to provide basic categorization
        if 'master' in degree:
            return 'Master of Science'  # Default for unmatched masters
        elif 'ph.d' in degree or 'doctorate' in degree:
            return 'Other Doctorate Programs'
        elif 'bachelor' in degree or 'b.' in degree:
            return 'Bachelor of Arts'  # Default for unmatched bachelors
        elif 'diploma' in degree:
            return 'Professional Diploma'
        else:
            return 'Pre-University Diploma'  # Default category
    
    # Apply the mapping
    df['degree'] = df['degree'].apply(map_degree)
    
    # Save the modified dataframe
    df.to_csv(output_file, index=False)
    
    # Print summary statistics
    print("\nDegree distribution after generalization:")
    print(df['degree'].value_counts())
    print(f"\nTotal number of unique degree categories: {df['degree'].nunique()}")

if __name__ == "__main__":
    input_file = "public-unis-aggregate-data.csv"
    output_file = "public-unis-aggregate-data-generalised.csv"
    generalize_degrees(input_file, output_file)