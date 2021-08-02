# Run a test server.
from app import app
import system_config


app.run(host=system_config.host, port=system_config.port, debug=False)