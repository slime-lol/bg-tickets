import os
import time
import discord
import discord.ui
from discord.ext import commands

os.system("pip install -r requirements.txt")

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

class CloseTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close(interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Closing ticket in 5 seconds...")
        await asyncio.sleep(5)
        await interaction.channel.delete()


class SupportTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create a Ticket", style=discord.ButtonStyle.green, custom_id="supportticket")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = discord.utils.get(interaction.guild.text_channels, name=f"ticket-{interaction.user.id}")
        if ticket is not None: await interaction.response.send_message(f"You already have a ticket open at {ticket.mention}!", ephemeral=True)
        else:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
                discord.utils.get(interaction.guild.roles, name="Support Team"): discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True)
            }
            embed = discord.Embed(
                title="Support Ticket",
                description="Please wait for a staff member to answer your ticket.",
                color=0xc8c800
            )
            channel = await discord.utils.get(interaction.guild.categories, name="👋┋Active Tickets").create_text_channel(name=f"ticket-{interaction.user.id}", overwrites=overwrites, reason=f"Ticket for {interaction.user}")
            await channel.send(embed=embed, view=CloseTicketButton())
            await interaction.response.send_message(f"I've opened a ticket here: {channel.mention}", ephemeral=True)

class ModeratorTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Create a Ticket", style=discord.ButtonStyle.green, custom_id="modticket")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = discord.utils.get(interaction.guild.text_channels, name=f"ticket-{interaction.user.id}")
        if ticket is not None: 
            await interaction.response.send_message(f"You already have a ticket open at {ticket.mention}!", ephemeral=True)
        else:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True, embed_links=True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
                discord.utils.get(interaction.guild.roles, name="Moderator Permissions"): discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_messages=True, attach_files=True, embed_links=True)
            }
            embed = discord.Embed(
                title=":ticket: Moderator Ticket",
                description="Please wait for a staff member to answer your ticket.",
                color=0xc8c800
            )
            channel = await discord.utils.get(interaction.guild.categories, name="👋┋Active Tickets").create_text_channel(name=f"ticket-{interaction.user.id}", overwrites=overwrites, reason=f"Ticket for {interaction.user}")
            await channel.send(embed=embed, view=CloseTicketButton())
            await interaction.response.send_message(f"I've opened a ticket here: {channel.mention}", ephemeral=True)

@bot.tree.command()
@commands.has_permissions(administrator=True)
async def ticketing(interaction: discord.Interaction, ticket_type):
    if ticket_type == "support_team":
        embed = discord.Embed(
            title=f":ticket: Support Team Tickets",
            description = "Click the button below to open a ticket!",
            color = 0x00c900
        )
        
        embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/white/ticket-xxl.png")

        embed.add_field(name="Uses for this ticket type:", value="", inline=False)
        embed.add_field(name=None, value=":white_check_mark: To get help with the server.", inline=False)
        embed.add_field(name=None, value=":white_check_mark: Common questions related to the server.", inline=False)

        await interaction.channel.send(embed=embed, view=SupportTicket())
        await interaction.response.send_message("I've sent the ticket launcher!", ephemeral=True)
    elif ticket_type == "moderators":
        embed = discord.Embed(
            title=f":ticket: Moderator Tickets",
            description = "Click the button below to open a moderator ticket!",
            color = 0x0000a5
        )
        embed.set_thumbnail(url="https://www.iconsdb.com/icons/preview/white/ticket-xxl.png")
        embed.add_field(name=":warning: Warning", value="This ticket is only used for moderation actions, please do not open a ticket simply to troll. You will be muted for this troll-like behaviour.", inline=False)
        embed.add_field(name="Uses for this ticket type:", value="", inline=False)
        embed.add_field(name=None, value=":white_check_mark: Reporting users in this server.", inline=False)
        embed.add_field(name=None, value=":white_check_mark: Appeal warnings/mutes.", inline=False)
        await interaction.channel.send(embed=embed, view=ModeratorTicket())
        await interaction.response.send_message("I've sent the ticket launcher!", ephemeral=True)
@bot.event
async def on_ready():
    print("Logged in as ", bot.user)
    await bot.tree.sync()
    bot.add_view(ModeratorTicket())
    bot.add_view(SupportTicket())
    bot.add_view(CloseTicketButton())

bot.run(os.environ["TOKEN"])
