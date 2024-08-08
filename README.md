# Research Paper Summarizer

## Overview

The Research Paper Summarizer is a web application designed to help users quickly fetch and summarize the latest research papers from arXiv. This tool is ideal for researchers, students, and anyone interested in staying updated with the latest scientific advancements. Simply enter a research topic, specify the number of papers to fetch, and let the application handle the rest!

## Features

- **Fetch Latest Research Papers:** Retrieve the most recent papers from arXiv by entering a topic.
- **Summarize Papers:** Generate concise summaries for individual research papers.
- **Download PDFs:** Download the full text of the research papers in PDF format directly from the application.
- **Clean and Professional UI:** Enjoy a user-friendly interface with a modern design.

## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **APIs:** OpenAI GPT-4 (for summarization), arXiv API (for fetching papers)
- **Libraries:** requests, PyPDF2, nltk, langchain

## Installation

### 1. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables:

- Create a `.env` file in the root directory.
- Add your OpenAI API key:

```makefile
OPENAI_API_KEY=your-openai-api-key
```

### 4. Run the application:

```bash
python app.py
```

### 5. Access the application:

- Open your web browser and navigate to `http://127.0.0.1:5001/`.

## Usage

### Homepage:
The homepage welcomes you with a brief overview of the tool. Enter your desired research topic and the number of papers you wish to retrieve.

### Fetch Papers:
After submitting the topic, the application fetches the most recent papers from arXiv and displays them on a results page.

### Summarize:
For each paper, click the "Summarize" button to generate a concise summary of the paper.

### Download PDF:
You can also download the full text of the research papers in PDF format using the "Download PDF" button.

## Screenshots

### Homepage

![Homepage](static/screenshots/homepage.png)

### Results Page

![Results](static/screenshots/results.png)

## Customization

You can customize the application by modifying the `style.css` file for styling or updating the backend logic in `app.py` for different summarization models or additional features.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

If you have any questions, feel free to contact me at [your-email@example.com](mailto:your-email@example.com).
