set -euo pipefail

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate

echo "==> Installing Backend Deps"
cd backend
python3 -m pip install -r requirements.txt
cd ..

echo "==> Installing Frontend Deps"
cd frontend
npm install
cd ..

echo "==> Running Backend Tests"
cd backend
python3 -m pytest tests/
cd ..

echo "==> Running Frontend Tests"
cd frontend
npm run test
cd ..

echo "==> Running Batch Processing"
python3 scripts/process_company_profiles.py

echo "==> Verifying Outputs"
python3 scripts/verify_processed_outputs.py

echo "==> ALL VALIDATIONS PASSED SUCCESSFULLY"
