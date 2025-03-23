"""Get resume and return"""

INDEX_FILE_NAME = "./public/index.html"
TEMPLATE_FILE_NAME = "./template/index.html"
from datetime import datetime
from jinja2 import Template
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GOOGLE_TOKEN = os.getenv("GOOGLE_TOKEN")
MICROSOFT_TOKEN = os.getenv("MICROSOFT_TOKEN")

def generate_resume():
    url = "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses"
    headers = {"Authorization": f"Bearer {GOOGLE_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        name_api = user_data.get('names', [])[0]['givenName']
    else:
        name_api = f"Ошибка: {response.status_code}"

    url = "https://graph.microsoft.com/v1.0/me"
    headers = {
        "Authorization": f"Bearer {MICROSOFT_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        email_api = user_data.get('mail', 'N/A')
        job_position_api = user_data.get('jobTitle', 'N/A')
        user_id_api = user_data.get('id', 'N/A')
    else:
        email_api = f"Ошибка: {response.status_code}"
        job_position_api = f"Ошибка: {response.status_code}"
        user_id_api = f"Ошибка: {response.status_code}"

    url = 'https://api.github.com/user/repos'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    repositories_api = []
    if response.status_code == 200:
        repositories = response.json()
        for repo in repositories:
            repositories_api.append({
                'name': repo['name'],
                'url': repo['html_url'],
                'created': repo['created_at'],
                'updated': repo['updated_at']
            })
    else:
        repositories_api.append({
                'name': f"Ошибка: {response.status_code}",
                'url': f"Ошибка: {response.status_code}",
                'created': f"Ошибка: {response.status_code}",
                'updated': f"Ошибка: {response.status_code}"
            })

    with open(TEMPLATE_FILE_NAME, "r", encoding="utf-8") as template_file:
        template_text = template_file.read()
        jinja_template = Template(template_text)
        rendered_resume = jinja_template.render(
            name = name_api,
            email = email_api,
            job_position = job_position_api,
            user_id = user_id_api,
            repositories = repositories_api,
            datetime = datetime.now()
        )
    with open(INDEX_FILE_NAME, "w", encoding="utf-8") as resume_file:
        resume_file.write(rendered_resume)

        return rendered_resume