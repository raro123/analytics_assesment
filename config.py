import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'default_password')
DATABASE_PATH = os.getenv('DATABASE_PATH', './data/assessment.db')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
