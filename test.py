#!/usr/bin/env python
import ldclient
from ldclient.config import Config

# Set sdk_key to your LaunchDarkly SDK key before running
sdk_key = ""

# Set feature_flag_key to the feature flag key you want to evaluate
feature_flag_key = "my-boolean-flag"

def show_message(s):
  print("*** %s" % s)
  print()

if __name__ == "__main__":
  if not sdk_key:
    show_message("Please edit test.py to set sdk_key to your LaunchDarkly SDK key first")
    exit()

  ldclient.set_config(Config(sdk_key))

  # The SDK starts up the first time ldclient.get() is called
  if ldclient.get().is_initialized():
    show_message("SDK successfully initialized!")
  else:
    show_message("SDK failed to initialize")
    exit()

  # Set up the user properties. This user should appear on your LaunchDarkly users dashboard
  # soon after you run the demo.
  user = {
    "key": "example-user-key",
    "name": "Sandy"
  }

  flag_value = ldclient.get().variation(feature_flag_key, user, False)

  show_message("Feature flag '%s' is %s for this user" % (feature_flag_key, flag_value))

  # Here we ensure that the SDK shuts down cleanly and has a chance to deliver analytics
  # events to LaunchDarkly before the program exits. If analytics events are not delivered,
  # the user properties and flag usage statistics will not appear on your dashboard. In a
  # normal long-running application, the SDK would continue running and events would be
  # delivered automatically in the background.
  ldclient.get().close()
