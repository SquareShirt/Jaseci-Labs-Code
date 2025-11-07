from fastapi import FastAPI
from pydantic import BaseModel
import subprocess, os, sys
from datetime import datetime
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = FastAPI(title="🧠 Code_base_Genius_Jac_App API")

class RepoRequest(BaseModel):
    repo_url: str

REPO_URL_FILE = os.path.join(BASE_DIR, "repo_url.txt")  # 🔹 remember last URL

def _load_last_repo_url() -> str:
    try:
        if os.path.exists(REPO_URL_FILE):
            with open(REPO_URL_FILE, "r", encoding="utf-8") as f:
                return f.read().strip()
    except:
        pass
    return ""

def _env_with_repo(url: str) -> dict:
    """Inject REPO_URL for Jac subprocesses."""
    env = os.environ.copy()
    if url:
        env["REPO_URL"] = url
    return env

# ------------------------------
#  ROUTES
# ------------------------------
@app.post("/clone_repo")
def clone_repo(data: RepoRequest):
    repo_url = data.repo_url.strip()
    if not repo_url:
        return {"status": "error", "error": "Empty repo_url."}

    # 🔹 persist for later steps
    try:
        with open(REPO_URL_FILE, "w", encoding="utf-8") as f:
            f.write(repo_url)
    except Exception as e:
        return {"status": "error", "error": f"Failed to save repo url: {e}"}

    print(f"🔄 Cloning repo: {repo_url}")
    proc = subprocess.run(
        ["jac", "run", "repo_mapper.jac"],
        cwd=BASE_DIR,
        input=repo_url.encode(),     # keep stdin for backward compatibility
        capture_output=True,
        env=_env_with_repo(repo_url) # 🔹 pass as environment for Jac
    )
    return {"status": "success", "output": proc.stdout.decode()}

@app.post("/map_repo")
def map_repo():
    print("🗂️ Mapping repository...")
    last = _load_last_repo_url()
    proc = subprocess.run(
        ["jac", "run", "repo_mapper.jac"],
        cwd=BASE_DIR,
        capture_output=True,
        env=_env_with_repo(last)     # 🔹 carry forward last repo URL if needed
    )
    return {"status": "success", "output": proc.stdout.decode()}

@app.post("/generate_docs")
def generate_docs():
    print("📘 Running full documentation supervisor...")
    last = _load_last_repo_url()
    proc = subprocess.run(
        ["jac", "run", "supervisor.jac"],
        cwd=BASE_DIR,
        capture_output=True,
        env=_env_with_repo(last)     # 🔹 supervisor also gets REPO_URL
    )
    output = proc.stdout.decode()

    final_path = os.path.join(BASE_DIR, "final_documentation.md")
    if os.path.exists(final_path):
        with open(final_path, "r", encoding="utf-8") as f:
            markdown = f.read()
    else:
        markdown = "⚠️ No documentation file found."

    return {"status": "success", "output": output, "markdown": markdown}

def _safe_read(path):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().strip()
    except Exception as e:
        return f"(Error reading {path}: {e})"
    return ""

def merge_docs():
    print("🧩 Merging text files into final_documentation.md...")

    readme_text   = _safe_read("repo_readme.txt") or "(No README found)"
    ai_summary    = _safe_read("ai_summary.md")
    ai_readme_nar = _safe_read("ai_readme_summary.md")
    analysis_txt  = _safe_read("code_analysis.txt") or "(No code analysis found)"
    mermaid_txt   = _safe_read("mermaid_diagram.txt")

    def _grep(section_keywords):
        for line in readme_text.splitlines():
            if any(k.lower() in line.lower() for k in section_keywords):
                return line.strip()
        return ""

    installation_hint = _grep(["install", "requirements", "pip", "setup"])
    usage_hint        = _grep(["usage", "run", "example", "how to"])

    combined = []
    combined.append("# 📘 Repository Documentation")
    combined.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    combined.append("## 🧭 Repository Summary (AI)")
    combined.append(ai_summary or "_Gemini summary unavailable._")
    combined.append("")

    combined.append("## 📝 Project Overview")
    combined.append(ai_readme_nar or "_No AI overview generated._")
    combined.append("")

    combined.append("## 🧩 Installation")
    combined.append(installation_hint or "_See README for detailed installation instructions._")
    combined.append("")

    combined.append("## ▶️ Usage")
    combined.append(usage_hint or "_See README for usage examples._")
    combined.append("")

    combined.append("## 📚 API Reference")
    combined.append("| Endpoint | Description |")
    combined.append("|-----------|-------------|")
    combined.append("| `/clone_repo` | Clone and prepare repository for analysis |")
    combined.append("| `/map_repo` | Generate structure map |")
    combined.append("| `/generate_docs` | Produce full Markdown documentation |")
    combined.append("")

    combined.append("## 🧠 Code Analysis")
    combined.append(analysis_txt)
    combined.append("")

    if mermaid_txt:
        combined.append("## 🪶 Repository Diagram")
        combined.append("```mermaid")
        combined.append(mermaid_txt)
        combined.append("```")
        combined.append("")

    combined.append("✨ _Generated by Code_base_Genius_Jac_App_")

    out_path = os.path.join(BASE_DIR, "final_documentation.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(combined))

    print(f"✅ Documentation combined successfully at {out_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--merge":
        merge_docs()
    else:
        print("🧩 Starting FastAPI backend server on port 8001...")
        uvicorn.run(app, host="0.0.0.0", port=8001)
