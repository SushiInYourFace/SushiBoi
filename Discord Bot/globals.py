#basically acts as a list of global variables
debugmode = False
sendas_guild = None
sendas_chan = None
sendas_content = None
sendas_completed = False
tts_ready = True

#No idea if this is needed
def load():
    global debugmode
    debugmode = False
    global sendas_guild
    sendas_guild = None
    global sendas_chan
    sendas_chan = None
    global sendas_content
    sendas_content = None
    global sendas_completed 
    sendas_completed = False
    global tts_ready
    tts_ready = True

