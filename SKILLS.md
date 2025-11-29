# Zman Project Summary

Zman is a simple command-line tool that calculates Jewish prayer times (zmanim) and religious events for any location and date. The application integrates with external APIs (Hebcal and Geonames) to provide accurate time-based calculations while maintaining a user-friendly interface with extensive customization options through YAML configuration files.

## Technical Skills & Experience

## Programming Languages & Technologies
- **Python 3.12+**: Advanced proficiency with modern Python features and type hints
- **CLI Development**: Built command-line interfaces using argparse and typer
- **API Integration**: RESTful API consumption with requests library
- **Data Processing**: JSON/YAML parsing, datetime manipulation, and data transformation

## Software Architecture & Design
- **Modular Design**: Clean separation of concerns with dedicated modules (main, helpers, date)
- **Configuration Management**: YAML-based configuration with default/user config merging
- **Error Handling**: Robust exception handling and user-friendly error messages
- **Caching Strategy**: Local file caching for API responses to improve performance

## External Services & APIs
- **Third-party API Integration**: Hebcal API for religious time calculations
- **Geolocation Services**: Geonames.org API for location resolution
- **Authentication**: API key management and secure credential handling

## Development Tools & Practices
- **Package Management**: setuptools, pyproject.toml, and modern Python packaging
- **Dependency Management**: UV for fast dependency resolution
- **Code Quality**: Type hints, structured error handling, and clean code principles
- **Cross-platform Compatibility**: XDG Base Directory specification for config/cache locations

## User Experience & Interface
- **Rich Terminal Output**: Enhanced CLI experience with rich library for better formatting
- **Flexible Configuration**: User-customizable settings with sensible defaults
- **Intuitive Command Structure**: Well-designed argument parsing and help systems

## Data Management
- **File I/O Operations**: JSON/YAML file handling with proper encoding
- **Caching Implementation**: Local caching system for API responses
- **Data Validation**: Input validation and error handling for user data

## Problem Solving
- **Algorithm Design**: Custom time calculation logic (e.g., candle lighting times)
- **System Integration**: Combining multiple APIs and data sources
- **Performance Optimization**: Caching strategies to reduce API calls
- **User Experience**: Balancing flexibility with ease of use
