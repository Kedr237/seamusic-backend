from datetime import date

from sqlalchemy import ForeignKey, Date, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.enums.auth import Role, AccessLevel
from src.models.albums import Album, artist_profile_album_association
from src.models.base import Base
from src.models.squads import Squad, squad_producer_profile_association, squad_artist_profile_association
from src.models.tags import Tag, artist_tags_association, producer_tags_association, listener_tags_association
from src.models.tracks import Track, artist_profile_track_association

user_to_artist_association = Table(
    "user_to_artist_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("artist_profile_id", ForeignKey("artist_profiles.id"), primary_key=True),
)


user_to_producer_association = Table(
    "user_to_producer_association",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("producer_profile_id", ForeignKey("producer_profiles.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    picture_url: Mapped[str] = mapped_column(nullable=True)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)

    artist_profile_id: Mapped[int] = mapped_column(ForeignKey("artist_profiles.id"), nullable=True)
    producer_profile_id: Mapped[int] = mapped_column(ForeignKey("producer_profiles.id"), nullable=True)

    artist_profile: Mapped["ArtistProfile"] = relationship(backref="user")  # type: ignore[name-defined]
    producer_profile: Mapped["ProducerProfile"] = relationship(backref="user")  # type: ignore[name-defined]
    roles: Mapped[Role] = mapped_column(nullable=False)
    access_level: Mapped[AccessLevel] = mapped_column(nullable=False, default=AccessLevel.user)
    tags: Mapped[list["Tag"]] = relationship(secondary=listener_tags_association, back_populates="listener_profiles")  # type: ignore[name-defined]
    squads: Mapped["Squad"] = relationship("Squad", overlaps="user")  # type: ignore[name-defined]
    albums: Mapped[list["Album"]] = relationship("Album", overlaps="user")  # type: ignore[name-defined]


class ArtistProfile(Base):
    __tablename__ = "artist_profiles"

    description: Mapped[str] = mapped_column(nullable=True)

    tracks: Mapped[list["Track"]] = relationship(  # type: ignore[name-defined]
        secondary=artist_profile_track_association,
        back_populates="artist_profiles"
    )
    albums: Mapped[list["Album"]] = relationship(  # type: ignore[name-defined]
        secondary=artist_profile_album_association,
        back_populates="artist_profiles"
    )
    squads: Mapped[list["Squad"]] = relationship(  # type: ignore[name-defined]
        secondary=squad_artist_profile_association,
        back_populates="artist_profiles"
    )
    tags: Mapped[list["Tag"]] = relationship(  # type: ignore[name-defined]
        secondary=artist_tags_association,
        back_populates="artist_profiles"
    )


class ProducerProfile(Base):
    __tablename__ = "producer_profiles"

    description: Mapped[str] = mapped_column()

    tags: Mapped[list["Tag"]] = relationship(  # type: ignore[name-defined]
        secondary=producer_tags_association,
        back_populates="producer_profiles"
    )
    squads: Mapped[list["Squad"]] = (relationship(  # type: ignore[name-defined]
        secondary=squad_producer_profile_association,
        back_populates="producer_profiles"
    ))
