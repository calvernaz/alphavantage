# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-alpine

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev --python /usr/local/bin/python3

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app

# Remove any existing virtual environment that might have been copied from host
RUN rm -rf .venv

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --python /usr/local/bin/python3

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Set transport mode to HTTP and port to 8080 as required by Smithery proxy
ENV TRANSPORT=http
ENV PORT=8080
EXPOSE 8080

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Run the application directly using the venv Python
CMD ["alphavantage"]