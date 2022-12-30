# LaunchDarkly sample Python application

We've built a console application that demonstrates how LaunchDarkly's SDK works.

Below, you'll find the basic build procedure. For more comprehensive instructions, you can visit your [Quickstart page](https://app.launchdarkly.com/quickstart#/) or the [Python SDK reference guide](https://docs.launchdarkly.com/sdk/server-side/python).

This demo requires Python version 3.7 or higher.

## Build instructions

1. Install the LaunchDarkly Python SDK by running `pip install -r requirements.txt`

2. Edit `test.py` and set the value of `sdk_key` to your LaunchDarkly SDK key. If there is an existing boolean feature flag in your LaunchDarkly project that you want to evaluate, set `feature_flag_key` to the flag key.

```python
sdk_key = "1234567890abcdef"

feature_flag_key = "my-flag"
```

3. Run `python test.py`.

You should receive the message `"Feature flag '<flag key>' is <true/false> for this user"`.
