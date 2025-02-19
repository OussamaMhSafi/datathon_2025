import pandas as pd

def add_growth_rate(file_path):
    """
    Add year-over-year growth rate column for each degree field
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Sort by year, degree, and university to ensure proper calculation
    df = df.sort_values(['year', 'degree', 'university'])
    
    # Group by year, degree to get total graduates per field per year
    yearly_totals = df.groupby(['year', 'degree'])['overall-aggregate'].sum().reset_index()
    
    # Calculate year-over-year growth rate
    yearly_totals['prev_year_total'] = yearly_totals.groupby('degree')['overall-aggregate'].shift(1)
    yearly_totals['growth_rate'] = ((yearly_totals['overall-aggregate'] - yearly_totals['prev_year_total']) / 
                                   yearly_totals['prev_year_total'] * 100).round(2)
    
    # Create a dictionary to map the growth rates back to original dataframe
    growth_rates = yearly_totals.set_index(['year', 'degree'])['growth_rate']
    
    # Add growth rate column to original dataframe
    df['yoy_growth_rate'] = df.apply(lambda row: growth_rates.get((row['year'], row['degree']), None), axis=1)
    
    # Save changes back to file
    df.to_csv(file_path, index=False)
    
    # Print summary of growth rates by year and degree
    print("\nYear-over-Year Growth Rates by Degree Field:")
    summary = yearly_totals[yearly_totals['growth_rate'].notna()].sort_values(['year', 'degree'])
    for _, row in summary.iterrows():
        if not pd.isna(row['growth_rate']):
            print(f"{row['year']} - {row['degree']}: {row['growth_rate']}%")

if __name__ == "__main__":
    file_path = "public-unis-aggregate-data-coordinates.csv"
    add_growth_rate(file_path)