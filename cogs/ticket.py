####
#
# Code based on: https://github.com/ifisq/discord-ticket-system
#
# Developed by: g5fighter
#
####

import discord
from discord.ext import commands
import json

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='create_ticket', brief='Creates a ticket message', description='Creates a message in the channel where it is written, which when reacted to by users, creates a chat in the same category')
    @commands.has_permissions(administrator=True)
    async def create_ticket(self, ctx):
        await ctx.message.delete()
        with open("data.json") as f:
            data = json.load(f)

        message = await ctx.send('React to this message with '+data["ticket-emoji"] + ' to open a private chat with the support team')
        data["ticket-react-message-id"] = int(message.id)
        await message.add_reaction(data["ticket-emoji"])
        with open("data.json", 'w') as f:
            json.dump(data, f)

    @commands.command(name='ticket_help', brief='Shows help', description='*ticket_help shows the ticket commands')
    async def ticket_help(self, ctx):
        with open("data.json") as f:
            data = json.load(f)
        
        valid_user = False

        for role_id in data["ticket-support-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if ctx.author.guild_permissions.administrator or valid_user:

            em = discord.Embed(title="Ticket Help", description="", color=0x00a8ff)
            em.add_field(name="create_ticket", value="Creates a message in the channel where it is written, which when reacted to by users, creates a chat in the same category")
            em.add_field(name="close", value="It closes the ticket channel")
            em.add_field(name="addsupport <role_id> <mentionRole=True>", value="Adds a role to the support team. It is added to mention role by defect. (admin-level command).")
            em.add_field(name="delsupport <role_id>", value="Removes role from support team. (admin-level command).")
            em.add_field(name="addmentionrole <role_id>", value="This command adds a role to the list of mentioned roles. (admin-level command).")
            em.add_field(name="delmentionrole <role_id>", value="This command removes a role from the list of mentioned roles. (admin-level command).")
            await ctx.send(embed=em)

    @commands.command(name='close', brief='Close ticket', description='*close closes the ticket channel')
    async def close(self, ctx):
        with open('data.json') as f:
            data = json.load(f)

        if ctx.channel.id in data["ticket-channel-ids"]:
            channel_id = ctx.channel.id
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel and message.content.lower() == "close"
            try:
                em = discord.Embed(title="Closing ticket", description="Are you sure you want to close this ticket? Reply with 'close' if you are sure.", color=0x00a8ff)  
                await ctx.send(embed=em)
                await self.bot.wait_for('message', check=check, timeout=60)
                await ctx.channel.delete()
                index = data["ticket-channel-ids"].index(channel_id)
                del data["ticket-channel-ids"][index]

                with open('data.json', 'w') as f:
                    json.dump(data, f)
            except:
                pass

    @commands.command(name='addsupport', brief='Add support role', description='*addsupport Adds a role to the support team. It is added to mention role by defect. (admin-level command).')
    async def addsupport(self, ctx, role_id=None, mentionRole = "true"):
        with open('data.json') as f:
            data = json.load(f)
        
        valid_user = False

        for role_id in data["ticket-support-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if valid_user or ctx.author.guild_permissions.administrator:
            role_id = int(role_id)

            if role_id not in data["ticket-support-roles"]:

                try:
                    role = ctx.guild.get_role(role_id)

                    with open("data.json") as f:
                        data = json.load(f)

                    data["ticket-support-roles"].append(role_id)

                    if str(mentionRole) == "true":
                        data["roles-to-mention"].append(role_id)

                    with open('data.json', 'w') as f:
                        json.dump(data, f)
                    
                    em = discord.Embed(title="Add support", description="You have successfully added `{}` to the support team.".format(role.name), color=0x00a8ff)

                    await ctx.send(embed=em)

                except:
                    em = discord.Embed(title="Add support", description="That isn't a valid role ID. Please try again with a valid role ID.")
                    await ctx.send(embed=em)
            
            else:
                em = discord.Embed(title="Add support", description="That role already has access to tickets!", color=0x00a8ff)
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Add support", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            await ctx.send(embed=em)

    @commands.command(name='delsupport', brief='Delete support role', description='*delsupport Removes role from support team. (admin-level command).')
    async def delsupport(self, ctx, role_id=None):
        with open('data.json') as f:
            data = json.load(f)

        valid_user = False

        for role_id in data["ticket-support-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass

        if valid_user or ctx.author.guild_permissions.administrator:

            try:
                role_id = int(role_id)
                role = ctx.guild.get_role(role_id)

                with open("data.json") as f:
                    data = json.load(f)

                valid_roles = data["ticket-support-roles"]

                if role_id in valid_roles:
                    index = valid_roles.index(role_id)

                    del valid_roles[index]

                    data["ticket-support-roles"] = valid_roles

                    with open('data.json', 'w') as f:
                        json.dump(data, f)

                    em = discord.Embed(title="Delete Support", description="You have successfully removed `{}` from the support team.".format(role.name), color=0x00a8ff)

                    await ctx.send(embed=em)
                
                else:
                    
                    em = discord.Embed(title="Delete Support", description="That role already doesn't have access to tickets!", color=0x00a8ff)
                    await ctx.send(embed=em)

            except:
                em = discord.Embed(title="Delete Support", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)

        else:
            em = discord.Embed(title="Delete Support", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            await ctx.send(embed=em)

    @commands.command(name='addmentionrole', brief='Add mentionable role', description='*addmentionrole This command adds a role to the list of mentioned roles. (admin-level command).')
    async def addmentionrole(self, ctx, role_id=None):

        with open('data.json') as f:
            data = json.load(f)
        
        valid_user = False

        for role_id in data["ticket-support-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if valid_user or ctx.author.guild_permissions.administrator:

            role_id = int(role_id)

            if role_id not in data["roles-to-mention"]:

                try:
                    role = ctx.guild.get_role(role_id)

                    with open("data.json") as f:
                        data = json.load(f)

                    data["roles-to-mention"].append(role_id)

                    with open('data.json', 'w') as f:
                        json.dump(data, f)

                    em = discord.Embed(title="Add mention", description="You have successfully added `{}` to the list of mentioned roles.".format(role.name), color=0x00a8ff)

                    await ctx.send(embed=em)

                except:
                    em = discord.Embed(title="Add mention", description="That isn't a valid role ID. Please try again with a valid role ID.")
                    await ctx.send(embed=em)
                
            else:
                em = discord.Embed(title="Add mention", description="That role already receives pings when tickets are created.", color=0x00a8ff)
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Add mention", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            await ctx.send(embed=em)

    @commands.command(name='delmentionrole', brief='Delete mentionable role', description='*delmentionrole This command removes a role from the list of mentioned roles. (admin-level command).')
    async def delmentionrole(self, ctx, role_id=None):

        with open('data.json') as f:
            data = json.load(f)
        
        valid_user = False

        for role_id in data["ticket-support-roles"]:
            try:
                if ctx.guild.get_role(role_id) in ctx.author.roles:
                    valid_user = True
            except:
                pass
        
        if valid_user or ctx.author.guild_permissions.administrator:

            try:
                role_id = int(role_id)
                role = ctx.guild.get_role(role_id)

                with open("data.json") as f:
                    data = json.load(f)

                pinged_roles = data["roles-to-mention"]

                if role_id in pinged_roles:
                    index = pinged_roles.index(role_id)

                    del pinged_roles[index]

                    data["roles-to-mention"] = pinged_roles

                    with open('data.json', 'w') as f:
                        json.dump(data, f)

                    em = discord.Embed(title="Delete mention", description="You have successfully removed `{}` from the list of mentioned roles.".format(role.name), color=0x00a8ff)
                    await ctx.send(embed=em)
                
                else:
                    em = discord.Embed(title="Delete mention", description="That role already isn't getting pinged when new tickets are created!", color=0x00a8ff)
                    await ctx.send(embed=em)

            except:
                em = discord.Embed(title="Delete mention", description="That isn't a valid role ID. Please try again with a valid role ID.")
                await ctx.send(embed=em)
        
        else:
            em = discord.Embed(title="Delete mention", description="Sorry, you don't have permission to run that command.", color=0x00a8ff)
            await ctx.send(embed=em)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        with open("data.json") as f:
            data = json.load(f)
        message_id = payload.message_id
        if message_id == int(data["ticket-react-message-id"]):
            if not data["bot-role"] in [y.name.lower() for y in payload.member.roles]:
                if payload.emoji.name == data["ticket-emoji"]:
                    mes= await payload.member.guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
                    await mes.remove_reaction(payload.emoji, payload.member)
                    ticket_number = int(data["ticket-counter"])
                    ticket_number += 1
                    
                    ticket_channel = await payload.member.guild.create_text_channel("ticket-{}".format(ticket_number), category=payload.member.guild.get_channel(payload.channel_id).category)
                    await ticket_channel.set_permissions(payload.member.guild.get_role(payload.member.guild.id), send_messages=False, read_messages=False)
                    await ticket_channel.set_permissions(payload.member, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

                    for role_id in data["ticket-support-roles"]:
                            role = payload.member.guild.get_role(role_id)

                            await ticket_channel.set_permissions(role, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)

                    em = discord.Embed(title="New ticket from {}#{}".format(payload.member.name, payload.member.discriminator), color=0x00a8ff)
                    em.add_field(name="Don't worry", value="You will get help in a short time")

                    pinged_msg_content = ""

                    if data["roles-to-mention"] != []:

                        for role_id in data["roles-to-mention"]:
                            role = payload.member.guild.get_role(role_id)

                            if role.mentionable:
                                pinged_msg_content += role.mention
                                pinged_msg_content += " "
                    if pinged_msg_content != "":
                        em.add_field(name = "Support team", value = pinged_msg_content)

                    await ticket_channel.send(embed=em)
                    data["ticket-channel-ids"].append(ticket_channel.id)
                    data["ticket-counter"] = int(ticket_number)
                    with open("data.json", 'w') as f:
                        json.dump(data, f)

def setup(bot):
    bot.add_cog(TicketCog(bot))