# Cache Insight

A Redis-based testing tool that monitors and validates cache performance and data integrity during automated test runs. Provides detailed insights into how applications interact with Redis caching layers.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from cache_insight import CacheInspector

# Initialize inspector
inspector = CacheInspector(redis_host='localhost', redis_port=6379)

# Start monitoring
with inspector.monitor():
    # Run your tests here
    pass

# Get results
print(inspector.get_metrics())
```

## Features

- Real-time Redis operation tracking during test execution
- Cache hit/miss ratio analysis and performance metrics
- Data integrity validation between application state and cached values

## Development

Run tests:

```bash
pytest tests/
```