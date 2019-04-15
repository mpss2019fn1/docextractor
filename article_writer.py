import re


class ArticleWriter:

    def __init__(self, output_dir, file_extension="article"):
        self._file_extension = file_extension
        self._is_within_article = False
        self._is_first_line = True
        self._output_dir = output_dir
        self._article_name = ""
        self._article_id = ""
        self._article_file = None
        self._extractor_regex = re.compile(r'id="(?P<id>\d+)".+title="(?P<title>[^(]+?)(\s\((?P<role>.+?)\))?"',
                                           re.IGNORECASE)

    def write_line(self, line):
        if len(line.strip()) < 1:
            return

        if not self._is_within_article:
            if not self._is_article_start(line):
                return

            self._start_article(line)
            return

        if not self._is_within_article:
            return

        if self._is_article_end(line):
            self._end_article()
            return

        if self._is_first_line:
            self._is_first_line = False
            return

        print(f"{self._replace_article_subject(line)}", file=self._article_file, end="")

    @staticmethod
    def _is_article_start(line):
        return line.strip().startswith("<doc")

    @staticmethod
    def _is_article_end(line):
        return line.strip().startswith("</doc")

    def _start_article(self, line):
        match = self._extractor_regex.search(line)
        if not match:
            return

        self._is_within_article = True
        self._is_first_line = True
        self._article_id = match.group("id")
        self._article_name = match.group("title")
        self._article_file = open(f"{self._output_dir}{self._article_name.replace(' ', '_')}_{self._article_id}.{self._file_extension}", "w+")

    def _end_article(self):
        print(f"{self._article_id} {self._article_name}")
        self._is_within_article = False
        self._article_file.close()

    def _replace_article_subject(self, line):
        return line.replace(f"{self._article_name}", f"{self._article_name.replace(' ', '_')}_{self._article_id}")
