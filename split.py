#!/usr/bin/env python3
"""A simple pdf splitter which makes books readable on small screens."""
import argparse
from copy import copy
from PyPDF2 import PdfFileReader, PdfFileWriter


def split_pdf_pages(args: argparse.Namespace):
    """Split pages of a pdf."""
    source = args.source
    target = args.target
    margin = args.margin
    split_count = args.splits

    with open(source, 'rb') as source_file, open(target, 'wb') as target_file:
        in_pdf = PdfFileReader(source_file)
        page_count = in_pdf.getNumPages()

        out_pdf = PdfFileWriter()

        # add first page untouched
        first_page = in_pdf.getPage(0)
        out_pdf.addPage(first_page)

        # split all following pages by half and add both halfs
        for page_number in range(2, page_count):
            page = in_pdf.getPage(page_number)

            width = page.mediaBox.upperRight[0]
            height = page.mediaBox.upperRight[1]
            cut_height = height // split_count

            for split_num in range(split_count):
                split_page = copy(page)
                split_page.mediaBox = copy(page.mediaBox)

                split_page.mediaBox.upperLeft = (
                    0,
                    min(height, margin + height - cut_height * split_num))
                split_page.mediaBox.upperRight = (
                    width,
                    min(height, margin + height - cut_height * split_num))
                split_page.mediaBox.lowerLeft = (
                    0,
                    max(0, height - cut_height * (1 + split_num) - margin))
                split_page.mediaBox.lowerRight = (
                    width,
                    max(0, height - cut_height * (1 + split_num) - margin))
                split_page.cropBox = split_page.mediaBox

                out_pdf.addPage(split_page)

        out_pdf.write(target_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('target')
    parser.add_argument('--margin', help='additional margin per split',
                        type=int, default=10)
    parser.add_argument('--splits', help='number of splits per page', type=int,
                        default=2)
    args = parser.parse_args()
    split_pdf_pages(args)
