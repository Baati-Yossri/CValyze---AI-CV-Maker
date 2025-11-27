from flask import Flask, render_template, request, jsonify, send_file
import os
from utils import generate_summary_gemini, generate_cv_gemini, compile_latex_to_pdf
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/create')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return "<h1>Server is working!</h1>"


@app.route('/api/generate-summary', methods=['POST'])
def generate_summary():
    data = request.json
    job_offer = data.get('job_offer')
    current_info = data.get('current_info')
    
    if not job_offer:
        return jsonify({'error': 'Job offer/Objective is required'}), 400

    try:
        summary = generate_summary_gemini(current_info, job_offer)
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-cv', methods=['POST'])
def generate_cv():
    data = request.json
    
    try:
        latex_code = generate_cv_gemini(data)
        
        pdf_path = compile_latex_to_pdf(latex_code)
        
        if pdf_path and os.path.exists(pdf_path):
            return send_file(pdf_path, as_attachment=True, download_name='cv.pdf')
        else:
            return jsonify({
                'warning': 'PDF generation failed (pdflatex might be missing). Here is the LaTeX code.',
                'latex_code': latex_code
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
