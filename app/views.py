"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os,datetime,uuid
from app import app, db
from flask import render_template, request, redirect, url_for, flash, session, abort, make_response,jsonify
from werkzeug.utils import secure_filename
from form import ProfileForm
from models import UserProfile


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


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    # Instantiate your form class
    U_form = ProfileForm()
    if request.method == 'POST' and U_form.validate_on_submit():
        # collection of data from the form
        FirstName = U_form.FirstName.data
        LastName = U_form.LastName.data
        gender = U_form.gender.data
        Email = U_form.Email.data
        Location = U_form.Location.data
        Biography = U_form.Biography.data
        dateCreated = str(datetime.date.today())
    
        
        # Get file data and save to your uploads folder
        file = request.files['photo']
        imagename = secure_filename(file.filename)
        
        # Validate file upload on submit
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename))
        
        # Genertating a unquie user id
        user_ID = str(uuid.uuid3(uuid.NAMESPACE_DNS, str(FirstName)))
    
        # save data to database
        addUser = UserProfile(user_ID,FirstName,LastName,gender,Email,Location,Biography,imagename, dateCreated)
        
        db.session.add(addUser)
        db.session.commit()

        flash("Profile Successfully Created", "success")
        return redirect(url_for("profile"))
    print U_form.errors.items()

    return render_template('createProfile.html',  form = U_form)
    

@app.route('/profiles',methods=['POST','GET'])
def profiles():
    user_list = UserProfile.query.all()
    users = [{"user_ID":user.user_ID,"FirstName": user.FirstName, "LastName": user.LastName, "gender": user.gender, "Location": user.Location} for user in user_list]
    
    if request.method == 'GET':
        if user_list is not None:
            return render_template("profiles.html", users=user_list)
        else:
            flash('No Users Found', 'danger')
            return redirect(url_for("home"))

@app.route('/profiles/<userid>', methods=['POST', 'GET'])
def viewProfile(userid):
    user = UserProfile.query.filter_by(user_ID=userid).first()
    if user is not None:
        return render_template('profile.html',user=user)
    else:
        flash('Unable to view user profile', 'danger')
        return redirect(url_for('profile'))
    
    
###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,error), 'danger')

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
