# Final app.py
# frontend/app.py
import streamlit as st
import requests
import os
import time
import re
from pathlib import Path

st.set_page_config(
    page_title="🧠 Code Base Genius",
    layout="wide",
    page_icon="🧩"
)

BACKEND_URL = "http://127.0.0.1:8001"
BACKEND_PATH = os.path.join(os.path.dirname(__file__), "../backend")


# ---------------------------
# Utility Functions
# ---------------------------
def wait_for_file(path, timeout=8):
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            return True
        time.sleep(0.5)
    return False


def read_backend_file(filename):
    path = os.path.abspath(os.path.join(BACKEND_PATH, filename))
    if wait_for_file(path, timeout=10):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            return f"(Error reading {filename}: {e})"
    else:
        return f"(File {filename} not generated in time.)"


def scroll_to_top():
    st.markdown("<script>window.scrollTo(0, 0);</script>", unsafe_allow_html=True)


# ---------------------------
# FRONTEND UI
# ---------------------------
st.title("🧠 Code Base Genius")
st.markdown(
    "Generate rich, human-readable repository documentation with **Gemini 2.0 Flash AI summaries**, "
    "clear structure maps, and code insights."
)

repo_url = st.text_input("🔗 Enter GitHub Repository URL:", "https://github.com/openai/tiktoken")

if st.button("🚀 Generate Documentation"):
    if not repo_url.strip():
        st.error("Please enter a valid repository URL.")
        st.stop()

    scroll_to_top()
    with st.spinner("Processing repository data..."):
        try:
            # Trigger backend process
            requests.post(f"{BACKEND_URL}/clone_repo", json={"repo_url": repo_url})
            response = requests.post(f"{BACKEND_URL}/generate_docs")
            data = response.json()

            if data.get("status") != "success":
                st.error(f"❌ Backend error: {data.get('error', 'Unknown error')}")
                st.code(data.get("output", "No output."), language="bash")
                st.stop()

            # --- Fetch backend outputs
            ai_summary = read_backend_file("ai_summary.md")
            ai_readme_summary = read_backend_file("ai_readme_summary.md")
            repo_structure = read_backend_file("repo_structure.txt")
            full_markdown = read_backend_file("final_documentation.md")

            # --- Repository Summary
            st.subheader("🧭 Repository Summary (AI)")
            st.markdown(ai_summary or ai_readme_summary or "_Gemini API call failed to produce summary._", unsafe_allow_html=True)

            # --- Repository Structure
            with st.expander("📁 Repository Structure", expanded=False):
                st.code(repo_structure or "No structure data found.", language="text")

            # --- Full Markdown Documentation
            st.subheader("📖 Full Markdown Documentation")
            if full_markdown and len(full_markdown.strip()) > 0:
                # Remove redundant & noisy sections
                cleaned = re.sub(r"(?i)#+\s*(contributing|get\s*started)[\s\S]*?(?=\n#+|$)", "", full_markdown)
                skip_sections = ("## 🧭 Repository Summary", "## 📝 Project Overview")
                filtered = [
                    ln for ln in cleaned.splitlines()
                    if not any(ln.strip().startswith(s) for s in skip_sections)
                ]
                markdown_text = "\n".join(filtered)

                # ---------- COLLAPSIBLE HEADINGS ----------
                # Convert markdown ##/### headings to collapsible <details>
                def make_collapsible(md_text: str) -> str:
                    lines = md_text.splitlines()
                    result = []
                    for line in lines:
                        if line.startswith("## "):
                            if result and not result[-1].endswith("</details>"):
                                result.append("</details>")
                            title = line.replace("## ", "").strip()
                            result.append(f"<details><summary><b>{title}</b></summary>")
                        else:
                            result.append(line)
                    if not result[-1].endswith("</details>"):
                        result.append("</details>")
                    return "\n".join(result)

                collapsible_md = make_collapsible(markdown_text)
                st.markdown(collapsible_md, unsafe_allow_html=True)

                # ---------- MERMAID DIAGRAM RENDER ----------
                mermaid_blocks = re.findall(r"```mermaid\n(.*?)```", markdown_text, re.DOTALL)
                if mermaid_blocks:
                    st.divider()
                    st.subheader("🪶 Rendered Mermaid Diagrams")
                    for i, diagram in enumerate(mermaid_blocks, 1):
                        st.markdown(f"**Diagram {i}**")
                        mermaid_html = f"""
                        <div class="mermaid">
                        {diagram}
                        </div>
                        <script type="module">
                          import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
                          mermaid.initialize({{
                            startOnLoad: true,
                            theme: "neutral",
                            themeVariables: {{
                                primaryColor: "#1e1e1e",
                                primaryTextColor: "#eee",
                                secondaryColor: "#303030",
                                tertiaryColor: "#505050",
                                edgeLabelBackground: "#222",
                                lineColor: "#ccc"
                            }}
                          }});
                        </script>
                        """
                        st.components.v1.html(mermaid_html, height=500, scrolling=True)

            else:
                st.warning("No Markdown content found.")

            st.success("✅ Documentation generated successfully!")

        except Exception as e:
            st.error(f"⚠️ Frontend error: {e}")
            st.stop()

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.caption("🪶 *Code Base Genius — AI documentation orchestrated by Jac + Gemini 2.0 Flash.*")
