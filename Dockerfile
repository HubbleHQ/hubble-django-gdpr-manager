FROM python:3.9-alpine as base

RUN mkdir /src
WORKDIR /src

# We always need pipenv, so it goes in base
RUN pip install pipenv

FROM base AS deps
# Install *only* the production dependencies
COPY "Pipfile" "Pipfile.lock" ./

RUN pipenv install --system

FROM deps AS deps-dev
# Add the dev dependencies
RUN pipenv install --system --dev

# Required for build and deployment
RUN pip install --upgrade build
RUN pip install --upgrade twine

RUN apk add --no-cache \
    # In development, git is used inside the container
    git \
    # The default shell is weird. Let's make zsh available.
    zsh

FROM deps-dev AS dev
COPY . .
# Keeps it open until you close it, dunno why but makes my brain happier
# Technically don't need this you could just shell in.
ENTRYPOINT ["tail", "-f", "/dev/null"] 

# Set the default target. This way, if we run `docker build` without specifying
# a target, it will build the dev image. NOTE: this _must_ be the last
# line in the file.
FROM dev