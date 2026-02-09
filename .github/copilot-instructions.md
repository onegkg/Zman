# Copilot Instructions for CLI-Zmanim

## Project Overview

CLI-Zmanim is a Python CLI tool that displays Jewish prayer times (zmanim) and religious events for any location and date. It integrates with two external APIs:
- **Hebcal API**: Provides zmanim calculations and Jewish calendar events
- **Geonames API**: Converts location names to geoname IDs for the Hebcal API

## Installation & Setup

```bash
# Install the package in development mode
pip install -e .

# Or use uv (faster)
uv pip install -e .

# First-time setup requires:
# 1. Get a free Geonames API key from https://www.geonames.org/login
# 2. Create config at $XDG_CONFIG_HOME/zman/config.yaml
# 3. Add geonames_key under APIs section
```

## Running the Application

```bash
# Show zmanim for today at default location
zman

# Specify date (MM/DD/YYYY format)
zman -d 12/25/2025

# Specify location
zman -l "Boston, MA"
```

## Architecture

### Module Structure

- **main.py**: Entry point, argument parsing, config loading, orchestration
- **helpers.py**: Core utilities (config parsing, API calls, text formatting, candle lighting calculation)
- **date.py**: Event handling and local caching of yearly events data
- **default_config.yaml**: Default settings for all zmanim toggles and application behavior

### Configuration System

The application uses a two-layer config merge system:
1. **default_config.yaml** (bundled): Contains all default settings
2. **user config.yaml** (`$XDG_CONFIG_HOME/zman/config.yaml`): User overrides

The `merge()` function in helpers.py recursively merges user config over defaults, allowing partial overrides.

### Caching Strategy

- **Events cache**: Yearly Jewish calendar events are cached locally at `$XDG_CACHE_HOME/cli-zmanim/events/{geoname_id}_{year}.json`
- Cache is created on first request per year/location combination
- Zmanim API calls are NOT cached (they're fast enough and date-specific)

### API Integration

**Hebcal Zmanim API**:
- Called via `hebcal_call()` in helpers.py
- Returns times in ISO 8601 format with timezone offset
- Endpoint: `https://www.hebcal.com/zmanim?cfg=json&geonameid={id}&date={YYYY-MM-DD}`

**Hebcal Events API**:
- Called via `write_events_json()` in date.py for yearly data
- Includes holidays, fasts, candle lighting, and special days
- Endpoint: `https://www.hebcal.com/hebcal?v=1&cfg=json&...&geonameid={id}`

**Geonames API**:
- Handled by `geocoder.geonames()` library wrapper
- Converts "Boston, MA" → geoname ID (4930956)
- Can be bypassed by setting `geonames_loc` directly in config

### Special Logic

**Friday Candle Lighting**: The `friday()` function in helpers.py adds a "candleLighting" entry on Fridays by:
1. Taking sunset time from API response
2. Subtracting `shabbat_start` minutes (default: 18)
3. Inserting the calculated time before the sunset entry

**Dynamic Time Formatting**: `format_text()` maps camelCase API keys to readable Hebrew terms using a hardcoded dictionary, with fallback title-case conversion.

## Key Conventions

### Configuration Keys
- All zmanim toggles in config use exact camelCase names from Hebcal API
- Setting a zman to `false` in config hides it from output (doesn't disable API return)
- `shabbat_start` is in minutes before sunset (18 for diaspora, 40 for Jerusalem)

### XDG Base Directory Specification
- Config: `$XDG_CONFIG_HOME/zman/` (falls back to `~/.config/zman/`)
- Cache: `$XDG_CACHE_HOME/cli-zmanim/` (falls back to `~/.cache/cli-zmanim/`)

### Date Handling
- User input: `MM/DD/YYYY` format via argparse
- Internal: Python `datetime` objects
- API communication: `YYYY-MM-DD` strings
- Display: `%I:%M:%S %p` format (12-hour with AM/PM)

### Error Handling
- Missing config file: Exit with helpful path message
- Missing geonames_key: Exit with instruction to get key or use geonames_loc
- API failures: Print exception and exit
- Invalid date format: Print format reminder and exit

## Dependencies

Core runtime dependencies:
- `requests`: HTTP API calls
- `geocoder`: Geonames API wrapper
- `pyyaml`: Config file parsing
- `rich`: Enhanced terminal output and tracebacks
- `datetime`: Date manipulation

## Type Hints

The codebase uses type hints with Python 3.12+ syntax:
- `TextIO` for file objects
- `dict[str, object]` for JSON responses
- `|` union syntax (e.g., `TextIO | None`)
- Return tuples explicitly typed (e.g., `tuple[dict, str, str, int, str]`)
