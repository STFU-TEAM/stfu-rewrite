import disnake


from disnake.ext import commands

from stfubot.globals.variables import GANGCREATIONCOST, GANGURL

# ui
from stfubot.ui.storage.ChooseDonor import ChooseStorage
from stfubot.ui.StandSelect import StandSelectDropdown
from stfubot.ui.confirmation import Confirm
from stfubot.ui.place_holder import PlaceHolder
from stfubot.ui.gang.gang_creation_prompt import GangModal
from stfubot.ui.gang.gang_join_select import GangSelectDropdown

# utils
from stfubot.utils.decorators import database_check, gang_check, gang_rank_check
from stfubot.utils.fight_logic import fight_instance
from stfubot.utils.functions import wait_for, add_to_available_storage, is_url_image

# stfu model
from stfubot.models.bot.stfubot import StfuBot
from stfubot.globals.emojis import CustomEmoji
from stfubot.models.gameobjects.gang import GangRank


class Gangs(commands.Cog):
    def __init__(self, stfubot: StfuBot):
        self.stfubot = stfubot

    # GANG MAIN COMMANDS
    @commands.slash_command(name="gang", description="Gangs related commands")
    @commands.max_concurrency(1, per=commands.BucketType.user, wait=False)
    @database_check()
    async def gang(self, Interaction: disnake.CommandInteraction):
        pass

    @gang.sub_command(name="create", description="Create a new gang")
    async def create(self, Interaction: disnake.CommandInteraction):

        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        entry = f"{GANGCREATIONCOST}{CustomEmoji.COIN}"
        balance = f"{user.coins}{CustomEmoji.COIN}"

        if not user.gang_id is None:
            embed = disnake.Embed(
                title=translation["gang_create"]["1"].format(entry, balance),
                color=disnake.Color.blue(),
            )
            embed.set_image(url=GANGURL)
            await Interaction.send(embed=embed)
            return

        embed = disnake.Embed(
            title=translation["gang_create"]["2"].format(entry, balance),
            color=disnake.Color.blue(),
        )
        embed.set_image(url=GANGURL)
        view = Confirm(Interaction)

        await Interaction.send(embed=embed, view=view)
        await wait_for(view)

        Interaction = view.interaction  # type: ignore

        if not view.value:
            embed = disnake.Embed(
                title=translation["gang_create"]["3"], color=disnake.Color.blue()
            )
            embed.set_image(url=GANGURL)
            await Interaction.response.edit_message(embed=embed, view=PlaceHolder())
            return

        if user.coins < GANGCREATIONCOST:
            amount = f"{GANGCREATIONCOST-user.coins}{CustomEmoji.COIN}"
            embed = disnake.Embed(
                title=translation["gang_create"]["4"].format(amount),
                color=disnake.Color.blue(),
            )
            embed.set_image(url=GANGURL)
            await Interaction.response.edit_message(embed=embed, view=PlaceHolder())
            return

        user.coins -= GANGCREATIONCOST
        modal = GangModal(translation)
        await Interaction.response.send_modal(modal=modal)  # type: ignore
        modal_inter: disnake.ModalInteraction = await self.stfubot.wait_for(
            "modal_submit",
            check=lambda i: i.custom_id == "create_gang"
            and i.author.id == Interaction.author.id,
            timeout=300,
        )

        gang_name = modal_inter.text_values["gang_name"]
        gang_motd = modal_inter.text_values["gang_motd"]
        gang_motto = modal_inter.text_values["gang_motto"]

        user.gang_id = await self.stfubot.database.add_gang(
            user.id, gang_name, gang_motd, gang_motto
        )
        await user.update()

    @gang.sub_command(name="join", description="join a new gang")
    async def join(self, Interaction: disnake.CommandInteraction):

        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        if not user.gang_id is None:
            embed = disnake.Embed(
                title=translation["gang_join"]["1"],
                color=disnake.Color.blue(),
            )
            embed.set_image(url=GANGURL)
            await Interaction.send(embed=embed)
            return

        gangs = [
            await self.stfubot.database.get_gang_info(i) for i in user.gang_invites
        ]

        if len(gangs) == 0:
            embed = disnake.Embed(
                title=translation["gang_join"]["2"],
                color=disnake.Color.blue(),
            )
            embed.set_image(url=GANGURL)
            await Interaction.send(embed=embed)
            return
        embed = disnake.Embed(
            title=translation["gang_join"]["3"],
            color=disnake.Color.blue(),
        )
        view = GangSelectDropdown(Interaction, gangs)
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)

        gang = gangs[view.value]

        embed = disnake.Embed(
            title=translation["gang_join"]["4"].format(gang.name),
            color=disnake.Color.blue(),
        )
        gang.users.append(user.id)
        gang.ranks[user.id] = GangRank.SOLDIER.value
        user.gang_id = gang.id
        user.gang_invites = []

        await gang.update()
        await user.update()

        await Interaction.send(embed=embed)

    @gang_check()
    @gang.sub_command(name="show", description="show your gang info's")
    async def show(self, Interaction: disnake.CommandInteraction):

        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        gang = await self.stfubot.database.get_gang_info(user.gang_id)

        member_names = []
        for member in gang.users:
            name: str = self.stfubot.api.get_user_detail(int(member))["username"]
            member_names.append(name)
        ranks = [GangRank.BOSS, GangRank.CAPOREGIME, GangRank.SOLDIER]

        embed = disnake.Embed(
            title=gang.name, description=gang.motto, color=disnake.Color.blue()
        )
        embed.set_image(url=gang.image_url)
        embed.add_field(
            name="`MOTD`",
            value=gang.motd,
            inline=False,
        )
        embed.add_field(
            name=translation["gang_show"]["1"].format(len(gang.users)),
            value=f"\n           ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
            inline=False,
        )
        for i, u in enumerate(gang.users):
            embed.add_field(
                name=f"`{member_names[i]}`",
                value=f"rank:{ranks[gang.ranks[u]].name}",
                inline=True,
            )

        if len(gang.stands) == 0:
            embed.add_field(
                name=translation["gang_show"]["2"],
                value=f"`None`\n           ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
                inline=False,
            )
        else:
            embed.add_field(
                name=translation["gang_show"]["2"],
                value=f"\n           ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
                inline=False,
            )
            for stand in gang.stands:
                stars = "⭐" * stand.stars + "🌟" * stand.ascension
                embed.add_field(
                    name=f"`｢{stand.name}｣`|`{stars}`",
                    value=f"{translation['gang_show']['3']}`{stand.level}`",
                    inline=True,
                )
        embed.add_field(
            name=translation["profile"]["2"],
            value=f"\n           ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
            inline=False,
        )
        embed.add_field(
            name=translation["gang_show"]["5"],
            value=f"`{gang.vault}`|{CustomEmoji.COIN}\n",
        )
        embed.add_field(
            name=translation["gang_show"]["4"],
            value=f"`{gang.war_elo}`|🏆\n",
        )

        await Interaction.send(embed=embed)

    # STAND GUARD MANAGEMENT
    @gang_rank_check(minimum_rank=GangRank.BOSS)
    @gang.sub_command_group(name="stand")
    async def stand(self, Interaction: disnake.CommandInteraction):
        pass

    @gang_check()
    @stand.sub_command(name="add", description="add a stand to guard your gang")
    async def add(self, Interaction: disnake.CommandInteraction):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author
        gang = await self.stfubot.database.get_gang_info(user.gang_id)

        if gang.stands == 3:
            embed = disnake.Embed(
                title=translation["gang_stand_add"]["1"], color=disnake.Color.blue()
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        if len(user.stand_storage) == 0 and len(user.pstand_storage) == 0:
            embed = disnake.Embed(
                title=translation["error_meesages"]["empty_storages"],
                color=disnake.Color.blue(),
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        storage = user.stand_storage
        premium = False
        if user.is_donator():
            embed = disnake.Embed(
                title=translation["ui"]["1"], color=disnake.Color.blue()
            )
            view = ChooseStorage(Interaction)
            await Interaction.send(embed=embed, view=view)
            await wait_for(view)
            Interaction = view.interaction  # type: ignore
            if not view.value:
                premium = True
                storage = user.pstand_storage

        if len(storage) == 0:
            embed = disnake.Embed(
                title=translation["error_meesages"]["empty_storages"],
                color=disnake.Color.blue(),
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        view = StandSelectDropdown(Interaction, storage)
        embed = disnake.Embed(
            title=translation["gang_stand_add"]["2"], color=disnake.Color.blue()
        )
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)
        stand = storage.pop(view.value)  # type: ignore
        gang.stands.append(stand)

        if premium:
            user.pstand_storage = storage
        else:
            user.stand_storage = storage

        embed = disnake.Embed(
            title=translation["gang_stand_add"]["3"].format(stand.name),
            color=disnake.Color.blue(),
        )
        embed.set_image(url=gang.image_url)
        await user.update()
        await gang.update()
        await Interaction.channel.send(embed=embed)

    @gang_check()
    @stand.sub_command(
        name="remove", description="remove a stand from guarding your guild"
    )
    async def remove(self, Interaction: disnake.ApplicationCommandInteraction):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author
        gang = await self.stfubot.database.get_gang_info(user.gang_id)

        if len(gang.stands) == 0:
            embed = disnake.Embed(
                title=translation["error_meesages"]["empty_storages"],
                color=disnake.Color.blue(),
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        view = StandSelectDropdown(Interaction, gang.stands)
        embed = disnake.Embed(
            title=translation["gang_stand_remove"]["1"], color=disnake.Color.blue()
        )
        await Interaction.send(embed=embed, view=view)
        await wait_for(view)
        stand = gang.stands.pop(view.value)  # type: ignore
        msg = add_to_available_storage(user, stand, skip_main=True)
        if not msg:
            embed = disnake.Embed(
                title=translation["use"]["4"], color=disnake.Color.blue()
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return
        await user.update()
        await gang.update()
        embed = disnake.Embed(
            title=translation["use"]["3"].format(msg), color=disnake.Color.blue()
        )
        embed.set_image(url=gang.image_url)
        await Interaction.send(embed=embed)

    # MEMBER MANAGEMENT
    @gang_check()
    @gang.sub_command_group(name="manage")
    async def manage(self, Interaction: disnake.CommandInteraction):
        pass

    @gang_rank_check(minimum_rank=GangRank.CAPOREGIME)
    @manage.sub_command(name="invite", description="invite someone into your gang")
    async def invite(self, Interaction: disnake.CommandInteraction, user: disnake.User):
        User = user
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author
        user2 = await self.stfubot.database.get_user_info(User.id)
        user2.discord = User

        gang = await self.stfubot.database.get_gang_info(user.gang_id)
        if user2.gang_id != None:
            embed = disnake.Embed(
                title=translation["gang_invite"]["1"], color=disnake.Color.blue()
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        if gang.id in user2.gang_invites:
            embed = disnake.Embed(
                title=translation["gang_invite"]["2"], color=disnake.Color.blue()
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        embed = disnake.Embed(
            title=translation["gang_invite"]["3"].format(user2.discord.name, gang.name),
            color=disnake.Color.blue(),
        )
        embed.set_image(url=gang.image_url)
        user2.gang_invites.append(gang.id)
        await user2.update()
        await Interaction.send(embed=embed)

    @gang_rank_check(minimum_rank=GangRank.CAPOREGIME)
    @manage.sub_command(name="kick", description="Kick someone from your gang")
    async def kick(
        self, Interaction: disnake.CommandInteraction, offender: disnake.User
    ):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author
        user2 = await self.stfubot.database.get_user_info(offender.id)
        user2.discord = offender

        gang = await self.stfubot.database.get_gang_info(user.gang_id)

        if not (user2.id in gang.users):
            embed = disnake.Embed(
                title=translation["gang_kick"]["1"], color=disnake.Color.blue()
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        rank1 = gang.ranks[user.id]
        rank2 = gang.ranks[user2.id]
        if rank1 >= rank2:
            embed = disnake.Embed(
                title=translation["gang_kick"]["2"], color=disnake.Color.blue()
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        user2.gang_id = None
        del gang.ranks[user2.id]
        gang.users.remove(user2.id)

        await gang.update()
        await user2.update()
        embed = disnake.Embed(
            title=translation["gang_kick"]["3"].format(user2.discord.name, gang.name),
            color=disnake.Color.blue(),
        )
        embed.set_image(url=gang.image_url)
        await Interaction.send(embed=embed)

    @gang_rank_check(minimum_rank=GangRank.BOSS)
    @manage.sub_command(name="promote", description="Promote a user of your gang")
    async def promote(
        self, Interaction: disnake.CommandInteraction, member: disnake.User
    ):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        User = member
        user2 = await self.stfubot.database.get_user_info(User.id)
        user2.discord = User
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        gang = await self.stfubot.database.get_gang_info(user.gang_id)

        if not (user2.id in gang.users) or user2.gang_id != None:
            embed = disnake.Embed(
                title=translation["gang_kick"]["1"], color=disnake.Color.blue()
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        rank = gang.ranks[user2.id]
        if rank == GangRank.CAPOREGIME:
            embed = disnake.Embed(
                title=translation["gang_promote"]["1"].format(user2.discord.name),
                color=disnake.Color.blue(),
            )
            embed.set_image(url=gang.image_url)
            view = Confirm(Interaction)
            await Interaction.send(embed=embed, view=view)
            await wait_for(view)
            Interaction = view.interaction  # type: ignore

            if not view.value:
                embed = disnake.Embed(
                    title=translation["gang_promote"]["2"].format(user2.discord.name),
                    color=disnake.Color.blue(),
                )
                embed.set_image(url=gang.image_url)
                await Interaction.send(embed=embed)
                return
            gang.ranks[user2.id], gang.ranks[user.id] = (
                gang.ranks[user.id],
                gang.ranks[user2.id],
            )
            embed = disnake.Embed(
                title=translation["gang_promote"]["3"].format(user2.discord.name),
                color=disnake.Color.blue(),
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        gang.ranks[user2.id] = GangRank.CAPOREGIME.value
        await gang.update()
        embed = disnake.Embed(
            title=translation["gang_promote"]["4"].format(
                user2.discord.name, GangRank.CAPOREGIME.name
            ),
            color=disnake.Color.blue(),
        )
        embed.set_image(url=gang.image_url)
        await Interaction.send(embed=embed)

    @gang_rank_check(minimum_rank=GangRank.BOSS)
    @manage.sub_command(name="demote", description="demote a user of your gang")
    async def demote(
        self, Interaction: disnake.CommandInteraction, member: disnake.User
    ):
        User = member
        translation = await self.stfubot.database.get_interaction_lang(Interaction)

        user2 = await self.stfubot.database.get_user_info(User.id)
        user2.discord = User
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        gang = await self.stfubot.database.get_gang_info(user.gang_id)

        if not (user2.id in gang.users) or user2.gang_id != None:
            embed = disnake.Embed(
                title=translation["gang_kick"]["1"], color=disnake.Color.blue()
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        rank = gang.ranks[user2.id]

        if rank == GangRank.SOLDIER:
            pass

        gang.ranks[user2.id] = GangRank.SOLDIER.value
        await gang.update()
        embed = disnake.Embed(
            title=translation["gang_promote"]["4"].format(
                user2.discord.name, GangRank.CAPOREGIME.value
            ),
            color=disnake.Color.blue(),
        )
        embed.set_image(url=gang.image_url)
        await Interaction.send(embed=embed)

    @gang_rank_check(minimum_rank=GangRank.BOSS)
    @manage.sub_command(name="changeimage", description="change your gang image")
    async def changeimage(self, Interaction: disnake.CommandInteraction, url: str):
        if is_url_image(url) == False:
            embed = disnake.Embed(
                title="URL Error",
                description="Please add a valid URL",
                color=disnake.Colour.red(),
            )
            await Interaction.send(embed=embed)
            return
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        gang = await self.stfubot.database.get_gang_info(user.gang_id)
        gang.image_url = url
        await gang.update()
        embed = disnake.Embed(
            title=translation["gang_changeimage"]["1"], color=disnake.Color.blue()
        )
        embed.set_image(url=url)
        await Interaction.send(embed=embed)

    # VAUT MANAGEMENT
    @gang_check()
    @gang.sub_command_group(name="vault")
    async def vault(self, Interaction: disnake.CommandInteraction):
        pass

    @gang_check()
    @vault.sub_command(name="deposit", description="deposit money into your gang vault")
    async def deposit(self, Interaction: disnake.CommandInteraction, ammount: int):
        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author

        gang = await self.stfubot.database.get_gang_info(user.gang_id)

        if ammount > user.coins:
            embed = disnake.Embed(
                title=translation["error_meesages"]["not_enough_money"],
                color=disnake.Color.blue(),
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        gang.vault += ammount
        user.coins -= ammount

        ammount_str = f"{ammount}{CustomEmoji.COIN}"

        await gang.update()
        await user.update()

        embed = disnake.Embed(
            title=translation["gang_deposit"]["1"].format(ammount_str),
            color=disnake.Color.blue(),
        )
        embed.set_image(url=gang.image_url)
        await Interaction.send(embed=embed)

    @gang_rank_check(minimum_rank=GangRank.BOSS)
    @vault.sub_command(name="pay", description="pay someone in your gang")
    async def pay(
        self,
        Interaction: disnake.CommandInteraction,
        member: disnake.User,
        ammount: int,
    ):

        translation = await self.stfubot.database.get_interaction_lang(Interaction)
        user = await self.stfubot.database.get_user_info(Interaction.author.id)
        user.discord = Interaction.author
        user2 = await self.stfubot.database.get_user_info(member.id)
        user2.discord = member

        gang = await self.stfubot.database.get_gang_info(user.gang_id)

        if ammount > gang.vault:
            embed = disnake.Embed(
                title=translation["error_meesages"]["not_enough_money"],
                color=disnake.Color.blue(),
            )
            embed.set_image(url=gang.image_url)
            await Interaction.send(embed=embed)
            return

        gang.vault -= ammount
        user2.coins += ammount

        ammount_str = f"{ammount}{CustomEmoji.COIN}"

        await gang.update()
        await user2.update()

        embed = disnake.Embed(
            title=translation["gang_pay"]["1"].format(ammount_str, user2.discord.name),
            color=disnake.Color.blue(),
        )
        embed.set_image(url=gang.image_url)
        await Interaction.send(embed=embed)

    """ TODO finish this lol
    # WAR COMMANDS
    @gang_check()
    @gang.sub_command_group(name="war")
    async def war(self, Interaction: disnake.CommandInteraction):
        pass

    @gang_rank_check(minimum_rank=GangRank.BOSS)
    @war.sub_command(name="begin", description="begin looking for a gang war")
    async def begin(self, Interaction: disnake.CommandInteraction):
        pass

    @war.sub_command(name="fight", description="fight in your gang war")
    async def fight(self, Interaction: disnake.CommandInteraction):
        pass

    @war.sub_command(name="result", description="show the result of your last gang war")
    async def result(self, Interaction: disnake.CommandInteraction):
        pass

    # RAID

    @gang.sub_command_group(name="raid")
    async def raid(self, Interaction: disnake.CommandInteraction):
        pass

    @gang_rank_check(minimum_rank=GangRank.BOSS)
    @raid.sub_command(name="start", description="Start a gang raid")
    async def start(self, Interaction: disnake.CommandInteraction):
        pass

    @raid.sub_command(name="participate", description="fight in a gang raid")
    async def participate(self, Interaction: disnake.CommandInteraction):
        pass
    """


def setup(stfubot: StfuBot):
    stfubot.add_cog(Gangs(stfubot))