from cube_helper.logger import log_module, log_inconsistent
import cube_helper as ch
from common import _redirect_stdout, _redirect_stderr
import platform
if float(platform.python_version()[0:3]) <= 2.7:
    from io import BytesIO as IO
else:
    from io import StringIO as IO
import unittest
import sys


class TestLogger(unittest.TestCase):

    def test_log_module_logging(self):
        with self.assertLogs('cube_helper.logger', level='INFO') \
                as cm:
            log_module().info('info message')
            log_module().warning('warning message')
            log_module().critical('critical message')
            log_module().error('error message')
        self.assertIn('INFO:cube_helper.logger:info message',
                      cm.output)
        self.assertIn('WARNING:cube_helper.logger:warning message',
                      cm.output)
        self.assertIn('CRITICAL:cube_helper.logger:critical message',
                      cm.output)
        self.assertIn('ERROR:cube_helper.logger:error message',
                      cm.output)

    def test_log_module_singleton(self):
        looger_a_keys = list(log_module().__dict__.keys())
        looger_b_keys = list(log_module().__dict__.keys())
        looger_a_vals = list(log_module().__dict__.values())
        looger_b_vals = list(log_module().__dict__.values())
        self.assertEqual(looger_a_keys, looger_b_keys)
        self.assertEqual(looger_a_vals, looger_b_vals)

    def test_log_module_display(self):
        out = IO()
        with _redirect_stdout(out):
            log_module().info('info')
            log_module().warning('warning')
            log_module().critical('critical')
            log_module().error('error')
        output = out.getvalue().strip()
        self.assertEqual(output,'info\nwarning\ncritical\nerror')
        with _redirect_stderr(out):
            pass
        output = out.getvalue().strip()
        self.assertEqual(output,'info\nwarning\ncritical\nerror')


if __name__ == '__main__':
    unittest.main()


