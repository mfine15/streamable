import unittest
import tempfile
from io import StringIO
from contextlib import redirect_stdout
from streamable import Stream

class TestProgress(unittest.TestCase):
    def test_progress(self):
        stream = Stream([1, 2, 3, 4, 5])
        result = list(stream.progress(total=5, disable=True))
        self.assertEqual(result, [1, 2, 3, 4, 5])
        
    def test_progress_with_total(self):
        stream = Stream(range(10))
        result = list(stream.progress(total=10, disable=True))
        self.assertEqual(result, list(range(10)))

if __name__ == '__main__':
    unittest.main()
