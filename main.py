from interface import *
import asyncio
import discord
import pyaudio
from utilitaries import *
from async_tkinter_loop import async_mainloop, async_handler


if __name__ == '__main__':

    window = Tk()
    window.config(bg="#0A062E", width=800, height=350)
    window.title("La Platine du turfu")
    window.resizable(0, 0)
    vinylswitch = VinylSwitch(window)
    vinylswitch.place(x=0, y=350, anchor='sw')
    window.update()


    intents = discord.Intents().default()
    client = discord.Client(intents=intents)

    file = open('C:/Users/cedri/OneDrive/NSI/DiscordPy/vinyles.csv', 'r')
    data = file.read()
    file.close()
    vinyles = data.split('\n')

    config = {}
    with open("config.ini", "r") as f:
        for line in f.readlines():
            key, arg = line[:-1].split('=')
            config[key] = int(arg) if arg.isdigit() else arg


    @client.event
    async def on_ready():
        global vc
        vc = None
        print(f'\n----------------------\nLogged in as {client.user}\n----------------------\n\n')
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='des vinyles'))
        connected = False
        for i in [i for i in client.get_all_channels() if i.type == discord.ChannelType.voice]:
            # print(config["user_id"], '\n', i.voice_states.keys())
            if config["owner_id"] in i.voice_states.keys():
                print(f"Connect to {i}")
                #vc = await i.connect()
                connected = True
                print(f"Connected to {i}")
                await play_audio_in_voice()
        if not connected:
            i = client.get_channel(config["default_channel_id"])
            print(f"Connect to {i}")
            vc = await i.connect()
            print(f"Connected to {i}")
            await play_audio_in_voice()
        '''
        #client.loop.create_task(bg_task())
        print('\nFaites votre choix:\n')
        for i in range(len(vinyles)):
            print(f'{i + 1}. {vinyles[i]}')
        print('\nSaisissez le numéro du vinyle: ', end='')'''


    class PyAudioPCM(discord.AudioSource):
        def __init__(self, channels=2, rate=48000, chunk=960, input_device=1) -> None:
            p = pyaudio.PyAudio()
            self.chunks = chunk
            self.input_stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True,
                                       input_device_index=input_device, frames_per_buffer=chunk)

        def read(self) -> bytes:
            return self.input_stream.read(self.chunks)


    async def play_audio_in_voice():
        vc.play(PyAudioPCM(), after=lambda e: print(f'Player error: {e}') if e else None)
        switch = Switch(window, function_on=vc.resume, function_off=vc.pause)
        switch.switch(0)
        switch.place(x=50, y=50)


    @async_handler
    async def client_start():
        try:
            await client.start(config["token"])
        except:
            Label(window, text="Erreur lors de la connexion avec le token\nVérifiez le token et redémarrez", fg="red")\
                .place(x=400, y=175, anchor='c')


    window.after(0, client_start)

    async_mainloop(window)
