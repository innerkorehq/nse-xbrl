# Installation

## Requirements

- **Python**: `>=3.12` (fully compatible and optimized for **Python 3.14**)
- Operating System: Linux, macOS, or Windows

## Installing with `uv` (Recommended)

[`uv`](https://github.com/astral-sh/uv) is the fastest Python package manager:

```bash
uv add nse-xbrl
```

## Installing with `pip`

```bash
pip install nse-xbrl
```

## Installing with `poetry`

```bash
poetry add nse-xbrl
```

## Development Installation

To install from source for local development:

```bash
git clone https://github.com/innerkorehq/nse-xbrl.git
cd nse-xbrl
uv sync --all-extras
```

Run test suite to verify:

```bash
uv run pytest
```
