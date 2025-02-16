import PyPDF2

def load_pdf(path):
    with open(path,"rb") as file_path:
        reader=PyPDF2.PdfFileReader(file_path)
        text="".join([page.extract_text() for page in reader])

    return text