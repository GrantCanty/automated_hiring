from unstructured.partition.pdf import partition_pdf
import io


def load_pdf(file):
    text = None
    file_name = None
    if file is not None:
        # cv has been submitted. save cv file name
        file_name = file.name
        if file_name is not None:
            file_bytes = file.read() # Convert file to bytes for DB storage
            blocks = partition_pdf(file=io.BytesIO(file_bytes))
            blocks = [str(el) for el in blocks]
            text = ''
            for i in range(len(blocks)):
                text += blocks[i]
                if i -1 < len(blocks):
                    text += ' '
    
    return file_name, file_name