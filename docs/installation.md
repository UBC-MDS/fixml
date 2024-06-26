# Installation

In this page, we will guide through you how to install FixML on your 
computer, and get started to using it for evaluating your code projects!

## Prerequisites

FixML is written to support Python version 3.12 or later. Make sure that you 
have Python with version 3.12 or later installed in your system.

```{note}
Get Python on their [official website](https://www.python.org).

Alternatively, you can use the ones that come with your Operating System, or
come from a virtual environment managers such
as [virtualenv](https://virtualenv.pypa.io) and/or [conda](https://conda.io).
```

## Getting the package from PyPI

`fixml` package is hosted
on [the Python Package Index (PyPI)](https://pypi.org). You can visit the
project page on PyPI [here](https://pypi.org/project/fixml/).

To install this, enter this command in your terminal:
```bash
pip install fixml

# or 

python3 -m pip install fixml
```

## Configuring API Keys

As of version 0.1.0, the only supported connector to LLMs is the OpenAI API. 
Therefore, for any workload that involves calls to LLMs, an API key for 
accessing OpenAI API is required.

### Getting the API Key

You can refer to OpenAI's page
on [obtaining API keys](https://platform.openai.com/api-keys).

```{warning}
The API keys are credentials that should be treated the same way you treat
passwords. Refer to OpenAI's page on best practices for
[keeping your API key safe](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety).
```

```{note}
FixML only use the API key stored *locally* in your system for calls to LLMs, 
and will not save, transmit, or leak the API keys in any way.
```

### Increasing Quota

```{note}
The free trial version of OpenAI API comes with many limits, such as a very 
low ceiling on the token per minute quota.

Although optimizations have been done to reduce the usage on the tokens, FixML
still need to transmit a significant portion of the code base when conducting
the analysis.

As such, for most code bases, the free trial version of the API is unsuitable
for use and would often result in errors stating rate limit has been reached.
```

To prevent FixML from hitting rate limit error, user should upgrade their API to
the paid version and thus raising the rate limit to remove this restriction.

Based
on [OpenAI's documentation](https://platform.openai.com/docs/guides/rate-limits/usage-tiers?context=tier-one),
we estimate you must be at least at Tier 1 to be able to use our tool without
the frequent intermittent rate limit errors.

Refer to OpenAI's documentations
on [rate limits and quotas](https://platform.openai.com/docs/guides/rate-limits)
and [account limits](https://platform.openai.com/account/limits).

### Saving the API Key into your system

Once obtained the API key, the key needs to be stored in your system in 
order for FixML to be able to discover it and subsequently use it for 
calling the OpenAI service endpoints.

Currently, FixML will look for such key through the use
of [Environment Variables](https://en.wikipedia.org/wiki/Environment_variable).

There are two ways to do this:

#### 1. Saving it Directly as an Environment Variable

This way we will directly save the API key into the Operating System's set of
environment variables.

```{note}
**Advantage**: Since it is saved as an Environment Variable in your Operating
System, it is accessible by `fixml` from any directory you are working on.

**Disadvantage**: This setting is transient and will not persist after a system 
reboot. To make this change permanent, you can add the `export` command below as
a part of start up script. 
```

##### Unix-like systems (Linux, MacOS, etc)

1. Run this in your console/terminal emulator:
    ```bash
    export OPENAI_API_KEY={your-openai-api-key}
    ```

2. After running the command, confirm that the variable has been saved into the 
system:
    ```bash
    export | grep OPENAI_API_KEY
    ```

##### Windows

1. Run this in your console:
    ```cmd
    SET OPENAI_API_KEY={your-openai-api-key}
    ```

2. After running the command, confirm that the variable has been saved into the
   system:
    ```cmd
    SET OPENAI_API_KEY
    ```
   
#### 2. Saving it inside an `.env` File

This method will save your API key into a file named `.env`. This will not 
be directly injecting your API key as an environment variable into your 
computer. Rather, when FixML is being run, it will look for file named `.
env` file in the *current working directory* and inject the content inside 
as a set of temporary Environment Variables.

```{note}
**Advantage**: Persistent storage, and will survive reboots as this is a file.

**Disadvantage**: Since it depends on the `.env` file's location, it is not
runnable outside the directory where there is no such `.env` file.
```

To do this, run the follow command:
```bash
echo OPENAI_API_KEY={your-openai-api-key} > .env
```