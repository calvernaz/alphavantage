# Run the server

Set the environment variable `ALPHAVANTAGE_API_KEY` to your Alphavantage API key.

```bash
uv --directory /Users/medusa/code/alphavantage run alphavantage
```


# Format

```bash
ruff check src/alphavantage_mcp_server/  --fix
```

# Run Tests

```bash
pytest tests/*.py
```

# Versioning

```bash
bumpversion patch
```