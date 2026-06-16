FROM python:3.13-slim AS base
FROM base AS builder

# Allows docker to cache installed dependencies between builds
RUN apt-get update && apt-get -y install libpq-dev gcc poppler-utils \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /build
COPY ./requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --target=/build/packages -r requirements.txt

FROM base AS runtime
COPY --from=builder /build/packages /usr/local/lib/python3.13/site-packages
ENV PYTHONPATH=/usr/local/lib/python3.13/site-packages

# Security Context 
RUN useradd -m nonroot
USER nonroot

COPY . code
WORKDIR code

EXPOSE 8000
# Run the production server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - passport.wsgi:application
