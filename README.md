# Failedkite

`Failedkite` is a webhook project for `Buildkite` to notify users via direct message (DM) on `Slack` for failed builds.

Currently, on Buildkite integration settings, you can only notify users via public/private `#channel`, not individually.

## How it works?

This application provides a `webhook` that should be triggered when a build fails on your Buildkite,
which will be like `http://your_host:8080/webhook`.

Please note that it is better to secure your connection using SSL/TLS to protect sensitive data. In a production
environment, we recommend creating a reverse proxy with nginx or a similar tool and securing your connection with SSL.

You can get more information about Buildkite Webhooks [here](https://buildkite.com/docs/apis/webhooks).

## Dependencies

- Python 3.11
- Flask 2.3.2
- slackclient 2.9.4
- gunicorn 21.2.0
- PyYAML 6.0.1

## Usage

You need:

- `GitHub` username to `Slack` email address mapping file (author mapping)
- A `Slack` token ([more info](https://api.slack.com/authentication/token-types)).
- This webhook to be set on `Buildkite` integration settings ([more info](https://buildkite.com/docs/apis/webhooks)).

You can run a Docker container with the existing image on Docker Hub:

```sh
docker run -v ./author_mapping.yml:/config/author_mapping.yml \
           -e SLACK_TOKEN=your_slack_token \
           -e DEFAULT_SLACK_EMAIL=your_default_email \
           -p 8080:8080 -d hadican/failedkite:latest
```

This application listens on port `8080` and the endpoint `/webhook` is exposed for receiving Buildkite webhook requests.

### Author Mapping

You need to provide an `author_mapping.yml` file located in the `/config` directory which matches GitHub usernames to
Slack email addresses. If no match is found, then `DEFAULT_SLACK_EMAIL` is notified.

### Environment Variables

You need to set the following environment variables:

- `SLACK_TOKEN`: This is your Slack token, which you can obtain [here](https://api.slack.com/authentication/basics).
- `DEFAULT_SLACK_EMAIL`: This is the default email address to be notified when the author cannot be identified.

### Build Your Own Image

Your Dockerfile is set to run the app. Here's a basic idea of the Docker commands:

To build the Docker image:

```sh
docker build -t failedkite .
```

To run the Docker container:

```sh
docker run -v ./author_mapping.yml:/config/author_mapping.yml \
           -e SLACK_TOKEN=your_slack_token \
           -e DEFAULT_SLACK_EMAIL=your_default_email \
           -p 8080:8080 -d failedkite
```
