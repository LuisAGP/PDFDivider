from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.core.window import Window
from PyPDF2 import PdfFileWriter, PdfFileReader
import database

Window.size = (400, 480)

db = None

class PDFSplitter(MDApp):
    title    = "PDFSplitter"
    pdf_url  = ""
    pdf_path = ""
    pdf_name = ""


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.manager = None



    def build(self):
        self.theme_cls.primary_palette = 'Teal'
        return


    '''
    Function for open the file manager
    @author Luis GP
    @return None
    '''
    def file_manager_open(self):
        path = db.getLatUrl()
        if not self.manager_open:
            self.file_manager = MDFileManager(exit_manager=self.exit_manager, select_path=self.select_path)
            self.file_manager.show(path)  # output manager to the screen
        self.manager_open = True




    '''
    Function for select a file in filemanager
    @author Luis GP
    @return None
    '''
    def select_path(self, path):
        last_path = '/'.join(str(path).split("\\")[:-1])
        db.setLastUrl(last_path if last_path != "" else "/Users")
        self.exit_manager()
        self.pdf_url = path
        self.pdf_path = last_path
        self.pdf_name = str(path).split("\\")[-1].split('.')[0]
        toast(path)




    '''
    Function for close the file manager
    @author Luis GP
    @return None
    '''
    def exit_manager(self, *args):
        self.file_manager.close()
        self.manager_open = False




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
    db = database.DB()
    PDFSplitter().run()