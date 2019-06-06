"""
This module aims at sending mail to users.
"""

from mailjet_rest import Client
from dslib.utils.templating import render_file, render_string


class MailSender:

    def __init__(self, public_key, private_key):
        self.mailjet = Client(auth=(public_key, private_key), version='v3.1')

    def send_mail(self, text, recipient_mail):
        """
        Send the text as an e_mail to the recipient
        :param text: text of your email
        :param recipients: list of email address of the recipients
        :return:
        """
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "smartmeetingplace@gmail.com",
                        "Name": "Smart Meeting Place"
                    },
                    "To": [
                        {
                            "Email": recipient_mail,
                            "Name": "You"
                        }
                    ],
                    "Subject": "Find out your potential meeting points!",
                    "TextPart": "Smart meeting place",
                    "HTMLPart": text
                }
            ]
        }
        result = self.mailjet.send.create(data=data)

    @staticmethod
    def generate_text(template, **params):
        """
        generate text of the email
        :param self:
        :param groupname:
        :param username:
        :return: html text to send
        """
        text = render_string(template, params)
        return text


def send_to_group(sender, template, group):

    group_name = group['group_name']
    user_list = group['users']

    for user in user_list:
        text = sender.generate_text(template, username=user['username'], groupname=group_name)
        sender.send_mail(text, user['email'])

