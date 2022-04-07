import datetime

import discord
from sqlalchemy import Column, Integer, DateTime, JSON, TEXT

from .views import IdeaView
from ..database import *


class DBIdeaInstance(Base):
    __tablename__ = "ideas"

    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    author_id = Column(Integer)
    created_at = Column(DateTime)
    text = Column(TEXT)
    attachments = Column(JSON)
    message_id = Column(Integer)


Base.metadata.create_all(bind=engine)


class Idea:
    def __init__(self, _text, _author, _attachments, _creation_date):
        self._text = _text
        self._author = _author
        self._attachments = _attachments
        self._creation_date = _creation_date

        self._session = GlobalSession

    @property
    def text(self) -> str:
        return self._text

    @property
    def author(self) -> discord.Member:
        return self._author

    @property
    def attachments(self) -> list[str]:
        return self._attachments

    @property
    def created_at(self) -> datetime.datetime:
        return self._creation_date

    async def send_idea(self, channel: discord.TextChannel) -> discord.Message:
        print('start')
        e = discord.Embed(
            description=self._text,
            colour=discord.Colour.blurple(),
            timestamp=discord.utils.utcnow()
        )

        e.set_author(name=self._author.display_name, icon_url=self._author.display_avatar.url)
        e.set_footer(text='by gigalegit-#0880')

        if len(self._attachments) > 0:
            e.set_image(url=self._attachments[0])

        i = DBIdeaInstance()
        i.text = self._text
        i.attachments = self._attachments
        i.created_at = self._creation_date
        i.author_id = self._author.id

        msg = await channel.send(embed=e, view=IdeaView())

        i.message_id = msg.id

        self._session.add(i)
        self._session.commit()

        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

        await msg.create_thread(name=f"IDEA: {i.id}")

        return msg

    @classmethod
    def form_object(
            cls,
            text: str,
            author: discord.Member,
            attachment,
            creation_date: datetime.datetime,
    ):

        if attachment is None:
            attachments = []
        else:
            attachments = [attachment.url]

        return cls(_text=text, _author=author, _attachments=attachments, _creation_date=creation_date)
