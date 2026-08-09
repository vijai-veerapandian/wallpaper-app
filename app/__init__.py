import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__)

    # Signs CSRF tokens. Must be identical across gunicorn workers and across
    # restarts, so it comes from the environment — never generated per process.
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-insecure-key")

    if test_config:
        app.config.update(test_config)

    csrf.init_app(app)

    from .routes import main

    app.register_blueprint(main)

    @app.after_request
    def set_security_headers(response):
        # default-src 'self' also covers script-src and style-src. This only
        # works because no template contains an inline <script> or style=.
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; object-src 'none'; "
            "frame-ancestors 'none'; base-uri 'self'",
        )
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "no-referrer")
        response.headers.setdefault(
            "Permissions-Policy", "geolocation=(), microphone=(), camera=()"
        )
        return response

    return app
