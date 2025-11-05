<!-- Setup Instructions -->
Follow the steps below to set up and run the Code_base_Genius_Jac_App

<!-- 1. Clone this repository -->
git clone https://github.com/SquareShirt/Jaseci-Labs-Code/tree/main/assignment_2.git

cd assignment2/Code_base_Genius_Jac_App

<!-- 2. Create and activate a virtual environment -->
python3 -m venv .venv
source .venv/bin/activate   # On Windows use: .venv\Scripts\activate

<!-- 3. Install dependencies -->
You can either install directly:
pip install -U pip
pip install -U jaclang byllm jac-cloud streamlit python-dotenv fastapi uvicorn
pip install google-generativeai

Or use the provided requirements file:
pip install -r requirements.txt

<!-- 4. Create a .env file inside the backend/ folder: -->
touch backend/.env

Then add your Gemini API key,GITHUB_TOKEN, and REPO_URL=https://github.com/openai/openai-python.git:
GOOGLE_API_KEY=your_google_gemini_api_key_here
GITHUB_TOKEN=your_github_token_here
REPO_URL=https://github.com/openai/openai-python.git

<!-- 5. From inside your backend folder -->
<!-- You will change to the backend folder -->
cd backend
<!-- and run a command to give your shell file permission to execute your backend -->
chmod +x run_backend.sh
<!-- run your shell file -->
./run_backend.sh

<!-- 6. Open a new terminal while the backend is running -->
cd frontend
or
cd ../frontend
If the terminal opens showing the backend folder.

<!-- 7. Activate your virtual environment inside your frontend folder then run your app -->
source ../.venv/bin/activate
streamlit run app.py
