# this file will translate a text PDF file into a text file
# install requirements first pip install -r ./requirements.txt or with pyenv - pyenv exec pip install -r ./requirements.txt
# to run this file, type in the command line:
# python pdf2txt.py -o <output file> -i <input pdf> -d <service name> -k <service key>
# the output file will be in the same directory as the input file
# output appends to existing file, so if you want to start fresh, delete the output file

import sys
import html
from pypdf import PdfReader, PdfWriter
import argparse
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

def table_to_html(table):
    table_html = "<table>"
    rows = [
        sorted([cell for cell in table.cells if cell.row_index == i], key=lambda cell: cell.column_index)
        for i in range(table.row_count)
    ]
    for row_cells in rows:
        table_html += "<tr>"
        for cell in row_cells:
            tag = "th" if (cell.kind == "columnHeader" or cell.kind == "rowHeader") else "td"
            cell_spans = ""
            if cell.column_span > 1:
                cell_spans += f" colSpan={cell.column_span}"
            if cell.row_span > 1:
                cell_spans += f" rowSpan={cell.row_span}"
            table_html += f"<{tag}{cell_spans}>{html.escape(cell.content)}</{tag}>"
        table_html += "</tr>\n"
    table_html += "</table>"
    return table_html

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Convert PDF to text. Output appends to existing file, so if you want to start fresh, delete the output file')
    parser.add_argument('-o', '--output', help='output file name', required=True)
    parser.add_argument('-i', '--input', help='input file name', required=True)
    
    parser.add_argument('-d', '--doc_intel', help='Service Name for Document Intelligence', required=True)
    parser.add_argument('-k', '--doc_key', help='Service Key for Document Intelligence', required=True)
    args = parser.parse_args()
    form_recognizer_creds = (
        default_creds if args.doc_key is None else AzureKeyCredential(args.doc_key)
    )

    offset = 0
    page_map = []
    form_recognizer_client = DocumentAnalysisClient(
        endpoint=f"https://{args.doc_intel}.cognitiveservices.azure.com/",
        credential=form_recognizer_creds,
        headers={"x-ms-useragent": "azure-search-chat-demo/1.0.0"},
    )
    with open(args.input, "rb") as f:
        poller = form_recognizer_client.begin_analyze_document("prebuilt-layout", f)
    form_recognizer_results = poller.result()
    for page_num, page in enumerate(form_recognizer_results.pages):
        tables_on_page = [
            table
            for table in form_recognizer_results.tables
            if table.bounding_regions[0].page_number == page_num + 1
        ]

        # mark all positions of the table spans in the page
        page_offset = page.spans[0].offset
        page_length = page.spans[0].length
        table_chars = [-1] * page_length
        for table_id, table in enumerate(tables_on_page):
            for span in table.spans:
                # replace all table spans with "table_id" in table_chars array
                for i in range(span.length):
                    idx = span.offset - page_offset + i
                    if idx >= 0 and idx < page_length:
                        table_chars[idx] = table_id

        # build page text by replacing characters in table spans with table html
        page_text = ""
        added_tables = set()
        for idx, table_id in enumerate(table_chars):
            if table_id == -1:
                page_text += form_recognizer_results.content[page_offset + idx]
            elif table_id not in added_tables:
                page_text += table_to_html(tables_on_page[table_id])
                added_tables.add(table_id)

        page_text += " "
        page_map.append((page_num, offset, page_text))
        with open(args.output, "a", encoding="utf-8") as out:
            out.write(page_text)
        offset += len(page_text)
        
    form_recognizer_client.close()
        






