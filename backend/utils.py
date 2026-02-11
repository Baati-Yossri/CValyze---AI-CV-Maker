from google import genai
import os
import subprocess
import tempfile
import re

def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    return genai.Client(api_key=api_key)

def generate_summary_gemini(current_info, job_offer, language="English"):
    client = get_gemini_client()
    
    prompt = f"""
    You are an expert career coach and CV writer.
    
    User's Current Info:
    {current_info}
    
    Target Job Offer / Objective:
    {job_offer}
    
    Target Language: {language}
    
    Task:
    Write a professional, compelling, and ATS-friendly professional summary (2-4 sentences) for this user's CV, tailored specifically to the target job offer/objective. Highlight relevant skills and experiences from their current info that match the job requirements.
    
    IMPORTANT: The output MUST be in {language}.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()

def generate_cv_gemini(data, language="English"):
    client = get_gemini_client()
    
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'cv_template.tex')
    with open(template_path, 'r') as f:
        template_content = f.read()
        
    prompt = f"""
You are an expert CV writer, LaTeX developer, and linguistic editor.

Your job is to generate a perfectly formatted, professional, ATS-friendly LaTeX CV.

---------------------------------------------
USER DATA (to be cleaned and expanded):
{data}

TARGET LANGUAGE: {language}

LATEX TEMPLATE:
{template_content}
---------------------------------------------

MANDATORY RULES:

1. **Language & Grammar**
   - The entire content of the CV (except for proper nouns like company names) MUST be in {language}.
   - Translate section headers, descriptions, and skills if necessary to match {language}.
   - Correct all grammar, spelling, and punctuation errors.
   - Resize text to sound professional and clear in {language}.

2. **Professionalization & Quantified Achievements**
   - **QUANTIFY IMPACT**: aggressively look for opportunities to add metrics.
     - Example: Change "Sold products" to "Generated sales revenue..." or "Increased sales volume by...".
     - If the user provides numbers, highlight them.
     - If exact numbers are missing, use result-oriented language (e.g., "Significantly reduced," "Maximized," "Doubled").
   - Improve bullet points by making them achievement-oriented.
   - Keep descriptions concise, factual, and ATS-friendly.
   - Expand incomplete sentences into full, well-structured statements.
   - If the user provides very short information (e.g., “web dev”), expand to a more complete form (“Web Developer specializing in …”).

3. **Template Filling Instructions**
   - Replace all placeholders in the template with the cleaned and enhanced data.
   - For [PROJECTS_LIST], create a list using \\resumeItem{{...}} or similar.
        Format: \\textbf{{Project Name}} $|$ \\emph{{Link/Tech}} \\\\ Description.
   - For [SKILLS_LIST], produce a comma-separated list.
   - For [LANGUAGES_LIST], include languages with proficiency labels (e.g., English (Fluent) or Anglais (Courant)).
   - For [CERTIFICATIONS_LIST], use:
        \\textbf{{Name}} -- Issuer (Year or Date)

4. **Missing Information - CRITICAL**
   - **DO NOT INVENT DATA**. If a section (Experience, Education, Projects, Certifications) is empty in the USER DATA, **DO NOT GENERATE IT**.
   - If the user provides no experience, the Experience section in the CV must be empty.
   - Do not fill empty fields with placeholders like "Company Name" or "Job Title".
   - If a specific field (e.g., date) is missing, omit it. Do not guess.

5. **LaTeX Safety**
   - Escape all LaTeX-sensitive characters: &, %, $, #, _, {{, }}, ^, ~.
   - Ensure the final LaTeX compiles without any errors.
   - Do not add any packages unless absolutely necessary.

6. **Output Format**
   - RETURN ONLY the final, complete LaTeX document.
   - Do NOT include markdown formatting, comments, explanations, or code fences.
   - The response MUST start directly with \\documentclass.

Generate the best possible CV using these rules.
"""
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    
    # Clean up response if it contains markdown blocks
    content = response.text.strip()
    if content.startswith("```latex"):
        content = content[8:]
    if content.startswith("```"):
        content = content[3:]
    if content.endswith("```"):
        content = content[:-3]
        
    return content.strip()

def compile_latex_to_pdf(latex_code):
    """
    Compiles LaTeX code to PDF using pdflatex.
    Returns the path to the generated PDF or None if failed.
    """
    miktex_bin_dir = r"C:\Users\GIGABYTE\AppData\Local\Programs\MiKTeX\miktex\bin\x64"
    pdflatex_cmd = os.path.join(miktex_bin_dir, 'pdflatex.exe')
    
    # Verify executable exists
    if not os.path.exists(pdflatex_cmd):
        print(f"Error: pdflatex executable not found at {pdflatex_cmd}")
        return None

    try:
        # Check if pdflatex is available using full path
        subprocess.run([pdflatex_cmd, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"pdflatex execution failed: {e}")
        return None

    with tempfile.TemporaryDirectory() as temp_dir:
        tex_path = os.path.join(temp_dir, 'cv.tex')
        pdf_path = os.path.join(temp_dir, 'cv.pdf')
        
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(latex_code)
            
        try:
            # Run pdflatex twice to resolve references if needed
            subprocess.run([pdflatex_cmd, '-interaction=nonstopmode', '-output-directory', temp_dir, tex_path], 
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Move the PDF to a persistent location (or return bytes, but file path is easier for Flask send_file)
            # For this simple app, we'll save it to a 'generated' folder in backend
            output_dir = os.path.join(os.path.dirname(__file__), 'generated')
            os.makedirs(output_dir, exist_ok=True)
            final_pdf_path = os.path.join(output_dir, 'cv.pdf')
            
            import shutil
            shutil.copy(pdf_path, final_pdf_path)
            
            return final_pdf_path
        except subprocess.CalledProcessError as e:
            print(f"LaTeX compilation failed: {e}")
            return None
