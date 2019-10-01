Example [Rossum](https://rossum.ai/) webhook endpoint that post to Slack

# How to run
For testing the webhook, one can use [ngrok](https://ngrok.com/).

```shell
$ ngrok http 5042
```

Copy the address produced by `ngrok` (something like: `https://aaabbbccc.ngrok.io`)
and set it to [`webhook.config.url`](https://api.elis.rossum.ai/docs/#webhook).

Then start the webserver on localhost...
```shell
$ export SLACK_URL="https://hooks.slack.com/services/<secret>"
$ export SECRET_KEY="<Secret key stored in webhook.config.secret>"
$ ./webhook_slack_notification.py
```

... and enjoy slack notifications whenever any annotation changes its status.
