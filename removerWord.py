from docx import Document

def remove_watermark_from_word(file_path):
    try:
        # Load the document
        doc = Document(file_path)
        
        # Iterate over all sections to clear headers and footers
        for section in doc.sections:
            # Clear header and footer content
            header = section.header
            for paragraph in header.paragraphs:
                paragraph.clear()  # Clears all text and elements in the header
            
            footer = section.footer
            for paragraph in footer.paragraphs:
                paragraph.clear()  # Clears all text and elements in the footer
        
        # Save the modified document
        output_path = file_path.replace(".docx", ".docx")
        doc.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error: {e}")
        return None
