#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ui.app import sqldb


class MC_User(sqldb.Model):
  # TODO: flag, openID, guild.id
  id = sqldb.Column(sqldb.Integer, primary_key=True)
  image_path = sqldb.Column(sqldb.String(50), nullable=False)
  image_hash = sqldb.Column(sqldb.String(32), nullable=False)


# class Guild(db.Model):
#     # TODO: flag, guildID
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=True)
