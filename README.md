# LaunchDarkly sample Python application

We've built a simple console application that demonstrates how LaunchDarkly's SDK works.

Below, you'll find the build procedure. For more comprehensive instructions, you can visit your [Quickstart page](https://app.launchdarkly.com/quickstart#/) or the [Python reference guide](https://docs.launchdarkly.com/sdk/server-side/python).

This demo requires Python 3.10 or higher.

## Build instructions

1. Set the environment variable `LAUNCHDARKLY_SDK_KEY` to your LaunchDarkly SDK key. If there is an existing boolean feature flag in your LaunchDarkly project that you want to evaluate, set `LAUNCHDARKLY_FLAG_KEY` to the flag key; otherwise, a boolean flag of `sample-feature` will be assumed.

    ```bash
    export LAUNCHDARKLY_SDK_KEY="1234567890abcdef"
    export LAUNCHDARKLY_FLAG_KEY="my-boolean-flag"
    ```

1. Ensure you have [Poetry](https://python-poetry.org/) installed.
1. Install the required dependencies with `poetry install`.
1. On the command line, run `poetry run python main.py`

You should receive the message "The <flagKey> feature flag evaluates to <flagValue>.". The application will run continuously and react to the flag changes in LaunchDarkly.

## Run with `vercel dev`

`main.py` also defines a small FastAPI app that serves the same flag evaluation over HTTP. Use it to check the SDK in a local Vercel Python runtime. This section does not deploy anything.

1. Install the [Vercel CLI](https://vercel.com/docs/cli) and run `vercel link` once. This step links the directory to a Vercel project. It does not deploy.
1. Install the dependencies in a virtual environment: `poetry install`.
1. Put your SDK key in a `.env` file in this directory. `vercel dev` does not read `.env.local`.

    ```bash
    LAUNCHDARKLY_SDK_KEY="1234567890abcdef"
    LAUNCHDARKLY_FLAG_KEY="my-boolean-flag"
    ```

1. Run `vercel dev`, then open `http://localhost:3000`.

Limits:

- `vercel dev` does not install dependencies. It uses the `.venv` or `venv` directory, or the active virtual environment. That environment must include `uvicorn`.
- The app does not flush events after each response. It depends on the SDK flush interval (5 seconds by default).
- `vercel dev` kills the app when you stop it. The app does not call `close()`, so buffered events can be lost.
- The app exits at startup when the SDK key is missing or the SDK fails to initialize. `vercel dev` then shows an error.
