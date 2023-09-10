import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecipeScraper:
    def __init__(self, url):
        self.url = url

    def get_recipe_data(self):
        response = requests.get(self.url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            recipe_title = soup.find(
                'h1', class_='recipe-title').get_text().strip()
            ingredients = soup.find_all('li', class_='ingredient')
            instructions = soup.find(
                'div', class_='instructions').get_text().strip()

            ingredient_list = [ingredient.get_text().strip()
                               for ingredient in ingredients]

            return {
                'title': recipe_title,
                'ingredients': ingredient_list,
                'instructions': instructions
            }
        else:
            return None


class RecipeAnalyzer:
    def __init__(self, recipe_data):
        self.recipe_data = recipe_data
        self.vectorizer = CountVectorizer().fit_transform(
            [self.recipe_data['instructions']])

    def get_cosine_similarity(self, recipe_instructions):
        instructions_list = [
            self.recipe_data['instructions'], recipe_instructions]
        instructions_vectorized = self.vectorizer.transform(instructions_list)

        cosine_similarities = cosine_similarity(instructions_vectorized)
        return cosine_similarities[0][1]


class SustainableRecipeRecommender:
    def __init__(self, recipes):
        self.recipes = recipes

    def recommend_recipe(self, user_preferences):
        recommended_recipe = None
        max_similarity = -1

        for recipe in self.recipes:
            analyzer = RecipeAnalyzer(recipe['data'])
            similarity = analyzer.get_cosine_similarity(
                user_preferences['instructions'])

            if similarity > max_similarity:
                max_similarity = similarity
                recommended_recipe = recipe

        return recommended_recipe


class UserProfiler:
    def __init__(self, username):
        self.username = username
        self.preferences = {}

    def set_user_preferences(self, preferences):
        self.preferences = preferences

    def get_user_preferences(self):
        return self.preferences


class SustainableFoodPlatform:
    def __init__(self):
        self.recipes = []

    def add_recipe(self, recipe_data):
        self.recipes.append({
            'data': recipe_data,
            'likes': 0,
            'comments': []
        })

    def get_top_recipes(self):
        sorted_recipes = sorted(
            self.recipes, key=lambda recipe: recipe['likes'], reverse=True)
        return sorted_recipes[:10]

    def add_comment(self, recipe_title, comment):
        for recipe in self.recipes:
            if recipe['data']['title'] == recipe_title:
                recipe['comments'].append(comment)
                break

    def like_recipe(self, recipe_title):
        for recipe in self.recipes:
            if recipe['data']['title'] == recipe_title:
                recipe['likes'] += 1
                break


# Example usage of the classes

scraper = RecipeScraper('https://www.example.com/recipe')
recipe_data = scraper.get_recipe_data()

sustainable_food_platform = SustainableFoodPlatform()
sustainable_food_platform.add_recipe(recipe_data)

user_profiler = UserProfiler('JohnDoe')
user_prefs = {
    'instructions': 'Mix all ingredients in a bowl'
}
user_profiler.set_user_preferences(user_prefs)

recipe_recommender = SustainableRecipeRecommender(
    sustainable_food_platform.recipes)
recommended_recipe = recipe_recommender.recommend_recipe(
    user_profiler.get_user_preferences())

if recommended_recipe:
    print('Recommended Recipe:', recommended_recipe['data']['title'])
else:
    print('No recipe recommendation available.')
