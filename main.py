import discord
from listener.core.client import NanoClient as Client

startup_extensions = [
    'listener.general_commands',
    'listener.konsolemod.fun',
    'listener.konsolemod.gnulinux',
    'listener.konsolemod.goodbye',
    'listener.konsolemod.infosystem',
    'listener.konsolemod.mod',
    'listener.konsolemod.submits',
    'listener.konsolemod.tickets',
    'listener.konsolemod.welcome',
    'listener.tools',
    'listener.wallpapers',
    'listener.minigames',
]

client = Client(command_prefix='$')
client.remove_command('help')

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            client.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

client.run("ваш токен")
