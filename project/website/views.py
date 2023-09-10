from flask import Blueprint, render_template, url_for, request, flash, redirect, jsonify
from flask_login import login_required, current_user
from .models import Task, User
import json
from website import db
import datetime
views = Blueprint('views', __name__) # views é o que é importado no init

status_options = ['None', 'ToDo', 'Done', 'Postponed', 'Deleted']

@views.route('/', methods=['GET'])
@login_required
def home():
    if request.method == 'GET':
        tasks  = Task.query.filter(Task.public == True, Task.user_id == current_user.id).all()
        for task in tasks: 
            print(task.name, task.public)
        return render_template("index.html", user=current_user, tasks=tasks, status_options=status_options)
@views.route('/filter', methods=['GET'])
@login_required
def filter_tasks():
    status_selected = request.args.get('status')
    
    if status_selected and status_selected != 'None':
        if status_selected == 'Deleted': 
            filtered_tasks = Task.query.filter(
                Task.public == False,
                Task.user_id == current_user.id
            ).all()
        else: 
            filtered_tasks = Task.query.filter(
            Task.public == True,
            Task.user_id == current_user.id,
            Task.status == status_selected
        ).all()
    else:
        filtered_tasks = Task.query.filter(
            Task.public == True,
            Task.user_id == current_user.id
        ).all()
    
    
    return render_template("index.html", user=current_user, tasks=filtered_tasks, status_options=status_options)


@views.route('/delete-task', methods=['POST'])
def delete_task():
    data = json.loads(request.data)
    task_id = data['taskId']
    task = Task.query.get(task_id)
    if task:
        if task.user_id == current_user.id:
            if task.public == True:
                task.public = False  # Update the 'public' attribute
            else:
                 db.session.delete(task)
            db.session.commit()  # Commit the changes to the database
            flash('Task resaved', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('You cannot delete this task', category='error')
            return redirect(url_for('views.home'))
    return jsonify({})

@views.route('/revive-task', methods=['POST'])
def revive_task():
    data = json.loads(request.data)
    task_id = data['taskId']
    task = Task.query.get(task_id)
    if task:
        if task.user_id == current_user.id:
            task.public = True  # Update the 'public' attribute
            db.session.commit()  # Commit the changes to the database
            flash('Task revived', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('You cannot revive this task', category='error')
            return redirect(url_for('views.home'))
    return jsonify({})




@views.route('/update-task/<int:task_id>', methods=['GET','POST'])
def update_task(task_id):
    if request.method == 'GET':
        task_to_update = Task.query.get(task_id)
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
                if status not in status_options:
                    flash('Dont try to be funny', category='error')
                    return
                task_to_update.status = status
                
                db.session.commit()
                flash('task updated', category='success')
            else:
                flash('You cannot update this task', category='error') 
        else:
             flash('Task not found', category='error') 
    return redirect(url_for('views.home'))



@views.route('/create-task', methods=['GET','POST'])
def create_task():
    if request.method == 'GET':
        
        return render_template("create.html", user=current_user)

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
        if status not in status_options:
            flash('Dont try to be funny', category='error')
            return
        new_task = Task(name=name, text=text, status= status, user_id=current_user.id, updated_at=datetime.datetime.now(), public=True)
        db.session.add(new_task)
        db.session.commit()
        flash('task added', category='success')
        return redirect(url_for('views.home'))
# @views.route('/update-task-request', methods=['POST'])
# def update_task_request():
#     if request.method == 'POST':
#         data = json.loads(request.data)
#         task_id = data['taskId']
#         return redirect(url_for('views.update_task', task_id=task_id))
