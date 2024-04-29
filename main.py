import os
import ldclient
from ldclient import Context
from ldclient.config import Config
from threading import Event
from halo import Halo


# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set feature_flag_key to the feature flag key you want to evaluate.
feature_flag_key = os.getenv('LAUNCHDARKLY_FLAG_KEY', 'sample-feature')

# Set this environment variable to skip the loop process and evaluate the flag
# a single time.
ci = os.getenv('CI')


def show_evaluation_result(key: str, value: bool):
    print()
    print(f"*** The {key} feature flag evaluates to {value}")

    if value:
        show_banner()


def show_banner():
    print()
    print("        ██       ")
    print("          ██     ")
    print("      ████████   ")
    print("         ███████ ")
    print("██ LAUNCHDARKLY █")
    print("         ███████ ")
    print("      ████████   ")
    print("          ██     ")
    print("        ██       ")
    print()


class FlagValueChangeListener:
    def flag_value_change_listener(self, flag_change):
        show_evaluation_result(flag_change.key, flag_change.new_value)


if __name__ == "__main__":
    if not sdk_key:
        print("*** Please set the LAUNCHDARKLY_SDK_KEY env first")
        exit()
    if not feature_flag_key:
        print("*** Please set the LAUNCHDARKLY_FLAG_KEY env first")
        exit()

    ldclient.set_config(Config(sdk_key))

    if not ldclient.get().is_initialized():
        print("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")
        exit()

    print("*** SDK successfully initialized")

    # Set up the evaluation context. This context should appear on your
    # LaunchDarkly contexts dashboard soon after you run the demo.
    context = \
        Context.builder('example-user-key').kind('user').name('Sandy').build()

    flag_value = ldclient.get().variation(feature_flag_key, context, False)
    show_evaluation_result(feature_flag_key, flag_value)

    if ci is None:
        change_listener = FlagValueChangeListener()
        listener = ldclient.get().flag_tracker \
            .add_flag_value_change_listener(feature_flag_key, context, change_listener.flag_value_change_listener)

        with Halo(text='Waiting for changes', spinner='dots'):
            try:
                Event().wait()
            except KeyboardInterrupt:
                pass
