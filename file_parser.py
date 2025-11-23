import logging
import docx2txt
import PyPDF2

def parse_pdf(file) -> str:
    logging.info("[Parser] PDF 파일 파싱 시작")
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    logging.info("[Parser] PDF 파싱 완료")
    return text

def parse_txt(file) -> str:
    logging.info("[Parser] TXT 파일 파싱 시작")
    return file.read().decode("utf-8")

def parse_docx(file) -> str:
    logging.info("[Parser] DOCX 파일 파싱 시작")
    return docx2txt.process(file)
