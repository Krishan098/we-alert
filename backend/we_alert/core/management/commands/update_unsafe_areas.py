from django.core.management.base import BaseCommand
from core.utils.crime_analyzer import CrimeDataAnalyzer
from core.models import UnsafeArea
import os

class Command(BaseCommand):
    help = 'Update unsafe areas database based on crime data analysis'

    def add_arguments(self, parser):
        parser.add_argument('--min-count', type=int, default=10, help='Minimum crime count to consider an area unsafe')
        parser.add_argument('--west-delhi-only', action='store_true', help='Only process West Delhi areas')

    def handle(self, *args, **options):
        min_count = options['min_count']
        west_delhi_only = options['west_delhi_only']
        
        # Print the expected data path for debugging
        from django.conf import settings
        expected_path = os.path.join(settings.BASE_DIR, '..', '..', 'unsafe_area_detect', 'final_cleaned_data.csv')
        self.stdout.write(f"Looking for data file at: {os.path.abspath(expected_path)}")
        
        if not os.path.exists(expected_path):
            self.stdout.write(self.style.ERROR(f"Data file not found at {expected_path}"))
            return
        
        analyzer = CrimeDataAnalyzer()
        
        # Let's check the actual fields in the UnsafeArea model
        model_fields = [field.name for field in UnsafeArea._meta.fields]
        self.stdout.write(f"Available fields in UnsafeArea model: {model_fields}")
        
        if west_delhi_only:
            unsafe_areas_data = analyzer.get_west_delhi_unsafe_areas(min_count)
            self.stdout.write(f"Found {len(unsafe_areas_data)} unsafe areas in West Delhi")
            
            for area_data in unsafe_areas_data:
                location = area_data['location']
                count = area_data['count']
                
                # Only use fields that exist in the model
                defaults = {
                    'latitude': 0.0,
                    'longitude': 0.0,
                }
                
                # Add notes field if it exists in the model
                if 'notes' in model_fields:
                    defaults['notes'] = f"West Delhi area with {count} reported crimes"
                # Try other possible field names for description
                elif 'description' in model_fields:
                    defaults['description'] = f"West Delhi area with {count} reported crimes"
                elif 'details' in model_fields:
                    defaults['details'] = f"West Delhi area with {count} reported crimes"
                
                UnsafeArea.objects.update_or_create(
                    name=location,
                    defaults=defaults
                )
                self.stdout.write(f"Added/Updated: {location} with {count} crimes")
        else:
            unsafe_areas_data = analyzer.get_unsafe_areas(min_count)
            self.stdout.write(f"Found {len(unsafe_areas_data)} unsafe areas overall")
            
            for area_data in unsafe_areas_data:
                location = area_data['location']
                count = area_data['count']
                
                # Only use fields that exist in the model
                defaults = {
                    'latitude': 0.0,
                    'longitude': 0.0,
                }
                
                # Add notes field if it exists in the model
                if 'notes' in model_fields:
                    defaults['notes'] = f"Area with {count} reported crimes"
                # Try other possible field names for description
                elif 'description' in model_fields:
                    defaults['description'] = f"Area with {count} reported crimes"
                elif 'details' in model_fields:
                    defaults['details'] = f"Area with {count} reported crimes"
                
                UnsafeArea.objects.update_or_create(
                    name=location,
                    defaults=defaults
                )
                self.stdout.write(f"Added/Updated: {location} with {count} crimes")
        
        self.stdout.write(self.style.SUCCESS('Successfully updated unsafe areas database'))