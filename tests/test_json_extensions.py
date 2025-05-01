import unittest
import tempfile
import os
import json
import shutil
from typing import List, Dict, Any, Optional
from streamable import Stream


class TestJsonExtensions(unittest.TestCase):
    def test_read_jsonl(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
            f.write('{"id": 1, "name": "Alice"}\n')
            f.write('{"id": 2, "name": "Bob"}\n')
            f.write('{"id": 3, "name": "Charlie"}\n')
            jsonl_file = f.name
        
        try:
            stream = Stream.from_json(jsonl_file, jsonl=True)
            result = list(stream)
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]["id"], 1)
            self.assertEqual(result[0]["name"], "Alice")
            self.assertEqual(result[1]["id"], 2)
            self.assertEqual(result[1]["name"], "Bob")
            self.assertEqual(result[2]["id"], 3)
            self.assertEqual(result[2]["name"], "Charlie")
        finally:
            os.unlink(jsonl_file)
    
    def test_write_jsonl(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
            jsonl_file = f.name
        
        try:
            data = [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
                {"id": 3, "name": "Charlie"}
            ]
            stream = Stream(data)
            result = list(stream.to_json(jsonl_file, jsonl=True))
            self.assertEqual(result, data)
            
            with open(jsonl_file, 'r') as f:
                lines = f.readlines()
                self.assertEqual(len(lines), 3)
                self.assertEqual(json.loads(lines[0]), {"id": 1, "name": "Alice"})
                self.assertEqual(json.loads(lines[1]), {"id": 2, "name": "Bob"})
                self.assertEqual(json.loads(lines[2]), {"id": 3, "name": "Charlie"})
        finally:
            os.unlink(jsonl_file)
    
    def test_read_directory(self):
        temp_dir = tempfile.mkdtemp()
        try:
            with open(os.path.join(temp_dir, "file1.json"), 'w') as f:
                json.dump([{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}], f)
            
            with open(os.path.join(temp_dir, "file2.json"), 'w') as f:
                json.dump([{"id": 3, "name": "Charlie"}, {"id": 4, "name": "Dave"}], f)
            
            stream = Stream.from_json_dir(temp_dir)
            result = list(stream)
            self.assertEqual(len(result), 4)
            
            ids = [item["id"] for item in result]
            self.assertIn(1, ids)
            self.assertIn(2, ids)
            self.assertIn(3, ids)
            self.assertIn(4, ids)
        finally:
            shutil.rmtree(temp_dir)
    
    def test_write_directory_with_chunks(self):
        temp_dir = tempfile.mkdtemp()
        try:
            data = [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
                {"id": 3, "name": "Charlie"},
                {"id": 4, "name": "Dave"}
            ]
            
            stream = Stream(data)
            result = list(stream.to_json(temp_dir, chunk_size=2))
            self.assertEqual(result, data)
            
            files = os.listdir(temp_dir)
            self.assertEqual(len(files), 2)
            
            with open(os.path.join(temp_dir, "data_0.json"), 'r') as f:
                chunk1 = json.load(f)
                self.assertEqual(len(chunk1), 2)
                self.assertEqual(chunk1[0]["id"], 1)
                self.assertEqual(chunk1[1]["id"], 2)
            
            with open(os.path.join(temp_dir, "data_1.json"), 'r') as f:
                chunk2 = json.load(f)
                self.assertEqual(len(chunk2), 2)
                self.assertEqual(chunk2[0]["id"], 3)
                self.assertEqual(chunk2[1]["id"], 4)
        finally:
            shutil.rmtree(temp_dir)
    
    def test_write_with_max_file_size(self):
        temp_dir = tempfile.mkdtemp()
        try:
            data = []
            for i in range(100):
                name = "X" * (i % 10 + 1)  # Names of length 1-10
                data.append({"id": i, "name": name})
            
            stream = Stream(data)
            result = list(stream.to_json(temp_dir, jsonl=True, max_file_size=1000))
            self.assertEqual(result, data)
            
            files = os.listdir(temp_dir)
            self.assertGreater(len(files), 1)
            
            all_items = []
            for file in files:
                with open(os.path.join(temp_dir, file), 'r') as f:
                    for line in f:
                        all_items.append(json.loads(line))
            
            self.assertEqual(len(all_items), 100)
            ids = [item["id"] for item in all_items]
            self.assertEqual(sorted(ids), list(range(100)))
            
            for file in files:
                file_size = os.path.getsize(os.path.join(temp_dir, file))
                self.assertLessEqual(file_size, 1000)
        finally:
            shutil.rmtree(temp_dir)
    
    def test_schema_validation(self):
        try:
            from pydantic import BaseModel
            has_pydantic = True
        except ImportError:
            has_pydantic = False
            self.skipTest("Pydantic is not installed, skipping schema validation test")
            return
        
        class Person(BaseModel):
            id: int
            name: str
            age: int
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump([
                {"id": 1, "name": "Alice", "age": 30},
                {"id": 2, "name": "Bob", "age": 25},
                {"id": 3, "name": "Charlie", "age": 35}
            ], f)
            json_file = f.name
        
        try:
            stream = Stream.from_json(json_file, schema=Person)
            result = list(stream)
            self.assertEqual(len(result), 3)
            self.assertIsInstance(result[0], Person)
            self.assertEqual(result[0].id, 1)
            self.assertEqual(result[0].name, "Alice")
            self.assertEqual(result[0].age, 30)
            
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                json.dump([
                    {"id": 1, "name": "Alice", "age": 30},
                    {"id": 2, "name": "Bob"},  # Missing age field
                    {"id": 3, "name": "Charlie", "age": 35}
                ], f)
                invalid_json_file = f.name
            
            with self.assertRaises(Exception):
                stream = Stream.from_json(invalid_json_file, schema=Person)
                list(stream)  # Force evaluation
        finally:
            os.unlink(json_file)
            if 'invalid_json_file' in locals():
                os.unlink(invalid_json_file)
