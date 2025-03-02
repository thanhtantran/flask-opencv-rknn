from flask import session, redirect, url_for, request, render_template
from controller.modules.user import user_blu
from controller.utils.camera import VideoCamera

# Đăng nhập
@user_blu.route("/login", methods=["GET", "POST"])
def login():
    username = session.get("username")

    if username:
        return redirect(url_for("home.index"))

    if request.method == "GET":
        return render_template("login.html")
    # Lấy đăng nhập
    username = request.form.get("username")
    password = request.form.get("password")
    # Lỗi đăng nhập
    if not all([username, password]):
        return render_template("login.html", errmsg="Lỗi đăng nhập")

    # Đăng nhập
    if username == "orangepi" and password == "orangepi.vn":
        session["username"] = username
        return redirect(url_for("home.index"))

    return render_template("login.html", errmsg="Lỗi đăng nhập")


# Đăng xuất
@user_blu.route("/logout")
def logout():
    # Set session user = None
    session.pop("username", None)
    # Quay lại trang đăng nhập
    return redirect(url_for("user.login"))