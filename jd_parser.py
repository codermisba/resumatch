import fitz  # PyMuPDF

def extract_jd_text(file_bytes, filename):
    if filename.endswith(".pdf"):
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = " ".join([page.get_text() for page in doc])
    elif filename.endswith(".txt"):
        text = file_bytes.decode("utf-8")
    else:
        raise ValueError("Unsupported JD file format. Please upload PDF or TXT.")
    return text
