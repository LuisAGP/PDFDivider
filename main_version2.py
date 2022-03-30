from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.core.window import Window
from PyPDF2 import PdfFileWriter, PdfFileReader
import tkinter as tk
from tkinter.filedialog import askopenfilename
tk.Tk().withdraw()

Window.size = (400, 480)

class PDFSplitter(MDApp):
    title    = "PDFSplitter"
    pdf_url  = ""
    pdf_path = ""
    pdf_name = ""


    def __init__(self, **kwargs):
        super().__init__(**kwargs)



    def build(self):
        self.theme_cls.primary_palette = 'Teal'
        return


    '''
    Function for open the file manager
    @author Luis GP
    @return None
    '''
    def file_manager_open(self):
        self.pdf_url   = askopenfilename()
        self.pdf_path  = '/'.join(str(self.pdf_url).split("/")[:-1])
        self.pdf_name  = str(self.pdf_url).split("/")[-1].split('.')[0]

        self.root.ids.label_pdf_path.text = str(self.pdf_url)
        toast(self.pdf_url)




    '''
    Function for split a PDF file
    @author Luis GP
    @return None
    '''
    def split_pdf(self):

        if self.pdf_url.split('.')[-1] != "pdf":
            toast("PDF no encontrado")
            return None

        todo  = self.root.ids.todo.active
        pares = self.root.ids.pares.active
        rango = self.root.ids.rango.active

        if todo:
            self.process_pdf("all")
        elif pares:
            self.process_pdf("pairs")
        elif rango:
            self.process_pdf("range", self.root.ids.rango_value.text)
        else:
            toast("No se ha seleccionado una opción")


    
    '''
    Function for process a PDF file
    @author Luis GP
    @return None
    '''
    def process_pdf(self, pages, pages_list=""):
        inputpdf = PdfFileReader(open(self.pdf_url, "rb"))

        try:

            # All pages split
            if pages == "all":
                for i in range(inputpdf.numPages):
                    output = PdfFileWriter()
                    output.addPage(inputpdf.getPage(i))
                    with open(f"{self.pdf_path}/{self.pdf_name}{i}.pdf", "wb") as outputStream:
                        output.write(outputStream)

            # Split PDF in pairs
            elif pages == "pairs":
                output = PdfFileWriter()
                for i in range(inputpdf.numPages):
                    output.addPage(inputpdf.getPage(i))
                    if (int(i) + 1) % 2 == 0:
                        with open(f"{self.pdf_path}/{self.pdf_name}{i}.pdf", "wb") as outputStream:
                            output.write(outputStream)
                        output = PdfFileWriter()

            # Split PDF by custom pages
            elif pages == "range":
                custom_pages = []

                # Range of pages
                if '-' in pages_list:
                    numbers = pages_list.split('-')
                    init = int(numbers[0]) - 1
                    end  = int(numbers[-1])
                    custom_pages = [i for i in range(init, end)]

                    output = PdfFileWriter()
                    for i in custom_pages:
                        if i >= 0 and i < inputpdf.numPages:
                            output.addPage(inputpdf.getPage(i))
                        else:
                            break

                    with open(f"{self.pdf_path}/{self.pdf_name}_rango-1.pdf", "wb") as outputStream:
                            output.write(outputStream)

                # Selected pages
                elif ',' in pages_list:
                    for i in pages_list.split(','):
                        custom_pages.append(int(str(i).strip()) - 1)

                    output = PdfFileWriter()
                    for i in custom_pages:
                        if i >= 0 and i < inputpdf.numPages:
                            output.addPage(inputpdf.getPage(i))
                        else:
                            continue

                    with open(f"{self.pdf_path}/{self.pdf_name}_rango-2.pdf", "wb") as outputStream:
                        output.write(outputStream)


                # Only one page
                else:
                    page = int(pages_list)-1

                    if page >= 0 and page < inputpdf.numPages: 
                        output = PdfFileWriter()
                        output.addPage(inputpdf.getPage(page))
                        with open(f"{self.pdf_path}/{self.pdf_name}_rango-3.pdf", "wb") as outputStream:
                            output.write(outputStream)


            toast(f"El PDF ha sido separado con exito!")

        except Exception as e:
            toast(f"error: {e}") 

        

if __name__=="__main__":
    PDFSplitter().run()