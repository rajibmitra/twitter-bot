# Twitter Auto Follow Back Bot

A Python based Twitter bot that automatically follows back users who follow a specified Twitter account. Built using Twitter API and Tweepy.

## Features

- Fetch followers of a target user
- Fetch users that the target user is following
- Automatically follow back users who aren't being followed yet
- Rate limiting implementation to comply with Twitter API guidelines
- Error handling and detailed logging
- Authentication testing

## Prerequisites

- Python 3.7+
- Twitter Developer Account
- Twitter API Keys and Tokens

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rajibmitra/twitter-bot.git
cd twitter-bot
```

2. Install required packages:
```bash
pip install tweepy
```

3. Create a `config.json` file in the project root:
```json
{
    "api_key": "your_api_key",
    "api_secret": "your_api_secret",
    "access_token": "your_access_token",
    "access_token_secret": "your_access_token_secret",
    "bearer_token": "your_bearer_token"
}
```

## Configuration

1. Create a Twitter Developer Account at [developer.twitter.com](https://developer.twitter.com)
2. Create a new Project and App in the Twitter Developer Portal
3. Generate the necessary API keys and tokens
4. Update the `config.json` file with your credentials

## Usage

Run the bot with:
```bash
python main.py
```

The bot will:
1. Authenticate with Twitter
2. Fetch the target user's followers
3. Fetch the users the target is following
4. Identify users to follow back
5. Follow users who aren't being followed yet

## Rate Limiting

The bot implements rate limiting to comply with Twitter's API guidelines:
- 2-second delay between API calls
- Maximum 100 results per pagination
- Automatic handling of Twitter API rate limits

## Error Handling

The bot includes comprehensive error handling for:
- Authentication failures
- API rate limits
- Network errors
- User not found scenarios
- Invalid credentials

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This bot is for educational purposes only. 

## Author

Your Name
- Twitter: [@xDevLo](https://x.com/xDevLo)
- GitHub: [yourusername](https://github.com/rajibmitra)