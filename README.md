# Streamable

Streamable is a Python library that provides a fluent interface for stream-like manipulation of iterables.

## Installation

You can install the package using `uv`:

```bash
uv install streamable
```

Or using pip:

```bash
pip install streamable
```

## Usage

### Basic Usage

```python
from streamable import Stream

# Create a stream from an iterable
stream = Stream([1, 2, 3, 4, 5])

# Apply operations
result = stream.filter(lambda x: x % 2 == 0).map(lambda x: x * 2).collect()
print(result)  # [4, 8]
```

### Progress Bar

You can add a progress bar to any stream operation using the `progress` method:

```python
from streamable import Stream

# Create a stream with a progress bar
stream = Stream(range(1000))
result = stream.progress(total=1000).filter(lambda x: x % 2 == 0).collect()
```

The `progress` method accepts all the parameters that `tqdm` accepts, including:

- `total`: The expected total number of elements (optional)
- `desc`: Description text to display alongside the progress bar
- `disable`: Whether to disable the progress bar
- And many more (see [tqdm documentation](https://github.com/tqdm/tqdm))

### JSON Operations

You can create a stream from a JSON file or write a stream to a JSON file:

```python
from streamable import Stream

# Create a stream from a JSON file
stream = Stream.from_json('data.json')

# Process the data
processed = stream.map(lambda x: x * 2)

# Write the processed data to a JSON file
processed.to_json('processed.json')
```

### CSV Operations

You can create a stream from a CSV file or write a stream to a CSV file:

```python
from streamable import Stream

# Create a stream from a CSV file
stream = Stream.from_csv('data.csv')

# Process the data
processed = stream.map(lambda x: {**x, 'value': int(x['value']) * 2})

# Write the processed data to a CSV file
processed.to_csv('processed.csv')
```

## License

Apache 2.0
