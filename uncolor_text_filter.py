import hexchat
import json
from pprint import pprint

__module_name__ = "uncolor_text_filter"
__module_version__ = "0.1.0"
__module_description__ = "Uncolor text based on nick blacklist/whitelist (hexchat addon)"

# Addon parameters.
BLACKLIST_MODE = True # Filter by blacklist or whitelist?
BLACKLIST = set([]) # Nicks to uncolor (only used in blacklist mode).
WHITELIST = set([]) # Nicks to NOT uncolor (only used in whitelist mode).

# Misc. variables.
RECURSIVE_CALL = False # mark to avoid infinite callback loops.

#
# Functions.
#
def params_dict():
    return {
        'mode': "blacklist" if BLACKLIST_MODE else "whitelist",
        'blacklist': list(BLACKLIST),
        'whitelist': list(WHITELIST),
    }

def save_parameters():
    params = params_dict()
    print("Saving parameters:", end=' ')
    pprint(params)
    hexchat.set_pluginpref("uncolor_text_filter", json.dumps(params, sort_keys=True))

def load_parameters():
    try:
        # read params and check types
        params_str = hexchat.get_pluginpref("uncolor_text_filter")
        if params_str is None: raise TypeError("there are no saved parameters for the moment")
        params = json.loads(params_str)
        print("Parameters read:", end=' ')
        pprint(params)
        if not isinstance(params['mode'], str): raise TypeError("mode is not a string")
        if params['mode'] not in ["blacklist", "whitelist"]: raise TypeError("mode is neither 'blacklist' nor 'whitelist'")
        if not isinstance(params['blacklist'], list): raise TypeError("blacklist is not a list")
        if not isinstance(params['whitelist'], list): raise TypeError("whitelist is not a list")
        for i, val in enumerate(params['blacklist']):
            if not isinstance(val, str): raise TypeError(f"blacklist's element (index={i}, value='{val}') is not a string")
        for i, val in enumerate(params['whitelist']):
            if not isinstance(val, str): raise TypeError(f"whitelist's element (index={i}, value='{val}') is not a string")

        # finally update params
        global BLACKLIST_MODE
        global BLACKLIST
        global WHITELIST
        BLACKLIST_MODE = params['mode'] == 'blacklist'
        BLACKLIST = set(params['blacklist'])
        WHITELIST = set(params['whitelist'])
    except json.JSONDecodeError as e:
        print(f"Could not load parameters (bad JSON params): {e}")
        print("WARNING: loaded default (empty) parameters")
    except TypeError as e:
        print(f"Could not load parameters (bad type in JSON params): {e}")
        print("WARNING: loaded default (empty) parameters")
    except KeyError as e:
        print(f"Could not load parameters (missing key in JSON params): {e}")
        print("WARNING: loaded default (empty) parameters")

def add_list(l, candidates):
    really_new = set(candidates) - l
    return (l | really_new, really_new)

def remove_list(l, candidates):
    really_removed = l & set(candidates)
    return (l - really_removed, really_removed)

#
# Commands.
#
def show_parameters(w, we, userdata):
    params = params_dict()
    print("Current parameters:", end=' ')
    pprint(params)
    return hexchat.EAT_ALL

def toggle_mode(w, we, userdata):
    global BLACKLIST_MODE
    BLACKLIST_MODE = not BLACKLIST_MODE
    if BLACKLIST_MODE:
        print("Mode is now BLACKLIST: Messages from blacklisted nicks will be uncolored")
    else:
        print("Mode is now WHITELIST: All messages will be uncolored but those from whitelisted nicks")
    save_parameters()
    return hexchat.EAT_ALL

def blacklist_add(w, we, userdata):
    global BLACKLIST
    BLACKLIST, added = add_list(BLACKLIST, w[1:])
    if len(added) > 0:
        print(f"Added nicks to blacklist: {list(added)}")
        save_parameters()
    return hexchat.EAT_ALL

def whitelist_add(w, we, userdata):
    global WHITELIST
    WHITELIST, added = add_list(WHITELIST, w[1:])
    if len(added) > 0:
        print(f"Added nicks to whitelist: {list(added)}")
        save_parameters()
    return hexchat.EAT_ALL

def blacklist_remove(w, we, userdata):
    global BLACKLIST
    BLACKLIST, removed = remove_list(BLACKLIST, w[1:])
    if len(removed) > 0:
        print(f"Removed nicks from blacklist: {list(removed)}")
        save_parameters()
    return hexchat.EAT_ALL

def whitelist_remove(w, we, userdata):
    global WHITELIST
    WHITELIST, removed = remove_list(WHITELIST, w[1:])
    if len(removed) > 0:
        print(f"Removed nicks from whitelist: {list(removed)}")
        save_parameters()
    return hexchat.EAT_ALL

def uncolor_text(w, we, event):
    global RECURSIVE_CALL
    if RECURSIVE_CALL:
        return hexchat.EAT_NONE

    if BLACKLIST_MODE:
        if w[0] in BLACKLIST:
            w = [hexchat.strip(x) for x in w]
    else:
        if w[0] not in WHITELIST:
            w = [hexchat.strip(x) for x in w]

    # Print as hexchat usually does via this RECURSIVE_CALL hack.
    RECURSIVE_CALL = True
    hexchat.emit_print(event, *w)
    RECURSIVE_CALL = False
    return hexchat.EAT_ALL

#
# Begin of script.
#

# Setup callback on received messages.
hook_names = ["Channel Message"]
for hook_name in hook_names:
    hexchat.hook_print(hook_name, uncolor_text, hook_name)

# Setup commands.
hexchat.hook_command('uncolor_show_parameters', show_parameters, help="Shows current parameters")
hexchat.hook_command('uncolor_toggle_mode', toggle_mode, help="Toggle blacklist/whitelist mode")
hexchat.hook_command('uncolor_blacklist_add', blacklist_add, help="Add nicks to the blacklist")
hexchat.hook_command('uncolor_blacklist_remove', blacklist_remove, help="Remove nicks from the blacklist")
hexchat.hook_command('uncolor_whitelist_add', whitelist_add, help="Add nicks to the whitelist")
hexchat.hook_command('uncolor_whitelist_remove', whitelist_remove, help="Remove nicks from the whitelist")

# Load existing parameters if any.
load_parameters()
