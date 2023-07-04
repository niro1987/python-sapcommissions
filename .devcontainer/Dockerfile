FROM python:3.11

# Install tools
RUN apt-get update && \
  apt-get install -y sudo \
  zsh \
  wget \
  locales \
  && locale-gen en_US.UTF-8

# Upgrade pip
RUN pip install --upgrade pip

# Install production dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Install development dependencies
COPY requirements-dev.txt /tmp/requirements-dev.txt
RUN pip install -r /tmp/requirements-dev.txt && \
    rm /tmp/requirements-dev.txt

# zsh
ENV SHELL /bin/zsh

RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true
RUN zsh -c 'git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions'
RUN zsh -c 'git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting'

COPY .devcontainer/.zshrc /tmp/.zshrc
RUN mv ~/.zshrc ~/.zshrc.bak
RUN mv /tmp/.zshrc ~/.zshrc
