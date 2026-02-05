from flask import Flask, render_template, request, redirect, url_for
from services.ai_service import generate_bio


app=Flask(__name__)
from database import session
from models import *
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
@app.route("/pages/")
def pages():
    pages = session.query(LinkPage).all()
    return render_template("pages.html", pages=pages)

@app.route("/page/<int:id>", methods=["GET", "POST"])
def page(id):
    page=session.query(LinkPage).filter_by(id=id).one()
    links=session.query(Link).filter_by(page_id=id).all()
    return render_template("detail.html",page=page,links=links)
@app.route("/add-link/<int:page_id>", methods=["GET", "POST"])
def add_link(page_id):
    if request.method == "POST":
        name=request.form.get("name")
        url=request.form.get("url")
        category=request.form.get("category")
        if not name or not url or not url.startswith("http"):
            return redirect(url_for("page",id=page_id))
        link=Link(page_id=page_id,name=name,url=url,category=category)
        print("Link hello")
        session.add(link)
        session.commit()
        return redirect(url_for("page",id=page_id))
    else:
        return redirect(url_for("page",id=page_id))

@app.route("/create", methods=["GET", "POST"])
def create():

    if request.method == "POST":
        action = request.form.get("action")

        title = request.form.get("title")
        bio = request.form.get("bio")
        image = request.form.get("image")
        name = request.form.get("name")
        info = request.form.get("info")
        style = request.form.get("style")

        if action == "ai":
            bio = generate_bio(name, info, style)

            return render_template(
                "create.html",
                title=title,
                image=image,
                bio=bio,
                name=name,
                info=info,
                style=style
            )

        elif action == "save":
            if not bio:
                return render_template("create.html", error="Bio and Title are required",
                                       title=title, image=image, bio=bio, name=name, info=info, style=style)
            page = LinkPage(title=title, bio=bio, image=image)
            session.add(page)
            session.commit()
            return redirect(url_for("page", id=page.id))

    return render_template("create.html")


@app.route("/edit-link/<int:link_id>", methods=["GET", "POST"])
def edit_link(link_id):
    link = session.query(Link).filter_by(id=link_id).first()
    if not link:
        return redirect(url_for("pages"))

    if request.method == "POST":
        link.name = request.form.get("name")
        link.url = request.form.get("url")
        link.category = request.form.get("category")
        session.commit()
        return redirect(url_for("page", id=link.page_id))

    return render_template("edit_link.html", link=link)


@app.route("/delete-link/<int:link_id>", methods=["POST"])
def delete_link(link_id):
    link = session.query(Link).filter_by(id=link_id).first()
    if link:
        page_id = link.page_id
        session.delete(link)
        session.commit()
        return redirect(url_for("page", id=page_id))
    return redirect(url_for("pages"))

@app.route("/edit-page/<int:page_id>", methods=["GET", "POST"])
def edit_page(page_id):
    page = session.query(LinkPage).filter_by(id=page_id).first()
    if not page:
        return redirect(url_for("pages"))

    if request.method == "POST":
        page.title = request.form.get("title")
        session.commit()
        return redirect(url_for("pages"))

    return render_template("edit_page.html", page=page)
@app.route("/delete-page/<int:page_id>", methods=["POST"])
def delete_page(page_id):
    page = session.query(LinkPage).filter_by(id=page_id).first()
    if page:
        session.query(Link).filter_by(page_id=page_id).delete()
        session.delete(page)
        session.commit()
    return redirect(url_for("pages"))

if __name__=="__main__":
    app.run(debug=True)