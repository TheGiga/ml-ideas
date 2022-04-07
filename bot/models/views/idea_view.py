import discord

from config import MODERATING_ROLES


class IdeaView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Принять",
        style=discord.ButtonStyle.green,
        custom_id="idea:approve",
    )
    async def approve(self, button: discord.ui.Button, interaction: discord.Interaction):
        for role in interaction.user.roles:
            if role.id not in MODERATING_ROLES:
                continue
            else:
                await interaction.message.edit(
                    content='**Принята.**',
                    embed=interaction.message.embeds[0].copy(),
                    view=None
                )

                return await interaction.response.send_message(ephemeral=True, content='Успешно!')

        await interaction.response.send_message(ephemeral=True, content='Недостаточно прав.')

    @discord.ui.button(
        label="Отклонить",
        style=discord.ButtonStyle.red,
        custom_id="idea:decline",
    )
    async def decline(self, button: discord.ui.Button, interaction: discord.Interaction):
        for role in interaction.user.roles:
            if role.id not in MODERATING_ROLES:
                continue
            else:
                await interaction.message.edit(
                    content='**Отклонена.**',
                    embed=interaction.message.embeds[0].copy(),
                    view=None
                )

                return await interaction.response.send_message(ephemeral=True, content='Успешно!')

        await interaction.response.send_message(ephemeral=True, content='Недостаточно прав.')
