import discord
from discord.ext import commands, tasks
from itertools import cycle

def get_prefix(client, message):
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
		
	return prefixes(str(message.guild.id))
	
client = commands.Bot(command_prefix = '*')
client.remove_command('help')
status = cycle (['Working for RXNPikachu', 'Made by GREATAK-YT'])


@client.event
async def on_ready():
	change_status.start()
	print("Bot just got online.")
			
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send('Command Not Found!')
	
@tasks.loop(seconds=30)
async def change_status():
	await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def help(ctx):
	embed=discord.Embed(title='Help Command', 
	description='',
	color=discord.Color.orange())
	embed.set_author(name='RXN Official', icon_url=ctx.me.avatar_url)
	embed.set_thumbnail(url=ctx.author.avatar_url)
	
	embed.add_field(name='PREFIX', value='Current Prefix: *', inline=False)
	embed.add_field(name='INFORMATION', value='RXN OFFICIAL Bot made for moderation on discord.py, by GREATAK-YT. This bot is only for RXNPikachu Discord Server.', inline=False)
	embed.add_field(name='COMMANDS', value='`kick`, `ban`, `unban`, `mute`, `unmute`, `addrole`, `removerole`,  `clear`, `lockchannel`, `unlockchannel`, `ping`, `av`.', inline=False)
	embed.set_footer(text=f'Asked by {ctx.author.name}')
	await ctx.send(content=None, embed=embed)

@client.command()
@commands.has_permissions(manage_roles=True, kick_members=True)
async def warn(ctx, user : discord.User, *, reason : str):
	if not reason:
		await ctx.send('Please provide a reason for warn.')
		
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
	await member.kick(reason=reason)
	await ctx.send(f'User was kicked Successfully!')
	
@kick.error
async def kick_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Please mention a user to Kick.')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
	await member.ban(reason=reason)
	await ctx.send(F'User was banned successfully!')
	
@ban.error
async def ban_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Please mention a user to Ban.')
	
@client.command()
async def unban(ctx, *, member):
		banned_users = await ctx.guild.bans()
		member_name, member_discriminator = member.split('#')
		
		for ban_entry in banned_users:
			user = ban_entry.user
			
			if (user.name, user.discriminator) == (member.name, member.discriminator):
				await ctx.guild.unban(user)
				await ctx.send(f'Unbanned User.')
				return
		
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
			await ctx.channel.purge(limit=amount)	
	
@clear.error
async def clear_error(ctx, error):
			if isinstance(error, commands.MissingRequiredArgument):
					await ctx.send('Please specify an amount to delete messages.')
								
@client.command()
async def ping(ctx):
	embed=discord.Embed(title='PONG!',
	description='',
	color=discord.Color.blue())
	embed.set_thumbnail(url = ctx.me.avatar_url)
	
	embed.add_field(name='Ping is:', value=f'{round(client.latency * 1000)}ms', inline=False)
	await ctx.send(content=None, embed=embed)
	
@client.command()
@commands.has_permissions(ban_members=True)
async def mute(ctx, member : discord.Member):
		guild = ctx.guild
		
		for role in guild.roles:
			if role.name == 'Muted':
				await member.add_roles(role)
				await ctx.send('{} has {} has been muted' .format(member.mention, ctx.author.mention))
				return 
				
				overwrite = discord.PermissionsOverwrite(send_messages=False)
				newRole = await guild.create_role(name='Muted')
				
				for channel in guild.text_channels:
					await channel.set_permissions(newrole, overwrite=overwrite)
					
				await member.add_roles(newRole)
				await ctx.send('{} has been muted' .format(member.mention))

@client.command()
@commands.has_permissions(ban_members=True)
async def unmute(ctx, member : discord.Member):
		guild = ctx.guild
		
		for role in guild.roles:
			if role.name == 'Muted':
				await member.remove_roles(role)
				await ctx.send('{} has been unmuted' .format(member.mention))
				return 			

@client.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member:discord.Member = None, *, role:discord.Role = None):
        embed = discord.Embed(title="Remove Role.",
        description=":x: | Specify a member to remove the role.",
        color = discord.Color.red())
        embed.set_author(name = "RXN OFFICIAL", icon_url = ctx.me.avatar_url)
        embed.set_footer(text = f'Asked by : {ctx.author.name}')
        #
        embedd = discord.Embed(title="Remove Role.",
        description=":x: | Type the exact name of the role.",
        color = discord.Color.red())
        embedd.set_author(name = "RXN OFFICIAL", icon_url = ctx.me.avatar_url)
        embedd.set_footer(text = f'Asked by : {ctx.author.name}')
        #
        embedddd = discord.Embed(title="Remove Role.",
        description=f":white_check_mark: | {ctx.author.name} has removed {role} from {member.name}.",
        color = discord.Color.orange())
        embedddd.set_author(name = "RXN OFFICIAL", icon_url = ctx.me.avatar_url)
        embedddd.set_footer(text = f'Asked by : {ctx.author.name}')
        if member == None:
                await ctx.send(content=None,embed=embed)
        if role == None:
                await ctx.send(content=None,embed=embedd)
        await member.remove_roles(role)
        await ctx.send(content=None,embed=embedddd)

@client.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member:discord.Member = None, *, role:discord.Role = None):
        embed = discord.Embed(title="ADD ROLE.",
        description=":x: | Specify a member to add the role.",
        color = discord.Color.red())
        embed.set_author(name = "RXN OFFICIAL", icon_url = ctx.me.avatar_url)
        embed.set_footer(text = f'Asked by : {ctx.author.name}')
        #
        embedd = discord.Embed(title="Add Role.",
        description=":x: | Type the exact name of the role.",
        color = discord.Color.red())
        embedd.set_author(name = "RXN OFFICIAL", icon_url = ctx.me.avatar_url)
        embedd.set_footer(text = f'Asked by : {ctx.author.name}')
        #
        embedddd = discord.Embed(title="Add Role.",
        description=f":white_check_mark: | {ctx.author.name} has given {role} to {member.name}.",
        color = discord.Color.orange())
        embedddd.set_author(name = "RXN OFFICIAL", icon_url = ctx.me.avatar_url)
        embedddd.set_footer(text = f'Asked by : {ctx.author.name}')
        if member == None:
                await ctx.send(content=None,embed=embed)
        if role == None:
                await ctx.send(content=None,embed=embedd)
        await member.add_roles(role)
        await ctx.send(content=None,embed=embedddd)				
												
@client.command()
async def av(ctx, member: discord.Member):
	show_avatar = discord.Embed(title='',
	description='',
	color=discord.Color.orange())
	show_avatar.set_author(name = 'RXN OFFICIAL', icon_url = ctx.me.avatar_url)
	
	show_avatar.add_field(name='Avatar Link', value='[AV LINK]({})'.format(member.avatar_url), inline=False)
    
	show_avatar.set_image(url='{}'.format(member.avatar_url))
	show_avatar.set_footer(text = f'Asked by {ctx.author.name}')
	
	await ctx.send(embed=show_avatar)

@client.command()
@commands.has_permissions(administrator=True)
async def lockchannel(ctx, channel : discord.TextChannel=None):
    embed = discord.Embed(title = 'Channel Lock',
    description = '',
    color = discord.Color.orange())
    embed.add_field(name="Locked.",value=f":white_check_mark: | Channel has been locked.",inline=False)
    embed.set_footer(text = f'Asked by : {ctx.author.name}')
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def unlockchannel(ctx, channel : discord.TextChannel=None):
    embed = discord.Embed(title = 'Channel UnLock',
    description = '',
    color = discord.Color.orange())
    embed.add_field(name="Locked.",value=f":white_check_mark: | Channel has been unlocked.",inline=False)
    embed.set_footer(text = f'Asked by : {ctx.author.name}')
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(embed=embed)

@client.command()
async def testembed(ctx):
	embed=discord.Embed(title='Test embed',
	description='Just testing',
	color=discord.Color.blue())
	embed.set_author(name = 'RXN Official',icon_url = ctx.me.avatar_url)
	embed.set_thumbnail(url = ctx.me.avatar_url)
	
	embed.add_field(name='Test', value='Testing field.', inline=True)
	embed.add_field(name='Test 2', value='Testing field 2', inline=False)
	embed.add_field(name='Test 3', value='Testing field 3', inline=False)
	embed.set_footer(text=f'Asked by {ctx.author.name}')
	await ctx.send(content=None, embed=embed)
	
client.run('NzgyNTU0NTYwNDA4NDUzMTI0.X8N4ug.SqIQQd4BFS1N9kDjx3UPietSzdM')