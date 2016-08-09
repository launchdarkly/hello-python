#!/usr/bin/env python
import ldclient

if __name__ == "__main__":
  ldclient.sdk_key = "YOUR_SDK_KEY"

  user = {
    "key": "bob@example.com",
    "firstName": "Bob",
    "lastName": "Loblaw",
    "custom": {
      "groups": "beta_testers"
    }
  }

  show_feature = ldclient.variation("YOUR_FLAG_KEY", user, False)

  if show_feature:
    print "Showing your feature"
  else:
    print "Not showing your feature"

  ld_client.flush()
