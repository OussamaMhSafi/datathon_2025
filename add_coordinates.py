import pandas as pd

def add_university_coordinates(input_file, output_file):
    """
    Add latitude and longitude coordinates for each university in Qatar
    """
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Define university coordinates dictionary
    university_coordinates = {
        'Qatar University': {'lat': 25.3750, 'lon': 51.4906},
        'Community College': {'lat': 25.2658, 'lon': 51.5161},
        'Ras Laffan College': {'lat': 25.8856, 'lon': 51.4300},
        'Qatar Aeronautical Academy': {'lat': 25.2799, 'lon': 51.5692},
        'University of Doha for Science and Technology': {'lat': 25.3604, 'lon': 51.4810},
        'Qatar Leadership Center': {'lat': 25.3165, 'lon': 51.5263},
        'Jossor Institute': {'lat': 25.3165, 'lon': 51.5263}
    }
    
    # Create new columns for coordinates
    df['latitude'] = df['university'].map(lambda x: university_coordinates.get(str(x).strip(), {'lat': None})['lat'])
    df['longitude'] = df['university'].map(lambda x: university_coordinates.get(str(x).strip(), {'lon': None})['lon'])
    
    # Save the modified dataframe
    df.to_csv(output_file, index=False)
    
    # Print summary
    print("\nUnique universities and their coordinates:")
    for uni in df['university'].unique():
        if pd.notna(uni):
            coords = university_coordinates.get(uni.strip(), {'lat': 'Not found', 'lon': 'Not found'})
            print(f"{uni}: ({coords['lat']}, {coords['lon']})")

if __name__ == "__main__":
    input_file = "public-unis-aggregate-data-generalised.csv"
    output_file = "public-unis-aggregate-data-coordinates.csv"
    add_university_coordinates(input_file, output_file)