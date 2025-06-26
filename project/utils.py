# recipes/utils.py

import requests
import os
from django.core.files.base import ContentFile
from django.utils import timezone
from django.conf import settings
from .models import Recipe, Ingredient
from urllib.parse import urlparse

def fetch_ingredients_by_id(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        'includeNutrition': False,
        'apiKey': settings.SPOONACULAR_API_KEY
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print(f"Failed to fetch ingredients for ID {recipe_id}")
        return []

    data = resp.json()
    ingredients = data.get('extendedIngredients', [])
    return ingredients


def fetch_steps_by_id(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/analyzedInstructions"
    params = {
        'stepBreakdown': True,
        'apiKey': settings.SPOONACULAR_API_KEY
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("Failed fetching instructions for ID:", recipe_id)
        return ""

    data = resp.json()
    if not data:
        return ""

    # data is a list of instruction blocks
    instructions = []
    for block in data:
        for step in block.get('steps', []):
            text = step.get('step', '').strip()
            if text:
                instructions.append(text)

    return "\n".join(instructions)


def download_image_to_field(url):
    """Download image from URL and return a ContentFile object and name."""
    if not url:
        return None, None

    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_name = os.path.basename(urlparse(url).path)
            return ContentFile(response.content), file_name
        else:
            print(f"Image download failed: {response.status_code}")
    except Exception as e:
        print(f"Exception while downloading image: {e}")

    return None, None


def load_data_from_spoonacular(query='pasta', number=5):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        'query': query,
        'number': number,
        'addRecipeInformation': True,
        'apiKey': settings.SPOONACULAR_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return

    data = response.json()
    recipes = data.get('results', [])

    for item in recipes:
        title = item.get('title', 'No title')
        description = item.get('summary', 'No description')
        cuisine = ', '.join(item.get('cuisines', [])) or 'Unknown'
        cooking_time = item.get('readyInMinutes', 0)
        image_url = item.get('image', '')
        source_url = item.get('sourceUrl', '')
        source_name = item.get('sourceName', 'Spoonacular')

        # Use reliable steps fetch by ID
        recipe_id = item.get('id')
        step_string = fetch_steps_by_id(recipe_id)

        # Fallback to raw text if step fetch fails
        if not step_string:
            step_string = item.get('instructions', '').strip() or 'No steps provided'

        steps_text = step_string

        # Download image
        image_file, image_name = download_image_to_field(image_url)

        # Create Recipe object
        recipe = Recipe(
            title=title,
            description=description,
            cuisine_type=cuisine,
            cooking_time=cooking_time,
            difficulty='Medium',
            steps=steps_text,
            date_added=timezone.now(),
            recipe_type='Scraped',
            source_url=source_url,
            source_name=source_name
        )

        # Attach the downloaded image
        if image_file and image_name:
            recipe.image.save(image_name, image_file, save=False)

        recipe.save()
        ingredients = fetch_ingredients_by_id(recipe_id)
        for ing in ingredients:
            Ingredient.objects.create(
                ingredient_name=ing.get('name', 'Unknown'),
                quantity=ing.get('original', ''),  # full string like "2 tablespoons olive oil"
                recipe=recipe
            )


    print(f"Successfully loaded {len(recipes)} recipes with image downloads.")


def load_data_from_spoonacular_url(url):
    """Takes a URL and attempts to fetch a recipe from Spoonacular based on it."""
    search_url = "https://api.spoonacular.com/recipes/extract"
    params = {
        'url': url,
        'apiKey': settings.SPOONACULAR_API_KEY
    }

    response = requests.get(search_url, params=params)
    if response.status_code != 200:
        print("Spoonacular extract error:", response.status_code)
        return False

    data = response.json()
    title = data.get('title', 'No title')
    description = data.get('summary', 'No description')
    cuisine = ', '.join(data.get('cuisines', [])) or 'Unknown'
    cooking_time = data.get('readyInMinutes', 0)
    image_url = data.get('image', '')
    source_url = data.get('sourceUrl', '')
    source_name = data.get('sourceName', 'Spoonacular')

    steps_text = ""
    for block in data.get('analyzedInstructions', []):
        for step in block.get('steps', []):
            steps_text += f"{step.get('step')}\n"

    if not steps_text:
        steps_text = data.get('instructions', '') or 'No steps provided'

    # Download image
    image_file, image_name = download_image_to_field(image_url)

    recipe = Recipe(
        title=title,
        description=description,
        cuisine_type=cuisine,
        cooking_time=cooking_time,
        difficulty='Medium',
        steps=steps_text,
        date_added=timezone.now(),
        recipe_type='UserSubmitted',
        source_url=source_url,
        source_name=source_name
    )

    if image_file and image_name:
        recipe.image.save(image_name, image_file, save=False)

    recipe.save()
    return True



# import requests
# from bs4 import BeautifulSoup
# from django.utils import timezone
# from .models import Recipe, StepRecipe

# def load_data_from_foodista(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#     except Exception as e:
#         print(f"Error fetching URL: {e}")
#         return

#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Extract title
#     title_tag = soup.find('h1')
#     title = title_tag.get_text(strip=True) if title_tag else 'No Title'

#     # Extract description
#     desc_tag = soup.find('div', class_='fd-recipe-description')
#     description = desc_tag.get_text(strip=True) if desc_tag else 'No description available'

#     # Extract steps (usually in <ol> list)
#     step_list = soup.find('ol', class_='instruction-list')
#     steps = ''
#     if step_list:
#         steps = '\n'.join(
#             li.get_text(strip=True)
#             for li in step_list.find_all('li')
#         )
#     else:
#         steps = 'No steps provided'

#     # Save to DB
#     step_obj = StepRecipe.objects.create(instructions=steps)

#     Recipe.objects.create(
#         title=title,
#         description=description,
#         cuisine_type='Unknown',
#         cooking_time=0,  # You can try to scrape it if visible
#         difficulty='Medium',
#         steps=step_obj,
#         date_added=timezone.now(),
#         recipe_type='Scraped',
#         source_url=url,
#         source_name='Foodista'
#     )

#     print(f"Successfully saved recipe: {title}")
