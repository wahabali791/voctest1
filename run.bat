@echo off
echo Running the first Python script...
python scrap_partial_survey.py
echo First script completed successfully!

echo Running the second Python script...
python scrap_completed_survey.py
echo Second script completed successfully!


echo Running the completed survery transformation...
python main.py
echo Third script completed successfully!


echo Running the partial survery transformation...
python main_new.py
echo Fourth script completed successfully!


echo Running the combine update transformation...
python combine_update.py
echo Fifth script completed successfully!

echo Running the dial code transformation...
python combine_dail_code_and_phone.py
echo Last script completed successfully!

pause