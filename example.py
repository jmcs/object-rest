from __future__ import print_function

import object_rest

openweathermap = object_rest.Service("http://api.openweathermap.org/data/2.5")
print(openweathermap.weather(q='Berlin,DE'))
print(openweathermap['weather'](q='Berlin,DE'))

local = object_rest.Service("http://127.0.0.1:5000")
print(local.test(param1=1, param2='b'))
print(local.test.abc("POST", param1=1, param2='b'))
local.test.cde = {'v': 4}

local_with_config = object_rest.Service(documentation="config/service.txt")
print(local_with_config.test())
print(local_with_config.test.abc())
print(local_with_config.without())
print(local_with_config.answers._42())
print(local_with_config.test.wildcard.test())
local_with_config.questions.objective_of_universe = {'answer': 42}
object_rest.help(local_with_config.test)
object_rest.help(local_with_config.test.abc)