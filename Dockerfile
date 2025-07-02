FROM public.ecr.aws/docker/library/python:3.11-slim-bullseye

WORKDIR /app
ADD . .

# Update aptitude and install required software
RUN apt-get update && apt-get install -y \
    git \
    curl \
    unzip \
    screen \
    iproute2 \
    tar \
    rsync \
    # WeasyPrint dependencies
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    libglib2.0-0

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf aws awscliv2.zip

# AWS credentials setup
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION=us-east-1

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION

RUN export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
RUN export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
RUN export AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION


# Configure git for CodeCommit
RUN git config --global credential.helper '!aws codecommit credential-helper $@'
RUN git config --global credential.UseHttpPath true



ARG DD_GIT_REPOSITORY_URL
ARG DD_GIT_COMMIT_SHA
ENV DD_GIT_REPOSITORY_URL=${DD_GIT_REPOSITORY_URL}
ENV DD_GIT_COMMIT_SHA=${DD_GIT_COMMIT_SHA}

# Make ssh dir

ARG SSH_KEY
ENV SSH_KEY=$SSH_KEY

# Make ssh dir
RUN mkdir $HOME/.ssh/

# Copy over private key, and set permissions

RUN echo "$SSH_KEY" > $HOME/.ssh/id_rsa
RUN chmod 600 $HOME/.ssh/id_rsa

# Create known_hosts
RUN touch $HOME/.ssh/known_hosts


RUN ssh-keyscan github.com >> $HOME/.ssh/known_hosts


# Set Git global configs
RUN git config --global user.email "admin@kavia.ai" && \
    git config --global user.name "CodeGen Bot"



ENV PYTHONPATH=/app
RUN export PYTHONPATH=/app

RUN aws codeartifact login --tool pip --domain kavia --domain-owner 058264095463 --repository kavia
RUN pip install --upgrade pip setuptools wheel
RUN pip install html2text pylatexenc pyperclip --no-build-isolation
RUN pip install -r requirements.txt --no-cache-dir



EXPOSE 8000

CMD ["ddtrace-run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--loop", "uvloop", "--timeout-keep-alive", "900"]