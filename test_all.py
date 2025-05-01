"""
Test script to verify all features of the streamable package.
Run with: uv run test_all.py
"""
import tempfile
import os
import json
import csv
from streamable import Stream

def test_progress_bar():
    print("\nTesting progress bar...")
    stream = Stream(range(100))
    result = list(stream.progress(total=100, desc="Progress Bar Test"))
    assert len(result) == 100
    print("Progress bar test passed!")

def test_json_operations():
    print("\nTesting JSON operations...")
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump([1, 2, 3, 4, 5], f)
        json_file = f.name
    
    try:
        stream = Stream.from_json(json_file)
        result = list(stream)
        assert result == [1, 2, 3, 4, 5]
        
        output_file = json_file + '.out'
        stream = Stream([6, 7, 8, 9, 10])
        list(stream.to_json(output_file))
        
        with open(output_file, 'r') as f:
            data = json.load(f)
            assert data == [6, 7, 8, 9, 10]
        
        os.unlink(output_file)
        print("JSON operations test passed!")
    finally:
        os.unlink(json_file)

def test_csv_operations():
    print("\nTesting CSV operations...")
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name'])
        writer.writeheader()
        writer.writerow({'id': '1', 'name': 'Alice'})
        writer.writerow({'id': '2', 'name': 'Bob'})
        csv_file = f.name
    
    try:
        stream = Stream.from_csv(csv_file)
        result = list(stream)
        assert len(result) == 2
        assert result[0]['id'] == '1'
        assert result[0]['name'] == 'Alice'
        
        output_file = csv_file + '.out'
        data = [
            {'id': '3', 'name': 'Charlie'},
            {'id': '4', 'name': 'Dave'}
        ]
        stream = Stream(data)
        list(stream.to_csv(output_file))
        
        with open(output_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 2
            assert rows[0]['id'] == '3'
            assert rows[0]['name'] == 'Charlie'
        
        os.unlink(output_file)
        print("CSV operations test passed!")
    finally:
        os.unlink(csv_file)

def test_combined_features():
    print("\nTesting combined features...")
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'value'])
        writer.writeheader()
        for i in range(100):
            writer.writerow({'id': str(i), 'value': str(i)})
        csv_file = f.name
    
    try:
        stream = Stream.from_csv(csv_file)
        
        output_file = csv_file + '.out'
        result = stream.progress(total=100, desc="Processing CSV").map(
            lambda x: {'id': x['id'], 'value': str(int(x['value']) * 2)}
        ).to_csv(output_file)
        
        list(result)  # Execute the stream
        
        with open(output_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 100
            assert rows[10]['value'] == str(10 * 2)
        
        os.unlink(output_file)
        print("Combined features test passed!")
    finally:
        os.unlink(csv_file)

if __name__ == "__main__":
    print("Running tests for streamable package...")
    test_progress_bar()
    test_json_operations()
    test_csv_operations()
    test_combined_features()
    print("\nAll tests passed! The streamable package is working correctly.")
