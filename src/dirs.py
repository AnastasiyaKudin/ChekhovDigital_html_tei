from pathlib import Path

BASE_PATH = Path(__file__).absolute().parent.parent
DATA_PATH = BASE_PATH / 'data'
Texts_HTML_PATH = DATA_PATH / 'texts_html'
Texts_TEI_PATH = DATA_PATH / 'texts_tei'
TEI_Preform_file = DATA_PATH / 'TEIdoc.xml'
NOTES_Preform_PATH = DATA_PATH / 'notes_html'