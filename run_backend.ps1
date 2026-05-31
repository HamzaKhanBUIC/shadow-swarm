cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
uvicorn main:app --reload
