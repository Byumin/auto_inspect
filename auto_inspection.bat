@echo off
pip install -r requirements.txt
cd module 
streamlit run user_defined_automation_pipeline.py
pause