# Zman
A simple CLI Zmanim tool powered by Hebcal.

## Features
- Zmanim and events (holidays, fasts, etc.) for any day at any location.
    - All zmanim provided in the hebcal API plus candle lighting are available 
    - Candle lighting calculated based on a custom variable allowing for 18 min, 40 min or any other period.
        - Automatic switching between 18 and 40 min candle lighting based on location (in development)

## Installation
1. Clone this repo to an appropriate location and cd into the resulting directory
''' {bash}
git clone https://github.com/onegkg/Zman.git
cd Zman
'''
2. Install using pip
''' {bash}
pip install .
'''
3. Before using zman, you'll need to create a geonames.org api key. this is a free service that is used to convert plain text place names to a unique identifier that can be used in the hebcal API
    1. Create a free [geonames.org](https://www.geonames.org/login) account.
    2. Once you've created your account, navigate to your account page and turn on "Free Web Services" for your account.
    3. Create a `config.yaml` file at `$XDG_CONFIG_HOME/zman/` (on MacOS, `$XDG_CONFIG_HOME` is usually `~/.config`) and add your geonames user name under `APIs -> geonames_key`. A sample minimal config.yaml file is provided under 

## Usage
- `zman` gives you the zmanim for the current day at the location from your config. [include picture]
- `zman -d` or `zman --date`allows you to get the zmanim on a particular date. [formatting, include picture]
- `zman -l` or `zman --location` allows you to get the zmanim in a particular location.
- `zman -h` prints the help message.

## Configuration
Configuration is done in a `config.yaml` file. This file should be placed at [path]. This file is merged with the `default_config.yaml` file (shown below) which provides the default settings. You'll want to make sure to override the location and geonames_key fields before use

``` {yaml}
Zmanim:
  chatzotNight: False
  alotHaShachar: False
  misheyakir: False
  misheyakirMachmir: False
  dawn: False
  sunrise: True
  sofZmanShmaMGA19Point8: False
  sofZmanShmaMGA16Point1: False
  sofZmanShmaMGA: False
  sofZmanShma: True
  sofZmanTfillaMGA19Point8: False
  sofZmanTfillaMGA16Point1: False
  sofZmanTfillaMGA: False
  sofZmanTfilla: True
  chatzot: True
  minchaGedola: True
  minchaGedolaMGA: False
  minchaKetana: True
  minchaKetanaMGA: False
  plagHaMincha: True
  candleLighting: True
  sunset: True
  beinHaShmashos: False
  dusk: True
  tzeit7083deg: False
  tzeit85deg: False
  tzeit42min: False
  tzeit50min: False
  tzeit72min: False

APIs:
  geonames_key: "" # This field must be replaced with your geonames key before first usage

Settings:
  location: "New York, NY" # Plain text location to be fed to the geonames api. The API will attempt to guess the location with the provided information. It is recommended that you include a state or country code to help prevent mismatches.
  shabbat_start: 18 # The number of minutes before sunset shabbat starts. Should generally be set to 18 in chutz la'aretz and 40 in yerushalayim.
```

## License

