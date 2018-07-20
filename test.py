#!/usr/bin/env python
import logging
import sys

import ldclient

root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

if __name__ == "__main__":
  ldclient.set_sdk_key("YOUR_SDK_KEY")

  user = {
    "key": "bob@example.com",
    "firstName": "Bob",
    "lastName": "Loblaw",
    "custom": {
      "groups": "beta_testers"
    }
  }

  show_feature = ldclient.get().variation("YOUR_FLAG_KEY", user, False)

  if show_feature:
    print "Showing your feature"
  else:
    print "Not showing your feature"

  ldclient.get().close() # close the client before exiting the program - ensures that all events are delivered
