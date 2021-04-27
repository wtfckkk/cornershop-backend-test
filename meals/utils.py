

class MenuMessage:
    """Constructs the menu message and stores the preferences of employees."""

    HEADER_BLOCK = {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": ":avocado: Today's menu is open ! :tomato: ",
            "emoji": True
        }
    }, {
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": "Must choose until 11:00 A.M "
            }
        ]
    }, {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Please select your preference:*"
        }
    }

    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, menu):
        self.menu = menu
        self.username = "Meals Service"
        self.text = "Menu is open !"

    def get_message_payload(self):
        return {
            "text": self.text,
            "username": self.username,
            "blocks": [
                *self.HEADER_BLOCK,
                self.DIVIDER_BLOCK,
                *self._get_menu_block(self.menu),
                self.DIVIDER_BLOCK,
            ],
        }

    @staticmethod
    def _get_menu_block(menu):
        block = []
        for count, meal in enumerate(menu.meals.all(), start=1):
            block.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{count}. {meal.name}",
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Choose"
                    },
                    "value": f"{meal.id}*{menu.id}"
                }
            })
        return block


