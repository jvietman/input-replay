import keyboard, time
from keyboard._keyboard_event import KEY_DOWN, KEY_UP
from tkinter import messagebox

keys = []
hotkeys = {
    "record": ["strg", "1"],
    "play": ["strg", "3"],
    "loop": ["strg", "2"],
    "debugreplay": ["strg", "4"]
}
recorded = []
looprecorded = []

playtime = 3
pause = 0.02
loop = 0
looprecord = False
recording = False

def key_combo(input, combo, order = True):
    if order:
        count = 0
        j = 0
        for i in input:
            if j >= len(combo):
                break
            if i == combo[j]:
                count += 1
                j += 1
        if count == len(combo):
            return True
        else:
            return False

def press_keys(sequence):
    log = []
    keyboard.release("strg")
    for i in sequence:
        if not i[0] in log:
            log.append(i[0])
        
        if i[1] == "down":
            keyboard.press(i[0])
        else:
            keyboard.release(i[0])
        time.sleep(pause)
        
    for i in log:
        keyboard.release(i)

def on_action(event):
    global keys, recording, recorded, loop, looprecord, looprecorded

    key = event.name.lower()

    if event.event_type == KEY_DOWN: # key down
        if key not in keys:
            if recording:
                recorded.append([key, "down"])
            if looprecord:
                looprecorded.append(key)
            
            keys.append(key)

    elif event.event_type == KEY_UP: # key up
        if key in keys:
            if recording:
                recorded.append([key, "up"])
            
            keys.remove(key)
    
    print(keys)

    # check for key combinations
    # record
    if key_combo(keys, hotkeys["record"]):
        if not recording:
            print("recording")
            recording = True
            keys, recorded = [], []
        elif recording:
            print("done")
            print(recorded)
            recorded = recorded[:-2]
            recording = False

    # play
    if key_combo(keys, hotkeys["play"]):
        if recorded:
            print("play")
            if loop > 0:
                print("play "+str(recorded))
                for i in range(loop):
                    print("loop "+str(i))
                    press_keys(recorded)
            else:
                press_keys(recorded)
    
    # loop
    if looprecord and "enter" in keys:
        looprecord = False
        tmp = ""
        for i in looprecorded:
            if i.isnumeric():
                tmp = tmp + str(i)
        loop = int(tmp)
        print("loop set to "+str(loop))

    if key_combo(keys, hotkeys["loop"]):
        print("recording loop")
        looprecord = True
        keys, looprecorded = [], []
    
    # debug (show recorded inputs)
    if key_combo(keys, hotkeys["debugreplay"]):
        print("Recording: \""+str(recorded)+"\"")

keyboard.hook(lambda e: on_action(e))
keyboard.wait()