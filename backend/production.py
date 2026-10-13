```python
import os
import sys

from waitress import serve

BACKEND_FOLDER = os.path.dirname(os.path.abspath(__file__))

if BACKEND_FOLDER not in sys.path:
    sys.path.insert(0, BACKEND_FOLDER)

from app import app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))

    serve(
        app,
        host="0.0.0.0",
        port=port
    )
```
