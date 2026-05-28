from flask import Flask, render_template_string, request, redirect, url_for, session
from users import authenticate

app = Flask(__name__)
app.secret_key = "supersecretkey"

login_page = """
<h2>Login</h2>

<form method="post">
    Usuário:
    <input name="username"><br><br>

    Senha:
    <input name="password" type="password"><br><br>

    <input type="submit" value="Entrar">
</form>

{% if error %}
<p style="color:red">{{ error }}</p>
{% endif %}
"""

admin_page = """
<h2>Área Administrativa</h2>
<p>Bem-vindo administrador {{ username }}</p>

<a href="/logout">Sair</a>
"""

user_page = """
<h2>Área do Usuário</h2>
<p>Bem-vindo usuário {{ username }}</p>

<a href="/logout">Sair</a>
"""

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        user = authenticate(username, password)

        if user:

            session["user"] = user

            if user["role"] == "admin":
                return redirect(url_for("admin"))

            return redirect(url_for("user"))

        return render_template_string(
            login_page,
            error="Usuário ou senha inválidos"
        )

    return render_template_string(login_page)

@app.route("/admin")
def admin():

    user = session.get("user")

    if not user or user["role"] != "admin":
        return redirect(url_for("login"))

    return render_template_string(
        admin_page,
        username=user["username"]
    )

@app.route("/user")
def user():

    user = session.get("user")

    if not user or user["role"] != "user":
        return redirect(url_for("login"))

    return render_template_string(
        user_page,
        username=user["username"]
    )

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)