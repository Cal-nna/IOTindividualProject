from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-28efa47f-1d37-4aa8-8cb0-bae3648e5eb2"
pnconfig.subscribe_key = "sub-c-764683fa-a709-42d5-a0bb-a9eca9c99146"
pnconfig.uuid = "calweb-server"

pubnub = PubNub(pnconfig)

CHANNEL = "calweb-visual-state"
