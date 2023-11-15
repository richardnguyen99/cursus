# -*- coding: utf-8 -*-

"""Cursus User model
"""

import cuid2

from sqlalchemy import String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, Relationship, relationship

from cursus.util.extensions import db


CUID_GENERATOR: cuid2.Cuid = cuid2.Cuid(length=11)


class User(db.Model):
    """Core User Model for Cursus Application"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        String(11),
        primary_key=True,
        default=CUID_GENERATOR.generate,
    )

    name: Mapped[str] = mapped_column(
        String(256),
        nullable=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(256),
        nullable=True,
        unique=True,
        index=True,
    )

    emailVerifiedDate: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    image: Mapped[str] = mapped_column(
        String(256),
        nullable=True,
    )

    accounts: Relationship[list["Account"]] = relationship(
        "Account",
        backref="user",
        lazy=True,
        collection_class=list,
    )

    sessions: Relationship[list["Session"]] = relationship(
        "Session",
        backref="user",
        lazy=True,
        collection_class=list,
    )

    def __init__(self, name: str, email: str, image: str):
        self.name = name
        self.email = email
        self.image = image

    def __repr__(self) -> str:
        return f"<User {self.name}>"

    def __str__(self) -> str:
        return self.name


class Account(db.Model):
    """Core Account Model for Cursus Application"""

    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(
        String(11),
        primary_key=True,
        default=CUID_GENERATOR.generate,
    )

    type: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )

    provider: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )

    providerAccountId: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
    )

    refresh_token: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )

    access_token: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )

    expires_at: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )

    token_type: Mapped[str] = mapped_column(
        String(64),
        nullable=True,
    )

    scope: Mapped[str] = mapped_column(
        String(256),
        nullable=True,
    )

    id_token: Mapped[str] = mapped_column(
        Text(),
        nullable=True,
    )

    session_state = mapped_column(
        String(256),
        nullable=True,
    )

    userId: Mapped[int] = mapped_column(
        String(11),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )


class Session(db.Model):
    id: Mapped[int] = mapped_column(
        String(11),
        primary_key=True,
        default=CUID_GENERATOR.generate,
    )

    expires: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    sessionToken: Mapped[str] = mapped_column(
        String(256),
        nullable=False,
        unique=True,
    )

    userId: Mapped[int] = mapped_column(
        String(11),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )


class VerificationToken(db.Model):
    id: Mapped[int] = mapped_column(
        String(11),
        primary_key=True,
        default=CUID_GENERATOR.generate,
    )

    token: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
        unique=True,
    )

    expires: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
    )

    userId: Mapped[int] = mapped_column(
        String(11),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
