#!/usr/bin/env python3
"""A simple pdf splitter which makes books readable on small screens."""
import argparse
from copy import copy
from PyPDF2 import PdfFileReader, PdfFileWriter


def split_pdf_pages(args: argparse.Namespace):
    """Split pages of a pdf."""
    with open(args.source, 'rb') as source_file, open(args.target, 'wb') as target_file:
        in_pdf = PdfFileReader(source_file)
        page_count = in_pdf.getNumPages()

        out_pdf = PdfFileWriter()

        first_split_page = 0
        if not args.split_first_page:
            # add first page untouched
            first_page = in_pdf.getPage(0)
            out_pdf.addPage(first_page)
            first_split_page = 1

        # split all following pages by half and add both halfs
        for page_number in range(first_split_page, page_count):
            page = in_pdf.getPage(page_number)

            actual_width = page.mediaBox.upperRight[0]
            actual_height = page.mediaBox.upperRight[1]
            width = actual_width - args.crop_left - args.crop_right
            height = actual_height - args.crop_top - args.crop_bottom
            cut_height = height // args.splits

            for split_num in range(args.splits):
                split_page = copy(page)
                split_page.mediaBox = copy(page.mediaBox)

                left_x = args.crop_left
                right_x = width + args.crop_left

                upper_y = min(
                    args.crop_bottom + height,
                    args.crop_bottom + args.margin + height - cut_height * split_num)
                lower_y = max(
                    args.crop_bottom,
                    args.crop_bottom - args.margin + height - cut_height * (
                        1 + split_num))

                split_page.mediaBox.upperLeft = left_x, upper_y
                split_page.mediaBox.upperRight = right_x, upper_y
                split_page.mediaBox.lowerLeft = left_x, lower_y
                split_page.mediaBox.lowerRight = right_x, lower_y

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
    parser.add_argument('--crop-left', type=int, default=0,
                        help='Additional margin to crop an all pages')
    parser.add_argument('--crop-top', type=int, default=0,
                        help='Additional margin to crop an all pages')
    parser.add_argument('--crop-right', type=int, default=0,
                        help='Additional margin to crop an all pages')
    parser.add_argument('--crop-bottom', type=int, default=0,
                        help='Additional margin to crop an all pages')
    parser.add_argument('--split-first-page', action='store_true',
                        help='Split the first page as well')
    args = parser.parse_args()
    if args.splits < 1:
        parser.error('argument --splits: invalid choice: '
                     'split count may not be zero.')
    split_pdf_pages(args)
