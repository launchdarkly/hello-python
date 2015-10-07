#!/usr/bin/env python
from ldclient import LDClient
from ldclient import Config

if __name__ == "__main__":
  ld_client = LDClient("YOUR_API_KEY")

  user = {
    "key": "bob@example.com",
    "firstName": "Bob",
    "lastName": "Loblaw",
    "custom": {
      "groups": "beta_testers"
    }
  }

  show_feature = ld_client.toggle("YOUR_FLAG_KEY", user, False)

  if show_feature:
    print "Showing your feature"
  else:
    print "Not showing your feature"

  ld_client.flush()
