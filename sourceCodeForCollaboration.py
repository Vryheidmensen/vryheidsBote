import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import random
import json
import datetime
import asyncio

intents = discord.Intents.all()

client = commands.Bot(command_prefix = '!', intents=intents)

#Feeding a population: Crops feed 100,000 per capita per turn, Meat feeds 160,000 per capita per turn, processed Food feeds 800,000 per capita per turn

grinder = ["bauxite", "bauxite", "bauxite", "bauxite", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "copper", "copper", "copper", "copper", "silver", "silver", "gold"]

rotary = ["bauxite", "bauxite", "bauxite", "copper", "copper", "copper", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "silver", "silver", "silver", "gold"]

feeding = [("crops", 100000), ("meat", 180000), ("fish", 120000), ("seafood", 700000), ("food", 900000), ("pastries", 400000), ("lemonade", 400000)]

materials = ["aluminium", "ammunition", "artillery", "bauxite", "books", "cars", "clothing", "concrete", "copper", "crops", "electronics", "firearms", "fish", "flour", "food", "fuel", "furniture", "glass", "gold", "household plastic", "houses", "iron", "lemonade", "meat", "oil", "ore", "paper", "pastries", "petroleum", "plastic",
             "seafood", "ships", "silver", "sneakers", "steel", "stone", "timber", "tissues", "toys", "wood"]

build_list = [{"Name":"Crop field","alias":["crop_field", "cropfield", "crop_fields", "farm"],"price":[("wood", 8), ("treasury", 6000)],"production":[("crops", 6)], "consumption":[],"description":"A field can be used to cultivate wheat, potato, corn, or cotton. Crops can be used for human feed, animal feed, textile manufacturing, or processing into other products."},
             {"Name":"Fruit field","alias":["fruit_field", "fruitfield", "fruit_fields"],"price":[("wood", 4), ("treasury", 3200)],"production":[("crops", 3)], "consumption":[],"description":"A field can be used to cultivate apples, oranges, or pears. Fruits can be used for human and animal feed."},
             {"Name":"Pasture","alias":["pasture", "pastures", "animal_farm", "animal_pasture"],"price":[("wood", 6), ("treasury", 5000)],"production":[("meat", 4)], "consumption":[("crops", 3)],"description":"A pasture can be used to graze cows, pigs, sheep, or chicken. Animals turn into meat and leather products, which can be used for human feed and textiles. Pastures need a supply of crops to operate."},
             {"Name":"Cattle shed","alias":["cattle_shed", "cattle_sheds", "shed", "sheds", "cattleshed", "cattlesheds"],"price":[("timber", 6), ("iron", 3), ("treasury", 15000)],"production":[("meat", 6)], "consumption":[("crops", 5)],"description":"A cattle shed can be used for raising cattle. Animals turn into meat and leather products, which can be used for human feed and textiles. Cattle sheds need a supply of crops to operate."},
             {"Name":"Flour mill","alias":["flour_mill", "flour_mills", "flourmill", "flourmills"],"price":[("timber", 8), ("iron", 2), ("treasury", 14000)],"production":[("flour", 4)], "consumption":[("crops", 2)],"description":"A flour mill grinds crops into flour. Flour can be processed into pastries. Flour mills need a supply of crops to operate."},
             {"Name":"Milking parlor","alias":["milking_parlor", "milking_parlors"],"price":[("steel", 3), ("concrete", 1), ("timber", 2), ("treasury", 24000)],"production":[("meat", 9)], "consumption":[("crops", 6)],"description":"A milking parlor milks cows into dairy products, which can be used for human feed. Milking parlors need a supply of crops to operate."},
             {"Name":"Slaughterhouse","alias":["slaughterhouse", "slaughterhouses", "slaughterhomes", "slaughter", "slaughters"],"price":[("steel", 6), ("concrete", 3), ("gold", 1), ("treasury", 56000)],"production":[("meat", 36)], "consumption":[("crops", 18)],"description":"A slaughterhouse slaughters animals into meat, which can be used for human feed. Slaughterhouses need a supply of crops to operate."},
             {"Name":"Fishery","alias":["fishery", "fisheries"],"price":[("wood", 3), ("iron", 1), ("treasury", 2000)],"production":[("fish", 1)], "consumption":[],"description":"A fishing harbor catches fish from the water. Fish can be used for human feed."},
             {"Name":"Fish farm","alias":["fish_farm", "fish_farms"],"price":[("timber", 2), ("iron", 3), ("stone", 3), ("treasury", 9000)],"production":[("fish", 4)], "consumption":[],"description":"A fish farm gathers fish in high yields. Fish can be used for human feed."},
             {"Name":"Algae farm","alias":["algae_farm", "algae_farms", "algae"],"price":[("timber", 6), ("stone", 5), ("iron", 4), ("treasury", 21000)],"production":[("fish", 12)], "consumption":[],"description":"An algae farm gathers algae in high yields. Fish can be used for human feed."},
             {"Name":"Seaweed farm","alias":["seaweed_farm", "seaweed_farms", "seaweed"],"price":[("steel", 6), ("concrete", 4), ("treasury", 60000)],"production":[("fish", 25)], "consumption":[],"description":"A seaweed farm gathers seaweed in high yields. Fish can be used for human feed."},
             {"Name":"Tree plantation","alias":["tree_plantation", "tree_plantations", "plantation", "plantations", "lumberjack", "lumberjacks"],"price":[("wood", 12), ("stone", 4), ("iron", 2), ("treasury", 12000)],"production":[("wood", 7)], "consumption":[],"description":"A tree plantation can be used to cultivate alder, beech, or conifer. Wood can be used for construction, or processed into timber."},
             {"Name":"Tree sapling field","alias":["tree_sapling_field", "tree_sapling_fields", "tree_field", "tree_fields", "tree_sapling", "tree_saplings", "sapling", "saplings"],"alias":[("wood", 6), ("stone", 2), ("treasury", 6000)],"production":[("wood", 3)], "consumption":[],"description":"A field can be used to plant tree saplings. Wood can be used for construction, or processed into timber."},
             {"Name":"Sawmill","alias":["sawmill", "sawmills"],"price":[("wood", 10), ("iron", 1), ("treasury", 9000)],"production":[("timber", 4)], "consumption":[("wood", 4)],"description":"A sawmill planes wood into lumber. Planed timber can be used for construction. Sawmills need a supply of wood to operate."},
             {"Name":"Biomass pellet plant","alias":["biomass_pellet_plant", "biomass_pellet_plants", "biomass_plant", "biomass_plants", "pellet_plant", "pellet_plants", "biomass", "pellet", "pellets", "bio"],"price":[("timber", 8), ("steel", 6), ("concrete", 3), ("treasury", 60000)],"production":[("paper", 20)], "consumption":[("wood", 14)],"description":"A biomass pellet plant processes wood into biomass pellets. Paper can be used for printing. Biomass pellet plants need a supply of wood to operate."},
             {"Name":"Engineered wood plant","alias":["engineered_wood_plant", "engineered_wood_plants", "wood_plant", "wood_plants", "engineered", "eng"],"price":[("timber", 6), ("steel", 3), ("concrete", 2), ("treasury", 20000)],"production":[("timber", 10)], "consumption":[("wood", 8)],"description":"An engineered wood plant engineers wood into lumber. Timber can be used for construction. Engineered wood plants need a supply of wood to operate."},
             {"Name":"Pulp mill","alias":["pulp_mill", "pulp_mills", "pulp"],"price":[("timber", 3), ("iron", 1), ("stone", 3), ("treasury",15000)],"production":[("paper", 5)], "consumption":[("wood", 5)],"description":"A pulp mill pulps wood into paper, which can be used for printing. Pulp mills need a supply of wood to operate."},
             {"Name":"Quarry","alias":["quarry", "quarries"],"price":[("wood", 3), ("iron", 1), ("treasury", 5000)],"production":[("stone", 5)], "consumption":[],"description":"A quarry excavates stone for construction."},
             {"Name":"Ore mine","alias":["ore_mine", "ore_mines", "mine", "mines"],"price":[("wood", 4), ("treasury", 6000)],"production":[("ore", 8)], "consumption":[],"description":"An ore mine excavates ore."},
             {"Name":"Ore grinding mill","alias":["ore_grinding_mill", "ore_grinding_mills", "ore_grinder", "grinder", "grinding", "grinding_mill", "grinding_mills", "grinders", "grind"],"price":[("wood", 5), ("iron", 1), ("stone", 3), ("treasury", 10000)],"production":[(random.choice(grinder), 1), (random.choice(grinder), 1), (random.choice(grinder), 1), (random.choice(grinder), 1), (random.choice(grinder), 1)], "consumption":[("ore", 5)],"description":"An ore grinding mill grinds ore into usable metals. Ore grinding mills need a supply of ore to operate."},
             {"Name":"Glass manufacturing plant","alias":["glass_manufacturing_plant", "glass_manufacturing_plants", "glass_manufactory"],"price":[("timber", 6), ("iron", 3), ("stone", 5), ("treasury", 20000)],"production":[("glass", 3)], "consumption":[("ore", 3)],"description":"A glass manufacturing plant manufactures ores into sheets of glass. Glass manufacturing plants need a supply of ore to operate."},
             {"Name":"Rotary kiln plant","alias":["rotary_kiln_plant", "rotary_kiln_plants", "rotary_kiln", "rotary"],"price":[("steel", 5), ("concrete", 3), ("treasury", 60000)],"production":[(random.choice(rotary), 5), (random.choice(rotary), 5), (random.choice(rotary), 5), (random.choice(rotary), 5), (random.choice(rotary), 5), (random.choice(rotary), 5), ], "consumption":[("ore", 27)],"description":"A rotary kiln plant heats ore to form metals. Rotary kiln plants need a supply of ore to operate."},
             {"Name":"Fiberglass plant","alias":["fiberglass_plant", "fiberglass_plants", "fiberglass", "fiber", "fibers", "fib", "fibs"],"price":[("steel", 6), ("concrete", 3), ("treasury", 75000)],"production":[("glass", 12)], "consumption":[("ore", 11)],"description":"A fiberglass plant produces glass. Fiberglass plants need a supply of ore to operate."},
             {"Name":"Oil rig","alias":["oil_rig", "oil_rigs", "rig", "rigs"],"price":[("wood", 25), ("steel", 4), ("treasury", 90000)],"production":[("oil", 6)], "consumption":[],"description":"An oil rig extracts oil from the earth."},
             {"Name":"Oil sludge pyrolysis plant","alias":["oil_sludge_prolysis_plant", "oil_sludge_pyrolysis_plants", "oil_sludge", "sludge", "pyrolysis"],"price":[("steel", 10), ("concrete", 4), ("treasury", 140000)],"production":[("petroleum", 3)], "consumption":[("oil", 3)],"description":"An oil sludge pyrolysis plant refines oil into petroleum. Oil sludge pyrolysis plants need a supply of oil to operate."},
             {"Name":"Petrochemical plant","alias":["petrochemical_plant", "petrochemical_plants", "petrochemical", "petrochemicals", "petro", "petros"],"price":[("steel", 10), ("concrete", 4), ("treasury", 140000)],"production":[("plastic", 3)], "consumption":[("oil", 3)],"description":"A petrochemical plant produces polymers and oilgomers. Plastic can be processed into toys. Petrochemical plants need a supply of oil to operate."},
             {"Name":"Waste oil refining plant","alias":["waste_oil_refining_plant", "waste_oil_refining_plants", "waste_oil_refinery", "waste_oil_refineries", "waste_oil", "waste"],"price":[("steel", 25), ("concrete", 12), ("gold", 2), ("treasury", 400000)],"production":[("petroleum", 7)], "consumption":[("oil", 6)],"description":"A waste oil refining plant produces petroleum. Waste oil refining plants need a supply of oil to operate."},
             {"Name":"Naphtha cracker plant","alias":["naphtha_cracker_plant", "naphtha_cracker_plants", "cracker_plant", "cracker_plants", "cracker", "crackers", "naphtha", "naphthas"],"price":[("steel", 25), ("concrete", 12), ("gold", 2), ("treasury", 400000)],"production":[("plastic", 7)], "consumption":[("oil", 6)],"description":"A naphtha cracker plant produces plastics. Plastic can be processed into toys and household plastic. Naphtha cracker plants need a supply of oil to operate."},
             {"Name":"Seafood factory","alias":["seafood_factory", "seafood_factories"],"price":[("steel", 25), ("concrete", 20), ("timber", 10), ("treasury", 300000)],"production":[("seafood", 15)], "consumption":[("fish", 30), ("plastic", 5)],"description":"A seafood factory processes fish into seafood products for human feed. Seafood factories need supplies of fish and plastic to operate."},
             {"Name":"Furniture factory","alias":["furniture_factory", "furniture_factories"],"price":[("steel", 30), ("concrete", 20), ("timber", 10), ("treasury", 410000)],"production":[("item", 10)], "consumption":[("timber", 16), ("paper", 5)],"description":"A furniture factory manufactures furniture for profit. Furniture factories need supplies of timber and paper to operate."},
             {"Name":"Bakery","alias":["bakery", "bakeries", "baker"],"price":[("steel", 10), ("concrete", 10), ("timber", 15), ("treasury", 380000)],"production":[("pastries", 12)], "consumption":[("meat", 7), ("crops", 5), ("flour", 15)],"description":"A bakery produces pastries for human feed. Bakeries need supply of meat, crops, and flour to operate."},
             {"Name":"Steel plant","alias":["steel_plant", "steel_plants", "steel_factory", "steel_factories", "forgery", "forgeries", "steelworks"],"price":[("stone", 20), ("iron", 15), ("treasury", 60000)],"production":[("steel", 20)], "consumption":[("iron", 15)],"description":"A forgery processes iron into steel and machine parts. Steel plants need a supply of iron to operate."},
             {"Name":"Household plastic factory","alias":["household_plastic_factory", "household_plastic_factories"],"price":[("steel", 20), ("concrete", 10), ("timber", 10), ("treasury", 300000)],"production":[("household plastic", 50)], "consumption":[("petroleum", 2), ("plastic", 15)],"description":"A household plastic factory produces household plastic products for profit. Household plastic factories need supplies of petroleum and plastic to operate."},
             {"Name":"Toy factory","alias":["toy_factory", "toy_factories"],"price":[("steel", 18), ("concrete", 10), ("timber", 10), ("treasury", 360000)],"production":[("toys", 40)], "consumption":[("paper", 5), ("timber", 15), ("plastic", 25)],"description":"A toy factory produces toys to entertain the children whilst making a profit. Toy factories need supplies of paper, timber, and plastic to operate."},
             {"Name":"Printing press","alias":["printing_press", "printing_presses", "book_factory", "book_factories", "printer", "printers", "press"],"price":[("steel", 16), ("concrete", 6), ("timber", 15), ("treasury", 160000)],"production":[("books", 20)], "consumption":[("paper", 30), ("plastic", 5)],"description":"A printing press prints paper into reading material for profit. Printing presses need supplies of paper and plastic to operate."},
             {"Name":"Lemonade factory","alias":["lemonade_factory", "lemonade_factories"],"price":[("steel", 18), ("concrete", 8), ("timber", 10), ("treasury", 340000)],"production":[("lemonade", 30)], "consumption":[("crops", 30), ("plastic", 10)],"description":"A lemonade factory produces refreshing lemonade for human consumption. Lemonade factories need supplies of crops and plastic to operate."},
             {"Name":"Electronics factory","alias":["electronics_factory", "electronics_factories", "foxconn", "foxconns"],"price":[("steel", 20), ("concrete", 8), ("timber", 10), ("copper", 4), ("treasury", 600000)],"production":[("electronics", 10)], "consumption":[("plastic", 9), ("glass", 9), ("copper", 15)],"description":"An electronics factory produces electronics for profit. Electronics factories need supplies of plastic, glass, and copper to operate."},
             {"Name":"Textile mill","alias":["textile_mill", "textile_mills", "clothing_factory", "clothing_factories", "textile", "textiles"],"price":[("iron", 20), ("steel", 4), ("treasury", 125000)],"production":[("clothing", 35)], "consumption":[("meat", 6), ("crops", 10), ("plastic", 8)],"description":"A textile mill produces textile clothing for profit. Textiler mills need supplies of meat, crops, and plastic to operate."},
             {"Name":"Petroleum refinery","alias":["petroleum_refinery", "petroleum_refineries", "refinery", "refineries"],"price":[("steel", 20), ("concrete", 10), ("timber", 12), ("treasury", 240000)],"production":[("fuel", 30)], "consumption":[("plastic", 5), ("petroleum", 25), ("iron", 5)],"description":"A petroleum refinery refines petroleum into fuel. Petroleum refineries need supplies of petroleum, plastic, and iron to operate."},
             {"Name":"Soft paper factory","alias":["soft_paper_factory", "soft_paper_factories", "tissue_factory", "tissue_factories"],"price":[("steel", 20), ("concrete", 10), ("timber", 12), ("treasury", 460000)],"production":[("tissues", 65)], "consumption":[("crops", 8), ("paper", 25), ("petroleum", 25), ("iron", 5)],"description":"A soft paper factory softens paper into tissues and toilet paper. Soft paper factories need supplies of crops, paper, petroleum, and plastic to operate."},
             {"Name":"Car factory","alias":["car_factory", "car_factories", "ford", "fords"],"price":[("steel", 40), ("concrete", 10), ("timber", 10), ("treasury", 1200000)],"production":[("cars", 12)], "consumption":[("meat", 10), ("plastic", 15), ("petroleum", 25), ("iron", 5)],"description":"A car factory manufactures cars and other automobiles for profit. Car factories need supplies of meat, plastic, glass, and iron to operate."},
             {"Name":"Food processing facility","alias":["food_processing_facility", "food_processing_facilities", "food_factory", "food_factories", "food_processor", "food_processors", "food_processing_factory", "food_processing_factories"],"price":[("steel", 15), ("concrete", 10), ("timber", 10), ("treasury", 400000)],"production":[("food", 20)], "consumption":[("crops", 16), ("meat", 20), ("flour", 10), ("paper", 4), ("plastic", 6)],"description":"A food factory manufactures convenience food for human feed. Food factories need supplies of crops, meat, flour, paper, and plastic to operate."},
             {"Name":"Sneaker factory","alias":["sneaker_factory", "sneaker_factories"],"price":[("steel", 15), ("concrete", 10), ("timber", 6), ("treasury", 430000)],"production":[("sneakers", 20)], "consumption":[("crops", 12), ("meat", 1), ("paper", 8), ("petroleum", 10), ("plastic", 15)],"description":"A sneaker factory manufactures shoes for profit. Sneaker factories need supplies of crops, meat, paper, petroleum, and plastic to operate."},
             {"Name":"Modular house factory","alias":["modular_house_factory", "modular_house_factories", "house_factory", "house_factories"],"price":[("steel", 20), ("concrete", 20), ("timber", 20), ("treasury", 1400000)],"production":[("houses", 40)], "consumption":[("timber", 30), ("plastic", 8), ("glass", 10), ("copper", 4), ("stone", 1), ("steel", 5)],"description":"A modular house factory manufactures houses for human residence. Modular house factories need supplies of timber, plastic, glass, copper, stone, and iron to operate."},
             {"Name":"Shipyard","alias":["shipyard", "shipyards"],"price":[("steel", 40), ("copper", 5), ("concrete", 25), ("timber", 20), ("treasury", 4000000)],"production":[("ships", 3)], "consumption":[("timber", 100), ("plastic", 50), ("glass", 30), ("steel", 200)],"description":"A shipyard assembles cruise ships for sea travel. Shipyards need supplies of timber, plastic, glass, and iron to operate."},
             {"Name":"Aluminum factory","alias":["aluminum_factory", "aluminum_factory", "aluminium_factory", "aluminium_factories"],"price":[("steel", 16), ("concrete", 9), ("timber", 10), ("treasury", 140000)],"production":[("aluminium", 20)], "consumption":[("bauxite", 10)],"description":"An aluminium factory processes bauxite into aluminium. Aluminium factories need a supply of bauxite to operate."},
             {"Name":"Ammunition factory","alias":["ammunition_factory", "ammunition_factories", "ammo_factory", "ammo_factories"],"price":[("iron", 10), ("stone", 10), ("timber", 5), ("steel", 6), ("treasury", 85000)],"production":[("ammunition", 120)], "consumption":[("steel", 20), ("copper", 1)],"description":"An ammunition factory manufactures ammunition for profit (if personal firearm possession is legal in your country) and for warfare. Ammunition factories need supplies of copper and iron to operate."},
             {"Name":"Artillery factory","alias":["artillery_factory", "artillery_factories"],"price":[("steel", 25), ("concrete", 10), ("treasury", 160000)],"production":[("artillery", 10)], "consumption":[("steel", 20)],"description":"An artillery factory manufactures artillery for warfare. Artillery factories need a supply of steel to operate."},
             {"Name":"Concrete factory","alias":["concrete_factory", "concrete_factories"],"price":[("steel", 10), ("stone", 15), ("treasury", 66000)],"production":[("concrete", 12)], "consumption":[("stone", 10)],"description":"A concrete factory manufactures concrete for infrastructure. Concrete factories need a supply of stone to operate."},
             {"Name":"Firearms factory","alias":["firearms_factory", "firearms_factories", "firearm_factory", "firearm_factories", "small_arms_factory", "small_arms_factories"],"price":[("stone", 15), ("steel", 6), ("timber", 10), ("treasury", 120000)],"production":[("firearms", 36)], "consumption":[("timber", 6), ("steel", 20)],"description":"A firearms factory manufactures firearms for profit (if personal firearm possession is legal in your country) and for warfare. Firearms factories need supplies of timber and steel to operate."},
             {"Name":"Market","alias":["market", "markets"],"price":[("wood", 12), ("stone", 4), ("treasury", 4000)],"production":[("actions", random.randrange(15,20)), ("treasury", random.randrange(2500,8076))], "consumption":[],"description":"The town market is the hub of economic activity for a small economy."}]

@client.event
async def on_ready():
	print("Logged in!")
	print("---------------------")
	await schedule_update()


@client.command()
async def today(ctx):
    await ctx.send(datetime.datetime.now)

@client.event
async def on_member_join(member):
        if member.guild.system_channel is not None:
                await member.guild.system_channel.send(f'{member.mention} has joined {member.guild.name}.')

@client.event
async def on_member_remove(member):
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(f'{member.name} is a traitor')

@client.event
async def on_voice_state_update(member, before, after):
        channel = client.get_channel(1129194438212726845)
        await channel.send(f'{member.name} has updated voice state in {member.guild.name}')

@client.event
async def on_reaction_add(reaction, user):
        channel = client.get_channel(1129194438212726845)
        await channel.send(f'{user.name} has reacted with {reaction.emoji} in {user.guild.name}')

@client.event
async def on_reaction_remove(reaction, user):
        channel = client.get_channel(1129194438212726845)
        await channel.send(f'{user.name} has unreacted in {user.guild.name}')

@client.event
async def on_thread_create(thread):
        channel = client.get_channel(1129194438212726845)
        await channel.send(f'{thread.name} has been created in {thread.guild.name}')

@client.command()
async def guildinfo(ctx):
    await ctx.send(f'{ctx.guild.name} has {ctx.guild.member_count} members and is owned by {ctx.guild.owner.name}. It was created at {ctx.guild.created_at}. Its AFK channel is {ctx.guild.afk_channel} with an AFK timeout of {ctx.guild.afk_timeout} seconds, and its System channel is {ctx.guild.system_channel}. Its explicit content filter is {ctx.guild.explicit_content_filter}. Its bitrate limit is {ctx.guild.bitrate_limit} and its emoji limit is {ctx.guild.emoji_limit} and its sticker limit is {ctx.guild.sticker_limit} and its filesize limit is {ctx.guild.filesize_limit} bytes. It is {ctx.guild.chunked} that the guild is chunked, and {ctx.guild.large} that it is large. Its default notification settings are {ctx.guild.default_notifications} and its authentication level is {ctx.guild.mfa_level} and its rating is {ctx.guild.nsfw_level}. Its description states: "{ctx.guild.description}".')

@client.command()
async def userinfo(ctx):
    await ctx.send(f'{ctx.author.name} joined this server at {ctx.author.joined_at}.')

@client.command()
async def connect(ctx):
        if (ctx.author.voice):
                voice = await ctx.author.voice.channel.connect()
                await ctx.message.add_reaction('✅')
                await ctx.send("Connected. To play a radio program, send 'start [program number]'. Send `!start` (without succeeding argument) to retrieve a list of available radio programs.")
        else:
                await ctx.send("Consider joining a voice channel first.")

@client.command()
async def disconnect(ctx):
        if (ctx.voice_client):
                await ctx.guild.voice_client.disconnect()
                await ctx.message.add_reaction('✅')
        else:
                await ctx.send("You can't disconnect me if I am not connected!")

@client.command()
async def nowplaying(ctx):
    await ctx.send(f'Now playing {playing_now}.')

@client.command()
async def buildings(ctx):
    board = discord.Embed(title="Building List (Page 1)")
    embed = discord.Embed(title="Building List (Page 2)")
    three = discord.Embed(title="Building List (Page 3)")
    counter = 0
    for building in build_list:
        counter += 1
        if counter < 25:
            board.add_field(name=f'{building["Name"]} (!build {building["alias"]})', value=f'{building["description"]} PRODUCTION: {building["production"]}; CONSUMPTION: {building["consumption"]}')
        elif counter < 43:
            embed.add_field(name=f'{building["Name"]} (!build {building["alias"]})', value=f'{building["description"]} PRODUCTION: {building["production"]}; CONSUMPTION: {building["consumption"]}')
        else:
            three.add_field(name=f'{building["Name"]} (!build {building["alias"]})', value=f'{building["description"]} PRODUCTION: {building["production"]}; CONSUMPTION: {building["consumption"]}')
    await ctx.send(embed=board)
    await ctx.send(embed=embed)
    await ctx.send(embed=three)

@start.error
async def start_error(ctx, error):
    await ctx.send("Command failed. If the bot is not connected to a voice channel, connect it and try again. If you are trying to switch radio programs, please disconnect and reconnect the bot, then try again.")

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()

async def schedule_update():
    while True:
        now = datetime.datetime.now()
        then = now+datetime.timedelta(hours=3)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)
        channel = client.get_channel(1146380714573574224)
        channel2 = client.get_channel(547554609355423755)
        newYear = None
        with open("civchaosyear.json","r") as year:
            newYear = json.load(year)
            newYear["Year"] += 1
        with open("civchaosyear.json","w") as year:
            json.dump(newYear,year)
        await channel.send(f'It is now the year {newYear["Year"]} in Civilized Chaos!')
        nations = await process_nation()
        for nation in nations.values():
            earnings = random.randrange(50,100)
            earnings += nation["actions"] * random.randrange(10,20)
            labor_power = random.randrange(2,5)
            nation["actions"] += labor_power
            to_send = ""
            for building in build_list:
                if building["Name"] in nation:
                    bbtimeout = False
                    for item, consume in building["consumption"]:
                        if bbtimeout == False:
                            checkcon = await process_consumption(nation, building["Name"], item, consume)
                            if checkcon[0] == False:
                                to_send += f'{nation["Name"]}\'s {building["Name"]} has stopped operating due to a shortage of {item} in the nation.\n'
                                bbtimeout = True
                            else:
                                nation[item] -= consume * nation[building["Name"]]
                    if bbtimeout == False:
                        for item2, produce in building["production"]:
                            nation[item2] += produce * nation[building["Name"]]
            feeder = nation["crops"] * 100000 + nation["meat"] * 180000 + nation["fish"] * 120000 + nation["seafood"] * 700000 + nation["food"] * 900000 + nation["pastries"] * 400000 + nation["lemonade"] * 400000
            if feeder >= nation["population"]:
                feast = 0
                while feast < nation["population"]:
                    newfood = random.choice(feeding)
                    if nation[newfood[0]] > 0:
                        feast += newfood[1]
                        nation[newfood[0]] -= 1
                        if newfood[0] == "seafood":
                            earnings += random.randrange(5000, 10000)
                        elif newfood[0] == "food":
                            earnings += random.randrange(6000, 12000)
                        elif newfood[0] == "pastries":
                            earnings += random.randrange(7500, 15000)
                        elif newfood[0] == "lemonade":
                            earnings += random.randrange(8000, 16000)
                nation["population"] += random.randrange(0, int(nation["population"] * 0.04 + 1))
            else:
                starved = int((nation["population"] - feeder) * random.random() + 1)
                nation["population"] -= starved
                to_send += f'{nation["Name"]}\'s population is starving! {starved} of its citizens have died of starvation.\n'
            nation["treasury"] += earnings
            to_send += f'{nation["Name"]} has earned {earnings} money and {labor_power} actions today!\n'
            to_send += f'{nation["Name"]} has {nation["actions"]} actions, of which 10% are used up by its citizens.\n'
            nation["actions"] = int(nation["actions"] * 0.9)
            await channel.send(to_send)
            await channel2.send(to_send)
        with open("civchaos.json","w") as war:
                json.dump(nations,war)

async def process_consumption(nation, building, item, consume):
    if consume * nation[building] > nation[item]:
        return False, item
    else:
        return True, item


@client.command()
async def leaderboard(ctx, arg=None):
    argument = arg.lower()
    if argument == "money":
        board = discord.Embed(title="Civilized Chaos Money Leaderboard", description="Alpha Season", color=0xffcccc)
        nations = await process_nation()
        sorting = sorted(nations.items(), key=lambda item: item[1]["treasury"], reverse=True)
        for nation in sorting:
            board.add_field(name=nation[1]["Name"], value=nation[1]["treasury"], inline=False)
        await ctx.send(embed=board)
    elif argument == "land":
        board = discord.Embed(title="Civilized Chaos Land Leaderboard", description="Pre-Alpha Season", color=0xffcccc)
        nations = await process_nation()
        sorting = sorted(nations.items(), key=lambda item: item[1]["land"], reverse=True)
        for nation in sorting:
            board.add_field(name=nation[1]["Name"], value=nation[1]["land"], inline=False)
        await ctx.send(embed=board)
    else:
        await ctx.send("Enter the leaderboard type and try again.")

@leaderboard.error
async def leaderboard_error(ctx, error):
    await ctx.send(error)

@client.command()
async def raw(ctx):
    nations = await process_nation()
    await ctx.send(nations)
    for nation in nations.values():
        await ctx.send(nation)

@raw.error
async def rawerror(ctx, error):
    await ctx.send(error)

@client.command()
async def chop(ctx, arg=1):
    founded = await nation(ctx.author)
    if founded:
        user = ctx.author
        nations = await process_nation()
        if nations[str(user.id)]["actions"] < arg:
            await ctx.send("Your labor force is exhausted!")
        else:
            nations[str(user.id)]["actions"] -= arg
            await ctx.send(f"You chopped {arg} wood")
            nations[str(user.id)]["wood"] += arg
            await savedata(nations)
    else:
        await ctx.send("You don't have a nation!")

@client.command()
async def dig(ctx, arg=1):
    founded = await nation(ctx.author)
    if founded:
        user = ctx.author
        nations = await process_nation()
        if nations[str(user.id)]["actions"] < arg:
            await ctx.send("Your labor force is exhausted!")
        else:
            nations[str(user.id)]["actions"] -= arg
            await ctx.send(f"You dug up {arg} stone")
            nations[str(user.id)]["stone"] += arg
            await savedata(nations)
    else:
        await ctx.send("You don't have a nation!")

async def check_buildlist(arg):
    for building in build_list:
        for alias in building["alias"]:
            if arg == alias:
                return building
    return False

@client.command()
async def build(ctx, arg=None, quantity=1):
    founded = await nation(ctx.author)
    if founded:
        user = ctx.author
        nations = await process_nation()
        if arg == None:
            await ctx.send("Add the building you want to build and try again. Here are some suggestions: Underscores for spaces, please. Use only 1 alias of the preferred building for the argument.")
        else:
            argument = arg.lower()
            valid_building = await check_buildlist(argument)
            if valid_building == False:
                await ctx.send("Invalid building argument! Refer to !buildings for the building list. Here are some suggestions: Underscores for spaces, please. Use only 1 alias of the preferred building for the argument.")
            else:
                nations = await process_nation()
                for item, price in valid_building["price"]:
                    if price * quantity > nations[str(user.id)][item]:
                        await ctx.send(f'You don\'t have enough {item}! {quantity} {valid_building["Name"]} costs {price * quantity} {item} to build.')
                        return
                    else:
                        nations[str(user.id)][item] -= price * quantity
                if valid_building["Name"] in nations[str(user.id)]:
                    nations[str(user.id)][valid_building["Name"]] += quantity
                else:
                    nations[str(user.id)][valid_building["Name"]] = quantity
                await ctx.send(f'You have built {quantity} {valid_building["Name"]}')
        await savedata(nations)
    else:
        await ctx.send("You don't have a nation!")

@build.error
async def builderror(ctx, error):
    await ctx.send(error)

@client.command()
async def stats(ctx):
    founded = await nation(ctx.author)
    if founded:
        nations = await process_nation()
        await ctx.send(nations[str(ctx.author.id)])
    else:
        await ctx.send("You don't have a nation!")

@client.command()
async def statistics(ctx):
    await stats(ctx)

@client.command()
async def inventory(ctx):
    founded = await nation(ctx.author)
    if founded:
        nations = await process_nation()
        inv = f"{nations[str(ctx.author.id)]['Name']}'s inventory:\n"
        for material in materials:
            inv += f'{material}: {nations[str(ctx.author.id)][material]}\n'
        await ctx.send(inv)
    else:
        await ctx.send("You don't have a nation!")

@inventory.error
async def inverror(ctx, error):
    await ctx.send(error)

@client.command()
async def rename(ctx, arg=None, arg2=None, arg3=None, arg4=None, arg5=None, arg6=None, arg7=None, arg8=None):
    founded = await nation(ctx.author)
    if founded:
        if arg==None:
            await ctx.send("Provide a new name for your nation and try again.")
        else:
            nations = await process_nation()
            if arg2==None:
                nations[str(ctx.author.id)]["Name"] = arg
            elif arg3==None:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2
            elif arg4==None:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2 + " " + arg3
            elif arg5==None:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2 + " " + arg3 + " " + arg4
            elif arg6==None:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2 + " " + arg3 + " " + arg4 + " " + arg5
            elif arg7==None:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2 + " " + arg3 + " " + arg4 + " " + arg5 + " " + arg6
            elif arg8==None:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2 + " " + arg3 + " " + arg4 + " " + arg5 + " " + arg6 + " " + arg7
            else:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2 + " " + arg3 + " " + arg4 + " " + arg5 + " " + arg6 + " " + arg7 + " " + arg8
            await ctx.send(f"You have renamed your nation to {nations[str(ctx.author.id)]['Name']}.")
            with open("civchaos.json","w") as ww:
                json.dump(nations,ww)
    else:
        await ctx.send("You don't have a nation!")

@client.command()
async def found(ctx, arg=None, arg2=None, arg3=None, arg4=None, arg5=None, arg6=None, arg7=None, arg8=None):
    if arg==None:
        await ctx.send("Please provide a name for your nation and try again.")
    else:
        nations = await process_nation()
        if str(ctx.author.id) in nations:
            await ctx.send("You already have a nation!")
        else:
            nations[str(ctx.author.id)] = {}
            if arg2==None:
                nations[str(ctx.author.id)]["Name"] = arg
            elif arg3==None:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2
            elif arg4==None:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2 + " " + arg3
            elif arg5==None:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2 + " " + arg3 + " " + arg4
            elif arg6==None:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2 + " " + arg3 + " " + arg4 + " " + arg5
            elif arg7==None:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2 + " " + arg3 + " " + arg4 + " " + arg5 + " " + arg6
            elif arg8==None:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2 + " " + arg3 + " " + arg4 + " " + arg5 + " " + arg6 + " " + arg7
            else:
                nations[str(ctx.author.id)]["Name"] = arg + " " + arg2 + " " + arg3 + " " + arg4 + " " + arg5 + " " + arg6 + " " + arg7 + " " + arg8
            nations[str(ctx.author.id)]["treasury"] = random.randrange(50000,100000)
            nations[str(ctx.author.id)]["land"] = 1
            nations[str(ctx.author.id)]["population"] = random.randrange(500000,1000000)
            nations[str(ctx.author.id)]["actions"] = random.randrange(18,25)
            nations[str(ctx.author.id)]["aluminium"] = 0
            nations[str(ctx.author.id)]["ammunition"] = 0
            nations[str(ctx.author.id)]["artillery"] = 0
            nations[str(ctx.author.id)]["bauxite"] = 0
            nations[str(ctx.author.id)]["books"] = 0
            nations[str(ctx.author.id)]["cars"] = 0
            nations[str(ctx.author.id)]["clothing"] = 0
            nations[str(ctx.author.id)]["concrete"] = 0
            nations[str(ctx.author.id)]["copper"] = 0
            nations[str(ctx.author.id)]["crops"] = 200
            nations[str(ctx.author.id)]["electronics"] = 0
            nations[str(ctx.author.id)]["firearms"] = 0
            nations[str(ctx.author.id)]["fish"] = 100
            nations[str(ctx.author.id)]["flour"] = 0
            nations[str(ctx.author.id)]["food"] = 0
            nations[str(ctx.author.id)]["fuel"] = 0
            nations[str(ctx.author.id)]["furniture"] = 0
            nations[str(ctx.author.id)]["glass"] = 0
            nations[str(ctx.author.id)]["gold"] = 0
            nations[str(ctx.author.id)]["household plastic"] = 0
            nations[str(ctx.author.id)]["houses"] = 0
            nations[str(ctx.author.id)]["iron"] = 5
            nations[str(ctx.author.id)]["lemonade"] = 0
            nations[str(ctx.author.id)]["meat"] = 100
            nations[str(ctx.author.id)]["oil"] = 0
            nations[str(ctx.author.id)]["ore"] = 0
            nations[str(ctx.author.id)]["paper"] = 0
            nations[str(ctx.author.id)]["pastries"] = 0
            nations[str(ctx.author.id)]["petroleum"] = 0
            nations[str(ctx.author.id)]["plastic"] = 0
            nations[str(ctx.author.id)]["seafood"] = 0
            nations[str(ctx.author.id)]["ships"] = 0
            nations[str(ctx.author.id)]["silver"] = 0
            nations[str(ctx.author.id)]["sneakers"] = 0
            nations[str(ctx.author.id)]["steel"] = 0
            nations[str(ctx.author.id)]["stone"] = 20
            nations[str(ctx.author.id)]["timber"] = 0
            nations[str(ctx.author.id)]["tissues"] = 0
            nations[str(ctx.author.id)]["toys"] = 0
            nations[str(ctx.author.id)]["wood"] = 12
            await ctx.send(f"{nations[str(ctx.author.id)]['Name']} has been founded")
            with open("civchaos.json","w") as ww:
                json.dump(nations,ww)

@found.error
async def founderror(ctx, error):
    await ctx.send(error)

@client.command()
async def expand(ctx, land=None):
    founded = await nation(ctx.author)
    if founded:
        if land == None:
            await ctx.send("Enter how much land you want and try again.")
        else:
            land = int(land)
            money = await process_purchase(ctx.author)
            if land > money[0]/100:
                await ctx.send("You don't have enough money to expand!")
            elif land<0:
                await ctx.send("You can't sell land!")
            else:
                await process_purchase(ctx.author,-100*land)
                await process_purchase(ctx.author,land,"land")
                await ctx.send(f'You bought {land} land!')
    else:
        await ctx.send("You don't have a nation!")

@expand.error
async def experror(ctx, error):
    await ctx.send(error)

async def savedata(data):
    with open("civchaos.json","w") as datafile:
        json.dump(data,datafile)

async def process_purchase(player,change = 0,mode = "treasury"):
    nations = await process_nation()
    nations[str(player.id)][mode] += change
    with open("civchaos.json","w") as natl:
        json.dump(nations,natl)
    bal = [nations[str(player.id)]["treasury"],nations[str(player.id)]["land"]]
    return bal

async def nation(player):
    nations = await process_nation()
    if str(player.id) in nations:
        return True
    else:
        return False

async def process_nation():
    with open("civchaos.json","r") as ll:
        nations = json.load(ll)
    return nations


# client.run('Bot token')
