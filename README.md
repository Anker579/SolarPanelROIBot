## General Notes
### Using the Solar API
For Google's Solar API much of the UK is at "medium" resolution, most of scotland & ireland is missed out entirely.
There are common issues with retrieving Building Insights data from anywhere that isn't "High" resolution it appears from StackOverflow.
Although Google's Solar API seems to be the most advanced of other APIs, this seems to mean it is quite restrictive, especially if it doesn't work for a certain location. The API wants to use 3D modelling of building roofs, however if my app will just make someone input their location by postcode, that isn't specific enough. Maybe my app could have an option to be more specific by using the google Solar API, otherwise it should use something else.
Solved this issue by using a specific url and making the request only need MEDIUM resolution
### Geocoding an address
I need the person to be able to input their address and for this to be converted into latitude and longitude, this is called geocoding.

I wanted to use an alternative API in the interest of limiting the requests I make to the Google API, however the first one I tried gave relatively inaccurate results for the latitude and longitude after inputting my address.
Using the Google Geocoding API this was much better and much more accurate, however an advantage of the first is I was able to pass a normal readable address to the request and it would format it itself. The google API cannot do this, I will need to adjust how the address is input slightly - probably separate text boxes for house number, road, post code etc.