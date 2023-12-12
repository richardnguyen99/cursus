# -*- coding: utf-8 -*-

"""Cursus history model for API authorization
"""

from typing import Optional

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cursus.util.extensions import db


class History(db.Model):
    __tablename__ = "history"

    id = db.Column(Integer, primary_key=True)

    user_id: Mapped[str] = mapped_column(
        String(11),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        index=True,
    )

    token_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("active_tokens.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True,
    )

    type: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        index=True,
    )

    at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
