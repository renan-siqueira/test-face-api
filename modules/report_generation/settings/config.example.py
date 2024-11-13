import os

# Path settings
APP_PATH_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

APP_PATH_ASSOCIATION_RESULTS = os.path.join(APP_PATH_ROOT, 'data', 'association')
APP_PATH_REPORTS_OUTPUT = os.path.join(APP_PATH_ROOT, 'data', 'reports')

# Report settings
APP_REPORT_CSV_FILENAME = 'detection_report.csv'
APP_REPORT_JSON_FILENAME = 'detection_report.json'
