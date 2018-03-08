"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os
from app import app, UploadFolder, Allowed_Uploads
from flask import render_template, request, redirect, url_for, flash, session, abort
from werkzeug.utils import secure_filename
from form import UploadForm

@app.route('/profile', methods=['POST','GET'])
def profile():
    P_form = ProfileForm()

    if request.method == "POST":
        if P_form.validate_on_submit():

            # collection of data from the form
            FirstName = P_form.FirstName.data
            LastName = P_form.LastName.data
            gender = P_form.gender.data
            Email = P_form.Email.data
            Location = P_form.Location.data
            Biography = P_form.Biography.data
            dateCreated = datetime.date.today()
            photo = P_form.photo.data

            # Genertating a unquie user id
            user_ID = uuid.uuid3(uuid.NAMESPACE_DNS, FirstName)

             # collecting the image and checking if is a valid image
            if AllowedFile(photo.filename):
                profile_photo = secure_filename(photo.filename)
                photo.save(os.path.join(UploadFolder, profile_photo))
            else:
                flash('Incorrect File Format', 'danger')
                return redirect(url_for('profile'))

            # save data to database
            newUser = UserProfile(user_ID=user_ID,FirstName=FirstName, LastName=LastName,  gender=gender, Email=Email,
                      Location=Location, Biography=Biography, created_on=dateCreated, photo=profile_photo)
            db.session.add(newUser)
            db.session.commit()

            flash("Profile Successfully Created", "success")
            return redirect(url_for("profile"))

    """Render the website's new profile"""
    return render_template('newProfile.html', form=P_form)


@app.route('/profiles',methods=['POST','GET'])
def profiles():
    all_profile = UserProfile.query.all()
    Profile_users = [{"Email": P_user.Email, "user_ID": P_user.user_ID} for P_user in all_profile]

    if request.method == 'POST':
        if all_profile is not None:
            response = make_response(jsonify({"all_profile":Profile_users}))
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            flash('No Profile Found')
            return redirect(url_for("home"))
    return render_template("profiles.html", Profile_usersr=all_profile)




@app.route('/profile/<user_ID>', methods=['GET', 'POST'])
def view_profile(user_ID):
    getProfile = UserProfile.query.filter_by(user_ID=user_ID).first()
    if request.method == 'POST':
        if getProfile is not None:
            response = make_response
            (
            jsonify
                (
                    user_ID = getProfile.user_ID,
                    FirstName = getProfile.FirstName,
                    LastName = getProfile.LastName,
                    gender = getProfile.gender,
                    Email = getProfile.Email,
                    Location = getProfile.Location,
                    Biography = getProfile.Biography,
                    dateCreated = getProfile.dateCreated,
                    photo = getProfile.photo,
                )
            )
            response.headers['Content-Type'] = 'application/json'
            return response
        else:
            flash('User Not Found', 'danger')
            return redirect(url_for("home"))
    return render_template('profile.html', getProfile = getProfile)
    
###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
