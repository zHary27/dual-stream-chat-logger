from chat_logger import YouTubeLogger, TwitchLogger
import dotenv
import os

import argparse
import asyncio

dotenv.load_dotenv()

async def main(youtube_id: str,stream_name: str, output_dir: str):
    logging_event = asyncio.Event()

    youtube_logger = YouTubeLogger(logging_event, youtube_id, stream_name, output_dir)
    twitch_logger = TwitchLogger(logging_event, os.getenv('TWITCH_NICKNAME'), os.getenv('TWITCH_OAUTH_TOKEN'), f'#{os.getenv('TWITCH_CHANNEL')}', stream_name, output_dir)

    async def key_listener():
        print('Press "q" then Enter to stop loggers.')
        loop = asyncio.get_running_loop()
        while not logging_event.is_set():
            inp = await loop.run_in_executor(None, input)
            if inp.strip().lower() == 'q':
                logging_event.set()
                print('Stopping loggers...')
                break

    async with asyncio.TaskGroup() as tg:
        tg.create_task(key_listener())
        for logger in (youtube_logger, twitch_logger):
            tg.create_task(logger.start())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Log Twitch and YouTube live chat messages.')
    parser.add_argument('youtube_id', help='YouTube video ID for the live stream')
    parser.add_argument('stream_name', help='Base name for the output log files')
    parser.add_argument('--output_dir', default='./logs', help='Directory to save log files (default: ./logs)')
    args = parser.parse_args()

    asyncio.run(main(args.youtube_id, args.stream_name, args.output_dir))