from HookLoader import hook
import json
import urllib.request
from logs.Logger import LogColor

@hook
def account_completed(message: str, settings):
    if settings.config['iftttAppletUrl']:
        sendIFTTT(message, '[PUSH NOTIFICATIONS]', LogColor.GREEN, settings)

@hook
def account_error(account, err, settings):
    if settings.config['iftttAppletUrl']:
        sendIFTTT(str(err), '[ERROR PUSH NOTIFICATIONS]', LogColor.GREEN, settings)

def sendIFTTT(message: str, title: str, color: LogColor, settings):
    data = json.dumps({"value1": str}).encode()
    req = urllib.request.Request(settings.config['iftttAppletUrl'])
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req, data) as opened_req:
        result = opened_req.read().decode()
    settings.logger.log(title, result, color)