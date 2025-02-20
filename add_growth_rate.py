import pandas as pd

def add_growth_rate(file_path):
    """
    Add year-over-year growth rate column for each degree field and education level
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Sort by year, degree, education-level, and university to ensure proper calculation
    df = df.sort_values(['year', 'degree', 'education-level', 'university'])
    
    # Group by year, degree, and education-level to get total graduates per field per year
    yearly_totals = df.groupby(['year', 'degree', 'education-level'])['overall-aggregate'].sum().reset_index()
    
    # Calculate year-over-year growth rate starting from 2018
    yearly_totals['prev_year_total'] = yearly_totals.groupby(['degree', 'education-level'])['overall-aggregate'].shift(1)
    yearly_totals['growth_rate'] = ((yearly_totals['overall-aggregate'] - yearly_totals['prev_year_total']) / 
                                   yearly_totals['prev_year_total'] * 100).round(2)
    
    # Handle division by zero and missing values
    yearly_totals['growth_rate'] = yearly_totals['growth_rate'].replace([float('inf'), -float('inf')], None)
    
    # Filter out years before 2018
    yearly_totals = yearly_totals[yearly_totals['year'] >= 2018]
    
    # Create a dictionary to map the growth rates back to original dataframe
    growth_rates = yearly_totals.set_index(['year', 'degree', 'education-level'])['growth_rate'].to_dict()
    
    # Add growth rate column to original dataframe
    df['yoy_growth_rate'] = df.apply(lambda row: growth_rates.get((row['year'], row['degree'], row['education-level']), None), axis=1)
    
    # Save changes back to file
    df.to_csv(file_path, index=False)
    
    # Print summary of growth rates by year, degree, and education level
    print("\nYear-over-Year Growth Rates by Degree Field and Education Level:")
    summary = yearly_totals[yearly_totals['growth_rate'].notna()].sort_values(['year', 'degree', 'education-level'])
    for _, row in summary.iterrows():
        print(f"{row['year']} - {row['degree']} ({row['education-level']}): {row['growth_rate']}%")

if __name__ == "__main__":
    file_path = "public-unis-aggregate-data-coordinates.csv"
    add_growth_rate(file_path)