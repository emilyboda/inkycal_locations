# Location Module
This is third-party module for the inkycal project

# Purpose
This module displays the locations of people who are sharing their locations with you via Google Location Sharing.

# Screenshot
<p align="center">
<img src="https://github.com/emilyboda/inkycal_locations/blob/master/locations%20module%20screenshot%20example.jpg" width="900"><img 
</p>

# Dependencies
* The locations must be sharing their location with you via the official Google Location Sharing site. This should be done via the Google Maps application. This can be done on any mobile platform. If the person has an iPhone, they will need to remember to open the Maps app every few days to ensure the iOS battery management settings doesn't put it to sleep. Google will frequently send emails to everyone reminding them that they are sharing their location, as a security measure. I chose Google Location Sharing because it is native to my mobile operating system and therefore the battery impact would be low when compared to other third-party apps like OwnTracks or Life360.
* The [locationsharinglib](https://locationsharinglib.readthedocs.io/) package pulls the locations. The only example of how it is currently used is in a project called Home Assistant, so the instructions are from that website.
* The [reverse_geocoder](https://pypi.org/project/reverse_geocoder/) package is used to convert the coordinates to readable locations.

# Installation instructions
1. Add inkycal_locations.py to /inkycal/modules/
2. Follow the installation instructions in inkcal_locations.py. Full instructions will be put wherever they need to be later.
3. Add the config to settings.json

# Sample Config
Add the following code under the "panel" in settings.json.

```
{
    "location": "bottom",
    "type": "Locations",
    "height": null,
    "config": {
				"cookies_file": "/home/pi/Inkycal/example.cookies",
				"my_name": "Me",
				"google_email": "insert@email.here",
				"options" : ["name", "admin1", "cc"],
				"title":"Where is my family today?",
				"last_updated": "yes",
				"names_preference": ["Bob", "Jane", "Me"],
				"names_limit": "no"
				}
  }
  ```

# Development Status
I'm actively developing this module.

# How to remove this module
Coming soon
