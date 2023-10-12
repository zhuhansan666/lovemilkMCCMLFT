import os
import sys
import subprocess
from pathlib import Path
from typing import Literal


class Manager:
    """
    You can use mgr.write(<sth>).delete().write(<sth>)...
    """

    def __init__(self, encoding: str | None = 'ascii', suffix: str = '# lovemilkMCCMLFT') -> None:
        self.encoding = encoding
        self.suffix = suffix

    @property
    def hosts_file(self) -> Path:
        return (
            Path(os.getenv('windir', 'C:/Windows')) /
            'System32/drivers/etc/hosts'
            if sys.platform == 'win32' else
            Path('/etc/hosts')
        )
    
    def open_hosts(self):
        if sys.platform == 'win32':
            os.popen(f'start {self.hosts_file}')
            return
        
        # Linux and MacOS untested
        # Default use system default editor open in the new Konsole
        subprocess.Popen(
            f'konsole -e "{os.getenv("EDITOR", "vim")} {self.hosts_file}"',
            close_fds=True,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            shell=True
        )


    def read(self):
        with self.hosts_file.open('r', encoding=self.encoding) as fp:
            return fp.read()

    def write(self, sign: Literal['auth', 'login'], data: str):
        # add <return> at start and end
        data = f'\n{data}' if not data.startswith('\n') else data
        data = f'{data}\n' if not data.endswith('\n') else data

        info = self.read().split('\n')

        with self.hosts_file.open('a', encoding=self.encoding) as fp:
            if len(info) > 0 and len(info[-1]) > 0:
                fp.write('\n')

            for line in data.split('\n'):
                if len(line) > 0:  # not empty
                    line = f'{line} {self.suffix}&{sign}\n'
                    fp.write(line)

        return self

    def delete(self, sign: Literal['auth', 'login'], write: bool = True):
        with self.hosts_file.open('r', encoding=self.encoding) as fp:
            result = fp.readlines()
            for line in result.copy():
                if line.strip().endswith('#MCLFT_') or \
                        line.strip().endswith(f'{self.suffix}&{sign}'):
                    result.remove(line)  # remove this line

        data = ''.join(result)
        if not write:
            return self

        with  self.hosts_file.open('w', encoding=self.encoding) as fp:
            fp.write(data)
        return self
