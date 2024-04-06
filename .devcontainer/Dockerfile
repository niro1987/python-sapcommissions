FROM mcr.microsoft.com/devcontainers/python:1-3.12

# Uninstall pre-installed formatting and linting tools
# They would conflict with our pinned versions
RUN pipx uninstall pydocstyle \
    && pipx uninstall pycodestyle \
    && pipx uninstall mypy \
    && pipx uninstall pylint

# Install Python dependencies from requirements
WORKDIR /usr/src/app
COPY . .
RUN python -m pip install --upgrade pip setuptools \
    && python -m pip install -r requirements.txt -r .devcontainer/requirements-dev.txt
