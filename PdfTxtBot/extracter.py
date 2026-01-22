import fitz  # PyMuPDF


class TextExtractor:
    def __init__(self, filename: str) -> None:
        self.filename = filename

    @property
    def extract(self) -> str:
        outpub = ""
        try:
            # Open the PDF file
            doc = fitz.open(self.filename)
            for page in doc:
                text = page.get_text()
                if text:
                    outpub += text
            doc.close()
            return outpub
        except Exception as e:
            print(f"Extraction error: {e}")
            return outpub


if __name__ == '__main__':
    txt = TextExtractor("https://api.telegram.org/file/bot6000547107:AAGQFqWez7wUDmT2xSWMS5GG_1tRH691cFk/documents/file_0.pdf")
    print(txt.extract)
