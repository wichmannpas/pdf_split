#!/usr/bin/env python3
"""A simple pdf splitter which makes books readable on small screens."""
import argparse
from copy import copy
from PyPDF2 import PdfFileReader, PdfFileWriter


def split_pdf_pages(args: argparse.Namespace):
    """Split pages of a pdf."""
    source = args.source
    target = args.target

    with open(source, 'rb') as source_file, open(target, 'wb') as target_file:
        in_pdf = PdfFileReader(source_file)
        page_count = in_pdf.getNumPages()

        out_pdf = PdfFileWriter()

        # add first page untouched
        first_page = in_pdf.getPage(1)
        out_pdf.addPage(first_page)

        # split all following pages by half and add both halfs
        for page_number in range(2, page_count):
            page = in_pdf.getPage(page_number)

            width = page.mediaBox.upperRight[0]
            height = page.mediaBox.upperRight[1]

            first_half = copy(page)
            first_half.mediaBox = copy(first_half.mediaBox)
            second_half = copy(page)
            second_half.mediaBox = copy(second_half.mediaBox)

            cut_point = height // 2

            # upper half
            first_half.mediaBox.lowerLeft = 0, cut_point - 10
            first_half.mediaBox.lowerRight = width, cut_point - 10

            # lower half
            second_half.mediaBox.upperLeft = 0, cut_point + 10
            second_half.mediaBox.upperRight = width, cut_point + 10

            out_pdf.addPage(first_half)
            out_pdf.addPage(second_half)

        out_pdf.write(target_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('target')
    args = parser.parse_args()
    split_pdf_pages(args)
