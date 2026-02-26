from dotenv import load_dotenv
load_dotenv()

from google import genai
import os
from google.genai import types

print('api key read', os.getenv('MODEL_API_KEY'))

client = genai.Client(
    api_key=os.getenv('MODEL_API_KEY'),
    http_options=types.HttpOptions(api_version='v1')
)

print('client created, listing models...')
print('models:', client.models.list())
