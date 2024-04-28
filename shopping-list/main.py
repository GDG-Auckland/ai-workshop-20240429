from flask import Flask, render_template, request, redirect, url_for
from item import Item
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PIL.Image

app = Flask(__name__)

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-pro-vision")


shopping_dict = {}
count = 0
def generate_id():
   global count
   count += 1
   return count

@app.route("/")
def home():
    item_list = list(shopping_dict.values())
    return render_template("base.html", item_list=item_list)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    item_id = generate_id()
    new_item = Item(title=title, id=item_id)
    shopping_dict[item_id] = new_item
    return redirect(url_for("home"))

@app.route("/update/<int:item_id>")
def update(item_id):
    item = shopping_dict.get(item_id)
    if item:
      item.toggle_complete()
    return redirect(url_for("home"))


@app.route("/delete/<int:item_id>")
def delete(item_id):
    shopping_dict.pop(item_id)
    return redirect(url_for("home"))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        photo = request.files['photo']
        img = PIL.Image.open(photo)
        
        response = model.generate_content(["Identify what is in the picture.",img])
        response.resolve()
        title = response.text
        item_id = generate_id()
        new_item = Item(title=title, id=item_id)
        shopping_dict[item_id] = new_item
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)