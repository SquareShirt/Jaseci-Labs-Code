"""Main entrypoint for Code_base_Genius_Jac_App backend.
Run with: jac serve main.jac
"""

import from dotenv { load_dotenv }
import os;
import subprocess;

with entry {
    load_dotenv();
    print("✅ Environment variables loaded.");
    print("🌐 Code_base_Genius_Jac_App backend is ready.");

    exec("""
from fastapi import FastAPI
from pydantic import BaseModel
import subprocess, os, json, sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI(title="🧠 Codebase Genius API (JacCloud Gateway)")

class RepoRequest(BaseModel):
    repo_url: str

@app.post('/clone_repo')
async def clone_repo(data: RepoRequest):
    print(f'🌀 Cloning repository: {data.repo_url}')
    proc = subprocess.run(['jac', 'run', 'repo_mapper.jac'], cwd=BASE_DIR, input=data.repo_url.encode(), capture_output=True)
    return {'status': 'success', 'output': proc.stdout.decode()}

@app.post('/map_repo')
async def map_repo():
    print('🗺️ Mapping repository...')
    proc = subprocess.run(['jac', 'run', 'repo_mapper.jac'], cwd=BASE_DIR, capture_output=True)
    return {'status': 'success', 'output': proc.stdout.decode()}

@app.post('/generate_docs')
async def generate_docs():
    print('📚 Generating full documentation via supervisor...')
    proc = subprocess.run(['jac', 'run', 'supervisor.jac'], cwd=BASE_DIR, capture_output=True)
    return {'status': 'success', 'output': proc.stdout.decode()}
""");
}


