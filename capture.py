import sys

path=sys.path[0]+"/test captures"

nextIdFile=open(f"{path}/.nextId.txt", mode="r+")

nextId=int(nextIdFile.read())
nextIdFile.truncate(0)
nextIdFile.seek(0)
nextIdFile.write(str(nextId+1))
nextIdFile.close()
print(nextId)


import pyautogui

screenshot = pyautogui.screenshot()

screenshot.save(f"{path}/{nextId}.png")
