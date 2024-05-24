import ast
import datetime
import json
import os
import re
import openai
from openai import OpenAI

openai.api_key = os.environ["OPENAI_API_KEY"]

class HtmlFile:
    def __init__(self, template_name, variables):
        """
        Initialise un objet HtmlFile.

        :param template_name: Contenu HTML sous forme de chaîne de caractères.
        :param variables: Dictionnaire contenant les variables à remplacer dans le contenu HTML.
        """
        if not isinstance(template_name, str):
            raise ValueError("html_template doit être une chaîne de caractères.")
        if not isinstance(variables, dict):
            raise ValueError("variables doit être un dictionnaire.")

        self.html_template = self.get_template(template_name)
        self.variables = self.get_variables(variables, template_name)
        self.template_name = template_name
        self.campaign_name = self.generate_campaign_name()
        self.sign = self.variables['sign']
        self.file_path = None

    def get_template(self, template_name):
        with open(os.path.join('templates', template_name), 'r', encoding='utf-8') as file:
            return file.read()

    def get_variables(self, variables, template_name):
        """
        Prépare les variables en assurant que les valeurs vides sont remplacées par une chaîne vide.

        :param variables: Dictionnaire des variables à traiter.
        :return: Dictionnaire des variables préparées.
        """
        with open("templates/templates_settings.json") as file:
            settings = json.load(file)
            prompt = settings[template_name]["prompt"]

        needed_variables = re.findall(r'\{\{([^}]*)', prompt)
        missing_variables = [var for var in needed_variables if var not in variables]
        unused_variables = [var for var in variables if var not in needed_variables]
        if unused_variables:
            print(
                f"Attention: Les variables suivantes ne sont pas utilisées dans le prompt_template : {', '.join(unused_variables)}")
        if missing_variables:
            raise ValueError(f"Il manque une ou plusieurs variables: {', '.join(missing_variables)}")

        for key, value in variables.items():
            prompt = prompt.replace(key, value)

        client = OpenAI()
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Tu es un assistant copywriter utile"},
                {"role": "user", "content": prompt}
            ]
        )

        output = str(completion.choices[0].message.content)
        print("output: ", output)
        start = output.find("{")
        end = output.rfind("}") + 1
        variables_dict = ast.literal_eval(output[start:end])
        print("variables_dict", variables_dict)
        variables_dict = {**variables, **variables_dict}
        print(variables_dict)
        return variables_dict

    def content(self):
        html_edited = self.html_template
        # Trier les clés par longueur décroissante pour éviter les sous-chaînes
        sorted_keys = sorted(self.variables.keys(), key=len, reverse=True)
        for key in sorted_keys:
            html_edited = html_edited.replace(key, self.variables[key])

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        file_name = f"Weekly_{self.variables['sign']}_{current_date}"
        self.file_path = os.path.join('templates', file_name)

        with open(self.file_path, 'w') as file:
            file.write(html_edited)

        return html_edited

    def generate_campaign_name(self):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        return f"Weekly {self.variables['sign']} - {current_date}.html"


# variables = {
#     "sign": "Cancer",
#     "sign_emoji": "♍️",
#     "love_img_url": "https://storage.mlcdn.com/account_image/954202/H2KjQhp6NnVK2ygP4GbcDxVURtZ17Y2agivQoFzq.png",
#     "money_img_url": "https://storage.mlcdn.com/account_image/954202/LYbN58bxFxnmjrFRXkhFmuMS4pbr7bWtK4ukW5Dz.png",
#     "health_img_url": "https://storage.mlcdn.com/account_image/954202/QWgMrXZJdFNuLEBAbWIqrUPc7oUa2GxXp692S5pf.png",
# }
#
# mon_html = HtmlFile("weekly_newsletter.html", variables)
# content = mon_html.content()
# print(content)