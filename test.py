import os
import ldclient
from ldclient import Context
from ldclient.config import Config

# Set sdk_key to your LaunchDarkly SDK key before running
sdk_key = os.getenv("LAUNCHDARKLY_SERVER_KEY")

# Set feature_flag_key to the feature flag key you want to evaluate
feature_flag_key = os.getenv("LAUNCHDARKLY_FLAG_KEY")


def show_message(s):
    print("*** %s" % s)
    print()


if __name__ == "__main__":
    if not sdk_key:
        show_message("Please set the LAUNCHDARKLY_SERVER_KEY env first")
        exit()
    if not feature_flag_key:
        show_message("Please set the LAUNCHDARKLY_FLAG_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key))

    # The SDK starts up the first time ldclient.get() is called
    if ldclient.get().is_initialized():
        show_message("SDK successfully initialized!")
    else:
        show_message("SDK failed to initialize")
        exit()

    # Set up the evaluation context. This context should appear on your
    # LaunchDarkly contexts dashboard soon after you run the demo.
    context = Context.builder('example-user-key').name('Sandy').build()

    flag_value = ldclient.get().variation(feature_flag_key, context, False)

    show_message("Feature flag '%s' is %s for this context" % (feature_flag_key, flag_value))

    # Here we ensure that the SDK shuts down cleanly and has a chance to
    # deliver analytics events to LaunchDarkly before the program exits. If
    # analytics events are not delivered, the context properties and flag usage
    # statistics will not appear on your dashboard. In a normal long-running
    # application, the SDK would continue running and events would be delivered
    # automatically in the background.
    ldclient.get().close()
