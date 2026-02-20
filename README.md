# Dual Stream Chat Logger

A Python tool to log live chat messages from both YouTube and Twitch streams, and parse them into a CSV for further analysis.

## Features
- Logs live chat from YouTube and Twitch simultaneously
- Saves logs to timestamped files in the `logs/` directory
- Parses logs into a structured CSV using a Jupyter notebook

## Requirements
- Python 3.8+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/zHary27/dual-stream-chat-logger.git
   cd dual-stream-chat-logger
   ```
2. Create a `.env` file in the root directory with your Twitch credentials:
   ```env
   TWITCH_NICKNAME=your_twitch_username
   TWITCH_OAUTH_TOKEN=your_twitch_oauth_token
   TWITCH_CHANNEL=your_twitch_channel
   ```
   You can generate a Twitch OAuth token at https://twitchtokengenerator.com/

## Usage

### Logging Live Chat
Run the logger from the command line:
```bash
python main.py <YOUTUBE_VIDEO_ID> <STREAM_NAME> [--output_dir ./logs]
```
- `<YOUTUBE_VIDEO_ID>`: The ID of the YouTube live stream
- `<STREAM_NAME>`: A base name for your log files (e.g., the stream date or title)
- `--output_dir`: (Optional) Directory to save log files (default: `./logs`)

Example:
```bash
python main.py 4LaMmR39UvE test
```

- Press `q` and Enter in the terminal to stop logging.

### Parsing Logs to CSV
Open `parser.ipynb` in Jupyter or VS Code and run all cells. This will:
- Parse both Twitch and YouTube logs
- Output a CSV file named `<stream_name>_chat_data.csv` with columns: `timestamp`, `platform`, `username`, `message`