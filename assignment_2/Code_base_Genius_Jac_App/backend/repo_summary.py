"""repo_summary.py — Summarize README.md using real Gemini 2.0 Flash API.
Generates ai_summary.md (concise) and ai_readme_summary.md (narrative + optional diagram).
"""

import os, time, google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ GOOGLE_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")


def summarize_readme(readme_text: str):
    concise_prompt = (
        "Summarize this README.md in under 10 lines. "
        "Keep it concise, clear, and suitable as a repository overview."
    )
    narrative_prompt = (
        "Rewrite this README.md as a human-readable project story in markdown. "
        "Explain its purpose, functionality, and use cases in natural language. "
        "Include a short Mermaid diagram or Markdown table showing system flow or architecture."
    )

    concise_summary, narrative_summary = "", ""

    try:
        concise_summary = model.generate_content(concise_prompt + "\n\n" + readme_text).text
    except Exception as e:
        concise_summary = f"⚠️ Gemini summarization failed: {e}"

    try:
        narrative_summary = model.generate_content(narrative_prompt + "\n\n" + readme_text).text
    except Exception as e:
        narrative_summary = f"⚠️ Gemini narrative generation failed: {e}"

    return concise_summary, narrative_summary


if __name__ == "__main__":
    print("🧠 Summarizing README with Gemini (flash)...")

    readme_path = os.path.join(BASE_DIR, "repo_readme.txt")
    if not os.path.exists(readme_path):
        print("⚠️ README file not found. Exiting.")
        exit(0)

    with open(readme_path, "r", encoding="utf-8", errors="ignore") as f:
        readme_content = f.read().strip()

    concise, narrative = summarize_readme(readme_content)

    concise_path = os.path.join(BASE_DIR, "ai_summary.md")
    narrative_path = os.path.join(BASE_DIR, "ai_readme_summary.md")

    with open(concise_path, "w", encoding="utf-8") as f:
        f.write(concise or "")
    with open(narrative_path, "w", encoding="utf-8") as f:
        f.write(narrative or "")

    print(f"📝 Created: {concise_path}")
    print(f"📝 Created: {narrative_path}")
    print("✅ Gemini AI summary generated successfully.")
    print("🏁 Repo Summary pipeline finished.")
