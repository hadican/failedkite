import logging


class NotificationService:
    def __init__(self, slack_client, config):
        self.slack_client = slack_client
        self.config = config
        self.default_user_id = self.slack_client.get_user_id_by_email(self.config.default_slack_email)
        if self.default_user_id is None:
            raise Exception(f"Failed to retrieve default Slack user ID for the email: {self.config.default_slack_email}")
        self.logger = logging.getLogger(self.__class__.__name__)

    def notify(self, build):
        build_web_url = build['web_url']
        build_source = build.get("source")
        if build_source == "schedule":
            trigger_message = f"Not a human-triggered job, no action was taken for the build url={build_web_url}"
            self.logger.info(trigger_message)
            return trigger_message, 200

        build_status = build.get("state")
        if build_status != "failed":
            build_status_message = f"Not a build failure, no action taken for the build url={build_web_url}."
            return build_status_message, 200

        build_creator = build.get("creator")
        build_author = build.get("author")

        if build_creator:
            email = build_creator.get("email")
        elif build_author:
            username = build_author.get("username")

            ignore_users: list[str] | None = self.config.ignore_users
            if ignore_users and username in ignore_users:
                build_user_message = f"The username={username} was ignored for the failing build url={build_web_url}"
                return build_user_message, 200

            slack_email = self.config.author_mapping.get(username)

            if slack_email:
                email = slack_email
            else:
                build_author_message = f"No user was found in the author mapping with the username={username} for the failing build url={build_web_url}"
                self.slack_client.send_message(build_author_message, self.default_user_id)
                return build_author_message, 500
        else:
            build_user_message = f"No user was found for the failing build url={build_web_url}"
            self.slack_client.send_message(build_user_message, self.default_user_id)
            return build_user_message, 500

        user_id = self.slack_client.get_user_id_by_email(email)

        if not user_id:
            user_message = f"Failed to fetch user ID from Slack for email={email} for build url={build_web_url}"
            return user_message, 500

        buildkite_message = f"Your build has `failed`. Here is the URL to check: {build_web_url}"
        status = self.slack_client.send_message(buildkite_message, user_id)
        if status:
            return buildkite_message, 200
        else:
            return "Failed to send Slack message.", 500
