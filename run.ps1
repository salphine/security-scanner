# run.ps1 - Start everything
Write-Host "?? Starting Security Scanner..." -ForegroundColor Cyan

# Install requirements
Write-Host "?? Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Initialize database
Write-Host "??? Initializing database..." -ForegroundColor Yellow
python -c "from backend.app.database.database import engine, Base; Base.metadata.create_all(bind=engine); print('? Database created!')"

# Start backend (in new window)
Write-Host "?? Starting backend server..." -ForegroundColor Yellow
$backend = Start-Process powershell -ArgumentList "-NoExit -Command cd backend; uvicorn app.main:app --reload --port 8000" -PassThru

# Wait a bit
Start-Sleep -Seconds 3

# Start frontend (in new window)
Write-Host "?? Starting frontend dashboard..." -ForegroundColor Yellow
$frontend = Start-Process powershell -ArgumentList "-NoExit -Command cd frontend; streamlit run streamlit_app.py" -PassThru

Write-Host @"
+------------------------------------------------------------+
¦  ? SERVICES STARTED!                                      ¦
¦  ?? Frontend: http://localhost:8501                        ¦
¦  ?? Backend:  http://localhost:8000                        ¦
¦  ?? API Docs: http://localhost:8000/docs                   ¦
+------------------------------------------------------------+
"@ -ForegroundColor Green

Write-Host ""
Write-Host "Press any key to stop all services..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $frontend.Id -Force -ErrorAction SilentlyContinue
Write-Host "Services stopped" -ForegroundColor Yellow
