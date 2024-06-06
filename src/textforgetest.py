import unittest
from forge import Forge


class TestMain(unittest.TestCase):
    def test_path_function(self) -> None:
        forge = Forge()
        test_cases = [
            {
                'input': {
                    'ext': '',
                    'path': 'path.txt.j2',
                    'prefix': '',
                    'suffix': '',
                    'outdir': '.'
                },
                'output': './path.txt'
            },
            {
                'input': {
                    'ext': '',
                    'path': 'path.txt.jinja',
                    'prefix': '',
                    'suffix': '',
                    'outdir': '.'
                },
                'output': './path.txt'
            },
            {
                'input': {
                    'ext': '',
                    'path': 'path.txt',
                    'prefix': '',
                    'suffix': '',
                    'outdir': '.'
                },
                'output': './path.txt'
            },
            {
                'input': {
                    'ext': '.other',
                    'path': 'path.txt.j2',
                    'prefix': '',
                    'suffix': '',
                    'outdir': '.'
                },
                'output': './path.other'
            },
            {
                'input': {
                    'ext': '',
                    'path': 'path.txt.j2',
                    'prefix': 'pre-',
                    'suffix': '-suf',
                    'outdir': '.'
                },
                'output': './pre-path-suf.txt'
            },
            {
                'input': {
                    'ext': '.chg',
                    'path': 'path.txt.j2',
                    'prefix': 'pre-',
                    'suffix': '-suf',
                    'outdir': 'mydir'
                },
                'output': 'mydir/pre-path-suf.chg'
            }
        ]
        for case in test_cases:
            with self.subTest(case=case):
                result = forge._process_file_name(**case['input'])
                self.assertEqual(result, case['output'])

    def test_render(self) -> None:
        forge = Forge()
        test_cases = [
            {
                'input': {
                    'content': 'This is a line {{ a }}',
                    'data': {
                        'a': 'VALUE'
                    }
                },
                'output': 'This is a line VALUE'
            },
            {
                'input': {
                    'content': 'This is a line {{ a.b }}',
                    'data': {
                        'a': {
                            'b': 123
                        }
                    }
                },
                'output': 'This is a line 123'
            },
            {
                'input': {
                    'content': 'This is a line {{ a }}\nNL',
                    'data': {
                        'a': {
                            'b': 123
                        }
                    }
                },
                'output': 'This is a line {\'b\': 123}\nNL'
            }
        ]
        for case in test_cases:
            with self.subTest(case=case):
                result = forge._render(**case['input'])
                self.assertEqual(result, case['output'])


if __name__ == "__main__":
    unittest.main()
