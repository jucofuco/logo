# Renders pictogram SVGs to PNG / WebP so they can be looked at and bundled on a machine without a browser.
FROM debian:bookworm-slim
RUN apt-get update \
 && apt-get install -y --no-install-recommends librsvg2-bin webp pngquant \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /w
