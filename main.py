from flask import Flask, render_template, url_for, redirect, request, jsonify
import pandas as pd
import folium


app = Flask(__name__)
class DataItem:
    def __init__(self, title, last_name, first_name, location, medium, type, description, latitude, longitude, mapped_location):
        self.title = title
        self.last_name = last_name
        self.first_name = first_name
        self.location = location
        self.medium = medium
        self.type = type
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.mapped_location = mapped_location



if __name__ == "__main__":
    app.run(debug=True)

def read_employers_data():
    with open('employers.txt', 'r') as f:
        data = f.readlines()
    employers = []
    for line in data:
        name, email = line.strip().split(',')
        employers.append({'name': name, 'email': email})
    return employers


employers = read_employers_data()

@app.route("/")
@app.route("/home")
def home():
    df = pd.read_csv("file.csv")
    df = df.to_dict()
    d = [{"name":"jack", "email":"jack@mail.com"}]
    for item in df:
        d.append({"name":item, "email":"lol"})

    return render_template("home.html", employers=d)



@app.route("/save_new", methods=["POST"])
def save_new():
    name = request.form["name"]
    email = request.form["email"]

    with open("employers.txt", "a") as file:
        file.write("{0},{1}\n".format(name, email))
    employers.append({"name":name, "email":email})

    return redirect(url_for("home"))

@app.route("/home1")
def home1():
    df = pd.read_csv("file.csv")
    return render_template("home1.html", data=df.to_html(classes='data-table'))


@app.route("/index")
def index():
    df = pd.read_csv("file.csv")
    tags = df['Type'].unique()
    data_items = []
    for index, row in df.iterrows():
        data_item = DataItem(
            title=row['Title'],
            last_name=row['Last Name'],
            first_name=row['First Name'],
            location=row['Location'],
            medium=row['Medium'],
            type=row['Type'],
            description=row['Description'],
            latitude=row['Latitude'],
            longitude=row['Longitude'],
            mapped_location=row['Mapped Location']
        )
        data_items.append(data_item)

    map = folium.Map(location=[data_items[0].latitude, data_items[0].longitude], zoom_start=13)
    for place in data_items:
        folium.Marker(
            location = [place.latitude, place.longitude],
            tooltip = "<i>"+str(place.title)+"</i>",
            popup=folium.Popup(f"<b>"+str(place.title)+"</b><br><br>"+str(place.description)+"<br>"+"<b><i>Address: </i></b>"+str(place.location), lazy=True, parse_html=False, max_width=450, max_height=450        )


        ).add_to(map)


    return render_template("index.html", map=map._repr_html_(), types=tags)


@app.route("/search", methods=["POST"])
def search():
    search_word = request.form.get("search_word")
    df = pd.read_csv("file.csv")
    df = df[
        (df['Title'].str.contains(search_word, case=False)) |
        (df['Last Name'].str.contains(search_word, case=False)) |
        (df['First Name'].str.contains(search_word, case=False)) |
        (df['Location'].str.contains(search_word, case=False)) |
        (df['Medium'].str.contains(search_word, case=False)) |
        (df['Type'].str.contains(search_word, case=False)) |
        (df['Description'].str.contains(search_word, case=False))
    ]
    return df.to_json(orient="index")






