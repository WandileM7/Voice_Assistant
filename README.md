# AI Personal Assistant

This project implements an AI-powered personal assistant with voice interaction capabilities, integrating various services and functionalities.

## Features

- Voice recognition and text-to-speech capabilities
- OpenAI GPT integration for natural language processing
- Spotify integration for music playback
- WhatsApp messaging functionality
- Email management (reading and sending) via Gmail API
- Application management (opening and closing)
- Event scheduling and calendar management
- Social media quick access

## Components

The project consists of several Python scripts:

1. `main.py`: The core script that handles user interactions and integrates various functionalities.
2. `utils.py`: Contains utility functions, including the text-to-speech functionality.
3. `gmail.py`: Handles email-related functions using the Gmail API.
4. `app.py`: A Flask application for handling WhatsApp integration via Twilio.
5. `run-assistant.py`: A script that runs both the main assistant and the WhatsApp server concurrently using threading.

## Setup and Installation

1. Clone the repository to your local machine.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up the necessary API keys and credentials (see Configuration section).

## Usage

To run the AI assistant and WhatsApp server concurrently:

```
python run-assistant.py
```

This will start both the main assistant for voice interaction and the WhatsApp server for messaging integration.

## Dependencies

The project relies on the following main dependencies:

- openai
- SpeechRecognition
- PyAudio
- pygame
- spotipy
- pyautogui
- google-api-python-client
- pyttsx3
- python-dotenv
- Flask
- Twilio

For a complete list of dependencies and their versions, refer to the `requirements.txt` file.

## Configuration

The project uses environment variables for various API keys and credentials. Make sure to set up a `.env` file with the following variables:

- `OPENAI_API_KEY`
- `SPOTIPY_CLIENT_ID`
- `SPOTIPY_CLIENT_SECRET`
- `SPOTIPY_REDIRECT_URI`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`

Additionally, you'll need to set up OAuth 2.0 credentials for the Google API integration.

## Contributing

Contributions to improve the AI Personal Assistant are welcome. Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Create a new Pull Request

## License

[MIT License](https://opensource.org/licenses/MIT)

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

