FROM python:3.12-alpine
RUN pip install --no-cache-dir flask==3.1.3 werkzeug==3.1.9 jinja2==3.1.6 markupsafe==3.0.4 \
    && adduser -D -H app
USER app
WORKDIR /app
CMD ["python", "app.py"]
