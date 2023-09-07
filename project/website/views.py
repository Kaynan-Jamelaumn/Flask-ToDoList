from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify
from flask_login import login_required, current_user
from .models import Task, User
import json
from website import db
import datetime
views = Blueprint('views', __name__) # views é o que é importado no init

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        tasks = Task.query.filter_by(public=True, user_id=current_user.id).all()
        return render_template("index.html", user=current_user, tasks=tasks)

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('You must be logged in to add a task', category='error')
            return redirect(url_for('auth.login'))
        name = request.form.get('name')
        text = request.form.get('text')
        status = request.form.get('status')
        if not name:
            flash('name is empty', category='error')
            return
        if not text:
            flash('text is empty', category='error')
            return
        new_task = Task(name=name, text=text, status= status, user_id=current_user.id, updated_at=datetime.datetime.now())
        db.session.add(new_task)
        db.session.commit()
        flash('task added', category='success')
        return redirect(url_for('views.home'))
    

@views.route('/delete-task', methods=['POST'])
def delete_task():
    data = json.loads(request.data)
    task_id = data['taskId']
    task_to_delete = Task.query.get(task_id)
    if task_to_delete:
        if task_to_delete.user_id == current_user.id:
            task_to_delete.public = False  # Update the 'public' attribute
            db.session.commit()  # Commit the changes to the database
            flash('Task deleted', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('You cannot delete this task', category='error')
            return redirect(url_for('views.home'))
    return jsonify({})



@views.route('/update-task/<int:task_id>', methods=['GET','POST'])
def update_task(task_id):
    if request.method == 'GET':
        print("aaa")
        task_to_update = Task.query.get(task_id)
        print("z")
        return render_template("update.html", task=task_to_update)
    
    if request.method == 'POST':
        task_to_update = Task.query.get(task_id)
        if task_to_update:
            if task_to_update.user_id == current_user.id:
                name = request.form.get('name')
                text = request.form.get('text')
                status = request.form.get('status')
                if not name:
                    flash('name is empty', category='error')
                    return
                if not text:
                    flash('text is empty', category='error')
                    return
                task_to_update.name = name
                task_to_update.text = text
                task_to_update.status = status
                db.session.commit()
                flash('task updated', category='success')
            else:
                flash('You cannot update this task', category='error') 
        else:
             flash('Task not found', category='error') 
    return redirect(url_for('views.home'))

# @views.route('/update-task-request', methods=['POST'])
# def update_task_request():
#     if request.method == 'POST':
#         data = json.loads(request.data)
#         task_id = data['taskId']
#         return redirect(url_for('views.update_task', task_id=task_id))
