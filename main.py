from interface import *
import asyncio
import discord
import pyaudio
from utilitaries import *
from async_tkinter_loop import async_mainloop, async_handler
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


@async_handler
async def device_callback(*args):
    config["input_device"] = int(device_choice.get().split(' - ')[0])
    try:
        await play_audio_in_voice(input_device=config["input_device"]-1)
    except Exception as error:
        print("device error : ", error)


@async_handler
async def status_callback(*args):
    try:
        status = status_choice.get()
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status))
    except:
        pass

if __name__ == '__main__':
    config = {}
    with open("config.ini", 'r', encoding='utf8') as f:
        for line in f.readlines():
            key, arg = line[:-1].split('=')
            config[key] = int(arg) if arg.isdigit() else arg

    vinyles_status = []
    with open("vinyles.txt", 'r', encoding='utf8') as f:
        for line in f.readlines():
            vinyles_status.append(line.replace('\n', ''))

    vc = None
    PCM = None

    window = Tk()
    window.config(bg="#0A062E", width=800, height=350)
    window.title("La Platine du turfu")
    window.resizable(0, 0)
    window.iconphoto(False, PhotoImage(file=resource_path('icon/icon.png')))
    vinylswitch = VinylSwitch(window)
    vinylswitch.place(x=0, y=350, anchor='sw')
    window.update()

    status_label = Label(text="Connexion to discord bot...", font=("System", 15), fg="#F5C110", bg="#0A062E")
    status_label.place(x=10, y=30)
    voice_status_label = Label(text="Connected to no voice channel", font=("System", 15), fg="#F5C110", bg="#0A062E")
    voice_status_label.place(x=10, y=60)

    discord_status_label = Label(text="Listening to :", font=("System", 15), fg="#F5C110", bg="#0A062E")
    discord_status_label.place(x=373, y=30)

    status_choice = StringVar(window)
    status_choice.trace('w', status_callback)
    status_menu = OptionMenu(window, variable=status_choice, value=vinyles_status)
    status_menu.config(width=50, font=("System", 15), fg="#0A062E", bg="#F5C110", relief="flat", highlightthickness=0,
                       highlightbackground="#F5C110", indicatoron=0)
    status_menu.place(x=790, y=55, anchor="ne")
    status_choice.set(vinyles_status[0])  # Définir le premier périphérique comme valeur par défaut dans le menu déroulant
    status_menu['menu'].delete(0, 'end')  # Supprimer les anciens éléments du menu déroulant
    for vinyle in vinyles_status:
        status_menu['menu'].add_command(label=vinyle, command=lambda value=vinyle: status_choice.set(value))
    status_menu['menu'].config(font=("System", 15), bg="#0A062E", fg="#DFDBED")

    devices = list_input_devices()
    device_choice = StringVar(window)
    device_choice.trace('w', device_callback)
    device_menu = OptionMenu(window, variable=device_choice, value=devices)
    device_menu.config(width=50, font=("System", 15), fg="#0A062E", bg="#F5C110", relief="flat", highlightthickness=0,
                       highlightbackground="#F5C110", indicatoron=0)
    device_menu.place(x=790, y=340, anchor="se")
    device_choice.set(devices[config["input_device"]-1])  # Définir le premier périphérique comme valeur par défaut dans le menu déroulant
    device_menu['menu'].delete(0, 'end')  # Supprimer les anciens éléments du menu déroulant
    for device in devices:
        device_menu['menu'].add_command(label=device, command=lambda value=device: device_choice.set(value))
    device_menu['menu'].config(font=("System", 15), bg="#0A062E", fg="#DFDBED")

    intents = discord.Intents().default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_voice_state_update(member, before, after):
        if member == client.user:
            if after.channel is None:
                voice_status_label.config(text="Connected to no voice channel")
            else:
                voice_status_label.config(text="Connected to " + after.channel.name)
        elif config["follow_owner"] and member.id == config["owner_id"]:
            if before.channel != after.channel:
                await connect_to_owner()


    @client.event
    async def on_ready():
        global vc
        status_label.config(text="Logged in as " + client.user.name)
        print(f'\n----------------------\nLogged in as {client.user}\n----------------------\n\n')
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=vinyles_status[0]))
        if config["auto_connect"]:
            connected = False
            for i in [i for i in client.get_all_channels() if i.type == discord.ChannelType.voice]:
                if config["owner_id"] in i.voice_states.keys():
                    vc = await i.connect()
                    connected = True
            if not connected:
                i = client.get_channel(config["default_channel_id"])
                vc = await i.connect()
        if not vinylswitch.state:
            vinylswitch.switch()
        if vc:
            await device_callback()


    class PyAudioPCM(discord.AudioSource):
        def __init__(self, channels=2, rate=48000, chunk=960, input_device=1) -> None:
            p = pyaudio.PyAudio()
            self.chunks = chunk
            self.input_stream = p.open(format=pyaudio.paInt16, channels=channels, rate=rate, input=True,
                                       input_device_index=input_device, frames_per_buffer=chunk)

        def read(self) -> bytes:
            return self.input_stream.read(self.chunks)


    async def play_audio_in_voice(input_device=1):
        global PCM
        if not vc:
            return
        if vc.is_playing():
            vc.stop()
        PCM = PyAudioPCM(input_device=input_device)
        discord.opus.load_opus('./libopus-0.64.dll')
        vc.play(PCM, after=lambda e: print(f'Player error: {e}') if e else None)
        vinylswitch.function_on = vc.resume
        vinylswitch.function_off = vc.pause


    @async_handler
    async def client_start():
        try:
            await client.start(config["token"])
        except:
            Label(window, text="Error while logging in with token\nCheck token and restart", fg="red",
                  font=("System", 16)) \
                .place(x=400, y=175, anchor='c')


    @async_handler
    async def connect_to_owner():
        global vc
        for i in [i for i in client.get_all_channels() if i.type == discord.ChannelType.voice]:
            if config["owner_id"] in i.voice_states.keys():
                if vc != None and vc.is_connected():
                    await vc.disconnect()
                vc = await i.connect()
                device_callback()

    button_connect_to_owner = Button(text="Connect to owner's voice channel", font=("System", 15), bg="#F5C110",
                                     fg="#0A062E", relief="flat", command=connect_to_owner)
    button_connect_to_owner.place(x=10, y=90)

    def f_switch_auto_connect(state):
        config["auto_connect"] = state

    switch_auto_connect = Switch(window, text="Auto connect to owner's voice channel on startup",
                                 function_on=lambda: f_switch_auto_connect(1),
                                 function_off=lambda: f_switch_auto_connect(0))
    if config["auto_connect"]: switch_auto_connect.switch()
    switch_auto_connect.place(x=400, y=100)

    def f_switch_follow_owner(state):
        config["follow_owner"] = state

    switch_follow_owner = Switch(window, text="Follow owner if he changes voice channel",
                                 function_on=lambda: f_switch_follow_owner(1),
                                 function_off=lambda: f_switch_follow_owner(0))
    if config["follow_owner"]: switch_follow_owner.switch()
    switch_follow_owner.place(x=400, y=130)

    window.after(0, client_start)

    async_mainloop(window)

    with open("config.ini", 'w') as f:
        for key in config.keys():
            f.write(f"{key}={config[key]}\n")
