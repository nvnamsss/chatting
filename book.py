from PyPDF2 import PdfReader

class BookFeeder:
    def read(self, path: str):
        reader = PdfReader(path)
        number_of_pages = len(reader.pages)
        page = reader.pages[0]
        text = page.extract_text()

        return text
    def Feed(self, path: str):
        text = self.read(path)
        

