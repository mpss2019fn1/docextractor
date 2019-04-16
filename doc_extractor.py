import argparse

from pathlib import Path
from validate_directory import ValidateDirectory
from article_writer import ArticleWriter


def main():
    parser = _create_arg_parser()
    args = parser.parse_args()

    writer = ArticleWriter(output_dir=args.target, file_extension=args.extension)
    _extract_articles_in_directory(Path(args.source), writer)


def _create_arg_parser():
    parser = argparse.ArgumentParser(description="merge files into a single document")
    parser.add_argument("--source", required=True, help="source directory, which contains the files to be merged",
                        action=ValidateDirectory)
    parser.add_argument("--target", required=True, help="output directory to write the documents to",
                        action=ValidateDirectory)
    parser.add_argument("--extension", required=False, help="output file extension", default="article")
    return parser


def _extract_articles_in_directory(parent, article_writer):
    for file in parent.iterdir():
        if file.is_file():
            _extract_articles_from_file(file, article_writer)
            continue

        if file.is_dir():
            _extract_articles_in_directory(file, article_writer)


def _extract_articles_from_file(file, article_writer):
    with file.open() as f:
        line = f.readline()
        while line:
            article_writer.write_line(line)
            line = f.readline()


if __name__ == "__main__":
    main()
