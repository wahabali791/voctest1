#!/bin/bash

echo "Running the first Python script..."
python3 scrap_partial_survey.py
echo "First script completed successfully!"

echo "Running the second Python script..."
python3 scrap_completed_survey.py
echo "Second script completed successfully!"

echo "Running the completed survey transformation..."
python3 main.py
echo "Third script completed successfully!"

echo "Running the partial survey transformation..."
python3 main_new.py
echo "Fourth script completed successfully!"

echo "Running the combine update transformation..."
python3 combine_update.py
echo "Fifth script completed successfully!"

echo "Running the dial code transformation..."
python3 combine_dail_code_and_phone.py
echo "Last script completed successfully!"
