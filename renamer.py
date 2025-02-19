import pandas as pd

def rename_community_college(file_path):
    """
    Rename 'Community College' to 'Community College Of Qatar' in the university column
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Replace values in university column
    df['university'] = df['university'].replace({'Community College': 'Community College Of Qatar',
                                               'Community College ': 'Community College Of Qatar'})
    
    # Save changes back to the same file
    df.to_csv(file_path, index=False)
    
    # Print confirmation
    print("\nUpdated university names:")
    print(df['university'].unique())

if __name__ == "__main__":
    file_path = "public-unis-aggregate-data-coordinates.csv"
    rename_community_college(file_path)