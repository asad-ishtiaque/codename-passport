FROM python:3.13-slim AS base
FROM base AS builder

WORKDIR /build
COPY ./requirements.txt requirements.txt
# rapidocr pulls in opencv-python (needs X11); swap for headless in containers
RUN pip3 install --no-cache-dir --target=/build/packages -r requirements.txt

FROM base AS runtime

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

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
