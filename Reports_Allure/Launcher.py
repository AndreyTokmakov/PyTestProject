import subprocess
import sys
from typing import Tuple


def run_command(cmd: str, print_output: bool = True) -> Tuple[str, int]:
    try:
        proc = subprocess.Popen(cmd.split(),
                                text=True,
                                shell=False,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        output: str = ''
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            if print_output:
                print(str(line.rstrip()).strip("b'"))
                sys.stdout.flush()

            output += line

        proc.wait()
        return output, proc.returncode

    except OSError as exc:
        return f"Can't run process. Error code = {exc}", -1


if __name__ == '__main__':
    params = ['python -m pytest',
              '-sv',
              'combine/ArpPoisoning.py',
              '--alluredir combine/results'
              ]

    output, code = run_command(" ".join(params))
