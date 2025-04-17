import pandas as pd
import os
from django.conf import settings

class CrimeDataAnalyzer:
    def __init__(self):
        self.data_path=os.path.join(settings.BASE_DIR, '..', '..', 'unsafe_area_detect', 'final_cleaned_data.csv')
        self.load_data()

    def load_data(self):
        try:
            self.data=pd.read_csv(self.data_path)
            self.data=self.data.fillna('')
            self.data['location_lower'] = self.data['location'].str.lower()
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = pd.DataFrame()

    def get_unsafe_areas(self,min_crime_count=5):
        if self.data.empty:
            return []
        location_counts=self.data.groupby('location').size().reset_index(name='count')
        loaction_counts=location_counts.sort_values(by='count', ascending=False) 
        unsafe_area=location_counts[location_counts['counts'] >=min_crime_count] 
        return unsafe_area['location'].tolist()

    def get_west_delhi_unsafe_areas(self,min_crime_count=5)   :
        west_delhi_areas=['Rajouri Garden', 'Punjabi Bagh', 'Paschim Vihar', 'Janakpuri',
            'Vikaspuri', 'Dwarka', 'Uttam Nagar', 'Tilak Nagar', 'Subhash Nagar',
            'Hari nagar', 'Moti Nagar', 'Kirti Nagar', 'West Patel Nagar', 'Mayapuri',
            'Ramesh Nagar', 'Rajendra Place', 'Shakur Basti', 'Naraina', 'Keshav Puram','Saket','Anand Vihar']   
        west_delhi_areas_lower = [area.lower() for area in west_delhi_areas]
        
        if self.data.empty:
            return []
        
        
        west_delhi_data = self.data[self.data['location_lower'].isin(west_delhi_areas_lower)]
        
        location_counts = west_delhi_data.groupby('location').size().reset_index(name='count')
       
        location_counts = location_counts.sort_values(by='count', ascending=False)
    
        unsafe_areas = location_counts[location_counts['count'] >= min_crime_count]
        
        return unsafe_areas.to_dict('records')
    
    def is_area_unsafe(self, location, threshold=5):
        """Check if a specific area is unsafe based on crime count"""
        if self.data.empty:
            return False
        
        location = location.lower()
        location_data = self.data[self.data['location_lower'] == location]
        crime_count = len(location_data)
        
        return {
            'is_unsafe': crime_count >= threshold,
            'crime_count': crime_count,
            'common_crimes': self.get_common_crimes(location)
        }
    
    def get_common_crimes(self, location):
        """Get the most common crime types for a location"""
        if self.data.empty:
            return []
        
        location = location.lower()
        location_data = self.data[self.data['location_lower'] == location]
        
        # Count crime types
        crime_types = []
        
        # Check offense_type column
        if 'offense_type' in location_data.columns:
            offense_types = location_data['offense_type'].dropna().tolist()
            crime_types.extend(offense_types)
        
        # Check crime_type column
        if 'crime_type' in location_data.columns:
            crime_types_col = location_data['crime_type'].dropna().tolist()
            crime_types.extend(crime_types_col)
            
        # Check crime column
        if 'crime' in location_data.columns:
            crimes = location_data['crime'].dropna().tolist()
            crime_types.extend(crimes)
        
        # Count occurrences of each crime type
        crime_counts = {}
        for crime in crime_types:
            if crime and crime.strip():
                crime = crime.strip().lower()
                if crime in crime_counts:
                    crime_counts[crime] += 1
                else:
                    crime_counts[crime] = 1
        
        # Sort by frequency
        sorted_crimes = sorted(crime_counts.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_crimes[:5]