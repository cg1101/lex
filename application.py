import os

from app import create_app

application = create_app(os.environ.get('ENVIRONMENT_TYPE', 'development'))
