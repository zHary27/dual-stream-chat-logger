import pytchat
import logging
import asyncio

class YouTubeLogger:
    def __init__(self, logging_event, video_id: str, stream_name: str, output_dir: str = './logs'):
        self.logging_event = logging_event
        self.video_id = video_id
        self.stream_name = stream_name
        self.output_dir = output_dir
        
        # Create a named logger for YouTube
        self.logger = logging.getLogger('youtube_chat')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(f'{self.output_dir}/{self.stream_name}_youtube_live_chat.log', encoding='utf-8')
        handler.setFormatter(logging.Formatter('%(asctime)s — %(message)s', datefmt='%Y-%m-%d_%H:%M:%S'))
        self.logger.addHandler(handler)

    async def start(self):
        while not self.logging_event.is_set():
            try:
                chat = pytchat.create(video_id=self.video_id)
                
                while chat.is_alive() and not self.logging_event.is_set():
                    for c in chat.get().sync_items():
                        self.logger.info(f'[{c.author.name}]- {c.message}')
                    await asyncio.sleep(0.1)
                
            except Exception as e:
                print(f'Error in YouTube logger: {e}')
                
            if not self.logging_event.is_set():
                await asyncio.sleep(2)