import os
import mux_python
from mux_python.rest import ApiException

# Authentication Setup
configuration = mux_python.Configuration()
configuration.username = 'b5c3ae10-c67c-4927-8e0f-8876a225d652'
configuration.password = 'aNqBcCrgthtejHkdxx0vQ0KXcCpQ+UlKr7FhFgxlCj63U/s7SspfR63is7c6VPVLw6c0iSa0xnU'

# API Client Initialization
assets_api = mux_python.AssetsApi(mux_python.ApiClient(configuration))

# List Assets
print("Listing Assets: \n")
try:
    list_assets_response = assets_api.list_assets()
    for asset in list_assets_response.data:
        print('Asset ID: ' + asset.id)
        print('Status: ' + asset.status)
        print('Duration: ' + str(asset.duration) + "\n")
except ApiException as e:
    print("Exception when calling AssetsApi->list_assets: %s\n" % e)