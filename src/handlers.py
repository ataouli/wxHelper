from tornado.web import RequestHandler
from bot import Bot

bot = Bot()


class RootHandler(RequestHandler):
    def get(self):
        self.write('hello')


class QrcodeHandler(RequestHandler):
    def get(self):
        bot.get_uuid()
        png = bot.get_qrcode()
        self.add_header('Content-Type', 'image/png')
        self.write(png)


class LoginHandler(RequestHandler):
    def get(self):
        self.write(bot.login())


class FriendsHandler(RequestHandler):
    def get(self):
        response = {
            'friends': [friend.to_json() for friend in bot.friends()]
        }
        self.write(response)


class GroupHandler(RequestHandler):
    def get(self):
        response = {
            'groups': [group.to_json() for group in bot.groups()]
        }
        self.write(response)


class GroupMemberHandler(RequestHandler):
    def get(self, user_name):
        group = bot.search_group(user_name)
        if group:
            members = group.members
            member_data_list = []
            for member in members:
                data = member.to_json()
                data['is_friend'] = member.is_friend
                member_data_list.append(data)

            response = {
                'members': member_data_list
            }
            self.write(response)
        else:
            self.set_status(404)


class FriendAvatarHandler(RequestHandler):
    def get(self, username):
        self.add_header('Content-Type', 'image/jpg')
        self.write(bot.get_friend_avatar(username))


class GroupAvatarHandler(RequestHandler):
    def get(self, username):
        self.add_header('Content-Type', 'image/jpg')
        self.write(bot.get_group_avatar(username))
