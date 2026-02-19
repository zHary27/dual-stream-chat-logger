import asyncio
import logging
from emoji import demojize

class TwitchLogger:
    def __init__(self, logging_event, nickname: str, token: str, channel: str, stream_name: str, output_dir: str = './logs'):
        self.logging_event = logging_event
        self.nickname = nickname
        self.token = token
        self.channel = channel
        self.stream_name = stream_name
        self.output_dir = output_dir
        
        # Create a named logger for Twitch
        self.logger = logging.getLogger('twitch_chat')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(f'{self.output_dir}/{self.stream_name}_twitch_live_chat.log', encoding='utf-8')
        handler.setFormatter(logging.Formatter('%(asctime)s — %(message)s', datefmt='%Y-%m-%d_%H:%M:%S'))
        self.logger.addHandler(handler)

    async def start(self):

        reader, writer = await asyncio.open_connection('irc.chat.twitch.tv', 6667)
        writer.write(f'PASS {self.token}\r\n'.encode('utf-8'))
        writer.write(f'NICK {self.nickname}\r\n'.encode('utf-8'))
        writer.write(f'JOIN {self.channel}\r\n'.encode('utf-8'))
        await writer.drain()

        while not self.logging_event.is_set():
            try:
                response = await asyncio.wait_for(reader.readline(), timeout=0.5)
                response = response.decode('utf-8').strip()
                if response.startswith('PING'):
                    writer.write('PONG :tmi.twitch.tv\r\n'.encode('utf-8'))
                    await writer.drain()
                elif 'PRIVMSG' in response:
                    self.logger.info(demojize(response))
            except asyncio.TimeoutError:
                continue

        writer.close()
        await writer.wait_closed()