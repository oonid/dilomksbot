# DiLoMksBot

DILo Makassar Telegram Bot

## Getting Started

Important steps

### Prerequisites

* Create Telegram bot by contacting @BotFather (currently [@DiLoMksBot](https://telegram.com/dilomksbot))
* Create Google App Engine project for Python (eg: xxyyzz.appspot.com)

## Built With

* [Flask](http://flask.pocoo.org//) - The web framework used

## Installation

Add Telegram webhook. webhook URL 
```
curl -F "url=https://xxyyzz.appspot.com/webhook/<YOURTOKEN>" https://api.telegram.org/bot<YOURTOKEN>/setWebhook
```

## Deployment

Update configuration on app.yaml. Your Telegram Token and Group ID. 

Install packages to lib/ directory, it will be deployed also to App Engine.

Deploy to your App Engine project.

```
gcloud app deploy --project xxyyzz --verbosity=info app.yaml
```

Create cron for scheduler and update to Google App Engine.

```
gcloud app deploy --project xxyyzz --verbosity=info app.yaml cron.yaml
```

## Authors

* **oon arfiandwi** - *Initial work* - [OonID](https://github.com/OonID)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* etc
