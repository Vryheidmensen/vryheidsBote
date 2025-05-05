import discord
from discord.ext import commands
import random
import json
import datetime
import asyncio
import validators

intents = discord.Intents.all()

client = commands.Bot(command_prefix = '!', intents=intents)

#Lines 16-195 should be a config file

#Feeding a population, per capita, per turn: Crops feed TBD, Meat feeds TBD, processed Food feeds TBD

grinder = ["bauxite", "bauxite", "bauxite", "bauxite", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "copper", "copper", "copper", "copper", "silver", "silver", "gold"]
rotary = ["bauxite", "bauxite", "bauxite", "copper", "copper", "copper", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "iron", "silver", "silver", "silver", "gold"]

feeding = [("crops", 100000), ("meat", 180000), ("fish", 120000), ("seafood", 700000), ("food", 900000), ("pastries", 400000), ("lemonade", 400000)]

materials = ["aluminium", "ammunition", "artillery", "bauxite", "books", "cars", "clothing", "concrete", "copper", "crops", "electronics", "firearms", "fish", "flour", "food", "fuel", "furniture", "glass", "gold", "household plastic", "houses", "iron", "lemonade", "meat", "oil", "ore", "paper", "pastries", "petroleum", "plastic",
             "seafood", "ships", "silver", "sneakers", "steel", "stone", "timber", "tissues", "toys", "wood"]

build_list = [{"Name":"Grain field",
               "alias":["grain_field", "grainfield", "grain_fields", "farm", "crop_field"],
               "type":"Agriculture",
               "price":[("wood", 12), ("treasury", 6400)],"production":[("grain", 120)], "consumption":[],"workers":400,
               "description":"A field can be used to cultivate wheat, potato, or corn. Crops can be used for human feed, animal fodder, textile manufacturing, or processing into other products."},
              {"Name":"Fruit field",
               "alias":["fruit_field", "fruitfield", "fruit_fields"],
               "type":"Agriculture",
               "price":[("wood", 5), ("treasury", 3200)],"production":[("vegetables", 75)], "consumption":[],
               "description":"A field can be used to cultivate apples, oranges, or pears. Fruits can be used for human feed,"},
              {"Name":"Cotton plantation",
               "alias":["cotton_plantation", "cotton_plantations"],
               "type":"Agriculture",
               "price":[("wood", 7), ("treasury", 5600)],"production":[("cotton", 5)], "consumption":[],
               "description":"A cotton plantation can be used to cultivate cotton. Cotton can be used for textiles."},
              {"Name":"Pasture",
               "alias":["pasture", "pastures", "animal_farm", "animal_pasture"],
               "type":"Agriculture",
               "price":[("wood", 8), ("treasury", 6000)],"production":[("meat", 50), ("hide", 2)], "consumption":[("grain", 60)],
               "description":"A pasture can be used to graze cows, pigs, sheep, or chicken. Animals turn into meat, which can be used for human feed. Pastures need a supply of grain to operate."},
              {"Name":"Cattle shed",
               "alias":["cattle_shed", "cattle_sheds", "shed", "sheds", "cattleshed", "cattlesheds"],
               "type":"Agriculture",
               "price":[("timber", 6), ("iron", 3), ("treasury", 15000)],"production":[("meat", 7), ("hide", 3)], "consumption":[("grain", 12)],
               "description":"A cattle shed can be used for raising cattle. Animals turn into meat and leather products, which can be used for human feed and textiles. Cattle sheds need a supply of crops to operate."},
              {"Name":"Flour mill",
               "alias":["flour_mill", "flour_mills", "flourmill", "flourmills"],
               "type":"Agriculture",
               "price":[("timber", 8), ("iron", 2), ("treasury", 14000)],"production":[("flour", 4)], "consumption":[("crops", 2)],
               "description":"A flour mill grinds crops into flour. Flour can be processed into pastries. Flour mills need a supply of crops to operate."},
              {"Name":"Milking parlor",
               "alias":["milking_parlor", "milking_parlors"],
               "type":"Agriculture",
               "price":[("steel", 3), ("concrete", 1), ("timber", 2), ("treasury", 24000)],"production":[("dairy", 9)], "consumption":[("crops", 6)],
               "description":"A milking parlor milks cows into dairy products, which can be used for human feed. Milking parlors need a supply of crops to operate."},
              {"Name":"Mechanized milking parlor",
               "alias":["milking_parlor", "milking_parlors"],
               "type":"Agriculture",
               "price":[("steel", 3), ("concrete", 1), ("timber", 2), ("treasury", 24000)],"production":[("dairy", 9)], "consumption":[("crops", 6)],
               "description":"A milking parlor milks cows into dairy products, which can be used for human feed. Milking parlors need a supply of crops to operate."},
              {"Name":"Slaughterhouse",
               "alias":["slaughterhouse", "slaughterhouses", "slaughterhomes", "slaughter", "slaughters"],
               "type":"Agriculture",
               "price":[("steel", 6), ("concrete", 3), ("gold", 1), ("treasury", 56000)],"production":[("meat", 36)], "consumption":[("crops", 18)],
               "description":"A slaughterhouse slaughters animals into meat, which can be used for human feed. Slaughterhouses need a supply of crops to operate."},
              {"Name":"Fishery",
               "alias":["fishery", "fisheries"],
               "type":"Agriculture",
               "price":[("wood", 3), ("iron", 1), ("treasury", 2000)],"production":[("fish", 1)], "consumption":[],
               "description":"A fishing harbor catches fish from the water. Fish can be used for human feed."},
              {"Name":"Fish farm",
               "alias":["fish_farm", "fish_farms"],
               "type":"Agriculture",
               "price":[("timber", 2), ("iron", 3), ("stone", 3), ("treasury", 9000)],"production":[("fish", 4)], "consumption":[],
               "description":"A fish farm gathers fish in high yields. Fish can be used for human feed."},
              {"Name":"Algae farm",
               "alias":["algae_farm", "algae_farms", "algae"],
               "type":"Agriculture",
               "price":[("timber", 6), ("stone", 5), ("iron", 4), ("treasury", 21000)],"production":[("fish", 12)], "consumption":[],
               "description":"An algae farm gathers algae in high yields. Fish can be used for human feed."},
              {"Name":"Seaweed farm",
               "alias":["seaweed_farm", "seaweed_farms", "seaweed"],
               "type":"Agriculture",
               "price":[("steel", 6), ("concrete", 4), ("treasury", 60000)],"production":[("fish", 25)], "consumption":[],
               "description":"A seaweed farm gathers seaweed in high yields. Fish can be used for human feed."},
              {"Name":"Tree plantation",
               "alias":["tree_plantation", "tree_plantations", "plantation", "plantations", "lumberjack", "lumberjacks"],
               "type":"Forestry",
               "price":[("wood", 12), ("stone", 4), ("iron", 2), ("treasury", 12000)],"production":[("wood", 9)], "consumption":[],
               "description":"A tree plantation can be used to cultivate alder, beech, or conifer. Wood can be used for construction, or processed into timber."},
              {"Name":"Tree sapling field",
               "alias":["tree_sapling_field", "tree_sapling_fields", "tree_field", "tree_fields", "tree_sapling", "tree_saplings", "sapling", "saplings"],
               "type":"Forestry",
               "price":[("wood", 6), ("stone", 2), ("treasury", 6000)],"production":[("wood", 4)], "consumption":[],"type":"Forestry",
               "description":"A field can be used to plant tree saplings. Wood can be used for construction, or processed into timber."},
              {"Name":"Sawmill",
               "alias":["sawmill", "sawmills"],
               "type":"Forestry",
               "price":[("wood", 10), ("iron", 1), ("treasury", 9000)],"production":[("timber", 4)], "consumption":[("wood", 4)],
               "description":"A sawmill planes wood into lumber. Planed timber can be used for construction. Sawmills need a supply of wood to operate."},
              {"Name":"Biomass pellet plant",
               "alias":["biomass_pellet_plant", "biomass_pellet_plants", "biomass_plant", "biomass_plants", "pellet_plant", "pellet_plants", "biomass", "pellet", "pellets", "bio"],
               "type":"Forestry",
               "price":[("timber", 8), ("steel", 6), ("concrete", 3), ("treasury", 60000)],"production":[("paper", 20)], "consumption":[("wood", 14)],
               "description":"A biomass pellet plant processes wood into biomass pellets. Paper can be used for printing. Biomass pellet plants need a supply of wood to operate."},
              {"Name":"Engineered wood plant",
               "alias":["engineered_wood_plant", "engineered_wood_plants", "wood_plant", "wood_plants", "engineered", "eng"],
               "type":"Forestry",
               "price":[("timber", 6), ("steel", 3), ("concrete", 2), ("treasury", 20000)],"production":[("timber", 10)], "consumption":[("wood", 8)],
               "description":"An engineered wood plant engineers wood into lumber. Timber can be used for construction. Engineered wood plants need a supply of wood to operate."},
              {"Name":"Pulp mill",
               "alias":["pulp_mill", "pulp_mills", "pulp"],
               "type":"Forestry",
               "price":[("timber", 3), ("iron", 1), ("stone", 3), ("treasury",15000)],"production":[("paper", 5)], "consumption":[("wood", 5)],
               "description":"A pulp mill pulps wood into paper, which can be used for printing. Pulp mills need a supply of wood to operate."},
              {"Name":"Quarry",
               "alias":["quarry", "quarries"],
               "type":"Mining",
               "price":[("wood", 3), ("iron", 1), ("treasury", 5000)],"production":[("stone", 5)], "consumption":[],
               "description":"A quarry excavates stone from the earth for construction."},
              {"Name":"Ore mine",
               "alias":["ore_mine", "ore_mines", "mine", "mines"],
               "type":"Mining",
               "price":[("wood", 4), ("treasury", 6000)],"production":[("ore", 8)], "consumption":[],
               "description":"An ore mine excavates ore from Earth's ore deposits."},
              {"Name":"Ore grinding mill",
               "alias":["ore_grinding_mill", "ore_grinding_mills", "ore_grinder", "grinder", "grinding", "grinding_mill", "grinding_mills", "grinders", "grind"],
               "type":"Mining",
               "price":[("wood", 5), ("iron", 1), ("stone", 3), ("treasury", 10000)],"production":[(random.choice(grinder), 1), (random.choice(grinder), 1), (random.choice(grinder), 1), (random.choice(grinder), 1), (random.choice(grinder), 1)], "consumption":[("ore", 5)],
               "description":"An ore grinding mill grinds ore into usable metals. Ore grinding mills need a supply of ore to operate."},
              {"Name":"Glass manufacturing plant",
               "alias":["glass_manufacturing_plant", "glass_manufacturing_plants", "glass_manufactory"],
               "type":"Mining",
               "price":[("timber", 6), ("iron", 3), ("stone", 5), ("treasury", 20000)],"production":[("glass", 3)], "consumption":[("ore", 3)],
               "description":"A glass manufacturing plant manufactures ores into sheets of glass. Glass manufacturing plants need a supply of ore to operate."},
              {"Name":"Rotary kiln plant",
               "alias":["rotary_kiln_plant", "rotary_kiln_plants", "rotary_kiln", "rotary"],
               "type":"Mining",
               "price":[("steel", 5), ("concrete", 3), ("treasury", 60000)],"production":[(random.choice(rotary), 5), (random.choice(rotary), 5), (random.choice(rotary), 5), (random.choice(rotary), 5), (random.choice(rotary), 5), (random.choice(rotary), 5), ], "consumption":[("ore", 27)],
               "description":"A rotary kiln plant heats ore to form metals. Rotary kiln plants need a supply of ore to operate."},
              {"Name":"Fiberglass plant",
               "alias":["fiberglass_plant", "fiberglass_plants", "fiberglass", "fiber", "fibers", "fib", "fibs"],
               "type":"Mining",
               "price":[("steel", 6), ("concrete", 3), ("treasury", 75000)],"production":[("glass", 12)], "consumption":[("ore", 11)],
               "description":"A fiberglass plant produces glass. Fiberglass plants need a supply of ore to operate."},
              {"Name":"Oil rig",
               "alias":["oil_rig", "oil_rigs", "rig", "rigs"],
               "type":"Drilling",
               "price":[("wood", 25), ("steel", 4), ("treasury", 90000)],"production":[("oil", 6)], "consumption":[],
               "description":"An oil rig extracts oil from the earth."},
              {"Name":"Oil sludge pyrolysis plant",
               "alias":["oil_sludge_prolysis_plant", "oil_sludge_pyrolysis_plants", "oil_sludge", "sludge", "pyrolysis"],
               "type":"Drilling",
               "price":[("steel", 10), ("concrete", 4), ("treasury", 140000)],"production":[("petroleum", 3)], "consumption":[("oil", 3)],
               "description":"An oil sludge pyrolysis plant refines oil into petroleum. Oil sludge pyrolysis plants need a supply of oil to operate."},
              {"Name":"Petrochemical plant",
               "alias":["petrochemical_plant", "petrochemical_plants", "petrochemical", "petrochemicals", "petro", "petros"],
               "type":"Drilling",
               "price":[("steel", 10), ("concrete", 4), ("treasury", 140000)],"production":[("plastic", 3)], "consumption":[("oil", 3)],
               "description":"A petrochemical plant produces polymers and oilgomers. Plastic can be processed into toys. Petrochemical plants need a supply of oil to operate."},
              {"Name":"Waste oil refining plant",
               "alias":["waste_oil_refining_plant", "waste_oil_refining_plants", "waste_oil_refinery", "waste_oil_refineries", "waste_oil", "waste"],
               "type":"Drilling",
               "price":[("steel", 25), ("concrete", 12), ("gold", 2), ("treasury", 400000)],"production":[("petroleum", 7)], "consumption":[("oil", 6)],
               "description":"A waste oil refining plant produces petroleum. Waste oil refining plants need a supply of oil to operate."},
              {"Name":"Naphtha cracker plant",
               "alias":["naphtha_cracker_plant", "naphtha_cracker_plants", "cracker_plant", "cracker_plants", "cracker", "crackers", "naphtha", "naphthas"],
               "type":"Drilling",
               "price":[("steel", 25), ("concrete", 12), ("gold", 2), ("treasury", 400000)],"production":[("plastic", 7)], "consumption":[("oil", 6)],
               "description":"A naphtha cracker plant produces plastics. Plastic can be processed into toys and household plastic. Naphtha cracker plants need a supply of oil to operate."},
              {"Name":"Seafood factory",
               "alias":["seafood_factory", "seafood_factories"],
               "type":"Processing",
               "price":[("steel", 25), ("concrete", 20), ("timber", 10), ("treasury", 300000)],"production":[("seafood", 15)], "consumption":[("fish", 30), ("plastic", 5)],
               "description":"A seafood factory processes fish into seafood products for human feed. Seafood factories need supplies of fish and plastic to operate."},
              {"Name":"Furniture factory",
               "alias":["furniture_factory", "furniture_factories"],
               "type":"Processing",
               "price":[("steel", 30), ("concrete", 20), ("timber", 10), ("treasury", 410000)],"production":[("item", 10)], "consumption":[("timber", 16), ("paper", 5)],
               "description":"A furniture factory manufactures furniture for profit. Furniture factories need supplies of timber and paper to operate."},
              {"Name":"Bakery",
               "alias":["bakery", "bakeries", "baker", "bake"],
               "type":"Processing",
               "price":[("steel", 10), ("concrete", 10), ("timber", 15), ("treasury", 380000)],"production":[("pastries", 12)], "consumption":[("meat", 7), ("crops", 5), ("flour", 15)],
               "description":"A bakery produces pastries for human feed. Bakeries need supply of meat, crops, and flour to operate."},
              {"Name":"Steel plant",
               "alias":["steel_plant", "steel_plants", "steel_factory", "steel_factories", "forgery", "forgeries", "steelworks"],
               "type":"Processing",
               "price":[("stone", 20), ("iron", 15), ("treasury", 60000)],"production":[("steel", 20)], "consumption":[("iron", 15)],
               "description":"A forgery processes iron into steel and machine parts. Steel plants need a supply of iron to operate."},
              {"Name":"Household plastic factory",
               "alias":["household_plastic_factory", "household_plastic_factories"],
               "type":"Processing",
               "price":[("steel", 20), ("concrete", 10), ("timber", 10), ("treasury", 300000)],"production":[("household plastic", 50)], "consumption":[("petroleum", 2), ("plastic", 15)],
               "description":"A household plastic factory produces household plastic products for profit. Household plastic factories need supplies of petroleum and plastic to operate."},
              {"Name":"Toy factory",
               "alias":["toy_factory", "toy_factories"],
               "type":"Processing",
               "price":[("steel", 18), ("concrete", 10), ("timber", 10), ("treasury", 360000)],"production":[("toys", 40)], "consumption":[("paper", 5), ("timber", 15), ("plastic", 25)],
               "description":"A toy factory produces toys to entertain the children whilst making a profit. Toy factories need supplies of paper, timber, and plastic to operate."},
              {"Name":"Printing press",
               "alias":["printing_press", "printing_presses", "book_factory", "book_factories", "printer", "printers", "press"],
               "type":"Processing",
               "price":[("steel", 16), ("concrete", 6), ("timber", 15), ("treasury", 160000)],"production":[("books", 20)], "consumption":[("paper", 30), ("plastic", 5)],
               "description":"A printing press prints paper into reading material for profit. Printing presses need supplies of paper and plastic to operate."},
              {"Name":"Lemonade factory",
               "alias":["lemonade_factory", "lemonade_factories"],
               "type":"Processing",
               "price":[("steel", 18), ("concrete", 8), ("timber", 10), ("treasury", 340000)],"production":[("lemonade", 30)], "consumption":[("crops", 30), ("plastic", 10)],
               "description":"A lemonade factory produces refreshing lemonade for human consumption. Lemonade factories need supplies of crops and plastic to operate."},
              {"Name":"Electronics factory",
               "alias":["electronics_factory", "electronics_factories", "foxconn", "foxconns"],
               "type":"Processing",
               "price":[("steel", 20), ("concrete", 8), ("timber", 10), ("copper", 4), ("treasury", 600000)],"production":[("electronics", 10)], "consumption":[("plastic", 9), ("glass", 9), ("copper", 15)],
               "description":"An electronics factory produces electronics for profit. Electronics factories need supplies of plastic, glass, and copper to operate."},
              {"Name":"Textile mill",
               "alias":["textile_mill", "textile_mills", "clothing_factory", "clothing_factories", "textile", "textiles"],
               "type":"Processing",
               "price":[("iron", 20), ("steel", 4), ("treasury", 125000)],"production":[("clothing", 35)], "consumption":[("meat", 6), ("crops", 10), ("plastic", 8)],
               "description":"A textile mill produces textile clothing for profit. Textiler mills need supplies of meat, crops, and plastic to operate."},
              {"Name":"Petroleum refinery",
               "alias":["petroleum_refinery", "petroleum_refineries", "refinery", "refineries"],
               "type":"Processing",
               "price":[("steel", 20), ("concrete", 10), ("timber", 12), ("treasury", 240000)],"production":[("fuel", 30)], "consumption":[("plastic", 5), ("petroleum", 25), ("iron", 5)],
               "description":"A petroleum refinery refines petroleum into fuel. Petroleum refineries need supplies of petroleum, plastic, and iron to operate."},
              {"Name":"Soft paper factory",
               "alias":["soft_paper_factory", "soft_paper_factories", "tissue_factory", "tissue_factories"],
               "type":"Processing",
               "price":[("steel", 20), ("concrete", 10), ("timber", 12), ("treasury", 460000)],"production":[("tissues", 65)], "consumption":[("crops", 8), ("paper", 25), ("petroleum", 25), ("iron", 5)],
               "description":"A soft paper factory softens paper into tissues and toilet paper. Soft paper factories need supplies of crops, paper, petroleum, and plastic to operate."},
              {"Name":"Car factory",
               "alias":["car_factory", "car_factories", "ford", "fords"],
               "type":"Processing",
               "price":[("steel", 40), ("concrete", 10), ("timber", 10), ("treasury", 1200000)],"production":[("cars", 12)], "consumption":[("meat", 10), ("plastic", 15), ("petroleum", 25), ("iron", 5)],
               "description":"A car factory manufactures cars and other automobiles for profit. Car factories need supplies of meat, plastic, glass, and iron to operate."},
              {"Name":"Food processing facility",
               "alias":["food_processing_facility", "food_processing_facilities", "food_factory", "food_factories", "food_processor", "food_processors", "food_processing_factory", "food_processing_factories"],
               "type":"Processing",
               "price":[("steel", 15), ("concrete", 10), ("timber", 10), ("treasury", 400000)],"production":[("food", 20)], "consumption":[("crops", 16), ("meat", 20), ("flour", 10), ("paper", 4), ("plastic", 6)],
               "description":"A food factory manufactures convenience food for human feed. Food factories need supplies of crops, meat, flour, paper, and plastic to operate."},
              {"Name":"Creamery",
               "alias":["milking_parlor", "milking_parlors"],
               "type":"Agriculture",
               "price":[("steel", 3), ("concrete", 1), ("timber", 2), ("treasury", 24000)],"production":[("dairy", 9)], "consumption":[("crops", 6)],
               "description":"A milking parlor milks cows into dairy products, which can be used for human feed. Milking parlors need a supply of crops to operate."},
              {"Name":"Sneaker factory",
               "alias":["sneaker_factory", "sneaker_factories"],
               "type":"Processing",
               "price":[("steel", 15), ("concrete", 10), ("timber", 6), ("treasury", 430000)],"production":[("sneakers", 20)], "consumption":[("crops", 12), ("meat", 1), ("paper", 8), ("petroleum", 10), ("plastic", 15)],
               "description":"A sneaker factory manufactures shoes for profit. Sneaker factories need supplies of crops, meat, paper, petroleum, and plastic to operate."},
              {"Name":"Modular house factory",
               "alias":["modular_house_factory", "modular_house_factories", "house_factory", "house_factories"],
               "type":"Processing",
               "price":[("steel", 20), ("concrete", 20), ("timber", 20), ("treasury", 1400000)],"production":[("houses", 40)], "consumption":[("timber", 30), ("plastic", 8), ("glass", 10), ("copper", 4), ("stone", 1), ("steel", 5)],
               "description":"A modular house factory manufactures houses for human residence. Modular house factories need supplies of timber, plastic, glass, copper, stone, and iron to operate."},
              {"Name":"Shipyard",
               "alias":["shipyard", "shipyards"],
               "type":"Processing",
               "price":[("steel", 40), ("copper", 5), ("concrete", 25), ("timber", 20), ("treasury", 4000000)],"production":[("ships", 3)], "consumption":[("timber", 100), ("plastic", 50), ("glass", 30), ("steel", 200)],
               "description":"A shipyard assembles cruise ships for sea travel. Shipyards need supplies of timber, plastic, glass, and iron to operate."},
              {"Name":"Aluminum factory",
               "alias":["aluminum_factory", "aluminum_factory", "aluminium_factory", "aluminium_factories"],
               "type":"Processing",
               "price":[("steel", 16), ("concrete", 9), ("timber", 10), ("treasury", 140000)],"production":[("aluminium", 20)], "consumption":[("bauxite", 10)],
               "description":"An aluminium factory processes bauxite into aluminium. Aluminium factories need a supply of bauxite to operate."},
              {"Name":"Ammunition factory",
               "alias":["ammunition_factory", "ammunition_factories", "ammo_factory", "ammo_factories"],
               "type":"Processing",
               "price":[("iron", 10), ("stone", 10), ("timber", 5), ("steel", 6), ("treasury", 85000)],"production":[("ammunition", 120)], "consumption":[("steel", 20), ("copper", 1)],
               "description":"An ammunition factory manufactures ammunition for profit (if personal firearm possession is legal in your country) and for warfare. Ammunition factories need supplies of copper and iron to operate."},
              {"Name":"Artillery factory",
               "alias":["artillery_factory", "artillery_factories"],
               "type":"Processing",
               "price":[("steel", 25), ("concrete", 10), ("treasury", 160000)],"production":[("artillery", 10)], "consumption":[("steel", 20)],
               "description":"An artillery factory manufactures artillery for warfare. Artillery factories need a supply of steel to operate."},
              {"Name":"Concrete factory",
               "alias":["concrete_factory", "concrete_factories"],
               "type":"Processing",
               "price":[("steel", 10), ("stone", 15), ("treasury", 66000)],"production":[("concrete", 12)], "consumption":[("stone", 10)],
               "description":"A concrete factory manufactures concrete for infrastructure. Concrete factories need a supply of stone to operate."},
              {"Name":"Firearms factory",
               "alias":["firearms_factory", "firearms_factories", "firearm_factory", "firearm_factories", "small_arms_factory", "small_arms_factories"],
               "type":"Processing",
               "price":[("stone", 15), ("steel", 6), ("timber", 10), ("treasury", 120000)],"production":[("firearms", 36)], "consumption":[("timber", 6), ("steel", 20)],
               "description":"A firearms factory manufactures firearms for profit (if personal firearm possession is legal in your country) and for warfare. Firearms factories need supplies of timber and steel to operate."},
              {"Name":"Market","alias":["market", "markets"],"type":"Commercial",#SCRAP
               "price":[("wood", 12), ("stone", 4), ("treasury", 4000)], "production":[("actions", random.randrange(12,16)), ("treasury", random.randrange(2500,6250))], "consumption":[],
               "description":"The town market is the hub of economic activity for a small economy."},
              {"Name":"Main Street","alias":["main_street", "main_streets", "high_street", "high_streets", "front_street", "front_streets", "broadway", "broadways"],"type":"Commercial",
               "price":[("iron", 2), ("stone", 6), ("wood", 20), ("treasury", 9500)],"production":[("actions", random.randrange(25,32)), ("treasury", random.randrange(8076,12500))], "consumption":[],
               "description":"The Main Street is the economic center of a small town, where business ventures congregate."},
              {"Name":"Industrial Park", "alias":["industrial_park", "industrial_zone", "industrial_zones", "industrial_parks"],"type":"Commercial",
               "price":[("timber", 16), ("concrete", 12), ("steel", 8), ("treasury", 40000)], "production":[("actions", random.randrange(45,70)), ("treasury", random.randrange(16000,25000))], "consumption":[],
               "description":"The industrial park is the modern way to zone factories together."},
              {"Name":"Central Business District", "alias":["central_business_district","city_centre","city_center","downtown","wall_street"],"type":"Commercial",
               "price":[("gold", 4), ("concrete", 20), ("steel", 24), ("copper", 2), ("glass", 6), ("treasury", 120000)], "production":[("actions", random.randrange(120,200)), ("treasury", random.randrange(120000,180000))], "consumption":[("gold", 1)],
               "description":"The Central Business District is the nucleus of the city."}]

@client.event
async def on_ready():
	print("Logged in!")
	print("---------------------")
	await schedule_update()

#Outdated, might as well be removed?
@client.command()
async def buildingsold(ctx):
    board1 = discord.Embed(title="Building List (Page 1)")
    board2 = discord.Embed(title="Building List (Page 2)")
    board3 = discord.Embed(title="Building List (Page 3)")
    counter = 0
    for building in build_list:
        counter += 1
        if counter < 25:
            board1.add_field(name=f'{building["Name"]} (!build {building["alias"]})', value=f'{building["description"]} PRODUCTION: {building["production"]}; CONSUMPTION: {building["consumption"]}')
        elif counter < 43:
            board2.add_field(name=f'{building["Name"]} (!build {building["alias"]})', value=f'{building["description"]} PRODUCTION: {building["production"]}; CONSUMPTION: {building["consumption"]}')
        else:
            board3.add_field(name=f'{building["Name"]} (!build {building["alias"]})', value=f'{building["description"]} PRODUCTION: {building["production"]}; CONSUMPTION: {building["consumption"]}')
    await ctx.send(embed=board1)
    await ctx.send(embed=board2)
    await ctx.send(embed=board3)

@client.command()
async def buildings(ctx, arg=None):
    if arg == None:
        board = discord.Embed(title="Buildings Lists (EXPERIMENTAL)")
        board.add_field(name='!buildings agriculture', value='Buildings specializing in agriculture: The growth of grain, vegetables, livestock, cotton, and fish. Processing into food and textiles.')
        board.add_field(name='!buildings forestry', value='Buildings specializing in forestry: The harvest of trees. Processing into paper and lumber.')
        board.add_field(name='!buildings mining', value='Buildings specializing in mining: The extraction of stone, coal, and ore. Processing into concrete, metals, minerals, and electricity.')
        board.add_field(name='!buildings drilling', value='Buildings specializing in drilling: The extraction of crude oil. Processing into plastic and petroleum.')
        await ctx.send(embed=board)
    elif arg == "agriculture":
        board = discord.Embed(title="Building List: Agriculture")
        for building in build_list:
            if building["type"] == "Agriculture":
                board.add_field(name=f'{building["Name"]} (!build {building["alias"]})', value=f'{building["description"]} PRICE: {building["price"]}; PRODUCTION: {building["production"]}; CONSUMPTION: {building["consumption"]}')
        await ctx.send(embed=board)
    elif arg == "forestry":
        board = discord.Embed(title="Building List: Forestry")
        for building in build_list:
            if building["type"] == "Forestry":
                board.add_field(name=f'{building["Name"]} (!build {building["alias"]})', value=f'{building["description"]} PRICE: {building["price"]}; PRODUCTION: {building["production"]}; CONSUMPTION: {building["consumption"]}')
        await ctx.send(embed=board)
    elif arg == "mining":
        board = discord.Embed(title="Building List: Mining")
        for building in build_list:
            if building["type"] == "Mining":
                board.add_field(name=f'{building["Name"]} (!build {building["alias"]})', value=f'{building["description"]} PRICE: {building["price"]}; PRODUCTION: {building["production"]}; CONSUMPTION: {building["consumption"]}')
        await ctx.send(embed=board)
    elif arg == "drilling":
        board = discord.Embed(title="Building List: Drilling")
        for building in build_list:
            if building["type"] == "Drilling":
                board.add_field(name=f'{building["Name"]} (!build {building["alias"]})', value=f'{building["description"]} PRICE: {building["price"]}; PRODUCTION: {building["production"]}; CONSUMPTION: {building["consumption"]}')
        await ctx.send(embed=board)

async def schedule_update():
    while True:
        now = datetime.datetime.now()
        then = now+datetime.timedelta(hours=3)
        wait_time = (then-now).total_seconds()
        await asyncio.sleep(wait_time)
        channel = client.get_channel(1146380714573574224)
        channel2 = client.get_channel(547554609355423755)
        newYear = None
        with open("civchaosyear.json","r") as gamedata:
            newYear = json.load(gamedata)
            newYear["Year"] += 1
        with open("civchaosyear.json","w") as gamedata:
            json.dump(newYear,gamedata)
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
        with open("civchaos.json","w") as database:
                json.dump(nations,database)

async def process_consumption(nation, building, item, consume):
    if consume * nation[building] > nation[item]:
        return False, item
    else:
        return True, item

@client.command(aliases=["transfer"])
async def give(ctx, material=None, recipient=None, quantity=1):
    founded = await nation(ctx.author)
    if founded:
        user = ctx.author
        if material == None:
            await ctx.send("Choose a material to donate, a nation to donate to, and a quantity to donate. Try again.")
            return
        else:
            arg = material.lower()
            for mat in materials:
                if arg == mat:
                    nations = await process_nation()
                    if nations[str(user.id)][arg] < quantity:
                        await ctx.send(f"You don't have enough {arg} to donate!")
                        return
                    elif recipient == None:
                        await ctx.send(f"Specify a nation to donate your material to and try again.")
                        return
                    elif quantity < 0:
                        await ctx.send("No stealing allowed!")
                        return
                    elif quantity == 0:
                        await ctx.send("You did nothing. Have a nice day.")
                        return
                    else:
                        for rec in nations.values():
                            if recipient.lower() in rec["Name"].lower():
                                rec[arg] += quantity
                                await ctx.send(f"{quantity} {arg} successfully given to **{rec['Name']}**.")
                                nations[str(user.id)][arg] -= quantity
                                await savedata(nations)
                                return
                        await ctx.send("No such nation could be found.")
                        return
            await ctx.send("No such material exists.")
    else:
        await ctx.send("You don't have a nation!")

@client.command()
async def peek(ctx, nation=None):
    nations = await process_nation()
    if nation == None:
        await ctx.send("Provide the name of a nation and try again")
    else:
        for rec in nations.values():
            if nation.lower() in rec["Name"].lower():
                await ctx.send(rec)
                return
        await ctx.send("Nation could not be found")

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

@client.command(aliases=["statistics"])
async def stats(ctx):
    founded = await nation(ctx.author)
    if founded:
        nations = await process_nation()
        board = discord.Embed(title=f"{nations[str(ctx.author.id)]['Common Name']}'s Statistics", description=nations[str(ctx.author.id)])
        board.set_thumbnail(url=nations[str(ctx.author.id)]["Flag"])
        await ctx.send(embed=board)
    else:
        await ctx.send("You don't have a nation!")

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


@client.command(aliases=["customise"])
async def customize(ctx, arg=None):
    founded = await nation(ctx.author)
    if founded:
        nations = await process_nation()
        if arg == 'common_name' or arg == 'nickname' or arg == 'nick' or arg == 'common':
            await ctx.send("Enter a common name for your nation. (Timeout = 5 minutes, send 'Cancel' to cancel.)")
            def check(response):
                return response.author.id == ctx.author.id and response.channel.id == ctx.channel.id
            try:
                common_name = await client.wait_for('message', check=check, timeout=300.0)
            except asyncio.TimeoutError:
                return
            else:
                if common_name.content.lower() == ('cancel'):
                    await ctx.send('Prompt cancelled.')
                    return
                elif validators.url(common_name.content):
                    await ctx.send("You can't set a link as your common name!")
                    return
                else:
                    await ctx.send(f'Common name set to {common_name.content}.')
                    nations[str(ctx.author.id)]["Common Name"] = common_name.content
                    with open("civchaos.json","w") as database:
                        json.dump(nations,database)
        elif arg == 'rename' or arg == 'new_name' or arg == 'name' or arg == 'full_name' or arg == 'official_name':
            await ctx.send("Enter an official name for your nation. (Timeout = 5 minutes, send 'Cancel' to cancel.)")
            def check(response):
                return response.author.id == ctx.author.id and response.channel.id == ctx.channel.id
            try:
                official_name = await client.wait_for('message', check=check, timeout=300.0)
            except asyncio.TimeoutError:
                return
            else:
                if official_name.content.lower() == ('cancel'):
                    await ctx.send('Prompt cancelled.')
                    return
                elif validators.url(official_name.content):
                    await ctx.send("You can't set a link as your official name!")
                    return
                else:
                    await ctx.send(f'Official name set to {official_name.content}.')
                    nations[str(ctx.author.id)]["Name"] = official_name.content
                    with open("civchaos.json","w") as database:
                        json.dump(nations,database)
        elif arg == 'flag' or arg == 'banner':
            await ctx.send("Enter a **URL** for your nation's flag. (Timeout = 5 minutes, send 'Cancel' to cancel.) Please do not upload graphic content or your nation may be deleted.")
            def check(response):
                return response.author.id == ctx.author.id and response.channel.id == ctx.channel.id
            try:
                new_flag = await client.wait_for('message', check=check, timeout=300.0)
            except asyncio.TimeoutError:
                return
            else:
                if new_flag.content.lower() == ('cancel'):
                    await ctx.send('Prompt cancelled.')
                    return
                elif validators.url(new_flag.content):
                    await ctx.send('Flag set.')
                    nations[str(ctx.author.id)]["Flag"] = new_flag.content
                    with open("civchaos.json","w") as database:
                        json.dump(nations,database)
                else:
                    await ctx.send('Not a valid URL!')
                    return
        elif arg == 'motto' or arg == 'slogan':
            await ctx.send("Enter a motto for your nation. (Timeout = 5 minutes, send 'Cancel' to cancel.)")
            def check(response):
                return response.author.id == ctx.author.id and response.channel.id == ctx.channel.id
            try:
                motto = await client.wait_for('message', check=check, timeout=300.0)
            except asyncio.TimeoutError:
                return
            else:
                if motto.content.lower() == ('cancel'):
                    await ctx.send('Prompt cancelled.')
                    return
                elif validators.url(motto.content):
                    await ctx.send("You can't set a link as your motto!")
                    return
                else:
                    await ctx.send(f'Motto set to {motto.content}.')
                    nations[str(ctx.author.id)]["Motto"] = motto.content
                    with open("civchaos.json","w") as database:
                        json.dump(nations,database)
        elif arg == 'demonym':
            await ctx.send("Enter a singular demonym for your nation. (Timeout = 5 minutes, send 'Cancel' to cancel.)")
            def check(response):
                return response.author.id == ctx.author.id and response.channel.id == ctx.channel.id
            try:
                demonym = await client.wait_for('message', check=check, timeout=300.0)
            except asyncio.TimeoutError:
                return
            else:
                if demonym.content.lower() == ('cancel'):
                    await ctx.send('Prompt cancelled.')
                    return
                elif validators.url(demonym.content):
                    await ctx.send("You can't set a link as your singular demonym!")
                    return
                else:
                    await ctx.send(f'Singular demonym set to {demonym.content}.')
                    nations[str(ctx.author.id)]["Demonym"] = demonym.content
                    with open("civchaos.json","w") as database:
                        json.dump(nations,database)
        elif arg == 'demonym_plural' or arg == 'plural':
            await ctx.send("Enter a plural demonym for your nation. (Timeout = 5 minutes, send 'Cancel' to cancel.)")
            def check(response):
                return response.author.id == ctx.author.id and response.channel.id == ctx.channel.id
            try:
                demonym_plural = await client.wait_for('message', check=check, timeout=300.0)
            except asyncio.TimeoutError:
                return
            else:
                if demonym_plural.content.lower() == ('cancel'):
                    await ctx.send('Prompt cancelled.')
                    return
                elif validators.url(demonym_plural.content):
                    await ctx.send("You can't set a link as your plural demonym!")
                    return
                else:
                    await ctx.send(f'Plural demonym set to {demonym_plural.content}.')
                    nations[str(ctx.author.id)]["Plural Demonym"] = demonym_plural.content
                    with open("civchaos.json","w") as database:
                        json.dump(nations,database)
        elif arg == 'demonym_adjective' or arg == 'adjective':
            await ctx.send("Enter an adjective demonym for your nation. (Timeout = 5 minutes, send 'Cancel' to cancel.")
            def check(response):
                return response.author.id == ctx.author.id and response.channel.id == ctx.channel.id
            try:
                demonym_adjective = await client.wait_for('message', check=check, timeout=300.0)
            except asyncio.TimeoutError:
                return
            else:
                if demonym_adjective.content.lower() == ('cancel'):
                    await ctx.send('Prompt cancelled.')
                    return
                elif validators.url(demonym_adjective.content):
                    await ctx.send("You can't set a link as your demonym adjective!")
                    return
                else:
                    await ctx.send(f'Demonym adjective set to {demonym_adjective.content}.')
                    nations[str(ctx.author.id)]["Demonym Adjective"] = demonym_adjective.content
                    with open("civchaos.json","w") as database:
                        json.dump(nations,database)
        elif arg == 'currency' or arg == 'money':
            await ctx.send("Enter a currency name for your nation. (Timeout = 5 minutes, send 'Cancel' to cancel.")
            def check(response):
                return response.author.id == ctx.author.id and response.channel.id == ctx.channel.id
            try:
                currency = await client.wait_for('message', check=check, timeout=300.0)
            except asyncio.TimeoutError:
                return
            else:
                if currency.content.lower() == ('cancel'):
                    await ctx.send('Prompt cancelled.')
                    return
                elif validators.url(currency.content):
                    await ctx.send("You can't set a link as your currency!")
                    return
                else:
                    await ctx.send(f'Currency set to {currency.content}.')
                    nations[str(ctx.author.id)]["Currency"] = currency.content
                    with open("civchaos.json","w") as database:
                        json.dump(nations,database)
        elif arg == 'currency_plural' or arg == 'money_plural':
            await ctx.send("Enter a currency plural name for your nation. (Timeout = 5 minutes, send 'Cancel' to cancel.")
            def check(response):
                return response.author.id == ctx.author.id and response.channel.id == ctx.channel.id
            try:
                currency_plural = await client.wait_for('message', check=check, timeout=300.0)
            except asyncio.TimeoutError:
                return
            else:
                if currency_plural.content.lower() == ('cancel'):
                    await ctx.send('Prompt cancelled.')
                    return
                elif validators.url(currency_plural.content):
                    await ctx.send("You can't set a link as your currency plural!")
                    return
                else:
                    await ctx.send(f'Currency plural set to {currency_plural.content}.')
                    nations[str(ctx.author.id)]["Currency-Plural"] = currency_plural.content
                    with open("civchaos.json","w") as database:
                        json.dump(nations,database)
        else:
            board = discord.Embed(title='Customization Options')
            board.add_field(name='Official Name (!customize rename)', value='Customize the full name of your nation. Example: United States of America')
            board.add_field(name='Common name (!customize common_name)', value='Customize the short name of your nation. Example: America')
            board.add_field(name='Flag (!customize flag)', value='Customize the flag representing your nation.')
            board.add_field(name='Motto (!customize motto)', value='Customize the motto of your nation. Example: From many, one.')
            board.add_field(name='Demonym (!customize demonym)', value='Customize the demonym of your nation.\n"I\'m a proud American!"')
            board.add_field(name='Plural Demonym (!customize demonym_plural)', value='Customize the plural demonym of your nation.\n"Here come the Americans!"')
            board.add_field(name='Adjective Demonym (!customize demonym_adjective)', value='Customize the adjective demonym of your nation.\n"I\'m proud to be American!"')
            board.add_field(name='Currency (!customize currency)', value='Customize your nation\'s currency name. Example: Dollar')
            board.add_field(name='Currency Plural (!customize currency_plural)', value='Customize your nation\'s currency plural name. Example: Dollars')
            await ctx.send(embed=board)
    else:
        await ctx.send("You don't have a nation!")

#WIP Rework of found command
@client.command()
async def foundnew(ctx):
    nations = await process_nation()
    if str(ctx.author.id) in nations:
        await ctx.send("You already have a nation!")
    else:
        nations[str(ctx.author.id)] = {}
        await ctx.send("Welcome to Civilized Chaos! Provide a full name for your nation to get started. (Timeout = 5 minutes, send 'Cancel' to cancel.")
        def check(response):
            return response.author.id == ctx.author.id and response.channel.id == ctx.channel.id
        try:
            name = await client.wait_for('message', check=check, timeout=300.0)
        except asyncio.TimeoutError:
            return
        else:
            if name.content.lower() == ('cancel'):
                await ctx.send('Prompt cancelled.')
                return
            elif validators.url(name.content):
                await ctx.send("You can't set a link as your nation name! Prompt cancelled.")
            else:
                await ctx.send(f'You have founded {name.content}! But you haven\'t, this is an experimental command.')
                return

#Rework this command
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
            with open("civchaos.json","w") as database:
                json.dump(nations,database)

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
    with open("civchaos.json","w") as database:
        json.dump(data,database)

async def process_purchase(player,change = 0,mode = "treasury"):
    nations = await process_nation()
    nations[str(player.id)][mode] += change
    with open("civchaos.json","w") as database:
        json.dump(nations,database)
    bal = [nations[str(player.id)]["treasury"],nations[str(player.id)]["land"]]
    return bal

async def nation(player):
    nations = await process_nation()
    if str(player.id) in nations:
        return True
    else:
        return False

async def process_nation():
    with open("civchaos.json","r") as database:
        nations = json.load(database)
    return nations


# client.run('Bot token')
