# Project Title

DiLo Makassar Telegram Bot

## Getting Started

Important steps

### Prerequisites

* Create Telegram bot by contacting @BotFather (currently @DiLoMksBot)
* Create Google App Engine project for Python (eg: xxyyzz.appspot.com)

## Built With

* [Flask](http://flask.pocoo.org//) - The web framework used

## Installation

Add Telegram webhook. webhook URL 
```
curl -F "url=https://xxyyzz.appspot.com/webhook/<YOURTOKEN>" https://api.telegram.org/bot<YOURTOKEN>/setWebhook
```

## Deployment

Install packages to lib/ directory, it will be deployed also to App Engine.

```
gcloud app deploy --project xxyyzz --verbosity=info app.yaml
```

## Authors

* **oon arfiandwi** - *Initial work* - [OonID](https://github.com/OonID)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* etc
