import unittest
import tempfile
import os
import json
import csv
from streamable import Stream

class TestJsonCsv(unittest.TestCase):
    def test_from_json(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump([1, 2, 3, 4, 5], f)
            json_file = f.name
        
        try:
            stream = Stream.from_json(json_file)
            result = list(stream)
            self.assertEqual(result, [1, 2, 3, 4, 5])
        finally:
            os.unlink(json_file)
    
    def test_to_json(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json_file = f.name
        
        try:
            stream = Stream([1, 2, 3, 4, 5])
            result = list(stream.to_json(json_file))
            self.assertEqual(result, [1, 2, 3, 4, 5])
            
            with open(json_file, 'r') as f:
                data = json.load(f)
                self.assertEqual(data, [1, 2, 3, 4, 5])
        finally:
            os.unlink(json_file)
    
    def test_from_csv(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name'])
            writer.writeheader()
            writer.writerow({'id': '1', 'name': 'Alice'})
            writer.writerow({'id': '2', 'name': 'Bob'})
            csv_file = f.name
        
        try:
            stream = Stream.from_csv(csv_file)
            result = list(stream)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]['id'], '1')
            self.assertEqual(result[0]['name'], 'Alice')
            self.assertEqual(result[1]['id'], '2')
            self.assertEqual(result[1]['name'], 'Bob')
        finally:
            os.unlink(csv_file)
    
    def test_to_csv(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            csv_file = f.name
        
        try:
            data = [
                {'id': '1', 'name': 'Alice'},
                {'id': '2', 'name': 'Bob'}
            ]
            stream = Stream(data)
            result = list(stream.to_csv(csv_file))
            self.assertEqual(result, data)
            
            with open(csv_file, 'r', newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                self.assertEqual(len(rows), 2)
                self.assertEqual(rows[0]['id'], '1')
                self.assertEqual(rows[0]['name'], 'Alice')
                self.assertEqual(rows[1]['id'], '2')
                self.assertEqual(rows[1]['name'], 'Bob')
        finally:
            os.unlink(csv_file)

if __name__ == '__main__':
    unittest.main()
