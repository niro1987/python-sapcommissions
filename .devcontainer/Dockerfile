FROM mcr.microsoft.com/devcontainers/python:1-3.12

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Uninstall pre-installed formatting and linting tools
# They would conflict with our pinned versions
RUN pipx uninstall pydocstyle \
    && pipx uninstall pycodestyle \
    && pipx uninstall mypy \
    && pipx uninstall pylint

RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies from requirements
WORKDIR /workspaces
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY .devcontainer/requirements-dev.txt ./requirements-dev.txt
RUN pip3 install -r requirements-dev.txt
RUN rm requirements.txt requirements-dev.txt

ENV SHELL /bin/bash
