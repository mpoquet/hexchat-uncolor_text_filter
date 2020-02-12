uncolor_text_filter
===================

A Hexchat_ addon_ to uncolor text messages based on their authors, either via a blacklist or a whitelist.

- In blacklist mode, colors are preserved in all messages but those coming from blacklisted users.
- In whitelist mode, colors are discarded in all messages but those coming from whitelisted users.

Installation instructions
-------------------------

Just copy ``uncolor_text_filter.py`` in the ``addons`` directory of your `Hexchat configuration folder`_.

Available commands
------------------

- ``/uncolor_toggle_mode`` toggles between blacklist and whitelist mode.
- ``/uncolor_show_parameters`` shows the addon's current parameters.
- ``/uncolor_blacklist_add`` adds nick(s) to the blacklist.
- ``/uncolor_blacklist_remove`` removes nick(s) from the blacklist.
- ``/uncolor_whitelist_add`` adds nick(s) to the whitelist.
- ``/uncolor_whitelist_remove`` removes nick(s) from the whitelist.

.. _Hexchat: https://hexchat.github.io/
.. _addon: https://hexchat.readthedocs.io/en/latest/addons.html
.. _Hexchat configuration folder: https://hexchat.readthedocs.io/en/latest/settings.html#config-files
