"""Repo Mapper — clones or reuses repo, extracts structure, reads README.md,
and triggers AI README summarization via repo_summary.py (Gemini flash)."""

def run_mapper {
    exec("""
import os, subprocess, sys, time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Prefer URL from env; Streamlit still passes it via REST to server.py/supervisor.jac
repo_url = os.getenv("REPO_URL", "https://github.com/openai/openai-python.git")
repo_name = repo_url.split("/")[-1].replace(".git", "")

print(f"🔄 Starting repository mapping for: {repo_name}")

# --- Clone or reuse
if not os.path.exists(repo_name):
    print(f"📦 Cloning repository {repo_name} ...")
    subprocess.run(["git", "clone", repo_url], check=True)
else:
    print(f"🗂️ Using cached repository: {repo_name}")

# --- Extract README.md
readme_path = os.path.join(repo_name, "README.md")
readme_txt  = "repo_readme.txt"
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
        txt = f.read()
    with open(readme_txt, "w", encoding="utf-8") as out:
        out.write(txt)
    print("📘 README.md extracted successfully.")
else:
    with open(readme_txt, "w", encoding="utf-8") as out:
        out.write("(No README.md found)")
    print("⚠️ No README.md found in repository.")

# --- Build simple file tree (filtering heavy/irrelevant dirs)
ignore_dirs = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__"}
lines = []
for root, dirs, files in os.walk(repo_name):
    # prune ignores in-place
    dirs[:] = [d for d in dirs if d not in ignore_dirs]
    depth = root.replace(repo_name, "").count(os.sep)
    indent = "  " * depth
    lines.append(f"{indent}📁 {os.path.basename(root)}/")
    for fn in files:
        lines.append(f"{indent}  ├── {fn}")

with open("repo_structure.txt", "w", encoding="utf-8") as out:
    out.write("\\n".join(lines))

print("✅ Repository mapping completed successfully.")

# --- Step: Summarize README with Gemini (Flash)
try:
    print("🧠 Summarizing README with Gemini (flash)...")
    proc = subprocess.run(
        [sys.executable, "repo_summary.py", "--from-files"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        timeout=90
    )

    if proc.returncode == 0:
        print("✅ Gemini AI summary generated successfully.")
    else:
        print(f"⚠️ Gemini summarization returned non-zero exit ({proc.returncode}):")
        print(proc.stderr or proc.stdout)

    # Verify files created
    ai_summary_path = os.path.join(BASE_DIR, "ai_summary.md")
    ai_readme_path  = os.path.join(BASE_DIR, "ai_readme_summary.md")
    for p in [ai_summary_path, ai_readme_path]:
        if os.path.exists(p):
            print(f"📝 Created: {p}")
        else:
            print(f"⚠️ Missing expected output file: {p}")

except subprocess.TimeoutExpired:
    print("❌ Gemini summarization timed out after 90 seconds.")
except Exception as e:
    print(f"⚠️ Could not run repo_summary.py: {e}")

print("🏁 Repo Mapper (with AI summary) finished.")
""");
}

with entry:__main__ { run_mapper(); }
