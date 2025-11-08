import os
import irc.bot
import irc.strings

class TwitchTrainTrackerBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel):
        server = 'irc.chat.twitch.tv'
        port = 6667
        nickname = 'twitchtraintracker'
        token = os.environ['OAUTH_TOKEN']
        
        # Routine to connect to twitchs irc server
        super().__init__([(server, port)], nickname, token)
        self.channel = channel

    def on_welcome(self, connection, event):
        connection.join(self.channel)

    def on_pubmsg(self, connection, event):
        # Respond to messages sent to the bot
        if event.arguments[0].startswith('!hello'):
            connection.privmsg(self.channel, 'Hello, world!')

if __name__ == "__main__":
    channel = os.environ['CHANNEL']
    bot = TTTbot(channel)
    bot.start()
