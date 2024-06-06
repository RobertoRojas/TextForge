import sys

from jinja2 import Template
from pathlib import Path
from typing import List

from file import get_content, out_file


class Forge():
    def _render(self, content: str, data: dict) -> str:
        try:
            t = Template(content)
            return t.render(data)
        except Exception as ex:
            print('Cannot forge the file: {}'.format(ex))
            sys.exit(5)

    def _remove_jinja_ext(self, path: str) -> str:
        if path.endswith('.jinja'):
            return path[:-6]
        if path.endswith('.j2'):
            return path[:-3]
        return path

    def _process_file_name(self, path: str, prefix: str,
                           suffix: str, ext: str,
                           outdir: str) -> str:
        filepath = Path(self._remove_jinja_ext(path=path))
        fileext = filepath.suffix if ext == '' else ext
        return f'{outdir}/{prefix}{filepath.stem}{suffix}{fileext}'

    def forge(self, templatespath: List[str], data: dict,
              prefix: str, suffix: str, ext: str,
              outdir: str) -> None:
        for path in templatespath:
            content = get_content(path=path)
            rendercontent = self._render(content=content, data=data)
            filename = self._process_file_name(path=path,
                                               prefix=prefix,
                                               suffix=suffix,
                                               ext=ext,
                                               outdir=outdir)
            out_file(content=rendercontent, path=filename)
