"""Code Genius (Supervisor) — Orchestrates Repo Mapper, Code Analyzer, AI Summaries, and DocGenie.
Stable Jac version using sequential Python execution (no nested defs).
"""

def run_supervisor {
    print("🧩 Starting Code Genius (Supervisor)...");

    exec("""
import subprocess
import sys
import os
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================================
# 🧹 Step 0: Clean up cache and temp files
# ============================================================
print('🧹 Cleaning up Jac cache and temporary files...')
for root, dirs, files in os.walk(BASE_DIR):
    for d in dirs:
        if d in ('__pycache__', '.jac_cache'):
            path = os.path.join(root, d)
            try:
                shutil.rmtree(path)
                print(f'   🧽 Removed cache directory: {path}')
            except Exception as e:
                print(f'   ⚠️ Could not remove {path}: {e}')
    for f in files:
        if f.endswith('.pyc'):
            try:
                os.remove(os.path.join(root, f))
            except Exception as e:
                print(f'   ⚠️ Could not delete {f}: {e}')
print('✅ Cleanup complete.\\n')


# ============================================================
# 🔹 Step 1: Repository Mapping
# ============================================================
print('🔹 Step 1: Running repo_mapper.jac...')
subprocess.run(["jac", "run", "repo_mapper.jac"], cwd=BASE_DIR, check=True)
print('✅ repo_mapper.jac completed successfully.')


# ============================================================
# 🤖 Step 1.5: Repository Summary (Gemini flash)
# ============================================================
print('\\n🤖 Step 1.5: Generating AI-enhanced repository summary...')
try:
    subprocess.run([sys.executable, "repo_summary.py", "--from-files"], cwd=BASE_DIR, check=False)
    print('✅ Repository summary generated successfully via Gemini.')
except Exception as e:
    print(f'⚠️ Repo summary skipped due to error: {e}')


# ============================================================
# 🔹 Step 2: Code Analysis
# ============================================================
print('\\n🔹 Step 2: Running code_analyzer.jac...')
subprocess.run(["jac", "run", "code_analyzer.jac"], cwd=BASE_DIR, check=True)
print('✅ code_analyzer.jac completed successfully.')


# ============================================================
# 🤖 Step 2.5: Gemini-enhanced Code Summary
# ============================================================
print('\\n🤖 Step 2.5: Running Gemini AI-enhanced code analysis...')
try:
    subprocess.run([sys.executable, "code_analyzer.py"], cwd=BASE_DIR, check=False)
    print('✅ Gemini AI summary completed and appended to code_analysis.txt')
except Exception as e:
    print(f'⚠️ Gemini summarization skipped due to error: {e}')


# ============================================================
# 🔹 Step 3: Documentation Generation
# ============================================================
print('\\n🔹 Step 3: Running doc_generator.jac...')
subprocess.run(["jac", "run", "doc_generator.jac"], cwd=BASE_DIR, check=True)
print('✅ doc_generator.jac completed successfully.')


# ============================================================
# 🧩 Step 4: Combine Results (delegated to server.py)
# ============================================================
print('\\n🧩 Combining results into final_documentation.md...')
subprocess.run([sys.executable, "server.py", "--merge"], cwd=BASE_DIR, check=True)
print('✅ Documentation combined and saved to final_documentation.md')


# ============================================================
# ✅ Summary
# ============================================================
print('\\n🏁 Supervisor process complete.')
print('----------------------------------')
print('Repo Mapper, Repo Summary, Code Analyzer, Doc Generator, and Gemini Summaries executed successfully.')
print('----------------------------------')
""");

    print("🧠 All processes completed successfully.");
    return "Supervisor execution finished.";
}

with entry:__main__ {
    print(f"{run_supervisor()}");
}
