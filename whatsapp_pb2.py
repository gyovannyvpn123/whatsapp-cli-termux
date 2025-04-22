# Stub minimal — extinde cu definițiile reale protobuf
from google.protobuf.message import Message
class Message(Message):
    key = type('K', (), {'remote_jid': ''})()
    conversation = ''
    def SerializeToString(self): ...
    @classmethod
    def FromString(cls, data): ...
