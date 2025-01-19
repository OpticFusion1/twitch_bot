import twitchio
from twitchio.ext import commands

class Bot(commands.Bot):

    def __init__(self, bot_token):
        # TODO: Initial Channels
        self.bot_token = bot_token
        super().__init__(prefix='?', initial_channels=['...'], token=bot_token)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def settitle(self, ctx, *, title: str):
        # TODO: See if there's a better way to do this
        user = super().create_user(self.user_id, self.nick)
        channel = super().get_channel(self.nick)
        await user.modify_stream(self.bot_token, title=title)
        await ctx.send(f"The stream's title has been set to {title}")