from django.core.management.base import BaseCommand
from core.models import UnsafeArea
import pandas as pd
import os

class Command(BaseCommand):
    help = 'Import unsafe areas from crime data CSV file'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to the crime data CSV file')
        parser.add_argument('--threshold', type=int, default=5, help='Crime count threshold to consider area as unsafe')

    def handle(self, *args, **options):
        # Set default file path if not provided
        file_path = options.get('file') or os.path.join('E:\\', 'we-alert', 'unsafe_area_detect', 'final_cleaned_data.csv')
        threshold = options.get('threshold', 5)

        self.stdout.write(f"Looking for data file at: {file_path}")
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
            
        try:
            # Load the crime data
            df = pd.read_csv(file_path)
            
            # Print available fields in model
            unsafe_area_fields = [field.name for field in UnsafeArea._meta.fields]
            self.stdout.write(f"Available fields in UnsafeArea model: {unsafe_area_fields}")
            
            # Process the data to get crime counts by location
            location_counts = df['location'].value_counts().reset_index()
            location_counts.columns = ['name', 'crime_count']
            
            # Filter to areas with crime count >= threshold
            unsafe_areas = location_counts[location_counts['crime_count'] >= threshold]
            
            # Define coordinates for known areas
            area_coordinates = {
                'Saket': (28.5245, 77.2099, 900),
                'Anand Vihar': (28.6472, 77.3159, 800),
                'West Patel Nagar': (28.6472, 77.1654, 700),
                'Subhash Nagar': (28.6363, 77.1277, 600),
                'Tilak Nagar': (28.6389, 77.0994, 600),
                'Kirti Nagar': (28.6518, 77.1518, 500),
                'Uttam Nagar': (28.6217, 77.0587, 500),
                # Add more coordinates as needed
                'Connaught Place': (28.6329, 77.2195, 800),
                'Rohini': (28.7410, 77.0658, 700),
                'Shahdara': (28.6695, 77.2804, 600),
                'Chanakyapuri': (28.5995, 77.1887, 800),
                'Delhi Cantonment': (28.5921, 77.1383, 700),
                'Munirka': (28.5569, 77.1758, 600),
                'Chandni Chowk': (28.6505, 77.2303, 500),
                'Dwarka': (28.5921, 77.0460, 700),
                'Vasant Kunj': (28.5253, 77.1552, 600),
                'Green Park': (28.5595, 77.2006, 600),
                'Paharganj': (28.6453, 77.2160, 550),
                'Laxmi Nagar': (28.6311, 77.2800, 550),
                'Mayur Vihar': (28.6066, 77.2919, 600),
                'Patparganj': (28.6186, 77.2891, 550),
                'Rajouri Garden': (28.6492, 77.1226, 600),
                'Malviya Nagar': (28.5394, 77.2152, 600),
                'Hauz Khas': (28.5535, 77.2006, 650),
                'South Extension': (28.5730, 77.2236, 600),
                'Lajpat Nagar': (28.5700, 77.2398, 550),
                'Govindpuri': (28.5376, 77.2639, 500),
                'Punjabi Bagh': (28.6732, 77.1270, 650),
                'Karol Bagh': (28.6520, 77.1901, 600),
                'Vikaspuri': (28.6363, 77.0897, 550),
                'Paschim Vihar': (28.6661, 77.0922, 600),
                'R.K. Puram': (28.5733, 77.1726, 650),
                'Preet Vihar': (28.6393, 77.2935, 550),
                'Defence Colony': (28.5838, 77.2273, 600),
                'Mehrauli': (28.5156, 77.1680, 550),
                'Rajinder Nagar': (28.6348, 77.1854, 550), # Fixed spelling from 'Rajender Nagar'
                'Civil Lines': (28.6814, 77.2226, 600),
                'Jantar Mantar': (28.6270, 77.2167, 400),
                'Ashram': (28.5784, 77.2566, 500),
                'IIT': (28.5456, 77.1926, 700),  # IIT Delhi
                'Safdarjung Enclave': (28.5679, 77.1967, 600),
                'Sarojini Nagar': (28.5775, 77.1969, 550),
                'Inderlok': (28.6733, 77.1778, 500),
                'Mayapuri': (28.6328, 77.1122, 500),
                'Ramesh Nagar': (28.6518, 77.1302, 500),
                'Hari Nagar': (28.6265, 77.1148, 500),
                'Ashok Nagar': (28.6709, 77.0906, 500),
                'Shalimar Bagh': (28.7164, 77.1608, 550),
                'Najafgarh': (28.6090, 76.9854, 550),
                'Nand Nagri': (28.6987, 77.3074, 500),
                'Delhi Cantt': (28.5921, 77.1383, 700), # Same as Delhi Cantonment
                'Dilshad Garden': (28.6812, 77.3220, 550),
                'Kailash Colony': (28.5554, 77.2424, 600),
                'Moti Nagar': (28.6595, 77.1368, 550),
                'Shaheen Bagh': (28.5594, 77.3014, 500),
                'Pragati Maidan': (28.6186, 77.2451, 500),
                'IGI Airport': (28.5562, 77.1000, 800),
                'Kashmere Gate': (28.6664, 77.2290, 550), # Fixed spelling from 'Kashmiri Gate'
                'GTB Nagar': (28.6977, 77.2077, 500),
                'Nehru Place': (28.5491, 77.2534, 600),
                'Akshardham': (28.6227, 77.2777, 600),
                'Prashant Vihar': (28.7214, 77.1400, 500),
                'Nirman Vihar': (28.6410, 77.2907, 500)
            }
            
            # Areas groupings
            west_delhi_areas = ['West Patel Nagar', 'Subhash Nagar', 'Tilak Nagar', 'Kirti Nagar', 'Uttam Nagar', 
                               'Rajouri Garden', 'Vikaspuri', 'Punjabi Bagh', 'Ramesh Nagar', 'Mayapuri', 
                               'Hari Nagar', 'Janakpuri', 'Paschim Vihar', 'Dwarka']
            south_delhi_areas = ['Saket', 'Malviya Nagar', 'Green Park', 'Hauz Khas', 'Lajpat Nagar',
                                'Defence Colony', 'South Extension', 'R.K. Puram', 'Vasant Kunj', 'Mehrauli']
            east_delhi_areas = ['Anand Vihar', 'Laxmi Nagar', 'Mayur Vihar', 'Patparganj', 'Preet Vihar',
                               'Shahdara', 'Dilshad Garden', 'Akshardham', 'Nirman Vihar']
            north_delhi_areas = ['Civil Lines', 'GTB Nagar', 'Kashmere Gate', 'Rohini', 'Shalimar Bagh']
            central_delhi_areas = ['Connaught Place', 'Karol Bagh', 'Paharganj', 'Rajinder Nagar', 'Chandni Chowk']

            areas_to_add = []
            for _, row in unsafe_areas.iterrows():
                name = row['name']
                crime_count = row['crime_count']
                
                # Skip entries that don't look like proper area names
                if name.lower() in ['unknown', '', 'east', 'west', 'north', 'south', 'share']:
                    continue

                if name in area_coordinates:
                    lat, long, radius = area_coordinates[name]
                    areas_to_add.append({
                        'name': name,
                        'latitude': lat,
                        'longitude': long,
                        'radius': radius,
                        'description': f'Area with {crime_count} reported crimes',
                        'crime_count': crime_count
                    })

            # Add/update areas in the database
            if areas_to_add:
                west_delhi_count = 0
                south_delhi_count = 0
                east_delhi_count = 0
                north_delhi_count = 0
                central_delhi_count = 0
                other_areas_count = 0
                
                for area_data in areas_to_add:
                    obj, created = UnsafeArea.objects.update_or_create(
                        name=area_data['name'],
                        defaults={
                            'latitude': area_data['latitude'],
                            'longitude': area_data['longitude'],
                            'radius': area_data['radius'],
                            'description': area_data['description']
                        }
                    )
                    
                    # Count areas by region
                    name = area_data['name']
                    if name in west_delhi_areas:
                        west_delhi_count += 1
                    elif name in south_delhi_areas:
                        south_delhi_count += 1
                    elif name in east_delhi_areas:
                        east_delhi_count += 1
                    elif name in north_delhi_areas:
                        north_delhi_count += 1
                    elif name in central_delhi_areas:
                        central_delhi_count += 1
                    else:
                        other_areas_count += 1
                    
                    action = "Added" if created else "Updated"
                    self.stdout.write(self.style.SUCCESS(f"{action}: {area_data['name']} with {area_data['crime_count']} crimes"))
                
                total_count = len(areas_to_add)
                self.stdout.write(self.style.SUCCESS(f"Total unsafe areas added/updated: {total_count}"))
                self.stdout.write(self.style.SUCCESS(f"Areas by region:"))
                self.stdout.write(self.style.SUCCESS(f"- West Delhi: {west_delhi_count}"))
                self.stdout.write(self.style.SUCCESS(f"- South Delhi: {south_delhi_count}"))
                self.stdout.write(self.style.SUCCESS(f"- East Delhi: {east_delhi_count}"))
                self.stdout.write(self.style.SUCCESS(f"- North Delhi: {north_delhi_count}"))
                self.stdout.write(self.style.SUCCESS(f"- Central Delhi: {central_delhi_count}"))
                self.stdout.write(self.style.SUCCESS(f"- Other areas: {other_areas_count}"))
            else:
                self.stdout.write(self.style.WARNING("No unsafe areas found meeting the criteria"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error processing data: {str(e)}"))