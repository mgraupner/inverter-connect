from bx_py_utils.auto_doc import assert_readme_block
from bx_py_utils.path import assert_is_file
from manageprojects.test_utils.click_cli_utils import invoke_click
from manageprojects.tests.base import BaseTestCase

from inverter import constants
from inverter.cli.cli_app import PACKAGE_ROOT, cli


def assert_cli_help_in_readme(text_block: str, marker: str):
    README_PATH = PACKAGE_ROOT / 'README.md'
    assert_is_file(README_PATH)

    text_block = text_block.replace(constants.CLI_EPILOG, '')
    text_block = f'```\n{text_block.strip()}\n```'
    assert_readme_block(
        readme_path=README_PATH,
        text_block=text_block,
        start_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} start ✂✂✂)',
        end_marker_line=f'[comment]: <> (✂✂✂ auto generated {marker} end ✂✂✂)',
    )


class ReadmeTestCase(BaseTestCase):
    def test_main_help(self):
        stdout = invoke_click(cli, '--help')
        self.assert_in_content(
            got=stdout,
            parts=(
                'Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...',
                'print-at-commands',
                'print-values',
                constants.CLI_EPILOG,
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='main help')

    def test_print_values_help(self):
        stdout = invoke_click(cli, 'print-values', '--help')
        self.assert_in_content(
            got=stdout,
            parts=(
                'Usage: ./cli.py print-values [OPTIONS] IP',
                '--port',
                '--debug/--no-debug',
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='print-values help')

    def test_print_at_commands(self):
        stdout = invoke_click(cli, 'print-at-commands', '--help')
        self.assert_in_content(
            got=stdout,
            parts=(
                'Usage: ./cli.py print-at-commands [OPTIONS] IP [COMMANDS]...',
                '--port',
                '--debug/--no-debug',
            ),
        )
        assert_cli_help_in_readme(text_block=stdout, marker='print-at-commands help')