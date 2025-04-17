import pandas as pd
import sys

def analyze_crime_data(data_path, area_filter=None):
    """Analyze crime data from the CSV file"""
    # Load data
    try:
        data = pd.read_csv(data_path)
        print(f"Successfully loaded data with {len(data)} records")
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # Clean data
    data = data.fillna('')
    data['location_lower'] = data['location'].str.lower()
    
    # Apply area filter if provided
    if area_filter:
        area_filter = area_filter.lower()
        data = data[data['location_lower'].str.contains(area_filter)]
        print(f"Filtered to {len(data)} records containing '{area_filter}'")
    
    # Group by location and count crimes
    location_counts = data.groupby('location').size().reset_index(name='count')
    location_counts = location_counts.sort_values(by='count', ascending=False)
    
    # Display top 20 areas by crime count
    print("\nTop 20 areas by crime count:")
    print(location_counts.head(20))
    
    # List West Delhi areas if requested
    if area_filter and area_filter.lower() == "west":
        west_delhi_areas = [
            'Rajouri Garden', 'Punjabi Bagh', 'Paschim Vihar', 'Janakpuri',
            'Vikaspuri', 'Dwarka', 'Uttam Nagar', 'Tilak Nagar', 'Subhash Nagar',
            'Hari nagar', 'Moti Nagar', 'Kirti Nagar', 'West Patel Nagar', 'Mayapuri',
            'Ramesh Nagar', 'Rajendra Place'
        ]
        west_delhi_areas_lower = [area.lower() for area in west_delhi_areas]
        west_delhi_data = data[data['location_lower'].isin(west_delhi_areas_lower)]
        
        west_counts = west_delhi_data.groupby('location').size().reset_index(name='count')
        west_counts = west_counts.sort_values(by='count', ascending=False)
        
        print("\nWest Delhi areas by crime count:")
        print(west_counts)

if __name__ == "__main__":
    data_path = "final_cleaned_data.csv"
    area_filter = None
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        area_filter = sys.argv[1]
    
    analyze_crime_data(data_path, area_filter)