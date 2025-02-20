import pandas as pd

def add_teacher_growth_rate(file_path):
    """
    Add year-over-year growth rate columns for male and female teachers
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Remove any leading/trailing whitespace from column names
    df.columns = df.columns.str.strip()
    
    # Convert the 'FEMALE' and 'MALE' columns to integers
    df['FEMALE'] = df['FEMALE'].str.replace(',', '').astype(int)
    df['MALE'] = df['MALE'].str.replace(',', '').astype(int)
    
    # Calculate year-over-year growth rate for females
    df['FEMALE_prev_year'] = df['FEMALE'].shift(1)
    df['FEMALE_growth_rate'] = ((df['FEMALE'] - df['FEMALE_prev_year']) / df['FEMALE_prev_year'] * 100).round(2)
    
    # Calculate year-over-year growth rate for males
    df['MALE_prev_year'] = df['MALE'].shift(1)
    df['MALE_growth_rate'] = ((df['MALE'] - df['MALE_prev_year']) / df['MALE_prev_year'] * 100).round(2)
    
    # Drop the temporary columns used for calculation
    df = df.drop(columns=['FEMALE_prev_year', 'MALE_prev_year'])
    
    # Save changes back to file
    df.to_csv(file_path, index=False)
    
    # Print summary of growth rates
    print("\nYear-over-Year Growth Rates for Teachers:")
    print(df[['YEAR', 'FEMALE_growth_rate', 'MALE_growth_rate']])

if __name__ == "__main__":
    file_path = "TEACHERS.csv"
    add_teacher_growth_rate(file_path)