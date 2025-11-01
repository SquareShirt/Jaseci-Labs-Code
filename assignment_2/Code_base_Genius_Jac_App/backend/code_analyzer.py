"""code_analyzer.py — Gemini-enhanced summarization of code analysis."""
import os, google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")


def summarize_code_analysis():
    analysis_path = os.path.join(BASE_DIR, "code_analysis.txt")
    if not os.path.exists(analysis_path):
        print("⚠️ No code_analysis.txt found.")
        return

    with open(analysis_path, "r", encoding="utf-8", errors="ignore") as f:
        code_data = f.read().strip()

    prompt = (
        "You are a code analysis expert. Summarize this codebase analysis in Markdown. "
        "Explain the architecture, main modules, and their relationships. "
        "Include a short Mermaid diagram or Markdown table summarizing dependencies or architecture flow."
    )

    print("🧠 Generating Gemini code summary...")
    try:
        result = model.generate_content(prompt + "\n\n" + code_data)
        summary = result.text
    except Exception as e:
        summary = f"⚠️ Gemini summarization failed: {e}"

    output_path = os.path.join(BASE_DIR, "ai_code_summary.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(summary)

    print(f"✅ Gemini AI summary written to {output_path}")
    try:
        with open(analysis_path, "a", encoding="utf-8") as f:
            f.write("\n\n---\n## 🤖 Gemini AI Code Summary\n" + summary)
    except Exception as e:
        print(f"⚠️ Could not append AI summary: {e}")


if __name__ == "__main__":
    summarize_code_analysis()
