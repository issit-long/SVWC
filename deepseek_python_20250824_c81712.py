import os

# Get TV IPs from environment variable or use defaults
TV_IPS = os.getenv('TV_IPS', '192.168.1.101,192.168.1.102,192.168.1.103,192.168.1.104').split(',')

# MagicInfo/Optisigns configuration (if available)
MAGICINFO_URL = os.getenv('MAGICINFO_URL', '')
MAGICINFO_USERNAME = os.getenv('MAGICINFO_USERNAME', '')
MAGICINFO_PASSWORD = os.getenv('MAGICINFO_PASSWORD', '')