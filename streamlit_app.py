"""
NagrikMitra - AI-Powered Multilingual Citizen Service Assistant
Streamlit Cloud Entry Point
"""

import sys
import os

# Add frontend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'frontend'))

# Import and run the frontend app
from streamlit_app import *
