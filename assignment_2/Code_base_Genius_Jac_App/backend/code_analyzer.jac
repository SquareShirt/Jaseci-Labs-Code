"""Code Analyzer — performs static analysis on source files (LLM-free)."""

def run_analyzer {
    print("🔍 Starting static code analysis...");

    exec("""
import os

# --- Step 1: Detect repository ---
repo_url = os.getenv("REPO_URL", "https://github.com/openai/openai-python.git")
repo_name = repo_url.split("/")[-1].replace(".git", "")

if not os.path.exists(repo_name):
    print(f"⚠️ Repository '{repo_name}' not found. Please run repo_mapper.jac first.")
    exit()

# --- Step 2: Walk files and count lines ---
summary_lines = []
valid_exts = (".py", ".js", ".jac", ".ts", ".cpp", ".java", ".html", ".css")
for root, dirs, files in os.walk(repo_name):
    for f in files:
        if f.endswith(valid_exts):
            path = os.path.join(root, f)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as file:
                    lines = file.readlines()
                    summary_lines.append(f"{path} — {len(lines)} lines")
            except Exception as e:
                summary_lines.append(f"{path} — (Error reading file: {e})")

# --- Step 3: Write results ---
if summary_lines:
    with open("code_analysis.txt", "w", encoding="utf-8") as out:
        out.write("\\n".join(summary_lines))
    print(f"✅ Analyzed {len(summary_lines)} source files.")
else:
    with open("code_analysis.txt", "w", encoding="utf-8") as out:
        out.write("(No source files found)")
    print("⚠️ No source files found for analysis.")
""");
}

with entry:__main__ {
    run_analyzer();
}
