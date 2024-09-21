# from flask import Flask, request, render_template
# import mysql.connector

# app = Flask(__name__)
# @app.route('/')
# def index():
#     return render_template('index.html')
# @app.route('/contact')
# def contact():
#     return render_template('contact.html')
# @app.route('/aboutus')
# def aboutus():
#     return render_template('aboutus.html')
# @app.route('/recipes')
# def recipes():
#     return render_template('recipes.html')
# @app.route('/testimonial')
# def testimonial():
#     return render_template('testimonial.html')
# # Login Route
# @app.route("/login", methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         em = request.form.get('email')
#         pwd = request.form.get('password')
        
#         try:
#             # Establish connection with MySQL database
#             m = mysql.connector.connect(host="localhost", user="root", passwd="", database='mydatabase')
#             cursor = m.cursor()
            
#             # Query to check user credentials
#             query = "SELECT * FROM user WHERE email = %s AND password = %s"
#             cursor.execute(query, (em, pwd))
#             user = cursor.fetchone()  # Fetch one matching user
            
#             cursor.close()
#             m.close()
            
#             if user:
#                 return render_template('login.html', message="Login successful!")
#             else:
#                 return render_template('login.html', message="Invalid credentials!")
#         except mysql.connector.Error as err:
#             return render_template('login.html', message=f"Error: {err}")
#     else:
#         return render_template('login.html')

# # Signup Route
# @app.route("/register", methods=['POST', 'GET'])
# def register():
#     if request.method == 'POST':
#         username = request.form.get('username')  # Use 'username' for the Username field
#         em = request.form.get('email')
#         pwd = request.form.get('password')
        
#         try:
#             # Establish connection with MySQL database
#             m = mysql.connector.connect(host="localhost", user="root", passwd="", database='mydatabase')
#             cursor = m.cursor()
            
#             # Query to insert new user into the 'user' table
#             query = "INSERT INTO user (Username, email, password) VALUES (%s, %s, %s)"
#             cursor.execute(query, (username, em, pwd))
#             m.commit()
            
#             cursor.close()
#             m.close()
            
#             return render_template('register.html', message="Signup successful!")
#         except mysql.connector.Error as err:
#             return render_template('register.html', message=f"Error: {err}")
#     else:
#         return render_template('register.html')

# # Run the Flask app
# if __name__ == "__main__":
#     app.run(debug=True)
from flask import Flask, request, render_template, session, redirect, url_for
import mysql.connector
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import StandardScaler
import numpy as np
import secrets
app = Flask(__name__)
app.secret_key = secrets.token_hex(16) 

# Load the dataset
df = pd.read_csv('Dataset.csv')  # Update with the correct path to your CSV file

# Define diet plans based on labels
diet_plans = {
    0: "You’re in the underweight range. Focus on eating calorie-dense foods like avocados, nuts, and whole grains. Include protein-rich foods like lean meats, legumes, and dairy. Consider eating more frequently with snacks in between meals to help with weight gain.",
    1: "You’re in the underweight range. Focus on eating calorie-dense foods like avocados, nuts, and whole grains. Include protein-rich foods like lean meats, legumes, and dairy. Consider eating more frequently with snacks in between meals to help with weight gain.",
    2: "You’re in the underweight range. Focus on eating calorie-dense foods like avocados, nuts, and whole grains. Include protein-rich foods like lean meats, legumes, and dairy. Consider eating more frequently with snacks in between meals to help with weight gain.",
    3: "You’re in the underweight range. Focus on eating calorie-dense foods like avocados, nuts, and whole grains. Include protein-rich foods like lean meats, legumes, and dairy. Consider eating more frequently with snacks in between meals to help with weight gain.",
    4: "You’re in the underweight range. Focus on eating calorie-dense foods like avocados, nuts, and whole grains. Include protein-rich foods like lean meats, legumes, and dairy. Consider eating more frequently with snacks in between meals to help with weight gain.",
    5: "You’re in the underweight range. Focus on eating calorie-dense foods like avocados, nuts, and whole grains. Include protein-rich foods like lean meats, legumes, and dairy. Consider eating more frequently with snacks in between meals to help with weight gain.",
    6: "You’re in the underweight range. Focus on eating calorie-dense foods like avocados, nuts, and whole grains. Include protein-rich foods like lean meats, legumes, and dairy. Consider eating more frequently with snacks in between meals to help with weight gain.",
    7: "You’re in the underweight range. Focus on eating calorie-dense foods like avocados, nuts, and whole grains. Include protein-rich foods like lean meats, legumes, and dairy. Consider eating more frequently with snacks in between meals to help with weight gain.",
    12: "You’re still considered underweight, so aim to increase your calorie intake with nutrient-dense foods. Include foods like sweet potatoes, quinoa, and lean proteins. Make sure you’re eating balanced meals with healthy fats, and consider seeing a nutritionist for personalized advice.",
    13: "Your BMI is in the normal range. Maintain your weight by continuing to eat a balanced diet with plenty of fruits, vegetables, lean proteins, and whole grains. Regular physical activity is also important for overall health.",
    14: "Your BMI is in the normal range. Maintain your weight by continuing to eat a balanced diet with plenty of fruits, vegetables, lean proteins, and whole grains. Regular physical activity is also important for overall health.",
    15: "Your BMI is in the normal range. Maintain your weight by continuing to eat a balanced diet with plenty of fruits, vegetables, lean proteins, and whole grains. Regular physical activity is also important for overall health.",
    16: "Your BMI is in the normal range. Maintain your weight by continuing to eat a balanced diet with plenty of fruits, vegetables, lean proteins, and whole grains. Regular physical activity is also important for overall health.",
    17: "Your BMI is in the normal range. Maintain your weight by continuing to eat a balanced diet with plenty of fruits, vegetables, lean proteins, and whole grains. Regular physical activity is also important for overall health.",
    18: "Your BMI is in the normal range. Maintain your weight by continuing to eat a balanced diet with plenty of fruits, vegetables, lean proteins, and whole grains. Regular physical activity is also important for overall health.",
    19: "Your BMI is in the normal range. Maintain your weight by continuing to eat a balanced diet with plenty of fruits, vegetables, lean proteins, and whole grains. Regular physical activity is also important for overall health.",
    20: "Your BMI is in the normal range. Maintain your weight by continuing to eat a balanced diet with plenty of fruits, vegetables, lean proteins, and whole grains. Regular physical activity is also important for overall health.",
    21: "You’re in the overweight range. Focus on portion control and choose nutrient-dense foods over calorie-dense ones. Incorporate regular exercise to help manage your weight and improve overall health. Avoid excessive snacking and sugary drinks",
    22: "You’re in the overweight range. Focus on portion control and choose nutrient-dense foods over calorie-dense ones. Incorporate regular exercise to help manage your weight and improve overall health. Avoid excessive snacking and sugary drinks",
    25: "You’re in the overweight range. Focus on portion control and choose nutrient-dense foods over calorie-dense ones. Incorporate regular exercise to help manage your weight and improve overall health. Avoid excessive snacking and sugary drinks.",
    26: "You’re in the overweight range. Focus on portion control and choose nutrient-dense foods over calorie-dense ones. Incorporate regular exercise to help manage your weight and improve overall health. Avoid excessive snacking and sugary drinks.",
    27: "You’re in the overweight range. Focus on portion control and choose nutrient-dense foods over calorie-dense ones. Incorporate regular exercise to help manage your weight and improve overall health. Avoid excessive snacking and sugary drinks.",
    28: "You’re in the overweight range. Focus on portion control and choose nutrient-dense foods over calorie-dense ones. Incorporate regular exercise to help manage your weight and improve overall health. Avoid excessive snacking and sugary drinks.",
    29: "You’re in the overweight range. Focus on portion control and choose nutrient-dense foods over calorie-dense ones. Incorporate regular exercise to help manage your weight and improve overall health. Avoid excessive snacking and sugary drinks.",
    30: "You’re in the obese range. Work on creating a balanced eating plan with controlled portions and avoid high-calorie, low-nutrition foods. Increase physical activity and consider consulting with a healthcare provider or dietitian for a tailored weight management plan.",
    31: "You’re in the obese range. Work on creating a balanced eating plan with controlled portions and avoid high-calorie, low-nutrition foods. Increase physical activity and consider consulting with a healthcare provider or dietitian for a tailored weight management plan.",
}
recipe_plans = {
    "12-12.5": {
        "breakfast": "Moong dal chilla with mint chutney and a glass of buttermilk.",
        "lunch": "Grilled paneer tikka with a side of roti and cucumber salad.",
        "dinner": "Vegetable pulao with a bowl of curd and mixed vegetable curry.",
        "nutrition": {
            "carbs": 44.55,
            "proteins": 23.64,
            "fats": 31.82
        }
    },
    "12.5-13": {
        "breakfast": "Masala oats with a boiled egg and a glass of fresh juice.",
        "lunch": "Rajma (kidney beans) curry with brown rice and a small salad.",
        "dinner": "Palak paneer with whole wheat roti and a side of raita.",
        "nutrition": {
            "carbs": 41.67,
            "proteins": 33.33,
            "fats": 25.00
        }
    },
    "13-13.5": {
        "breakfast": "Upma with mixed vegetables and a glass of coconut water.",
        "lunch": "Chole (chickpeas) with jeera rice and a cucumber-tomato salad.",
        "dinner": "Dal tadka with quinoa and sautéed spinach.",
        "nutrition": {
            "carbs": 48.00,
            "proteins": 30.00,
            "fats": 22.00
        }
    },
    "13.5-14": {
        "breakfast": "Idli with sambar and coconut chutney.",
        "lunch": "Baingan bharta with roti and a small bowl of curd.",
        "dinner": "Mixed dal khichdi with roasted papad and pickle.",
        "nutrition": {
            "carbs": 49.00,
            "proteins": 22.00,
            "fats": 29.00
        }
    },
    "14-14.5": {
        "breakfast": "Poha with peanuts, curry leaves, and a glass of buttermilk.",
        "lunch": "Aloo gobi with whole wheat roti and a side of green chutney.",
        "dinner": "Lauki (bottle gourd) sabzi with bajra roti and cucumber raita.",
        "nutrition": {
            "carbs": 49.25,
            "proteins": 23.75,
            "fats": 27.00
        }
    },
    "14.5-15": {
        "breakfast": "Besan chilla with green chutney and a boiled egg.",
        "lunch": "Kadhi with brown rice and cucumber salad.",
        "dinner": "Oats khichdi with moong dal and a side of curd.",
        "nutrition": {
            "carbs": 50.00,
            "proteins": 25.00,
            "fats": 25.00
        }
    },
    "15-15.5": {
        "breakfast": "Daliya (broken wheat) with vegetables and curd.",
        "lunch": "Paneer bhurji with roti and a bowl of cucumber raita.",
        "dinner": "Methi (fenugreek) paratha with a side of aloo sabzi.",
        "nutrition": {
            "carbs": 50.00,
            "proteins": 25.00,
            "fats": 25.00
        }
    },
    "15.5-16": {
        "breakfast": "Stuffed paratha with curd and green chutney.",
        "lunch": "Tawa sabzi with jeera rice and a side of salad.",
        "dinner": "Pesarattu (green gram dosa) with tomato chutney.",
        "nutrition": {
            "carbs": 48.75,
            "proteins": 26.88,
            "fats": 24.37
        }
    },
    "16-16.5": {
        "breakfast": "Sprouts salad with lemon and masala chai.",
        "lunch": "Vegetable pulao with boondi raita.",
        "dinner": "Dal palak with multigrain roti and a side salad.",
        "nutrition": {
            "carbs": 47.37,
            "proteins": 29.47,
            "fats": 23.16
        }
    },
    "16.5-17": {
        "breakfast": "Vegetable poha with peanuts and a glass of chaas (buttermilk).",
        "lunch": "Masoor dal with brown rice and salad.",
        "dinner": "Bhindi (okra) sabzi with bajra roti and raita.",
        "nutrition": {
            "carbs": 45.71,
            "proteins": 31.43,
            "fats": 22.86
        }
    },
    "17-17.5": {
        "breakfast": "Ragi porridge with jaggery and almonds.",
        "lunch": "Paneer tikka masala with whole wheat roti and salad.",
        "dinner": "Vegetable stew with appam.",
        "nutrition": {
            "carbs": 46.67,
            "proteins": 30.00,
            "fats": 23.33
        }
    },
    "17.5-18": {
        "breakfast": "Millet idli with sambar and coconut chutney.",
        "lunch": "Tofu stir-fry with rice noodles and sesame sauce.",
        "dinner": "Vegetable biryani with raita and papad.",
        "nutrition": {
            "carbs": 44.44,
            "proteins": 33.33,
            "fats": 22.22
        }
    },
    "18-18.5": {
        "breakfast": "Quinoa upma with coconut chutney and a glass of lemon water.",
        "lunch": "Fish curry with brown rice and cucumber salad.",
        "dinner": "Soya chunks curry with whole wheat roti.",
        "nutrition": {
            "carbs": 46.67,
            "proteins": 30.00,
            "fats": 23.33
        }
    },
    "18.5-19": {
        "breakfast": "Oats idli with sambar and a side of coconut chutney.",
        "lunch": "Chicken curry with millet roti and green salad.",
        "dinner": "Rajma (kidney beans) curry with brown rice and raita.",
        "nutrition": {
            "carbs": 44.00,
            "proteins": 33.00,
            "fats": 23.00
        }
    },
    "19-19.5": {
        "breakfast": "Vegetable dalia with buttermilk.",
        "lunch": "Grilled paneer with a side of roti and salad.",
        "dinner": "Vegetable biryani with cucumber raita.",
        "nutrition": {
            "carbs": 45.45,
            "proteins": 31.82,
            "fats": 22.73
        }
    },
    "19.5-20": {
        "breakfast": "Multigrain bread sandwich with paneer and vegetables.",
        "lunch": "Grilled chicken salad with olive oil dressing.",
        "dinner": "Lentil soup with quinoa and a side salad.",
        "nutrition": {
            "carbs": 47.62,
            "proteins": 30.95,
            "fats": 21.43
        }
    },
    "20-20.5": {
        "breakfast": "Vegetable upma with a glass of buttermilk.",
        "lunch": "Chicken stew with brown rice and cucumber salad.",
        "dinner": "Grilled fish with sautéed spinach.",
        "nutrition": {
            "carbs": 48.00,
            "proteins": 29.00,
            "fats": 23.00
        }
    },
    "20.5-21": {
        "breakfast": "Ragi dosa with coconut chutney.",
        "lunch": "Vegetable dal khichdi with roasted papad.",
        "dinner": "Paneer bhurji with bajra roti and a small salad.",
        "nutrition": {
            "carbs": 46.67,
            "proteins": 30.00,
            "fats": 23.33
        }
    },
    "21-21.5": {
        "breakfast": "Moong dal dosa with sambar and chutney.",
        "lunch": "Grilled chicken wrap with hummus and salad.",
        "dinner": "Masoor dal with brown rice and steamed vegetables.",
        "nutrition": {
            "carbs": 45.71,
            "proteins": 31.43,
            "fats": 22.86
        }
    },
    "21.5-22": {
        "breakfast": "Vegetable oats with green chutney.",
        "lunch": "Mixed vegetable curry with whole wheat roti.",
        "dinner": "Chicken curry with millet rice and cucumber salad.",
        "nutrition": {
            "carbs": 47.37,
            "proteins": 30.00,
            "fats": 22.63
        }
    },
    "22-22.5": {
        "breakfast": "Besan chilla with curd and mint chutney.",
        "lunch": "Fish curry with brown rice and a green salad.",
        "dinner": "Grilled chicken tikka with a side of steamed vegetables.",
        "nutrition": {
            "carbs": 45.00,
            "proteins": 32.50,
            "fats": 22.50
        }
    },
    "22.5-23": {
        "breakfast": "Vegetable dalia with a glass of fresh juice.",
        "lunch": "Grilled tofu with quinoa and a green salad.",
        "dinner": "Lentil soup with roasted vegetables.",
        "nutrition": {
            "carbs": 47.00,
            "proteins": 31.00,
            "fats": 22.00
        }
    },
    "23-23.5": {
        "breakfast": "Smoothie bowl with spinach, banana, and chia seeds.",
        "lunch": "Vegetable stir-fry with tofu and brown rice.",
        "dinner": "Oats and vegetable khichdi with cucumber salad.",
        "nutrition": {
            "carbs": 46.00,
            "proteins": 32.00,
            "fats": 22.00
        }
    },
    "23.5-24": {
        "breakfast": "Masala oats with a boiled egg and lemon water.",
        "lunch": "Soya chunks curry with brown rice and salad.",
        "dinner": "Vegetable soup with moong dal chilla.",
        "nutrition": {
            "carbs": 48.00,
            "proteins": 30.00,
            "fats": 22.00
        }
    },
    "24-24.5": {
        "breakfast": "Idli with sambar and coconut chutney.",
        "lunch": "Grilled paneer with whole wheat roti and salad.",
        "dinner": "Vegetable stew with steamed brown rice.",
        "nutrition": {
            "carbs": 47.00,
            "proteins": 31.00,
            "fats": 22.00
        }
    },
    "24.5-25": {
        "breakfast": "Poha with peanuts and a glass of buttermilk.",
        "lunch": "Chickpea salad with cucumber, tomatoes, and mint chutney.",
        "dinner": "Lentil soup with quinoa and a green salad.",
        "nutrition": {
            "carbs": 46.67,
            "proteins": 31.11,
            "fats": 22.22
        }
    },
    "25-25.5": {
        "breakfast": "Vegetable upma with a glass of buttermilk.",
        "lunch": "Chicken stew with brown rice and cucumber salad.",
        "dinner": "Grilled fish with sautéed spinach.",
        "nutrition": {
            "carbs": 48.00,
            "proteins": 30.00,
            "fats": 22.00
        }
    },
    "25.5-26": {
        "breakfast": "Ragi dosa with coconut chutney.",
        "lunch": "Vegetable dal khichdi with roasted papad.",
        "dinner": "Paneer bhurji with bajra roti and a small salad.",
        "nutrition": {
            "carbs": 47.00,
            "proteins": 32.00,
            "fats": 21.00
        }
    },
    "26-26.5": {
        "breakfast": "Moong dal dosa with sambar and chutney.",
        "lunch": "Grilled chicken wrap with hummus and salad.",
        "dinner": "Masoor dal with brown rice and steamed vegetables.",
        "nutrition": {
            "carbs": 46.00,
            "proteins": 32.00,
            "fats": 22.00
        }
    },
    "26.5-27": {
        "breakfast": "Vegetable oats with green chutney.",
        "lunch": "Mixed vegetable curry with whole wheat roti.",
        "dinner": "Tandoori chicken with sautéed spinach.",
        "nutrition": {
            "carbs": 47.00,
            "proteins": 31.00,
            "fats": 22.00
        }
    },
    "27-27.5": {
        "breakfast": "Besan chilla with curd and mint chutney.",
        "lunch": "Fish curry with brown rice and a green salad.",
        "dinner": "Grilled chicken tikka with a side of steamed vegetables.",
        "nutrition": {
            "carbs": 45.00,
            "proteins": 32.50,
            "fats": 22.50
        }
    },
    "27.5-28": {
        "breakfast": "Vegetable dalia with a glass of fresh juice.",
        "lunch": "Grilled tofu with quinoa and a green salad.",
        "dinner": "Lentil soup with roasted vegetables.",
        "nutrition": {
            "carbs": 47.00,
            "proteins": 31.00,
            "fats": 22.00
        }
    },
    "28-28.5": {
        "breakfast": "Smoothie bowl with spinach, banana, and chia seeds.",
        "lunch": "Vegetable stir-fry with tofu and brown rice.",
        "dinner": "Oats and vegetable khichdi with cucumber salad.",
        "nutrition": {
            "carbs": 46.00,
            "proteins": 32.00,
            "fats": 22.00
        }
    },
    "28.5-29": {
        "breakfast": "Masala oats with a boiled egg and lemon water.",
        "lunch": "Soya chunks curry with brown rice and salad.",
        "dinner": "Vegetable soup with moong dal chilla.",
        "nutrition": {
            "carbs": 48.00,
            "proteins": 30.00,
            "fats": 22.00
        }
    },
    "29-29.5": {
        "breakfast": "Idli with sambar and coconut chutney.",
        "lunch": "Grilled paneer with whole wheat roti and salad.",
        "dinner": "Vegetable stew with steamed brown rice.",
        "nutrition": {
            "carbs": 47.00,
            "proteins": 31.00,
            "fats": 22.00
        }
    },
    "29.5-30": {
        "breakfast": "Poha with peanuts and a glass of buttermilk.",
        "lunch": "Chickpea salad with cucumber, tomatoes, and mint chutney.",
        "dinner": "Lentil soup with quinoa and a green salad.",
        "nutrition": {
            "carbs": 46.67,
            "proteins": 31.11,
            "fats": 22.22
        }
    },
    "30-30.5": {
        "breakfast": "Vegetable upma with a glass of buttermilk.",
        "lunch": "Chicken stew with brown rice and cucumber salad.",
        "dinner": "Grilled fish with sautéed spinach.",
        "nutrition": {
            "carbs": 48.00,
            "proteins": 30.00,
            "fats": 22.00
        }
    },
    "30.5-31": {
        "breakfast": "Ragi dosa with coconut chutney.",
        "lunch": "Vegetable dal khichdi with roasted papad.",
        "dinner": "Paneer bhurji with bajra roti and a small salad.",
        "nutrition": {
            "carbs": 47.00,
            "proteins": 32.00,
            "fats": 21.00
        }
    },
    "31-31.5": {
        "breakfast": "Moong dal dosa with sambar and chutney.",
        "lunch": "Grilled chicken wrap with hummus and salad.",
        "dinner": "Masoor dal with brown rice and steamed vegetables.",
        "nutrition": {
            "carbs": 46.00,
            "proteins": 32.00,
            "fats": 22.00
        }
    },
    "31.5-32": {
        "breakfast": "Vegetable oats with green chutney.",
        "lunch": "Mixed vegetable curry with whole wheat roti.",
        "dinner": "Tandoori chicken with sautéed spinach.",
        "nutrition": {
            "carbs": 47.00,
            "proteins": 31.00,
            "fats": 22.00
        }
    },
    "32-32.5": {
        "breakfast": "Besan chilla with curd and mint chutney.",
        "lunch": "Fish curry with brown rice and a green salad.",
        "dinner": "Grilled chicken tikka with a side of steamed vegetables.",
        "nutrition": {
            "carbs": 45.00,
            "proteins": 32.50,
            "fats": 22.50
        }
    },
    "32.5-33": {
        "breakfast": "Vegetable dalia with a glass of fresh juice.",
        "lunch": "Grilled tofu with quinoa and a green salad.",
        "dinner": "Lentil soup with roasted vegetables.",
        "nutrition": {
            "carbs": 47.00,
            "proteins": 31.00,
            "fats": 22.00
        }
    },
    "33-33.5": {
        "breakfast": "Smoothie bowl with spinach, banana, and chia seeds.",
        "lunch": "Vegetable stir-fry with tofu and brown rice.",
        "dinner": "Oats and vegetable khichdi with cucumber salad.",
        "nutrition": {
            "carbs": 46.00,
            "proteins": 32.00,
            "fats": 22.00
        }
    },
    "33.5-34": {
        "breakfast": "Masala oats with a boiled egg and lemon water.",
        "lunch": "Soya chunks curry with brown rice and salad.",
        "dinner": "Vegetable soup with moong dal chilla.",
        "nutrition": {
            "carbs": 48.00,
            "proteins": 30.00,
            "fats": 22.00
        }
    },
    "34-34.5": {
        "breakfast": "Idli with sambar and coconut chutney.",
        "lunch": "Grilled paneer with whole wheat roti and salad.",
        "dinner": "Vegetable stew with steamed brown rice.",
        "nutrition": {
            "carbs": 47.00,
            "proteins": 31.00,
            "fats": 22.00
        }
    },
    "34.5-35": {
        "breakfast": "Poha with peanuts and a glass of buttermilk.",
        "lunch": "Chickpea salad with cucumber, tomatoes, and mint chutney.",
        "dinner": "Lentil soup with quinoa and a green salad.",
        "nutrition": {
            "carbs": 46.67,
            "proteins": 31.11,
            "fats": 22.22
        }
    }
}
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/reccrecipies')
def reccrecipies():
    return render_template('reccrecipies.html')

# Login Route
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        em = request.form.get('email')
        pwd = request.form.get('password')

        try:
            m = mysql.connector.connect(host="localhost", user="root", passwd="", database='mydatabase')
            cursor = m.cursor()

            query = "SELECT * FROM user WHERE email = %s AND password = %s"
            cursor.execute(query, (em, pwd))
            user = cursor.fetchone()

            cursor.close()
            m.close()

            if user:
                session['user'] = em  # Save user email in session
                return render_template('bmi.html')
            else:
                return render_template('login.html', message="Invalid credentials!")
        except mysql.connector.Error as err:
            return render_template('login.html', message=f"Error: {err}")
    else:
        return render_template('login.html')

# Signup Route
@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        em = request.form.get('email')
        pwd = request.form.get('password')

        try:
            m = mysql.connector.connect(host="localhost", user="root", passwd="", database='mydatabase')
            cursor = m.cursor()

            query = "INSERT INTO user (Username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, em, pwd))
            m.commit()

            cursor.close()
            m.close()

            return render_template('login.html', message="Signup successful!")
        except mysql.connector.Error as err:
            return render_template('register.html', message=f"Error: {err}")
    else:
        return render_template('register.html')

# BMI Route (Accessible after login)
@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    if 'user' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    if request.method == 'POST':
        # Get user input
        # Get user input
        age = int(request.form['age'])
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        gender = request.form['gender']

    # Convert gender to numeric value (e.g., 0 for Male, 1 for Female)
        gender_map = {'Male': 0, 'Female': 1}
        gender_numeric = gender_map.get(gender, -1)

    # Calculate BMI for the user input
        bmi_user = weight / (height ** 2)
        print(f"User BMI: {bmi_user:.2f}")
        bmi_user_str = f"{bmi_user:.2f}"

    # Prepare user input as an array (not strictly necessary for BMI matching)
        user_input = np.array([age, weight, height, gender_numeric]).reshape(1, -1)

        # Convert gender in dataset to numeric if necessary
        df['gender_numeric'] = df['gender'].map(gender_map).fillna(-1)

    # Find the closest BMI from the dataset
        df['bmi_difference'] = abs(df['BMI'] - bmi_user)
        closest_index = df['bmi_difference'].idxmin()

    # Debug: Print out the closest record and its label
        print(f"User Input BMI: {bmi_user}")
        print(f"Closest Record BMI: {df.iloc[closest_index]['BMI']}")
        print(f"Closest Label: {df.iloc[closest_index]['Label']}")

    # Get the label from the closest record
        closest_record = df.iloc[closest_index]
        label = closest_record['Label']

    # Assign the diet plan based on the label
        diet_plan = diet_plans.get(label, "No specific diet plan available")


        # Map BMI to recipe range
        if 12 <= bmi_user < 12.5:
            recipe_plan = recipe_plans.get('12-12.5', {})
        elif 12.5 <= bmi_user < 13:
            recipe_plan = recipe_plans.get('12.5-13', {})
        elif 13 <= bmi_user < 13.5:
            recipe_plan = recipe_plans.get('13-13.5', {})
        elif 13.5 <= bmi_user < 14:
            recipe_plan = recipe_plans.get('13.5-14', {})
        elif 14 <= bmi_user < 14.5:
            recipe_plan = recipe_plans.get('14-14.5', {})
        elif 14.5 <= bmi_user < 15:
            recipe_plan = recipe_plans.get('14.5-15', {})
        elif 15 <= bmi_user < 15.5:
            recipe_plan = recipe_plans.get('15-15.5', {})
        elif 15.5 <= bmi_user < 16:
            recipe_plan = recipe_plans.get('15.5-16', {})
        elif 16 <= bmi_user < 16.5:
            recipe_plan = recipe_plans.get('16-16.5', {})
        elif 16.5 <= bmi_user < 17:
            recipe_plan = recipe_plans.get('16.5-17', {})
        elif 17 <= bmi_user < 17.5:
            recipe_plan = recipe_plans.get('17-17.5', {})
        elif 17.5 <= bmi_user < 18:
            recipe_plan = recipe_plans.get('17.5-18', {})
        elif 18 <= bmi_user < 18.5:
            recipe_plan = recipe_plans.get('18-18.5', {})
        elif 18.5 <= bmi_user < 19:
            recipe_plan = recipe_plans.get('18.5-19', {})
        elif 19 <= bmi_user < 19.5:
            recipe_plan = recipe_plans.get('19-19.5', {})
        elif 19.5 <= bmi_user < 20:
            recipe_plan = recipe_plans.get('19.5-20', {})
        elif 20 <= bmi_user < 20.5:
            recipe_plan = recipe_plans.get('20-20.5', {})
        elif 20.5 <= bmi_user < 21:
            recipe_plan = recipe_plans.get('20.5-21', {})
        elif 21 <= bmi_user < 21.5:
            recipe_plan = recipe_plans.get('21-21.5', {})
        elif 21.5 <= bmi_user < 22:
            recipe_plan = recipe_plans.get('21.5-22', {})
        elif 22 <= bmi_user < 22.5:
            recipe_plan = recipe_plans.get('22-22.5', {})
        elif 22.5 <= bmi_user < 23:
            recipe_plan = recipe_plans.get('22.5-23', {})
        elif 23 <= bmi_user < 23.5:
            recipe_plan = recipe_plans.get('23-23.5', {})
        elif 23.5 <= bmi_user < 24:
            recipe_plan = recipe_plans.get('23.5-24', {})
        elif 24 <= bmi_user < 24.5:
            recipe_plan = recipe_plans.get('24-24.5', {})
        elif 24.5 <= bmi_user < 25:
            recipe_plan = recipe_plans.get('24.5-25', {})
        elif 25 <= bmi_user < 25.5:
            recipe_plan = recipe_plans.get('25-25.5', {})
        elif 25.5 <= bmi_user < 26:
            recipe_plan = recipe_plans.get('25.5-26', {})
        elif 26 <= bmi_user < 26.5:
            recipe_plan = recipe_plans.get('26-26.5', {})
        elif 26.5 <= bmi_user < 27:
            recipe_plan = recipe_plans.get('26.5-27', {})
        elif 27 <= bmi_user < 27.5:
            recipe_plan = recipe_plans.get('27-27.5', {})
        elif 27.5 <= bmi_user < 28:
            recipe_plan = recipe_plans.get('27.5-28', {})
        elif 28 <= bmi_user < 28.5:
            recipe_plan = recipe_plans.get('28-28.5', {})
        elif 28.5 <= bmi_user < 29:
            recipe_plan = recipe_plans.get('28.5-29', {})
        elif 29 <= bmi_user < 29.5:
            recipe_plan = recipe_plans.get('29-29.5', {})
        elif 29.5 <= bmi_user < 30:
            recipe_plan = recipe_plans.get('29.5-30', {})
        elif 30 <= bmi_user < 30.5:
            recipe_plan = recipe_plans.get('30-30.5', {})
        elif 30.5 <= bmi_user < 31:
            recipe_plan = recipe_plans.get('30.5-31', {})
        elif 31 <= bmi_user < 31.5:
            recipe_plan = recipe_plans.get('31-31.5', {})
        elif 31.5 <= bmi_user < 32:
            recipe_plan = recipe_plans.get('31.5-32', {})
        elif 32 <= bmi_user < 32.5:
            recipe_plan = recipe_plans.get('32-32.5', {})
        elif 32.5 <= bmi_user < 33:
            recipe_plan = recipe_plans.get('32.5-33', {})
        elif 33 <= bmi_user < 33.5:
            recipe_plan = recipe_plans.get('33-33.5', {})
        elif 33.5 <= bmi_user < 34:
            recipe_plan = recipe_plans.get('33.5-34', {})
        elif 34 <= bmi_user < 34.5:
            recipe_plan = recipe_plans.get('34-34.5', {})
        elif 34.5 <= bmi_user < 35:
            recipe_plan = recipe_plans.get('34.5-35', {})
        else:
            recipe_plan = {}

        return render_template('dietpage.html', bmi_user=bmi_user_str, diet_plan=diet_plan, recipe_plan=recipe_plan ,  nutrition=recipe_plan.get('nutrition', {}))
    return render_template('bmi.html')

# # Logout Route
# @app.route('/logout')
# def logout():
#     session.pop('user', None)  # Clear the session
#     return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
