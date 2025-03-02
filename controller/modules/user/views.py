from flask import session, redirect, url_for, request, render_template
from controller.modules.user import user_blu
from controller.utils.camera import VideoCamera

# Dang nhap
@user_blu.route("/login", methods=["GET", "POST"])
def login():
    username = session.get("username")

    if username:
        return redirect(url_for("home.index"))

    if request.method == "GET":
        return render_template("login.html")
    # 获取参数
    username = request.form.get("username")
    password = request.form.get("password")
    # 校验参数
    if not all([username, password]):
        return render_template("login.html", errmsg="Loi dang nhap")

    # 校验对应的管理员用户数据
    if username == "cat" and password == "temppwd":
        # 验证通过
        session["username"] = username
        return redirect(url_for("home.index"))

    return render_template("login.html", errmsg="Loi dang nhap")


# Dang xuat
@user_blu.route("/logout")
def logout():
    # Set session user = None
    session.pop("username", None)
    # Quay lai trang dang nhap
    return redirect(url_for("user.login"))