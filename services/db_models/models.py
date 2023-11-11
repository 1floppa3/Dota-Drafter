from datetime import datetime

import sqlalchemy as sa

from services.database import db


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: list[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


class TimedBaseModel(BaseModel):
    __abstract__ = True

    created_at = sa.Column(db.DateTime(True), server_default=db.func.now())
    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=db.func.now(),
    )


class Payments(BaseModel):
    __tablename__ = 'payments'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    is_active = sa.Column(sa.Boolean, default=True)
    paid = sa.Column(sa.Boolean, default=False)
    user_id = sa.Column(sa.Integer)

    query: sa.sql.select


class Users(TimedBaseModel):
    __tablename__ = 'users'

    user_id = sa.Column(sa.Integer, primary_key=True)
    is_active = sa.Column(sa.Boolean, default=True)
    is_sub = sa.Column(sa.Boolean, default=False)
    sub_expires = sa.Column(sa.DateTime(timezone=True), default=datetime.utcnow)
    username = sa.Column(sa.String(255))
    name = sa.Column(sa.String(255))
    command_count = sa.Column(sa.Integer, default=0)
    max_picks_per_day = sa.Column(sa.Integer, default=5)

    query: sa.sql.select
