#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Module template for Inky-Calendar Project

Create your own module with this template

Copyright by aceisace
"""

#############################################################################
#                           Required imports (do not remove)
#############################################################################
# Required for setting up this module
from inkycal.modules.template import inkycal_module
from inkycal.custom import *

#############################################################################
#                           Built-in library imports
#############################################################################

# Built-in libraries go here
import arrow

#############################################################################
#                         External library imports
#############################################################################

# For external libraries, which require installing,
# use try...except ImportError to check if it has been installed
# If it is not found, print a short message on how to install this dependency

try:
  from locationsharinglib import Service
except ImportError:
  print('locationsharinglib is not installed! Please install with:')
  print('pip3 install locationsharinglib')

try:
  import reverse_geocoder as rg
except ImportError:
  print('reverse_geocoder is not installed! Please install with:')
  print('pip3 install reverse_geocoder && sudo apt-get install libatlas-base-dev')

#############################################################################
#                         Filename + logging (do not remove)
#############################################################################

# Get the name of this file, set up logging for this filename
filename = os.path.basename(__file__).split('.py')[0]
logger = logging.getLogger(filename)
logger.setLevel(level=logging.INFO)

#############################################################################
#                         Class setup
#############################################################################

# info: you can change Simple to something else
# Please remember to keep the first letter a capital
# Avoid giving too long names to classes

class Locations(inkycal_module):
  """ Locations Class
  This module takes the location data of anyone who has shared their location
  with you via Google Location Sharing and displays it on your inkycal display.
  
  Instructions:

  1. Add the following under "panels" in your settings.json file:

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
  
  2. You will need to create a cookies file with the instructions in step 2 here:
     https://www.home-assistant.io/integrations/google_maps/
     Log in to the google location sharing after installing one of the two extensions
     and then download the cookies file.
  3. Set cookies_file as the path to your file.
  4. Edit email_address to reflect the email address you just logged in to.
  5. Choose which format how you would like the location to show and set "options".
     name:      usually the city name (ex. "Philadelphia" or "Stuttgart")
     admin1:    usually the state, province, or district (ex. "Pennsylvania" or "Baden-Wuerttemberg")
     admin2:    Not used in the US or Canada, used in the rest of the world. (ex. "Regierungsbezirk" or "Lincolnshire")
     cc:        Country abbreviation (ex. "US", "CA", or "DE") REMEMBER THIS IS LOWER CASE
     I recommend using two or three of the options.
     Using the above examples, setting ["name", "admin1", "cc"] will result in showing "Richmond, Virginia, US"
  6. If you would like to order the names, write the nicknames in order of preference in set names_preference. Leave as [] otherwise.
  7. If you would like to limit the names shown to only those listed in names_preference, set limit to "yes".
     "no" will allow the program to fill in the rest of the names below the preference list.
  """

  # Initialise the class (do not remove)
  def __init__(self, section_size, section_config):
    """Initialize inkycal_locations module"""

    # Initialise this module via the inkycal_module template (required)
    super().__init__(section_size, section_config)

    # module name (required)
    self.name = self.__class__.__name__

    # module specific parameters (optional)
    self.do_something = True
    self.time_format = "HH:mm"
    self.hours = 12
    self.language = 'en'
    self.timezone = get_system_tz()
    self.cookies_file = self.config['cookies_file']
    self.my_name = self.config['my_name']
    self.google_email = self.config['google_email']
    self.options = self.config['options']
    self.title = self.config['title']
    self.last_updated = self.config['last_updated']
    self.names_preference = self.config['names_preference']
    self.names_limit = self.config['names_limit']

    # give an OK message (optional)
    print('{0} loaded'.format(self.name))

#############################################################################
#                 Validation of module specific parameters                  #
#############################################################################

  def _validate(self):
    """Validate module-specific parameters"""
    # Check the type of module-specific parameters
    # This function is optional, but very useful for debugging.

    # Here, we are checking if do_something (from init) is True/False
    if not isinstance(self.do_something, bool):
      print('do_something has to be a boolean: True/False')

#############################################################################
#                       Generating the image                                #
#############################################################################

  def generate_image(self):
    """Generate image for this module"""

    # Define new image size with respect to padding (required)
    im_width = int(self.width - (self.width * 2 * self.margin_x))
    im_height = int(self.height - (self.height * 2 * self.margin_y))
    im_size = im_width, im_height

    # Use logger.info(), logger.debug(), logger.warning() to display
    # useful information for the developer
    logger.info('image size: {} x {} px'.format(im_width, im_height))

    # Create an image for black pixels and one for coloured pixels (required)
    im_black = Image.new('RGB', size = im_size, color = 'white')
    im_colour = Image.new('RGB', size = im_size, color = 'white')

    #################################################################    
               
    service = Service(cookies_file=self.cookies_file, authenticating_account=self.google_email)
    
    # Define new image size with respect to padding
    im_width = int(self.width - (self.width * 2 * self.margin_x))
    im_height = int(self.height - (self.height * 2 * self.margin_y))
    im_size = im_width, im_height
    logger.info('image size: {} x {} px'.format(im_width, im_height))

    # Create an image for black pixels and one for coloured pixels
    im_black = Image.new('RGB', size = im_size, color = 'white')
    im_colour = Image.new('RGB', size = im_size, color = 'white')
    
    # Check if internet is available
    if internet_available() == True:
      logger.info('Connection test passed')
    else:
      raise Exception('Network could not be reached :/')
      
    # Set some parameters for formatting locations feeds
    line_spacing = 1
    line_height = self.font.getsize('hg')[1] + line_spacing
    line_width = im_width
    max_lines = (im_height // (self.font.getsize('hg')[1] + line_spacing))

    # Calculate padding from top so the lines look centralised
    spacing_top = int( im_height % line_height / 2 )

    # Calculate line_positions
    line_positions = [
      (0, spacing_top + _ * line_height ) for _ in range(max_lines)]
    
    font = self.font
    
    locations_display = []
    names_display = []
    
    longest_name = 0
    print('')
    print('Found the locations of the following people:')
    
    """Get location info from everyone who has shared their location with you"""
    for p in service.get_all_people():
      """Get nickname of person found and create the name text"""
      # fun fact: in addition to returning all the people who have shared their location
      # with you, this also returns your own devices location! This is something I need
      # to verify by testing with other people's accounts. Anyway, p.full_name and p.nickname
      # are equal to your email address instead of your actual name when it returns your info.
      # To fix this I added this little thing so it would add your name instead.
      if p.full_name == self.google_email:
          name = self.my_name + ":"
      else:
          name = p.nickname + ":"
      names_display.append(name)
    
      """Finds the longest name of all that were given so we can indent later"""
      name_size = font.getsize(name)[0]
      if name_size > longest_name:
          longest_name = name_size
          
      """Get city/state name from coordinates"""
      search = rg.search((p.latitude, p.longitude))
      
      """Use the format set in the settings file and create the location text"""
      loc = ""
      for option in range(len(self.options)):
          if option == 0:
              loc = search[0][self.options[option]]
          else:
              loc = loc +", "+ search[0][self.options[option]]
      print(name, loc)
      locations_display.append(loc)
    
    """If the person has set an ordered preference in the settings file, reordered the display"""
    if self.names_preference != []:
      names_display_ordered = []
      locations_display_ordered = []

      """Goes through each preferred name and then each actual name and adds it to a new list if matched"""
      for o_name in self.names_preference:
          for n in range(len(names_display)):
              if o_name+":" == names_display[n]:
                  names_display_ordered.append(names_display[n])
                  locations_display_ordered.append(locations_display[n])

      """Then go through the old list and find any that weren't added and add them"""
      if self.names_limit == "no":
          for n in range(len(names_display)):
              if names_display[n] not in names_display_ordered:
                  names_display_ordered.append(names_display[n])
                  locations_display_ordered.append(locations_display[n]) 
        
      """Make the old list equal to the new ordered list"""
      names_display = names_display_ordered
      locations_display = locations_display_ordered
      
    """Add the title"""
    names_display.insert(0,self.title)
    locations_display.insert(0,'')
    
    """Add a 'last updated' timestamp, if requested"""
    # This section will only exist until the last_updated option is added universally
    if self.last_updated == "yes":
      if self.hours == 24:
          last_updated = "Last updated at "+arrow.utcnow().to(get_system_tz()).format("H:mm")
      else:
          last_updated = "Last updated at "+arrow.utcnow().to(get_system_tz()).format("h:mm a")
      """Truncate the lines, in case too many people share their location with you (in the case of timestamp"""
      if len(names_display) > max_lines-1:
          print('not enough space to show:', names_display[max_lines-1:len(names_display)])
          names_display = names_display[0:max_lines-1]
          locations_display = locations_display[0:max_lines-1]
          names_display.append(last_updated)
          locations_display.append('')
      else:
          names_display.append(last_updated)
          locations_display.append('')
    else:
      """Truncate the lines, in case too many people share their location with you"""
      if len(names_display) > max_lines:
          print('not enough space to show:', names_display[max_lines:len(names_display)])
          names_display = names_display[0:max_lines]
          locations_display = locations_display[0:max_lines]
    
    """Write the name text on the display"""
    for _ in range(len(names_display)):
      write(im_black, line_positions[_], (line_width, line_height),
        names_display[_], font = font, alignment= 'left')
        
    """Write the location text on the display (indented)"""
    indent_size = longest_name+6
    for _ in range(len(locations_display)):
      write(im_black, (line_positions[_][0] + indent_size, line_positions[_][1]), 
        (line_width-indent_size, line_height), locations_display[_], font = font, alignment = 'left')

    #################################################################

    # Save image of black and colour channel in image-folder
    im_black.save(images+self.name+'.png', 'PNG')
    im_colour.save(images+self.name+'_colour.png', 'PNG')

# Check if the module is being run by itself
if __name__ == '__main__':
  print('running {0} in standalone mode'.format(filename))
