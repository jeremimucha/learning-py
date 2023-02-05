from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Static files can be served automatically from a directory using StaticFiles.

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# "mounting" means adding a complete "independant" application in specific path,
# that then takes care of handling all the sub-paths.

# The first "/static" refers to the sub-path this "sub-application" will be "mounted" on.
# So, any path that starts with "/static" will be handled by it.
# The directory="static" refers to the name of the directory that contains your static files.
# The name="static" gives it a name that can be used internally by FastAPI.
# All these parameters can be different than "static",
# adjust them with the needs and specific details of your own application.