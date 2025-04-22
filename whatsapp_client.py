import os
import json
import base64
import asyncio
import websockets

from utils import log, show_pairing_code, save_bin, load_bin
from signal_protocol import SignalProtocol
import whatsapp_pb2 as WAPB

WA_SERVER = 'wss://web.whatsapp.com/ws'
KEY_DIR = '.keys'

class WhatsAppClient:
    def __init__(self):
        self.ws = None
        self.signal = SignalProtocol(KEY_DIR)
        self.remote = None

    async def connect(self):
        self.ws = await websockets.connect(WA_SERVER)
        log('[+] Conectat la WhatsApp Web', 'green')
        await self._init_handshake()
        asyncio.create_task(self._recv_loop())

    async def _init_handshake(self):
        # Trimite init către server
        await self.ws.send(json.dumps({'type': 'init'}))
        msg = await self.ws.recv()
        data = json.loads(msg)
        # Afișăm cod textual
        show_pairing_code(data.get('ref', ''))
        await self._wait_for_login()

    async def _wait_for_login(self):
        while True:
            msg = await self.ws.recv()
            data = json.loads(msg)
            if data.get('type') == 'login':
                save_bin(os.path.join(KEY_DIR, 'session.bin'),
                         base64.b64decode(data['session']))
                log('[+] Autentificat cu succes!', 'green')
                self.signal.load_session(load_bin(os.path.join(KEY_DIR, 'session.bin')))
                return

    async def _recv_loop(self):
        while True:
            raw = await self.ws.recv()
            enc = base64.b64decode(raw)
            plain = self.signal.decrypt(enc)
            msg = WAPB.Message.FromString(plain)
            if hasattr(msg, 'conversation'):
                sender = msg.key.remote_jid
                text = msg.conversation
                log(f"[{sender}] {text}", 'yellow')

    async def send_message(self, to: str, message: str):
        msg = WAPB.Message()
        msg.key.remote_jid = to
        msg.conversation = message
        data = msg.SerializeToString()
        enc = self.signal.encrypt(data, to)
        await self.ws.send(base64.b64encode(enc).decode())
        log(f"[Me -> {to}] {message}", 'blue')
