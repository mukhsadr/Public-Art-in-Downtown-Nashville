from flask import Flask, render_template, request
import folium
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("file.csv")
df["Type"] = df["Type"].str.capitalize()
df["Type"] = df["Type"].replace("mural", "Mural")
tags = list(df["Type"].unique())

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        keyword = request.form["keyword"]
        search_result = df[df.apply(lambda row: row.astype(str).str.contains(keyword).any(), axis=1)]
        m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=13)
        for index, row in search_result.iterrows():
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=folium.Popup(
                    max_width=450,
                    html=f"<div style='color: black'>"
                         f"<h4>{row['Title']}</h4>"
                         f"<p style='font-size: 14px;'>{row['Description']}</p>"
                         f"<p><b>Address :</b> {row['Location']}</p>"
                         f"</div>"
                )
            ).add_to(m)
        m.save("templates/map.html")
        return render_template("index.html", map=m._repr_html_(), tags=tags)
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=13)
    for index, row in df.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=folium.Popup(
                max_width=450,
                html=f"<div style='color: black'>"
                         f"<h4>{row['Title']}</h4>"
                         f"<p style='font-size: 14px;'>{row['Description']}</p>"
                         f"<p><b>Address :</b> {row['Location']}</p>"
                         f"</div>"
            )
        ).add_to(m)
    m.save("templates/map.html")
    return render_template("index.html", map=m._repr_html_(), tags=tags)

@app.route("/update_map", methods=["GET", "POST"])
def update_map():
    tag = request.form["tag"]
    search_result = df[df["Type"] == tag]
    m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=13)
    for index, row in search_result.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=folium.Popup(
                max_width=450,
                html=f"<div style='color: black'>"
                         f"<h4>{row['Title']}</h4>"
                         f"<p style='font-size: 14px;'>{row['Description']}</p>"
                         f"<p><b>Address :</b> {row['Location']}</p>"
                         f"</div>"
            )
        ).add_to(m)
    m.save("templates/map.html")
    return render_template("index.html", map=m._repr_html_(), tags=tags)

if __name__ == "__main__":
    app.run()
