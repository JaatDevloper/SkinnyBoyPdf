# -*- coding: utf-8 -*-
from PdfTxtBot import PDFBot
from config import TOKEN
from healthcheck import start_healthcheck_server

if __name__=='__main__':
    start_healthcheck_server()
    ob=PDFBot(TOKEN)
    ob.app.run_polling()