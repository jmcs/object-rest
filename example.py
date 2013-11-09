from __future__ import print_function

from object_rest import Service

openweathermap = Service("http://api.openweathermap.org/data/2.5")
print(openweathermap.weather(q='Berlin,DE'))
print(openweathermap['weather'](q='Berlin,DE'))

local = Service("http://127.0.0.1:5000")
print(local.test(param1=1, param2='b'))
print(local.test.abc("POST", param1=1, param2='b'))
local.test.cde = {'v': 4}

local_with_config = Service(documentation="config/service.txt")
print(local_with_config.test())
print(local_with_config.test.abc())
print(local_with_config.without())