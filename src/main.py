#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ui.app import game_tools, sqldb, login_manager

from games.monster_castle.ui.views import monster_castle


@login_manager.user_loader
def load_user(user_id):
  return 1


with game_tools.app_context():
  game_tools.register_blueprint(monster_castle, url_prefix='/monster_castle')

  sqldb.create_all()
  sqldb.session.commit()


if __name__ == '__main__':
  game_tools.run(debug=True)
