import os
import markdown


class ScannerParseException(Exception):
    '''
    Parser exception
    '''


class ScannerException(Exception):
    '''
    Scanner general exception
    '''


class Scanner(object):
    '''
    Scan articles and sort their types.
    '''
    def __init__(self, path):
        '''
        Object scanner

        :param path:
        :param slider: Category string for slider
        '''
        if os.path.exists(path):
            self._path = path
        else:
            raise OSError('Path "{0}" does not exist.'.format(path))
        self.slider = list()
        self.slider_type = 'slider'

    def scan(self):
        '''
        Scan for the articles.

        :return:
        '''
        self.slider = list()
        for r_path, dirs, files in os.walk(self._path):
            for obj in files:
                self.categorize(os.path.join(r_path, obj))

        return self

    def categorize(self, path):
        '''
        Categorize article

        :param path:
        :return:
        '''
        if not path.endswith(".md"):
            return

        data = self._parse_md_object(path)
        if data.get('type', '').lower() == self.slider_type:
            self.slider.append(data)

    def _parse_md_object(self, path):
        '''
        Parse Markdown file.

        :param path:
        :return:
        '''
        chunks = open(path).read().split(os.linesep * 2, 1)
        if len(chunks) != 2:
            raise ScannerParseException('Parse error: file "{0}" should have header and a content!'.format(path))
        header, content = chunks
        data = dict()
        for line in header.split(os.linesep):
            line = line.split(":", 1)
            if len(line) != 2:
                raise ScannerParseException('Parse error: file "{0}" has an invalid header: "{1}"'.format(
                    path, ':'.join(line)))
            data[line[0].strip().lower()] = line[1].strip()
        data['content'] = markdown.markdown(unicode(content, 'UTF-8'))

        return data
