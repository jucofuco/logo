# Renders pictogram SVGs to PNG so they can be looked at on a machine without a browser.
FROM debian:bookworm-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends librsvg2-bin \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /w
