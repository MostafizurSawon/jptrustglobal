from django.conf import settings
import json
from web_project.template_helpers.theme import TemplateHelper
from pathlib import Path

# Load menu JSON path dynamically by role
def get_menu_file_path(role):
    role = (role or "guest").lower()  # Normalize role to lowercase
    filename_map = {
        "admin": "vertical_menu.json",
        "guest": "vertical_guest_menu.json",
        "hr": "vertical_hr_menu.json",
        "agent": "vertical_agent_menu.json",
        "employee": "vertical_employee_menu.json",
        # Add more roles and corresponding JSON file names here
    }

    filename = filename_map.get(role, "vertical_menu.json")  # Default menu
    return Path(settings.BASE_DIR) / "templates" / "layout" / "partials" / "menu" / "vertical" / "json" / filename

class TemplateBootstrapLayoutVertical:
    @staticmethod
    def init(context):
        context.update({
            "layout": "vertical",
            "content_navbar": True,
            "is_navbar": True,
            "is_menu": True,
            "is_footer": True,
            "navbar_detached": True,
        })

        # Map context
        TemplateHelper.map_context(context)

        user = context.get("user")
        if hasattr(user, "role"):
            role = user.role
        elif isinstance(user, dict) and "role" in user:
            role = user["role"]
        else:
            role = "guest"

        role = role.lower()
        # print("--",user)
        # print("--",role)

        TemplateBootstrapLayoutVertical.init_menu_data(context, role)
        return context

    @staticmethod
    def init_menu_data(context, role):
        menu_file_path = get_menu_file_path(role)

        try:
            with open(menu_file_path, 'r', encoding='utf-8') as file:
                context["menu_data"] = json.load(file)

            # with open(menu_file_path, 'r') as file:
            #     context["menu_data"] = json.load(file)
        except FileNotFoundError:
            context["menu_data"] = []
