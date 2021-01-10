import os
from datetime import datetime

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

from LiYunkai import app, db, Config, models
from LiYunkai.form import SignInForm, LoginForm, AddCommentForm, PersonalEditForm, AlgorithmEditForm
from LiYunkai.models import User, Post, Personal, Algorithm


@app.route('/')
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        if form.password.data == form.passwordConfirm.data:
            user_in_db = User.query.filter(User.email == form.email.data).first()
            if not user_in_db:
                username = form.username.data
                pass_hash = generate_password_hash(form.password.data)
                email = form.email.data
                user_in_db = User(username=username, email=email, password=pass_hash)
                db.session.add(user_in_db)
                db.session.commit()
                session["email"] = email
                session["username"] = username
                return redirect(url_for('main'))
            else:
                flash("This email is already registered, please Sign in or register using a different email address")
                return redirect(url_for('signin'))
        else:
            flash("Password not same, please check again")
            return redirect(url_for('signin'))
    else:
        if form.email.errors:
            form.email.render_kw = {"style": "background-color:red"}
        if form.username.errors:
            form.firstName.render_kw = {"style": "background-color:red"}
        if form.password.errors:
            form.password.render_kw = {"style": "background-color:red"}
        if form.passwordConfirm.errors:
            form.passwordConfirm.render_kw = {"style": "background-color:red"}
        return render_template('signin.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_in_db = User.query.filter(User.email == form.email.data).first()
        if not user_in_db:
            flash("Not found this user, please sign in first")
            print(1111111111111111111111)
            return redirect(url_for('login'))
        else:
            if check_password_hash(user_in_db.password, form.password.data):
                session["email"] = user_in_db.email
                session["username"] = user_in_db.username
                print(222222222222222222222)
                return redirect(url_for('main'))
            else:
                flash("Password not correct")
                print(3333333333333333333333333)
                return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)


@app.route('/main', methods=['GET', 'POST'])
def main():
    if session.get('email') is not None:
        user_in_db = User.query.filter(User.email == session.get("email")).first()
        personalInfo_in_db = Personal.query.filter(Personal.user == user_in_db).first()
        if personalInfo_in_db is not None:
            picture = personalInfo_in_db.avatar
            path = '/static/uploaded_AVATAR/' + picture
        else:
            path = '../static/img/1.jpg'
        return render_template('main.html', path=path)
    else:
        return redirect(url_for('login'))


@app.route('/personalEdit', methods=['GET', 'POST'])
def personalEdit():
    form = PersonalEditForm()
    if session.get('email') is not None:
        if form.validate_on_submit():
            user_in_db = User.query.filter(User.email == session.get("email")).first()
            stored_personalInfo = Personal.query.filter(Personal.user == user_in_db).first()
            if not stored_personalInfo:
                avatar_dir = Config.AVATAR_UPLOAD_DIR
                file_obj = form.avatar.data
                avatar_filename = session.get("username") + 'AVATAR.jpg'
                file_obj.save(os.path.join(avatar_dir, avatar_filename))
                personalInfo = Personal(nickname=form.nickname.data, fullname=form.fullname.data, birthday=form.birthday.data, presentation=form.presentation.data, gender=form.gender.data, avatar=avatar_filename, country=form.country.data, user=user_in_db)
                db.session.add(personalInfo)
            else:
                os.remove(Config.AVATAR_UPLOAD_DIR + "/" + session.get("username") + 'AVATAR.jpg')
                avatar_dir = Config.AVATAR_UPLOAD_DIR
                file_obj = form.avatar.data
                avatar_filename = session.get("username") + 'AVATAR.jpg'
                file_obj.save(os.path.join(avatar_dir, avatar_filename))
                stored_personalInfo.nickname = form.nickname.data
                stored_personalInfo.fullname = form.fullname.data
                stored_personalInfo.birthday = form.birthday.data
                stored_personalInfo.presentation = form.presentation.data
                stored_personalInfo.gender = form.gender.data
                stored_personalInfo.avatar = avatar_filename
                stored_personalInfo.country = form.country.data
            db.session.commit()
            return redirect(url_for('personal'))
        else:
            if form.nickname.errors:
                form.nickname.render_kw = {"style": "background-color:red"}
                flash("Please check the nickname")
            if form.fullname.errors:
                form.fullname.render_kw = {"style": "background-color:red"}
                flash("Please check the fullname")
            if form.birthday.errors:
                form.birthday.render_kw = {"style": "background-color:red"}
                flash("Please check the birthday")
            if form.presentation.errors:
                form.presentation.render_kw = {"style": "background-color:red"}
                flash("Please check the presentation")
            if form.gender.errors:
                form.gender.render_kw = {"style": "background-color:red"}
                flash("Please check the gender")
            if form.country.errors:
                form.country.render_kw = {"style": "background-color:red"}
                flash("Please check the country")
        return render_template('personal_edit.html', form=form)
    else:
        return redirect(url_for('login'))


@app.route('/personal')
def personal():
    if session.get('email') is not None:
        user_in_db = User.query.filter(User.email == session.get("email")).first()
        personalInfo_in_db = Personal.query.filter(Personal.user == user_in_db).first()
        if personalInfo_in_db is not None:
            picture = personalInfo_in_db.avatar
            path = '/static/uploaded_AVATAR/' + picture
        else:
            # path = '../static/img/1.jpg'
            return redirect(url_for('personalEdit'))
        information = Personal.query.filter(Personal.user == user_in_db).first()
        return render_template('personal.html', path=path, information=information, user_in_db=user_in_db)
    else:
        return redirect(url_for('login'))


@app.route('/bucket_sort', methods=['GET', 'POST'])
def bucket_sort():
    form = AddCommentForm()
    if session.get('email') is not None:
        user_in_db = User.query.filter(User.email == session.get('email')).first()
        posts = Post.query.filter(Post.post_id == 'bucket_sort').all()
        if form.validate_on_submit():
            if form.content.data is not None:
                addPost = Post(comment=form.content.data, post_id='bucket_sort', author=user_in_db)
                db.session.add(addPost)
                db.session.commit()
                flash("Add comment successful!")
                return redirect(url_for('bucket_sort'))
            else:
                flash("Comment can't be null! Please enter again...")
                return redirect(url_for('bucket_sort'))
        else:
            return render_template('Bucket_Sort.html', form=form, posts=posts)
    else:
        return redirect(url_for('login'))


@app.route('/bubble_sort', methods=['GET', 'POST'])
def bubble_sort():
    form = AddCommentForm()
    if session.get('email') is not None:
        user_in_db = User.query.filter(User.email == session.get('email')).first()
        posts = Post.query.filter(Post.post_id == 'bubble_sort').all()
        if form.validate_on_submit():
            if form.content.data is not None:
                addPost = Post(comment=form.content.data, post_id='bubble_sort', author=user_in_db)
                db.session.add(addPost)
                db.session.commit()
                flash("Add comment successful!")
                return redirect(url_for('bubble_sort'))
            else:
                flash("Comment can't be null! Please enter again...")
                return redirect(url_for('bubble_sort'))
        else:
            return render_template('Bubble_sort.html', form=form, posts=posts)
    else:
        return redirect(url_for('login'))


@app.route('/binary_search', methods=['GET', 'POST'])
def binary_search():
    form = AddCommentForm()
    if session.get('email') is not None:
        user_in_db = User.query.filter(User.email == session.get('email')).first()
        posts = Post.query.filter(Post.post_id == 'binary_search').all()
        if form.validate_on_submit():
            if form.content.data is not None:
                addPost = Post(comment=form.content.data, post_id='binary_search', author=user_in_db)
                db.session.add(addPost)
                db.session.commit()
                flash("Add comment successful!")
                return redirect(url_for('binary_search'))
            else:
                flash("Comment can't be null! Please enter again...")
                return redirect(url_for('binary_search'))
        else:
            return render_template('Binary_search.html', form=form, posts=posts)
    else:
        return redirect(url_for('login'))


@app.route('/depth_first_search', methods=['GET', 'POST'])
def depth_first_search():
    form = AddCommentForm()
    if session.get('email') is not None:
        user_in_db = User.query.filter(User.email == session.get('email')).first()
        posts = Post.query.filter(Post.post_id == 'depth_first_search').all()
        if form.validate_on_submit():
            if form.content.data is not None:
                addPost = Post(comment=form.content.data, post_id='depth_first_search', author=user_in_db)
                db.session.add(addPost)
                db.session.commit()
                flash("Add comment successful!")
                return redirect(url_for('depth_first_search'))
            else:
                flash("Comment can't be null! Please enter again...")
                return redirect(url_for('depth_first_search'))
        else:
            return render_template('Depth_first_search.html', form=form, posts=posts)
    else:
        return redirect(url_for('login'))


@app.route('/breadth_first_search', methods=['GET', 'POST'])
def breadth_first_search():
    form = AddCommentForm()
    if session.get('email') is not None:
        user_in_db = User.query.filter(User.email == session.get('email')).first()
        posts = Post.query.filter(Post.post_id == 'breadth_first_search').all()
        if form.validate_on_submit():
            if form.content.data is not None:
                addPost = Post(comment=form.content.data, post_id='breadth_first_search', author=user_in_db)
                db.session.add(addPost)
                db.session.commit()
                flash("Add comment successful!")
                return redirect(url_for('breadth_first_search'))
            else:
                flash("Comment can't be null! Please enter again...")
                return redirect(url_for('breadth_first_search'))
        else:
            return render_template('Breadth_first_search.html', form=form, posts=posts)
    else:
        return redirect(url_for('login'))


@app.route('/dynamic_programming', methods=['GET', 'POST'])
def dynamic_programming():
    form = AddCommentForm()
    if session.get('email') is not None:
        user_in_db = User.query.filter(User.email == session.get('email')).first()
        posts = Post.query.filter(Post.post_id == 'dynamic_programming').all()
        if form.validate_on_submit():
            if form.content.data is not None:
                addPost = Post(comment=form.content.data, post_id='dynamic_programming', author=user_in_db)
                db.session.add(addPost)
                db.session.commit()
                flash("Add comment successful!")
                return redirect(url_for('dynamic_programming'))
            else:
                flash("Comment can't be null! Please enter again...")
                return redirect(url_for('dynamic_programming'))
        else:
            return render_template('Dynamic_programming.html', form=form, posts=posts)
    else:
        return redirect(url_for('login'))


@app.route('/diy_algorithm_edit', methods=['GET', 'POST'])
def diy_algorithm_edit():
    form = AlgorithmEditForm()
    if session.get('email') is not None:
        if form.validate_on_submit():
            algorithm_in_db = Algorithm.query.filter(Algorithm.name == form.name.data).first()
            if algorithm_in_db is not None:
                flash('This algorithm has been create!')
                return redirect(url_for('diy_algorithm_edit'))
            else:
                code_dir = Config.CODE_UPLOAD_DIR
                file_obj = form.code_pic.data
                code_filename = form.name.data + '_CODE.jpg'
                file_obj.save(os.path.join(code_dir, code_filename))
                new_algorithm = Algorithm(name=form.name.data, code_pic=code_filename, theory=form.theory.data, complexity=form.complexity.data, application=form.application.data)
                db.session.add(new_algorithm)
                db.session.commit()
                return redirect(url_for('newAlgorithm'))
        return render_template('diy_algorithm_edit.html', form=form)
    else:
        return redirect(url_for('login'))


@app.route('/newAlgorithm', methods=['GET', 'POST'])
def newAlgorithm():
    if session.get('email') is not None:
        user_in_db = User.query.filter(User.email == session.get("email")).first()
        personalInfo_in_db = Personal.query.filter(Personal.user == user_in_db).first()
        if personalInfo_in_db is not None:
            picture = personalInfo_in_db.avatar
            path = '/static/uploaded_AVATAR/' + picture
            algorithm_in_db = Algorithm.query.filter().all()
            if algorithm_in_db is not None:
                return render_template('NewAlgorithm.html', path=path, algorithm=algorithm_in_db)
            else:
                return render_template('NewAlgorithm.html', path=path, algorithm="")
        else:
            path = '../static/img/1.jpg'
            algorithm_in_db = Algorithm.query.filter().all()
            if algorithm_in_db is not None:
                return render_template('NewAlgorithm.html', path=path, algorithm=algorithm_in_db)
            else:
                return render_template('NewAlgorithm.html', path=path, algorithm="")
    else:
        return redirect(url_for('login'))


@app.route('/diy_algorithm/<name>', methods=['GET', 'POST'])
def diy_algorithm(name):
    form = AddCommentForm()
    algorithm_in_db = Algorithm.query.filter(Algorithm.name == name).first()
    picture = algorithm_in_db.code_pic
    path = '/static/uploaded_CODE/' + picture
    user_in_db = User.query.filter(User.email == session.get('email')).first()
    posts = Post.query.filter(Post.post_id == name).all()
    if form.validate_on_submit():
        if form.content.data is not None:
            addPost = Post(comment=form.content.data, post_id=name, author=user_in_db)
            db.session.add(addPost)
            db.session.commit()
            flash("Add comment successful!")
            return redirect(url_for('diy_algorithm', name=name))
            # return render_template('diy_algorithm.html', name=name, algorithm_in_db=algorithm_in_db, path=path,
            #                        form=form, posts=posts)
        else:
            flash("Comment can't be null! Please enter again...")
            return redirect(url_for('diy_algorithm', name=name))
    else:
        return render_template('diy_algorithm.html', name=name, algorithm_in_db=algorithm_in_db, path=path, form=form, posts=posts)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))
