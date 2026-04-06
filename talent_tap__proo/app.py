from flask import Flask, request, render_template_string

app = Flask(__name__)

# ----- DATA -----
users = [
    {"username": "Sanket", "password": "123", "skills": ["Python","UI"], "name":"Sanket Chinthala"}
]

projects = [
    {"title": "AI Startup", "skills": ["Python","AI"]},
    {"title": "UI App", "skills": ["Design","Frontend"]}
]

# ----- HTML INLINE -----
html_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Smart Campus App</title>
    <style>
        body { font-family: Arial; padding:20px; background:#f5f5f5; }
        input, button { padding:8px; margin:5px 0; width:100%; }
        h2,h3 { color:#333; }
        .card { border:1px solid #ccc; padding:10px; margin:10px 0; border-radius:5px; }
    </style>
</head>
<body>
<div class="container">

{% if not user %}
<h2>Login</h2>
{% if error %}<p style="color:red">{{ error }}</p>{% endif %}
<form method="POST">
    <input type="text" name="username" placeholder="Username" required>
    <input type="password" name="password" placeholder="Password" required>
    <button type="submit">Login</button>
</form>
{% endif %}

{% if user %}
<h2>Dashboard</h2>
<p>Welcome {{ user.name }}</p>

<h3>Project Matches</h3>
{% for p in matches %}
<div class="card">
<strong>{{ p.project }}</strong> - Match: {{ p.match }}%
</div>
{% endfor %}

<h3>Profile</h3>
<p>Name: {{ user.name }}</p>
<p>Skills: {{ user.skills | join(', ') }}</p>

<h3>DigiLocker Verification</h3>
<p>Status: Verified ✅</p>

<h3>Badges</h3>
<p>AI Project, UI App</p>

<h3>Chat (Demo)</h3>
<p>Front-end chat only</p>
<input type="text" placeholder="Type message">
<button>Send</button>
{% endif %}

</div>
</body>
</html>
"""

# ----- HELPERS -----
def get_user(username):
    for u in users:
        if u["username"].lower() == username.lower():
            return u
    return None

def match_score(user_skills, project_skills):
    matched = set(user_skills).intersection(set(project_skills))
    return round((len(matched)/len(project_skills))*100, 2)

# ----- ROUTES -----
@app.route("/", methods=["GET","POST"])
def index():
    error = None
    user = None
    matches = []
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        user = get_user(username)
        if user and user["password"] == password:
            matches = [{"project": p["title"], "match": match_score(user["skills"], p["skills"])} for p in projects]
        else:
            error = "Invalid credentials"
            user = None
    return render_template_string(html_page, user=user, matches=matches, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=5000)