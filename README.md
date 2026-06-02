to run the project 
1. pip install -r requirements.txt
2. cd backend
   python -m uvicorn app.main:app --reload
3. add another terminal from root
   cd frontend
   npm run dev
4. visit node local host
   register(if not on registration page manipulate url to ../register)
   register via email, verify otp
   login
   engage with PHEMA by giving phishing or safe urls, files and manipulate tone in text field
   download the report and get detailed analysis
5. For developers
   check logs, console and terminal o/p for better analysis
   see correlator/risk_scorer, correlation, ect files
   checkout orchestrator/phema_engine.py and modules/module_adaptor.py for event pipelines
   
