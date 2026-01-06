import unittest
from src.simulation.logger import Logger

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()

    def test_initialization(self):
        self.assertEqual(self.logger.get(), [])

    def test_log(self):
        self.logger.log(1, 100, 0.5, 0.3, 25)
        self.assertEqual(self.logger.get(), [(1, 100, 0.5, 0.3, 25)])

    def test_multiple_logs(self):
        self.logger.log(1, 100, 0.5, 0.3, 25)
        self.logger.log(2, 150, 0.6, 0.4, 30)
        self.assertEqual(self.logger.get(), [
            (1, 100, 0.5, 0.3, 25),
            (2, 150, 0.6, 0.4, 30)
        ])

    def test_get_empty(self):
        self.assertEqual(self.logger.get(), [])

if __name__ == '__main__':
    unittest.main()