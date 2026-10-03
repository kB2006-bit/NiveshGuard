import sys
from docx import Document

def extract_text(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_docx.py <file1> <file2> ...")
        sys.exit(1)
    
    for path in sys.argv[1:]:
        print(f"--- START OF FILE: {path} ---")
        print(extract_text(path))
        print(f"--- END OF FILE: {path} ---\n")
