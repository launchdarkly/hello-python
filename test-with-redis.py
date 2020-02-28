#!/usr/bin/env python
import logging
import sys
from ldclient.config import Config
from ldclient.feature_store import CacheConfig
from ldclient.integrations import Redis  # Install redis package using redis-requirements.txt
import ldclient

root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

if __name__ == "__main__":
  store = Redis.new_feature_store(url='redis://localhost:6379/DATABASE_NUMBER',
                                  prefix='DESIRED_PREFIX', caching=CacheConfig(expiration=30))

  config = Config(sdk_key='YOUR_SDK_KEY', feature_store=store) # load redis with feature flags added on the dashboard
  # config = Config(feature_store=store, use_ldd=True) # Comment out the previous line and uncomment this line to have Launchdarkly SDK work against your redis

  ldclient.set_config(config)

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
    print("Showing your feature")
  else:
    print("Not showing your feature")

  ldclient.get().close() # close the client before exiting the program - ensures that all events are delivered
