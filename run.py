import os
from phonescrubber import create_app

app = create_app(os.environ.get("PHONESCRUBBER_ENV", "default"))
