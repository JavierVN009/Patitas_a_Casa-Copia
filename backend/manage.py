import os
import sys
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patitas_a_casa.settings')

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
