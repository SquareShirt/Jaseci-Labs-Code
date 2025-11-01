import os
from dotenv import load_dotenv
from byllm.llm import Model

def summarize_markdown():
    """Generate concise executive summary and append to markdown."""
    load_dotenv()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    source_path = os.path.join(BASE_DIR, "final_documentation.md")
    output_path = os.path.join(BASE_DIR, "ai_summary.md")

    if not os.path.exists(source_path):
        print("⚠️ No final_documentation.md found — skipping AI summary.")
        return

    # --- Read markdown content ---
    with open(source_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    print("🤖 Generating concise AI summary using Gemini...")

    # --- Initialize Gemini model ---
    try:
        llm = Model(
            model_name="gemini/gemini-2.0-flash",
            api_key=os.getenv("GEMINI_API_KEY"),
            verbose=False,
        )
    except Exception as e:
        print(f"❌ Error initializing Gemini model: {e}")
        return

    # --- Define prompt ---
    prompt = f"""
You are a skilled technical writer.
Summarize the following repository documentation into a short,
human-readable overview suitable for the first page of a report.

Rules:
- Keep your summary under 10 lines.
- Capture key goals, architecture, and functionality.
- Include **at most one** simple Mermaid diagram or ASCII chart
  showing system flow or module relationships.
- Do NOT repeat code or bullet-dump lists.
- Use professional tone and clear structure.

---
{markdown_text[:15000]}  # Limit to avoid token overflow
"""

    # --- Run model ---
    try:
        result = llm(prompt=prompt)
        summary = (
            result.get("text", "").strip()
            if isinstance(result, dict)
            else str(result).strip()
        )
        if not summary:
            summary = "(No summary returned by Gemini model.)"
    except Exception as e:
        summary = f"(Error during Gemini summarization: {e})"
        print(summary)

    # --- Save standalone summary ---
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(summary)

    # --- Embed summary into markdown ---
    try:
        combined_path = os.path.join(BASE_DIR, "final_documentation.md")
        with open(combined_path, "r", encoding="utf-8") as f:
            existing_md = f.read()

        final_text = (
            "# 🧭 Executive AI Summary\n\n"
            + summary.strip()
            + "\n\n---\n"
            + existing_md.strip()
        )

        with open(combined_path, "w", encoding="utf-8") as f:
            f.write(final_text)

        print(f"✅ AI summary embedded into {combined_path}")
    except Exception as e:
        print(f"⚠️ Could not embed AI summary into final_documentation.md: {e}")

    print(f"✅ AI summary saved to {output_path}")


if __name__ == "__main__":
    summarize_markdown()
