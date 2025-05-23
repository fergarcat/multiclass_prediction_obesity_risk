import os
import sys

sys.path.append(os.path.dirname(__file__))

from client.app import app

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8050)