import json
import re

import requests

# Globals
model_name = 'gpt-oss:20b'

def send_ai_request(text: str):
    url = 'http://localhost:11434/api/generate'

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "model": model_name,
        "prompt": text,
        "stream": False
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data['response']
        # print(actual_response)
        return actual_response
    else:
        return None


def check_closeness(term: str, compare_to: str, lang_to: str) -> int:
    for i in range(3):
        try:
            txt = f'I need you to examine two translated words/phrases and decide a percent of closeness between them and only return a JSON response.  For a rating between 0-100 of how well the phrase/word "{term}" in English (US) compares to "{compare_to}" in {lang_to}.  Only Return the result as JSON with the following format {{"rating":"100"}}, no description or explanations.'
            rsp = send_ai_request(txt)

            return int(json.loads(rsp)['rating'])
        except:
            pass


def extract_json(response: str):
    try:
        # Try parsing as JSON directly
        return json.loads(response)
    except json.JSONDecodeError:
        pass

    # Find the last occurrence of a JSON-like structure
    match = re.search(r'(\{.*\}|\[.*\])\s*$', response, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass

    raise ValueError("No valid JSON found")


def  get_translated_for(term: str, lang_to: str, key: str) -> str:
    if len(term) > 0:
        for i in range(3):
            try:
                txt = f'I need you to translate the phrase/word "{term}" from "English" to "{lang_to}" and only return a JSON response.  Do not attempt to provide a python solution! For context, the term will be used on a media player application, which may be text for a button, action, tooltip or description.  The word may have () or [] in the text and they should stay in the relevant spots.  Also the text may contain tokens in this format {{{{token_name}}}}  Only Return the result as JSON with the following format {{"translated":"value"}}, no description or explanations.'
                rsp = send_ai_request(txt)

                return extract_json(rsp)['translated']
            except:
                pass
    return ''