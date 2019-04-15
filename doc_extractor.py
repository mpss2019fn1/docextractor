import argparse
import os

from validate_directory import ValidateDirectory
from article_writer import ArticleWriter


def main():
    parser = _create_arg_parser()
    args = parser.parse_args()

    writer = ArticleWriter(output_dir=args.target, file_extension=args.extension)
    for filename in os.listdir(args.source):
        with open(f"{args.source}/{filename}", "r") as file:
            line = file.readline()
            while line:
                writer.write_line(line)
                line = file.readline()


def _create_arg_parser():
    parser = argparse.ArgumentParser(description="merge files into a single document")
    parser.add_argument("--source", required=True, help="source directory, which contains the files to be merged",
                        action=ValidateDirectory)
    parser.add_argument("--target", required=True, help="output directory to write the documents to",
                        action=ValidateDirectory)
    parser.add_argument("--extension", required=False, help="output file extension", default="article")
    return parser


if __name__ == "__main__":
    main()
