import asyncio
import os
from pdf2jpg import pdf2jpg

async def extractImg(filename):
    output = os.path.join("PdfTxtBot", "Docs")
    page=pdf2jpg.convert_pdf2jpg(filename,output,dpi=300,pages="ALL")
    return page
        
if __name__=='__main__':
    asyncio.run(extractImg("PdfTxtBot\sample.pdf"))