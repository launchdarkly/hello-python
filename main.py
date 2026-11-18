import os
import sys
from contextlib import asynccontextmanager
from threading import Event

import ldclient
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from halo import Halo
from ldclient import Context
from ldclient.config import Config

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')

# Set feature_flag_key to the feature flag key you want to evaluate.
feature_flag_key = os.getenv('LAUNCHDARKLY_FLAG_KEY') or 'sample-feature'

# Set this environment variable to skip the loop process and evaluate the flag
# a single time.
ci = os.getenv('CI')

# Set up the evaluation context. This context should appear on your
# LaunchDarkly contexts dashboard soon after you run the demo.
context = \
    Context.builder('example-user-key').kind('user').name('Sandy').build()


def show_evaluation_result(key: str, value: bool):
    print()
    print(f"*** The {key} feature flag evaluates to {value}.")

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


def start_client():
    """Start the SDK client. Exit with a clear message when it cannot start."""
    if not sdk_key:
        sys.exit("LaunchDarkly SDK key is required: set the LAUNCHDARKLY_SDK_KEY environment variable and try again.")
    if not feature_flag_key:
        sys.exit("LaunchDarkly flag key is required: set the feature_flag_key variable in main.py, "
                 "or the LAUNCHDARKLY_FLAG_KEY environment variable and try again.")

    ldclient.set_config(Config(sdk_key))

    if not ldclient.get().is_initialized():
        sys.exit("*** SDK failed to initialize. Please check your internet connection and SDK credential for any typo.")

    print("*** SDK successfully initialized!")


def add_change_listener():
    change_listener = FlagValueChangeListener()
    ldclient.get().flag_tracker \
        .add_flag_value_change_listener(feature_flag_key, context, change_listener.flag_value_change_listener)


@asynccontextmanager
async def lifespan(_app):
    start_client()
    add_change_listener()
    yield


# `vercel dev` loads this variable.
app = FastAPI(lifespan=lifespan)


@app.get("/", response_class=PlainTextResponse)
def index():
    flag_value = ldclient.get().variation(feature_flag_key, context, False)
    return f"*** The {feature_flag_key} feature flag evaluates to {flag_value}.\n"


if __name__ == "__main__":
    start_client()

    flag_value = ldclient.get().variation(feature_flag_key, context, False)
    show_evaluation_result(feature_flag_key, flag_value)

    if ci is None:
        add_change_listener()

        with Halo(text='Waiting for changes', spinner='dots'):
            try:
                Event().wait()
            except KeyboardInterrupt:
                pass
