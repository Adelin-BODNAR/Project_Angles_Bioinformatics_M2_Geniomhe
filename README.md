# Project_Angles_Bioinformatics_M2_Geniomhe

##Virtual environment

###Creating a vitual environment
python -m venv .venv

###Activating the virtual environment
source .venv/bin/activate

###Deactivating the virtual environment
deactivate

###Saving the libraries installed while the environment is activated
pip freeze > requirements.txt

###Installing the libraries on the environment from the "requirements.txt" file while the environment is activated
pip install -r requirements.txt
