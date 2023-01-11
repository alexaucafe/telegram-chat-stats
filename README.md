# telegram-chat-stats

A simple python script with allows you to get basic Telegram chat statistics in plain text (or any other, because ```Chat.get_group_stats()``` returns ```dict```) by analyzing chat export from Telegram Desktop.
Example:

```
Alex:  100 messages (11 replies, 3 forwarded)
Katya: 93 messages (18 replies, 19 forwarded)
Max:   49 messages (20 replies, 10 forwarded)
```

## Exporting chat

Open any group with Telegram Desktop > ```Group Info``` > three-dot-menu > ```Export chat history```
Change format to ```json```. Other settings won't have any effect

## Usage

Just clone or download this repo and make sure ```main.py``` and ```chat.py``` are in the same folder.
Then simply copy your ```result.json``` to this folder and run ```main.py``` through command line

```python main.py```
