from lennox_api import Lennox_iComfort_API

"""Setup the api"""
api = Lennox_iComfort_API("myUsernameGoesHERE", "MyPasswordGoesHere", 0, 0)
api.get()
