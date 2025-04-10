import os
import tempfile

import fitz  # PyMuPDF


def get_pdf_text(parsed_file, password):
    # Create a temporary file to save the parsed PDF
    with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
        temp_pdf.write(parsed_file.read())

    # Open the temporary file to read its bytes
    with open(temp_pdf.name, "rb") as f:
        pdf_bytes = f.read()

    try:
        pdf_reader = fitz.open(stream=pdf_bytes, filetype="pdf")
        pdf_reader.authenticate(password)

        if pdf_reader.is_encrypted and not pdf_reader.is_authenticated:
            raise ValueError("Could not decrypt PDF.")
    except Exception as e:
        os.unlink(temp_pdf.name)
        raise ValueError(f"{str(e)}")

    # Reading PDF content
    text_content = ""
    for page_number in range(len(pdf_reader)):
        page = pdf_reader[page_number]
        text_content += page.get_text("text")
    # Delete the temporary PDF file
    os.unlink(temp_pdf.name)
    return text_content
