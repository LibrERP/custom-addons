# © 2016-2018 Savoir-faire Linux
# © 2018 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).

import psutil
import signal
import subprocess
import time
import logging

from odoo import _
from odoo.exceptions import ValidationError
from typing import List

_logger = logging.getLogger(__name__)


def run_subprocess(command: List[str], timeout):
    """Run the given command as a subprocess.

    When the timeout expires, the process is terminated.

    :param command: the command to execute
    :param timeout: the timeout of the process in seconds
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    timetaken = 0

    while True:
        output, error = process.communicate()
        status = process.returncode
        if status is 0:
            break
        elif status is not None:
            _logger.info('Errore validazione {errore}'.format(errore=error))
            raise ValidationError(
                _('Command {command} exited with status {status} and error {error}.').format(
                    command=command,
                    status=status,
                    error=error,
                ))

        timetaken += 0.1
        time.sleep(0.1)

        if timetaken > timeout:
            terminate_process(process)
            raise ValidationError(
                _('Timeout ({timeout} seconds) expired while executing '
                  'the command: {command}').format(
                    command=command,
                    timeout=timeout,
                ))


def terminate_process(process):
    """Attempt to terminate the process.

    Kill the process if it is still alive after 60 seconds.

    :param string process: the process pid to kill
    """
    process.terminate()
    for i in range(60):
        time.sleep(1)
        if process.poll() is not None:
            return

    parent = psutil.Process(process.pid)
    for child in parent.children(recursive=True):
        child.send_signal(signal.SIGKILL)
    parent.send_signal(signal.SIGKILL)
