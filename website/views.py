from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .api_utils import search_food_item, get_nutrient_info
from .models import FoodItem, db
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user = current_user)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        food_name = request.form.get('food_name')
        food_data = search_food_item(food_name)
        
        if food_data:
            fdc_id = food_data['fdcId']
            nutrient_info = get_nutrient_info(fdc_id)
            
            calories = next((n for n in nutrient_info['foodNutrients'] if n['nutrient']['name'] == 'Energy'), None)
            protein = next((n for n in nutrient_info['foodNutrients'] if n['nutrient']['name'] == 'Protein'), None)
            carbs = next((n for n in nutrient_info['foodNutrients'] if n['nutrient']['name'] == 'Carbohydrate, by difference'), None)
            fat = next((n for n in nutrient_info['foodNutrients'] if n['nutrient']['name'] == 'Total lipid (fat)'), None)
            
            new_food = FoodItem(food_name=food_data['description'], 
                                calories=calories['amount'] if calories else None, 
                                protein=protein['amount'] if protein else None, 
                                carbs = carbs['amount'] if carbs else None, 
                                fat=fat['amount'] if fat else None)
            db.session.add(new_food)
            db.session.commit()
            
            flash(f"Food '{food_name}' added successfully!", "success")
        else:
            flash("Food item not found.", "error")
    
    return render_template("search.html")