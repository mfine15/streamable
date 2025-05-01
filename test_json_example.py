import json
import os
import tempfile
from streamable import Stream

# Create a temporary JSON file with test data
data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 35}
]

# Test the read_json functionality
def test_read_json():
    # Create a temporary JSON file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        json.dump(data, f)
        json_file = f.name
    
    try:
        # Create a stream from the JSON file
        stream = Stream.from_json(json_file)
        
        # Process the stream - let's filter people over 30 and map to just their names
        result = list(stream
                     .filter(lambda x: x["age"] > 30)
                     .map(lambda x: x["name"]))
        
        # Verify the results
        assert result == ["Charlie"], f"Expected ['Charlie'], but got {result}"
        print("✓ Successfully filtered and processed JSON data")
        
    finally:
        # Clean up the temporary file
        os.unlink(json_file)

if __name__ == "__main__":
    test_read_json() 