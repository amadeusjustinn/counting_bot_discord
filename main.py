import discord
from dotenv import load_dotenv
import json
import os
import functions as func


client = discord.Client()


@client.event
async def on_ready():
    print('Logged in')
    return


@client.event
async def on_message(message):
    # Don't check message if written by self
    if message.author == client.user:
        return

    # Access JSON file for counting sentences checked and verified
    filename = os.path.dirname(os.path.realpath(__file__)) + '/data.json'
    with open(filename, "r") as file1:
        data = json.load(file1)
        file1.close()

    # Setting counting channel using tailwhip!set
    if message.content.startswith('tailwhip!set'):
        # This is the setting part
        data["channel"] = message.channel.id

        # Confirmation message
        embed_m = discord.Embed()
        embed_m.add_field(
            name="𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝘀𝗲𝘁 <:mitlogo:923878289427279892>",
            value=f"𝗖𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝘀𝗲𝘁 𝘁𝗼 <#{message.channel.id}>. 𝗚𝗲𝘁 𝗰𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗮𝗻𝗱 𝗵𝗮𝘃𝗲 𝗳𝘂𝗻! <:please:752187454760419511>")
        await message.channel.send(embed=embed_m)

    # Only react to other messages if they are sent in counting channel
    if message.channel.id == data["channel"]:

        emoji_list = ["<a:untourablealbumheart:923876065670234164>",
                      "<a:yellowSparkles:790413445790826507>",
                      "<a:onclejazzheart:923398534802321438>"
                      "<a:youdeservethisheart:923398534714253372>",
                      "<a:daysgobyheart:923778036476809227>"]
        # Unsetting counting channel using tailwhip!set
        if message.content.startswith('tailwhip!unset'):
            # This is the unsetting part
            data["channel"] = 0

            # Confirmation message
            embed_m = discord.Embed()
            embed_m.add_field(
                name="𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝘂𝗻𝘀𝗲𝘁 <a:FrogSkip:826047991462100994>",
                value=f"𝗖𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝗶𝘀 𝗻𝗼 𝗹𝗼𝗻𝗴𝗲𝗿 <#{message.channel.id}>. 𝗨𝘀𝗲 `tailwhip!set` 𝘁𝗼 𝘀𝗲𝘁 𝗮 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝗳𝗼𝗿 𝗰𝗼𝘂𝗻𝘁𝗶𝗻𝗴. <:mitfrog:923878290689753148>")
            await message.channel.send(embed=embed_m)

        elif message.content.startswith('tailwhip!user'):
            user = 0
            msg_arr = message.content.split()
            if len(msg_arr) == 1:
                user = message.author.id
            elif msg_arr[1][:2] == "<@":
                user = msg_arr[1][2:20]
            else:
                return

            count_total = 0
            count_correct = 0
            async for msg in message.channel.history():
                if msg.author.id == user and func.eval_helper(msg.content.split()[0])[1]:
                    count_total += 1
                if any(react1 in msg.reactions for react1 in emoji_list) and any(user.id == client.user.id for user in react2.users() for react2 in msg.reactions):
                    count_correct += 1

            embed_m = discord.Embed()
            embed_m.add_field(
                name=f"𝗖𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝘀𝘁𝗮𝘁𝘀 𝗳𝗼𝗿 <@{user}>",
                value=f"• 𝗧𝗼𝘁𝗮𝗹 𝗰𝗼𝘂𝗻𝘁𝘀: {count_total}\n• 𝗖𝗼𝗿𝗿𝗲𝗰𝘁 𝗰𝗼𝘂𝗻𝘁𝘀: {count_correct}\n• 𝗖𝗼𝘂𝗻𝘁𝗶𝗻𝗴 𝗮𝗰𝗰𝘂𝗿𝗮𝗰𝘆: {count_correct / count_total * 100}%")
            await message.channel.send(embed=embed_m)

        else:
            # Evaluate first string before whitespace
            expression = message.content.split()[0]

            # Disregard if there are letters
            if not any(char.isalpha() for char in expression):
                # Check using evaluate and check for user repeat counting
                result = func.evaluate(expression, data["curr_count"])
                if result[1] and data["last_user"] != message.author.id:
                    emoji = emoji_list[0]
                    data["last_user"] = message.author.id
                    data["curr_count"] = result[0]
                    if data["curr_count"] == 69:
                        emoji = emoji_list[1]
                    if data["curr_count"] == 100:
                        emoji = emoji_list[2]
                    elif data["curr_count"] == 200:
                        emoji = emoji_list[3]
                    elif data["curr_count"] == 420:
                        emoji = emoji_list[4]
                    await message.add_reaction(emoji)
                else:
                    # Reset all data except for counting channel
                    data["curr_count"] = 0
                    data["last_user"] = 0
                    await message.add_reaction("<a:hummingmanheart:923398534785548298>")
                    embed_m = discord.Embed()
                    embed_m.add_field(
                        name="<a:mitexclaimed:923519148967985172> 𝗪𝗿𝗼𝗻𝗴 𝗰𝗼𝘂𝗻𝘁",
                        value=f"𝗢𝗵 𝗻𝗼! 𝗟𝗼𝗼𝗸𝘀 𝗹𝗶𝗸𝗲 <@{message.author.id}> 𝗺𝗲𝘀𝘀𝗲𝗱 𝘂𝗽 𝘁𝗵𝗲 𝘀𝗲𝗾𝘂𝗲𝗻𝗰𝗲.\n𝗧𝗵𝗲 𝗻𝗲𝘅𝘁 𝗻𝘂𝗺𝗯𝗲𝗿 𝗶𝘀 𝟭! <:proulxheart:923818448641986560>")
                    await message.channel.send(embed=embed_m)

    # Update JSON file
    with open(filename, "w") as file2:
        json.dump(data, file2, indent=4)
        file2.close()

    return


# Read secret token
load_dotenv()
client.run(os.getenv('TOKEN'))
