import os

from django.apps import AppConfig


def load_policy():
    from dauthz.core import enforcer
    p_rules = [
        ["anonymous", "/", "(GET)|(POST)"],
        ["anonymous", "/login", "(GET)|(POST)"],
        ["anonymous", "/register", "(GET)|(POST)"],
        ["normal_user", "/logout", "(GET)|(POST)"],
        ["admin", "/all_users_profile", "(GET)|(POST)"],
    ]
    g_rules = [
        ["normal_user", "anonymous"],
        ["admin", "normal_user"]
    ]
    enforcer.add_policies(p_rules)
    enforcer.add_grouping_policies(g_rules)
    enforcer.save_policy()


class UserManagementConfig(AppConfig):
    default_auto_filed = 'django.db.models.BigAutoField'
    name = 'user_management'

    def ready(self):
        if os.environ.get('RUN_MAIN'):
            load_policy()
