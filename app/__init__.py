# ===========================================================
# YOUR PROJECT TITLE HERE
# YOUR NAME HERE
# -----------------------------------------------------------
# BRIEF DESCRIPTION OF YOUR PROJECT HERE
# ===========================================================


from flask import Flask, render_template, request, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import html
import base64

from app.helpers.session import init_session
from app.helpers.db import connect_db
from app.helpers.errors import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.auth import login_required
from app.helpers.time import init_datetime, utc_timestamp, utc_timestamp_now
from io import BytesIO
from PIL import Image


# Create the app
app = Flask(__name__)

# Configure app
init_session(app)  # Setup a session for messages, etc.
init_logging(app)  # Log requests
init_error(app)  # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps


# -----------------------------------------------------------
# Home page route
# -----------------------------------------------------------
@app.get("/")
def index():
    # When logged in show the projects list
    # Otherwise show the generic home page for onboarding
    if "logged_in" in session:
        with connect_db() as client:
            # Select all entries where the user is either assigned to the project or the owner of the project
            sql = """
                SELECT DISTINCT 
                    p.*,
                    m.active,
                    m.invited
                FROM projects p
                LEFT JOIN member_of m ON p.id = m.project
                WHERE m.user = ? OR p.owner = ?
                ORDER BY
                    CASE WHEN p.owner = ? THEN 0 ELSE 1 END,
                    p.name ASC;
            """
            params = [session["userid"], session["userid"], session["userid"]]
            result = client.execute(sql, params)

            # Encode image data to base64 for each project
            projects = []
            for row in result.rows:
                # Access fields explicitly
                icon_data = row["icon_data"]
                icon_mime = row["icon_mime"]

                if icon_data:
                    icon_b64 = base64.b64encode(icon_data).decode("utf-8")
                else:
                    icon_b64 = None

                projects.append(
                    {
                        "id": row["id"],
                        "name": row["name"],
                        "owner": row["owner"],
                        "active": row["active"],
                        "invited": row["invited"],
                        "icon_data": icon_b64,
                        "icon_mime": icon_mime,
                    }
                )

            return render_template("pages/home-projects.jinja", projects=projects)
    else:
        return render_template("pages/home.jinja")


# -----------------------------------------------------------
# Thing page route - Show details of a single thing
# -----------------------------------------------------------
@app.get("/project/<int:id>")
@login_required
def project(id):
    with connect_db() as client:
        # Check if the user is a member of the project or the owner
        sql = """
            SELECT 1
            FROM projects p
            LEFT JOIN member_of m ON p.id = m.project AND m.user = ?
            WHERE p.id = ? 
                AND (p.owner = ? OR m.user IS NOT NULL)
            LIMIT 1;
        """
        params = [session["userid"], id, session["userid"]]
        result = client.execute(sql, params)
        if not result.rows:
            flash("You do not have access to that project", "error")
            return redirect("/")

        # Get all information about the project
        sql = """SELECT * FROM projects WHERE id = ?"""
        params = [id]
        project = client.execute(sql, params)
        # Will need to redo the joins and such when implementing categories and groups
        # Will probably move this to a separate root for categories
        sql = """
            SELECT 
                t.id                AS task_id,
                t.name              AS task_name,
                t.priority          AS task_priority,
                t.description       AS task_description,
                t.created_timestamp AS task_created_timestamp,
                t.completed_timestamp AS task_completed_timestamp,
                t.deadline_timestamp  AS task_deadline_timestamp,
                GROUP_CONCAT(u.id) AS assigned_users
            FROM tasks t
            LEFT JOIN assigned_to a
                ON a.task = t.id
            LEFT JOIN users u
                ON u.id = a.user
            WHERE t."group" = ?
            GROUP BY 
                t.id, t.name, t.priority, t.description, 
                t.created_timestamp, t.completed_timestamp, t.deadline_timestamp;
        """
        params = [id]
        tasks = client.execute(sql, params)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            return render_template("pages/project.jinja", project=result.rows[0])

        else:
            # No, so show error
            return not_found_error()


# Crop the image to 1:1 from the center
def crop_center(img: Image.Image) -> Image.Image:
    width, height = img.size
    if width == height:
        return img
    new_side = min(width, height)
    left = (width - new_side) // 2
    top = (height - new_side) // 2
    right = left + new_side
    bottom = top + new_side
    return img.crop((left, top, right, bottom))


# -----------------------------------------------------------
# Route for adding a thing, using data posted from a form
# - Restricted to logged in users
# -----------------------------------------------------------
@app.post("/project")
@login_required
def create_project():
    # Get the data from the form
    name = request.form.get("name")
    image_file = request.files.get("image")

    # Sanitise the text inputs
    name = html.escape(name)

    # Extract the image data if possible
    image_data = None
    image_mime = None

    if image_file and image_file.filename != "":
        try:
            # Resize to 256x256 using Pillow
            img = (
                crop_center(Image.open(image_file))
                .convert("RGBA")
                .resize((256, 256), Image.Resampling.LANCZOS)
            )

            # Save as a PNG
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)

            image_data = buffer.read()
            image_mime = "image/png"

            # image_data = image_file.read()  # store raw binary
            # image_mime = image_file.mimetype  # e.g. "image/png"
        except:
            flash("Invalid image upload", "error")

    # Get the user id from the session
    userid = session["userid"]

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO projects (name, owner, icon_data, icon_mime) VALUES (?, ?, ?, ?)"
        params = [name, userid, image_data, image_mime]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Project '{name}' created", "success")
        return redirect("/")


# -----------------------------------------------------------
# Route for deleting a thing, Id given in the route
# - Restricted to logged in users
# -----------------------------------------------------------
# @app.get("/delete/<int:id>")
# @login_required
# def delete_a_thing(id):
#     # Get the user id from the session
#     user_id = session["user_id"]

#     with connect_db() as client:
#         # Delete the thing from the DB only if we own it
#         sql = "DELETE FROM things WHERE id=? AND user_id=?"
#         params = [id, user_id]
#         client.execute(sql, params)

#         # Go back to the home page
#         flash("Thing deleted", "success")
#         return redirect("/things")


# -----------------------------------------------------------
# User registration form route
# -----------------------------------------------------------
@app.get("/user/register")
def register_form():
    return render_template("pages/user-register.jinja")


# -----------------------------------------------------------
# User login form route
# -----------------------------------------------------------
@app.get("/user/login")
def login_form():
    return render_template("pages/user-login.jinja")


# -----------------------------------------------------------
# Route for adding a user when registration form submitted
# -----------------------------------------------------------
@app.post("/user/new")
def add_user():
    # Get the data from the form
    username = request.form.get("username")
    password = request.form.get("password")

    # Salt and hash the password
    hash = generate_password_hash(password)

    with connect_db() as client:
        # Attempt to add this user to the database
        sql = "INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)"
        values = [username, hash]
        result = client.execute(sql, values)

        if result.rows_affected == 0:
            # Handle if a username is already taken
            flash("Username already taken.", "error")
            return redirect("/register")
        else:
            # Sign the user in immediately
            session["userid"] = result.last_insert_rowid
            session["username"] = username
            session["logged_in"] = True
            session.permanent = True

            flash(f"User {username} registered successfully", "success")
            return redirect("/")


# -----------------------------------------------------------
# Route for processing a user login
# -----------------------------------------------------------
@app.post("/user/login")
def login_user():
    # Get the login form data
    username = request.form.get("username")
    password = request.form.get("password")
    remember = request.form.get("remember")

    with connect_db() as client:
        # Attempt to find a record for that user
        sql = "SELECT * FROM users WHERE username = ?"
        params = [username]
        result = client.execute(sql, params)

        # Did we find a record?
        if result.rows:
            # Yes, so check password
            user = result.rows[0]
            hash = user["password_hash"]

            # Hash matches?
            if check_password_hash(hash, password):
                # Yes, so save info in the session
                session["userid"] = user["id"]
                session["username"] = user["username"]
                session["logged_in"] = True

                if remember:
                    session.permanent = True
                else:
                    session.permanent = False

                # And head back to the home page
                flash("Login successful", "success")
                return redirect("/")

        # Either username not found, or password was wrong
        flash("Invalid credentials", "error")
        return redirect("/login")


# -----------------------------------------------------------
# Route for processing a user logout
# -----------------------------------------------------------
@app.get("/user/logout")
def logout():
    # Clear the details from the session
    session.pop("userid", None)
    session.pop("username", None)
    session.pop("logged_in", None)

    # And head back to the home page
    flash("Logged out successfully", "success")
    return redirect("/")
