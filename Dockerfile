FROM python:3.9.13-slim-buster

# install ubuntu packages
RUN DEBIAN_FRONTEND=noninteractive apt-get update \
    && apt-get --yes install \
        bash \
        bash-completion \
        git \
    && rm -rf /var/lib/apt/lists/*

# args
ARG UID=1000
ARG GID=1000
ARG PROJECT_DIR=/opt/project
ARG STATIC_ROOT=/opt/static

# runtime user
RUN useradd -l --uid $UID --base-dir /home --create-home --home-dir /home/testuser testuser

# environment
ENV PROJECT_DIR=$PROJECT_DIR \
    DJANGO_SETTINGS_MODULE=project.settings \
    PATH=/home/testuser/.local/bin:$PATH

# add project directories
RUN mkdir $PROJECT_DIR $STATIC_ROOT && \
    chown -R testuser:testuser $PROJECT_DIR $STATIC_ROOT

# copy project to project dir and make sure /opt is owned by testuser
COPY --chown=testuser:testuser . ${PROJECT_DIR}

# use non priviledged user
USER testuser

# set pip configuration and install requirements
RUN pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org" &&  \
    pip install --no-cache-dir --prefer-binary -r $PROJECT_DIR/requirements.txt

# default expose port
EXPOSE 8000

WORKDIR $PROJECT_DIR