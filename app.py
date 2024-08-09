from flask import Flask, render_template, request, jsonify
import arxiv
import requests
import os
import re
import nltk
import PyPDF2
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI
from langchain.schema import Document

nltk.download('punkt')

app = Flask(__name__)

# Function to fetch recent papers
def fetch_recent_papers(topic, max_results=5):
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    papers = []
    for result in search.results():
        paper_info = {
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "summary": result.summary,
            "published": result.published,
            "pdf_url": result.pdf_url
        }
        papers.append(paper_info)
    return papers

# Function to download PDF
def download_pdf(pdf_url, output_path):
    response = requests.get(pdf_url)
    with open(output_path, 'wb') as file:
        file.write(response.content)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to save text to file
def save_text_to_file(text, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

# Function to extract sections
def extract_sections(text):
    sections = {
        'abstract': '',
        'introduction': '',
        'experiment': '',
        'results': '',
        'conclusion': '',
        'future_work': ''
    }

    patterns = {
        'abstract': re.compile(r'\bAbstract\b(.*?)(?=\b1\s+Introduction\b)', re.DOTALL | re.IGNORECASE),
        'introduction': re.compile(r'\b1\s+Introduction\b(.*?)(?=\b(?:2\s+|Methods|Experiments?|Experiment)\b)', re.DOTALL | re.IGNORECASE),
        'experiment': re.compile(r'\b(?:Methods|Experiments?|Experiment)\b(.*?)(?=\b(?:[3-9]\s+|Results?|Discussion|Conclusion|Future Work)\b)', re.DOTALL | re.IGNORECASE),
        'results': re.compile(r'\b(?:Results?|Findings)\b(.*?)(?=\b(?:[4-9]\s+|Discussion|Conclusion|Future Work)\b)', re.DOTALL | re.IGNORECASE),
        'conclusion': re.compile(r'\b(?:Conclusion|Summary)\b(.*?)(?=\b(?:Future Work|Acknowledgements|References)\b)', re.DOTALL | re.IGNORECASE),
        'future_work': re.compile(r'\b(?:Future Work|Future Directions)\b(.*?)(?=\b(?:Acknowledgements|References)\b)', re.DOTALL | re.IGNORECASE)
    }

    for section, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            sections[section] = match.group(1).strip()

    return sections

# Function to summarize sections
def summarize_sections(extracted_sections, llm):
    chain = load_summarize_chain(llm, chain_type="stuff")
    combined_summary = []
    
    for section, content in extracted_sections.items():
        if content:
            mock_document = Document(page_content=content)
            result = chain.invoke([mock_document])
            combined_summary.append(result["output_text"])
    
    return " ".join(combined_summary)

# Home route to render index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch and display papers
@app.route('/fetch_papers', methods=['POST'])
def fetch_papers():
    topic = request.form['topic']
    max_results = int(request.form['max_results'])
    
    papers = fetch_recent_papers(topic, max_results=max_results)
    
    return render_template('result.html', papers=papers, topic=topic)

# Route to summarize a specific paper
@app.route('/summarize_paper', methods=['POST'])
def summarize_paper():
    paper_url = request.form['paper_url']
    pdf_filename = os.path.basename(paper_url)
    pdf_path = os.path.join('pdfs', pdf_filename)
    
    if not os.path.exists(pdf_path):
        download_pdf(paper_url, pdf_path)
    
    text_path = pdf_path.replace('pdfs', 'texts').replace('.pdf', '.txt')
    
    if not os.path.exists(text_path):
        text = extract_text_from_pdf(pdf_path)
        save_text_to_file(text, text_path)
    else:
        with open(text_path, 'r', encoding='utf-8') as file:
            text = file.read()
    
    # Extract sections
    extracted_sections = extract_sections(text)
    
    # Initialize the language model
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
    
    # Summarize sections
    combined_summary = summarize_sections(extracted_sections, llm)
    
    return jsonify(summary=combined_summary)

if __name__ == '__main__':
    if not os.path.exists('pdfs'):
        os.makedirs('pdfs')
    if not os.path.exists('texts'):
        os.makedirs('texts')
    app.run(debug=True, port=5001)
