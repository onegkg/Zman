"""
CLI-Zmanim: Command-line interface for Jewish prayer times.

This package provides a command-line tool to display zmanim (Jewish prayer times)
and Jewish calendar events for any location and date. It integrates with the
Hebcal API for zmanim calculations and the Geonames API for location resolution.

Main components:
    - main: Entry point and command-line interface
    - helpers: Configuration management, API calls, and formatting utilities
    - date: Jewish calendar event handling and caching

Usage:
    $ zman                      # Show today's zmanim for default location
    $ zman -d 12/25/2025        # Show zmanim for specific date
    $ zman -l "Boston, MA"      # Show zmanim for specific location

Configuration:
    User configuration is stored at: $XDG_CONFIG_HOME/zman/config.yaml
    Cache directory is at: $XDG_CACHE_HOME/cli-zmanim/events/

For more information, visit: https://github.com/yourusername/CLI-Zmanim
"""

__version__ = "1.0.0"
__author__ = "CLI-Zmanim Contributors"
