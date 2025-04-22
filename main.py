import asyncio
from whatsapp_client import WhatsAppClient
from termcolor import cprint

async def main():
    cprint('=== WhatsApp CLI Python - Termux ===', 'blue')
    client = WhatsAppClient()
    await client.connect()

    while True:
        try:
            parts = input('> ').strip().split(' ', 2)
            cmd = parts[0].lower()
            if cmd == 'send' and len(parts) == 3:
                to, msg = parts[1], parts[2]
                await client.send_message(to, msg)
            elif cmd in ('exit', 'quit'):
                break
            else:
                print('Comenzi:')
                print(' send <numar> <mesaj>')
                print(' exit/quit')
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    asyncio.run(main())
