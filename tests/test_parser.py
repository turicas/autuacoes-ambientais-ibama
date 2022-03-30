import re

import rows


def test_parse_pdf():
    filename = "tests/data/amazonas-2010.pdf"
    page_number = 1
    table_rows = rows.plugins.pdf.pdf_table_lines(
        filename,
        page_numbers=(page_number,),
        starts_after="DIRETORIA DE PROTEÇÃO AMBIENTAL",
        ends_before=re.compile("Pag [0-9]+/[0-9]+"),
        algorithm="rects-boundaries",
        backend="pdfminer.six",
    )

    doc = rows.plugins.pdf.PDFMinerBackend(filename)
    # TODO: assert if the result is equal to `tests/data/amazonas-2010.csv`
