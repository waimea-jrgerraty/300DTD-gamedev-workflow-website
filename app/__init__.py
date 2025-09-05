# ===========================================================
# YOUR PROJECT TITLE HERE
# YOUR NAME HERE
# -----------------------------------------------------------
# BRIEF DESCRIPTION OF YOUR PROJECT HERE
# ===========================================================


from flask import (
    Response,
    Flask,
    render_template,
    send_file,
    redirect,
    jsonify,
    flash,
    request,
    session,
)
from werkzeug.security import generate_password_hash, check_password_hash
import html
import base64
import json
import os

from app.helpers.session import init_session
from app.helpers.db import connect_db
from app.helpers.errors import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.auth import login_required
from app.helpers.time import init_datetime, utc_timestamp, utc_timestamp_now
from io import BytesIO
from PIL import Image
from datetime import timedelta


# Create the app
app = Flask(__name__)

# Configure app
init_session(app)  # Setup a session for messages, etc.
init_logging(app)  # Log requests
init_error(app)  # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps


@app.template_filter("from_json")
def from_json(value):
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return []


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
# Project root route, redirect to first valid category
# -----------------------------------------------------------
@app.get("/project/<int:project_id>/")
@login_required
def project_root(project_id: int):
    # Skip for MVP
    return redirect(f"/project/{project_id}/category/1")

    with connect_db() as client:
        # Authentication is done on the category route
        sql = """
            SELECT id FROM categories
            WHERE project = ?
            ORDER BY id LIMIT 1
        """
        params = [project_id]
        result = client.execute(sql, params)

        if result.rows:
            category_id = result.rows[0]["id"]
            return redirect(f"/project/{project_id}/category/{category_id}")
        else:
            flash(
                f"Unexpected error: No categories found for project {project_id}",
                "error",
            )
            return redirect("/")


# -----------------------------------------------------------
# Project/category route, display all tasks in this category
# -----------------------------------------------------------
@app.get("/project/<int:project_id>/category/<int:category_id>")
@login_required
def category_root(project_id: int, category_id: int):
    with connect_db() as client:
        # FOR FINAL RELEASE:
        # Implement categories and groups

        # Check if the user is a member of the project or the owner
        sql = """
            SELECT 1
            FROM projects p
            LEFT JOIN member_of m ON p.id = m.project AND m.user = ?
            WHERE p.id = ? 
                AND (p.owner = ? OR m.user IS NOT NULL)
            LIMIT 1;
        """
        params = [session["userid"], project_id, session["userid"]]
        result = client.execute(sql, params)
        if not result.rows:
            flash("You do not have access to that project", "error")
            return redirect("/")

        # Get all information about the project
        sql = """SELECT * FROM projects WHERE id = ?"""
        params = [project_id]
        project = client.execute(sql, params)
        # Will need to redo the joins and such when implementing categories and groups
        # Not all selected values will be used on the category page, can be optimized later
        sql = """
            SELECT 
                t.id                AS task_id,
                t.name              AS task_name,
                t.priority          AS task_priority,
                t.description       AS task_description,
                t.created_timestamp AS task_created_timestamp,
                t.completed_timestamp AS task_completed_timestamp,
                t.deadline_timestamp  AS task_deadline_timestamp,
                COALESCE(
                    json_group_array(
                        json_object(
                            'id', u.id,
                            'username', u.username
                        )
                    ), '[]'
                ) AS assigned_users
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
        params = [project_id]
        tasks = client.execute(sql, params)

        # Did we get a result?
        if project.rows:
            # yes, so show it on the page
            return render_template(
                "pages/project.jinja",
                project=project.rows[0],
                tasks=tasks.rows,
                category={"id": 1},  # testing
            )

        else:
            # No, so show error
            return not_found_error()


# -----------------------------------------------------------
# Project/category/task route, display detailed info for this task
# -----------------------------------------------------------
@app.get("/project/<int:project_id>/category/<int:category_id>/task/<int:task_id>")
@login_required
def task_root(project_id: int, category_id: int, task_id: int):
    with connect_db() as client:
        # FOR FINAL RELEASE:
        # Implement categories and groups

        # Check if the user is a member of the project or the owner
        sql = """
            SELECT 1
            FROM projects p
            LEFT JOIN member_of m ON p.id = m.project AND m.user = ?
            WHERE p.id = ? 
                AND (p.owner = ? OR m.user IS NOT NULL)
            LIMIT 1;
        """
        params = [session["userid"], project_id, session["userid"]]
        result = client.execute(sql, params)
        if not result.rows:
            flash("You do not have access to that task", "error")
            return redirect("/")

        # Get all information about the project
        sql = """SELECT * FROM projects WHERE id = ?"""
        params = [project_id]
        project = client.execute(sql, params)
        sql = """
            SELECT 
                t.id                AS task_id,
                t.name              AS task_name,
                t.priority          AS task_priority,
                t.description       AS task_description,
                t.created_timestamp AS task_created_timestamp,
                t.completed_timestamp AS task_completed_timestamp,
                t.deadline_timestamp  AS task_deadline_timestamp,
                COALESCE(
                    json_group_array(
                        json_object(
                            'id', u.id,
                            'username', u.username
                        )
                    ), '[]'
                ) AS assigned_users
            FROM tasks t
            LEFT JOIN assigned_to a
                ON a.task = t.id
            LEFT JOIN users u
                ON u.id = a.user
            WHERE t.id = ?
            GROUP BY 
                t.id, t.name, t.priority, t.description, 
                t.created_timestamp, t.completed_timestamp, t.deadline_timestamp;
        """
        params = [task_id]
        task = client.execute(sql, params)

        # Did we get a result?
        if project.rows and task.rows:
            # yes, so show it on the page
            return render_template(
                "pages/task.jinja",
                project=project.rows[0],
                task=task.rows[0],
            )

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
# Route for adding a thing, using data posted from a form
# - Restricted to logged in users
# -----------------------------------------------------------
@app.post("/task")
@login_required
def create_task():
    # Get the data from the form
    name = request.form.get("name")
    description = request.form.get("description")
    priority = request.form.get("priority")
    deadline = request.form.get("deadline")
    group = request.form.get("group")
    project = request.form.get("project")
    category = request.form.get("category")

    # Sanitise the text inputs
    name = html.escape(name)
    description = html.escape(description)

    # Get the user id from the session
    userid = session["userid"]

    with connect_db() as client:
        # Add the thing to the DB
        sql = """
            INSERT INTO tasks 
                (name, description, priority, deadline_timestamp, "group") 
            VALUES (?, ?, ?, ?, ?)
        """
        params = [name, description, priority, deadline, group]
        result = client.execute(sql, params)
        task_id = result.last_insert_rowid

        # Assign the task to the user who created it
        sql = "INSERT INTO assigned_to (task, user) VALUES (?, ?)"
        params = [task_id, userid]
        client.execute(sql, params)

        # Go back to the project page
        flash(f"Task '{name}' created", "success")
        return redirect(f"/project/{project}/category/{category}")


# -----------------------------------------------------------
# Gets the users associated with a project for autocomplete on the front end
# -----------------------------------------------------------
@app.get("/api/project/<int:project_id>/members")
def project_members(project_id: int):
    with connect_db() as client:
        # Get all users assigned to this project
        sql = """
            SELECT u.id, u.username
            FROM users u
            JOIN member_of m ON u.id = m.user
            JOIN projects p ON p.id = m.project
            WHERE p.id = ?
            
            UNION

            SELECT u.id, u.username
            FROM users u
            JOIN projects p ON p.owner = u.id
            WHERE p.id = ?

            ORDER BY u.username;
        """
        params = [project_id, project_id]
        rows = client.execute(sql, params)

        # Convert rows to list of dicts
        members = [{"id": r["id"], "username": r["username"]} for r in rows]

    return jsonify(members)


# -----------------------------------------------------------
# Updates the description of a task
# -----------------------------------------------------------
@app.post("/api/update-description/<int:task_id>")
@login_required
def update_description(task_id: int):
    data = request.get_json()
    description = data.get("description")

    # Sanitise the text inputs
    description = html.escape(description)

    with connect_db() as client:
        # Get the project id for this task
        # sql = """
        #     SELECT p.id AS project_id
        #     FROM tasks t
        #     JOIN "group" g ON g.id = t."group"
        #     JOIN category c ON c.id = g.category
        #     JOIN project p ON p.id = c.project
        #     WHERE t.id = ?;
        # """
        # Testing without categories and groups
        sql = """
            SELECT p.id AS project_id
            FROM tasks t
            JOIN projects p ON p.id = t."group"
            WHERE t.id = ?;
        """
        params = [task_id]
        result = client.execute(sql, params)

        if not result.rows:
            return jsonify({"success": False, "error": "Task not found"}), 404

        # Check if the user is a member of the project or the owner
        sql = """
            SELECT 1
            FROM projects p
            LEFT JOIN member_of m ON p.id = m.project AND m.user = ?
            WHERE p.id = ? 
                AND (p.owner = ? OR m.user IS NOT NULL)
            LIMIT 1;
        """
        params = [session["userid"], result.rows[0]["project_id"], session["userid"]]
        result = client.execute(sql, params)

        if not result.rows:
            return jsonify({"success": False, "error": "Access denied"}), 403

        # Update the task description
        sql = "UPDATE tasks SET description = ? WHERE id = ?"
        params = [description, task_id]
        client.execute(sql, params)

    return jsonify({"success": True})


@app.post("/api/tasks/<int:task_id>/assign")
@login_required
def assign_user_to_task(task_id):
    data = request.get_json(silent=True)
    if not data or "user_id" not in data:
        return jsonify({"success": False, "error": "Missing user_id"}), 400

    user_id = data["user_id"]

    with connect_db() as client:
        # Get the project id for this task
        # sql = """
        #     SELECT p.id AS project_id
        #     FROM tasks t
        #     JOIN "group" g ON g.id = t."group"
        #     JOIN category c ON c.id = g.category
        #     JOIN project p ON p.id = c.project
        #     WHERE t.id = ?;
        # """
        # Testing without categories and groups
        sql = """
            SELECT p.id AS project_id
            FROM tasks t
            JOIN projects p ON p.id = t."group"
            WHERE t.id = ?;
        """
        params = [task_id]
        result = client.execute(sql, params)

        if not result.rows:
            return jsonify({"success": False, "error": "Task not found"}), 404

        # Check if the user is a member of the project or the owner
        sql = """
            SELECT 1
            FROM projects p
            LEFT JOIN member_of m ON p.id = m.project AND m.user = ?
            WHERE p.id = ? 
                AND (p.owner = ? OR m.user IS NOT NULL)
            LIMIT 1;
        """
        params = [session["userid"], result.rows[0]["project_id"], session["userid"]]
        result = client.execute(sql, params)

        if not result.rows:
            return jsonify({"success": False, "error": "Access denied"}), 403

        sql = """INSERT OR IGNORE INTO assigned_to (task, user) VALUES (?, ?)"""
        params = [task_id, user_id]
        result = client.execute(sql, params)

    return jsonify({"success": True, "rows_affected": result.rows_affected})


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
# Route for getting a users icon image
# -----------------------------------------------------------
@app.get("/user/<int:id>/icon")
def user_icon(id: int):
    with connect_db() as client:
        sql = "SELECT image_blob, image_mime FROM users WHERE id = ?"
        params = [id]
        result = client.execute(sql, params)

        if result.rows:
            row = result.rows[0]
            icon_data = row["image_blob"]
            icon_mime = row["image_mime"]

            if icon_data and icon_mime:
                # Stream the blob back with the correct content type and caching headers
                response = Response(icon_data, mimetype=icon_mime)
                response.headers["cache-control"] = (
                    f"public, max-age={timedelta(days=7).total_seconds()}"
                )
                return response

    # Return placeholder as a Response
    placeholder_path = os.path.join(
        app.root_path, "static", "images", "placeholder.svg"
    )
    with open(placeholder_path, "rb") as f:
        icon_data = f.read()

    response = Response(icon_data, mimetype="image/svg+xml")
    response.headers["cache-control"] = (
        f"public, max-age={timedelta(days=7).total_seconds()}"
    )
    return response


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
