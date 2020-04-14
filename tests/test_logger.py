from cube_helper.logger import log_module, log_inconsistent,\
    _to_comma_and_str, muffle_logger, reset_logger
from common import _redirect_stdout, _redirect_stderr
import unittest
import sys
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

    def test_log_module(self):
        logger = log_module()
        handler = logger.handlers[0]
        self.assertEqual(len(logger.handlers), 1)
        self.assertEqual(logger.name, 'cube_helper.logger')
        self.assertEqual(handler.stream, sys.stdout)

    def test_muffle_logger(self):
        muffle_logger()
        logger = log_module()
        handler = logger.handlers[0]
        self.assertEqual(len(logger.handlers), 1)
        self.assertEqual(logger.name, 'cube_helper.logger')
        self.assertEqual(logger.level, 40)
        self.assertEqual(handler.level, 40)
        self.assertEqual(handler.stream, sys.stdout)

    def test_reset_logger(self):
        reset_logger()
        logger = log_module()
        handler = logger.handlers[0]
        self.assertEqual(len(logger.handlers), 1)
        self.assertEqual(logger.name, 'cube_helper.logger')
        self.assertEqual(logger.level, 20)
        self.assertEqual(handler.level, 20)
        self.assertEqual(handler.stream, sys.stdout)

    def test_log_module_redirect(self):
        logger = log_module()
        out = IO()
        with _redirect_stdout(out):
            logger.info('Message on stdout')
        output = out.getvalue().strip()
        self.assertEqual(output, 'Message on stdout')
        out = IO()
        with _redirect_stdout(out):
            logger.info('Message on stderr')
        output = out.getvalue().strip()
        self.assertEqual(output, 'Message on stderr')

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
