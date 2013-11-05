from __future__ import print_function

from object_rest import Service

openweathermap = Service("http://api.openweathermap.org/data/2.5")
print(openweathermap.weather(q='Berlin,DE'))

