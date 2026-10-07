# What pyproject.toml controls

**Date:** 2026-07-12
**Topic:** pyproject.toml in the yfinance-helpers repo
**Turn:** 003b

## User request

Explain the purpose of the pyproject.toml file and what it controls.

## Work and response

Three things, from most important to least:

### 1. Makes the repo installable

```toml
[build-system]
requires = ["setuptools>=64"]
build-backend = "setuptools.build_meta"

[project]
name = "yfinance-helpers"
version = "0.1.0"
dependencies = ["numpy", "pandas", "yfinance"]

[tool.setuptools]
py-modules = ["yf"]
```

This is what `pip install -e .` reads. It tells pip: "this is a Python project, here's the name, here's what it depends on, and here's where the code lives." Without it, `from yf import ...` only works if you're in the same directory — the editable install is what puts it on the Python path globally.

### 2. Declares dependencies

```toml
dependencies = ["numpy", "pandas", "yfinance"]
```

When someone installs this package, pip automatically installs these too. Right now we're in the sandbox where everything is already installed, so it's moot — but if you cloned this repo into a fresh environment, `pip install -e .` would pull numpy, pandas, and yfinance automatically.

### 3. Configures pytest

```toml
[tool.pytest.ini_options]
markers = [
    "integration: tests that require network access (yfinance)",
]
```

This registers the `@pytest.mark.integration` marker so pytest doesn't warn about it. Without this, `pytest -m "not integration"` still works, but you get those "Unknown pytest.mark.integration" warnings we saw earlier.

### What it does NOT do

It doesn't control runtime behaviour, imports, or execution. It's purely a build/packaging manifest. Once the package is installed, the `pyproject.toml` is never read again — the installed package lives in site-packages as a link to `yf.py`.