import os
# import pypdf # Uncomment when installed

def extract_text_from_file(file_path, file_type):
    """
    Extracts text from various file types.
    """
    text = ""
    try:
        if file_type == 'PDF':
            # try:
            #     reader = pypdf.PdfReader(file_path)
            #     for page in reader.pages:
            #         text += page.extract_text() + "\n"
            # except Exception as e:
            #     print(f"Error reading PDF: {e}")
            pass # Placeholder
        elif file_type == 'CODE' or file_type == 'NOTE':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        elif file_type == 'SLIDE':
             # Placeholder for PPTX extraction
             pass
    except Exception as e:
        print(f"Error extracting text: {e}")
    
    return text
