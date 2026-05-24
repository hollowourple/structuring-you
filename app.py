from flask import Flask,render_template,redirect,session,request,url_for,flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb  import MySQL
from config import Config

app=Flask(__name__)
app.config.from_object(Config)
mysql=MySQL(app)

@app.route('/',methods=['GET','POST'])
def userlogin():
    if request.method=='POST':
        action = request.form.get('action')
        if action == 'signup':
            return redirect(url_for('signup'))
            
        username=request.form.get("username")
        password=request.form.get("password")
        
        cur=mysql.connection.cursor()
        cur.execute('select * from users where user_name=%s',(username,))
        r=cur.fetchone()
        if r and check_password_hash(r['password'],password):
            session['user_id'] = r['user_id']
            session['username'] = r['user_name']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('userlogin.html')
        cur.close()
    return render_template('userlogin.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username=request.form.get("username")
        email=request.form.get("email")
        password=request.form.get("password")
        c_password=request.form.get("c_password")
        if(password!=c_password):
            flash('Passwords do not match!','error')
            return render_template('signup.html')
        cur=mysql.connection.cursor()
        cur.execute('select * from users where user_name=%s',(username,))
        r=cur.fetchone()
        if r:
            flash('Username already exists.','error')
            return render_template('signup.html')
        if len(password) < 8:
            flash('Password must be at least 8 characters!')
            return render_template('signup.html')
        
        hashed_password = generate_password_hash(password)
        cur.execute('insert into users(user_name,email,password) values(%s,%s,%s)',(username,email,hashed_password))
        cur.close()
        return redirect(url_for('userlogin'))
        
    return render_template('signup.html')

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('userlogin'))
    
    cur=mysql.connection.cursor()
    cur.execute('select taskTitle,deadline from userTasks where userID=%s and isArchived=false order by priority desc, deadline asc limit 1',(session['user_id'],))
    task=cur.fetchone()
    cur.execute('select count(*) as total from userTasks where userID=%s and isArchived=false',(session['user_id'],))
    taskCt=cur.fetchone()
    if request.method=='POST':
        action=request.form.get('action')
        if(action=='Tasks'):
            return redirect(url_for('tasks'))
        
        if action=='Logout':
            return redirect(url_for('logout'))
        
    return render_template('dashboard.html',task=task,taskCt=taskCt)

@app.route('/tasks',methods=['GET','POST'])
def tasks():
    if 'user_id' not in session:
        return redirect(url_for('userlogin'))
    
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM userTasks WHERE userID=%s AND isArchived=FALSE order by priority desc,deadline asc', (session['user_id'],))
    tasks = cur.fetchall()

    cur.execute('SELECT * FROM userTasks WHERE userID=%s AND isArchived=TRUE ORDER BY priority DESC,deadline ASC',(session['user_id'],))
    archived_tasks = cur.fetchall()
    if request.method=='POST':
        
        action=request.form.get('action')
        if(action=='Overview'):
            return redirect(url_for('dashboard'))

        if action=='Logout':
            return redirect(url_for('logout'))
        
        if action=='saveTask':
            userID=session['user_id']
            taskTitle=request.form.get('taskTitle')
            taskDesc=request.form.get('taskDesc')
            deadline=request.form.get('deadline')
            priority = request.form.get('priority')
            priority = int(priority) if priority else 1
            cur.execute('insert into userTasks(userID,taskTitle,taskDesc,deadline,priority) values(%s,%s,%s,%s,%s)',(userID,taskTitle,taskDesc,deadline,priority))
            return redirect(url_for('tasks'))
    cur.close()
    return render_template('tasks.html', user=session['username'],tasks=tasks,archived_tasks=archived_tasks)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('userlogin'))

@app.route('/archive_task',methods=['POST'])
def archive_task():
    if 'user_id' not in session:
        return redirect(url_for('userlogin'))
    data =request.get_json()
    task_id=data['task_id']
    cur=mysql.connection.cursor()
    cur.execute('update userTasks set isArchived=TRUE where taskID=%s and userID=%s',(task_id,session['user_id']))
    cur.close()
    return {'status':'ok'}

@app.route('/delete_task',methods=['POST'])
def delete_task():
    if 'user_id' not in session:
        return redirect(url_for('userlogin'))
    data =request.get_json()
    task_id=data['task_id']
    cur=mysql.connection.cursor()
    cur.execute('delete from userTasks where taskID=%s and userID=%s',(task_id,session['user_id']))
    cur.close()
    return {'status':'ok'}

@app.route('/edit_task', methods=['POST'])
def edit_task():
    if 'user_id' not in session:
        return redirect(url_for('userlogin'))
    data=request.get_json()
    task_id=data['task_id']
    title = data['title']
    desc = data['desc']
    deadline = data['deadline']
    priority = data['priority']
    cur = mysql.connection.cursor()
    cur.execute('UPDATE userTasks SET taskTitle=%s, taskDesc=%s, deadline=%s, priority=%s WHERE taskID=%s AND userID=%s',(title, desc, deadline, priority, task_id, session['user_id']))
    cur.close()
    return {'status': 'ok'}