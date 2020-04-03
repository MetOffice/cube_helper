from cube_helper.logger import log_module, log_inconsistent, _to_comma_and_str
from common import _redirect_stdout, _redirect_stderr
import unittest
import platform
if float(platform.python_version()[0:3]) <= 2.8:
    from io import BytesIO as IO
else:
    from io import StringIO as IO


class TestLogger(unittest.TestCase):

    def test_log_module_singleton(self):
        logger = log_module()
        looger_a_keys = list(logger.__dict__.keys())
        looger_b_keys = list(logger.__dict__.keys())
        looger_a_vals = list(logger.__dict__.values())
        looger_b_vals = list(logger.__dict__.values())
        self.assertEqual(looger_a_keys, looger_b_keys)
        self.assertEqual(looger_a_vals, looger_b_vals)

    def test_log_module_redirect(self):
        logger = log_module()
        out = IO()
        with _redirect_stdout(out):
            logger.info('Message on stdout and stderr')
        output = out.getvalue().strip()
        self.assertEqual(output, 'Message on stdout and stderr')
        out = IO()
        with _redirect_stderr(out):
            logger.info('Message on stdout and stderr')
        output = out.getvalue().strip()
        self.assertEqual(output, 'Message on stdout and stderr')

    def test_to_comma_and_str(self):
        component_list = ['creation_date',
                          'tracking_id',
                          'history']
        metadata_component = 'attributes'
        output = _to_comma_and_str(component_list,
                                   metadata_component)
        expected_output = 'creation_date, tracking_id ' \
                          'and history attributes'
        self.assertEqual(output, expected_output)


if __name__ == '__main__':
    unittest.main()
