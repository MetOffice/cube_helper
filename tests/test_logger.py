from cube_helper.logger import log_module, log_inconsistent
from common import _redirect_stdout, _redirect_stderr
import unittest
import platform
if float(platform.python_version()[0:3]) <= 2.7:
    from io import BytesIO as IO
else:
    from io import StringIO as IO


class TestLogger(unittest.TestCase):

    def test_log_module_logging(self):
        logger = log_module()
        with self.assertLogs('cube_helper.logger', level='INFO') \
                as cm:
            logger.info('info message')
            logger.warning('warning message')
            logger.critical('critical message')
            logger.error('error message')
            self.assertIn('INFO:cube_helper.logger:info message',
                          cm.output)
            self.assertIn('WARNING:cube_helper.logger:warning message',
                          cm.output)
            self.assertIn('CRITICAL:cube_helper.logger:critical message',
                          cm.output)
            self.assertIn('ERROR:cube_helper.logger:error message',
                          cm.output)

    def test_log_module_singleton(self):
        logger = log_module()
        looger_a_keys = list(logger.__dict__.keys())
        looger_b_keys = list(logger.__dict__.keys())
        looger_a_vals = list(logger.__dict__.values())
        looger_b_vals = list(logger.__dict__.values())
        self.assertEqual(looger_a_keys, looger_b_keys)
        self.assertEqual(looger_a_vals, looger_b_vals)

    def test_log_module_stout(self):
        out = IO()
        with _redirect_stdout(out):
            print('Message on stdout and stderr')
        output = out.getvalue().strip()
        self.assertEqual(output, 'Message on stdout and stderr')
        with _redirect_stderr(out):
            print('Message on stdout and stderr')
        output = out.getvalue().strip()
        self.assertEqual(output, 'Message on stdout and stderr')


if __name__ == '__main__':
    unittest.main()
