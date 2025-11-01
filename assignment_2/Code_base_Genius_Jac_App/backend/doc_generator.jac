"""Doc Generator — combines repository data into AI-ready documentation format (LLM-free)."""

def run_doc_generator {
    print("🎨 Generating repository documentation summary...");

    exec("""
import os
from datetime import datetime

# --- Step 1: Safe file reading ---
def safe_read(path):
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read().strip()
    except Exception as e:
        return f"(Error reading {path}: {e})"
    return "(File not found)"

readme_text   = safe_read('repo_readme.txt')
structure_txt = safe_read('repo_structure.txt')
analysis_txt  = safe_read('code_analysis.txt')

# --- Step 2: Build summary text ---
summary = []
summary.append("# 🧭 Repository Documentation Summary")
summary.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
summary.append("\\n---\\n")
summary.append("## 📝 Project Overview")
summary.append(readme_text or "(No README found)")
summary.append("\\n---\\n")
summary.append("## 🗂️ Repository Structure")
summary.append("```")
summary.append(structure_txt or "(No structure information found)")
summary.append("```")
summary.append("\\n---\\n")
summary.append("## 🧠 Code Analysis Summary")
summary.append(analysis_txt or "(No analysis available)")
summary.append("\\n---\\n")
summary.append("_Generated automatically by Code_base_Genius_Jac_App_")

# --- Step 3: Write to file ---
with open("ai_doc_summary.txt", "w", encoding="utf-8") as f:
    f.write("\\n".join(summary))

print("✅ Documentation summary created successfully.")
""");
}

with entry:__main__ {
    run_doc_generator();
}
