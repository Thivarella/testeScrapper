import os
import shutil

from flask import send_file, Response
from flask_restful import Resource

from models import GenerateCsv


class ProdutoResource(Resource):
    @staticmethod
    def get(pages):
        if int(pages) < 2:
            return Response('Número de páginas precisa ser maior ou igual a 2')

        _clear_folder('output')
        generate_csv = GenerateCsv()
        filepath, filename = generate_csv.get_pages(int(pages))
        return send_file(filepath,
                         mimetype='text/csv',
                         attachment_filename=filename,
                         as_attachment=True,
                         cache_timeout=0)


def _clear_folder(path):
    folder = path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
