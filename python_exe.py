import functools
import multiprocessing
import re
import subprocess
import sys
from io import StringIO
from typing import Dict, Optional


@functools.lru_cache(maxsize=None)
def warn_once() -> None:
    """Warn once about the dangers of PythonREPL."""
    pass


def sanitize_input(query: str) -> str:
    """Sanitize input to the python REPL.

    Remove whitespace, backtick & python (if llm mistakes python console as terminal)

    Args:
        query: The query to sanitize

    Returns:
        str: The sanitized query
    """

    # Removes `, whitespace & python from start
    index1 = query.index("```python")
    index2 = query.index("```", index1 + 1)
    return query[index1 + 9: index2]


class PythonREPL:
    """Simulates a standalone Python REPL."""

    globals = {}
    locals = {}

    @classmethod
    def worker(
            cls,
            command: str,
            globals: Optional[Dict],
            locals: Optional[Dict],
            queue: multiprocessing.Queue,
    ) -> None:
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, globals, locals)
            sys.stdout = old_stdout
            queue.put(mystdout.getvalue())
        except Exception as e:
            sys.stdout = old_stdout
            queue.put(repr(e))

    def run(self, command: str, timeout: Optional[int] = None) -> int:
        """Run command with own globals/locals and returns anything printed.
        Timeout after the specified number of seconds."""

        command = sanitize_input(command)
        if len(command) == 0:
            raise Exception("invalid command")
        # Warn against dangers of PythonREPL
        with open('tmp/cmd.py', 'w') as f:
            f.write(command)

        pid = subprocess.Popen([sys.executable, "tmp/cmd.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)

        return pid
