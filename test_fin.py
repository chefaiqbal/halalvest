import requests
import os
import streamlit as st
import sys
sys.path.append('streamlit_app')
from finnhub_client import get_fundamental_ratios
import json
print(json.dumps(get_fundamental_ratios("AAPL"), indent=2))
