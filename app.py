from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
import MySQLdb

app = Flask(__name__)
app.secret_key = 'b7e2f8c1-4a6d-4e2a-9c3e-7f1a2b5d6c8e'

# MySQL config (update with your credentials)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'reservations'

# Email config (update with your credentials)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

mail = Mail(app)

def get_db():
    return MySQLdb.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        passwd=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB']
    )

def format_journey_time(hours):
    """Convert hours to readable format (e.g., 26 -> '1 day 2 hours')"""
    try:
        # Handle both string and integer inputs
        if isinstance(hours, str):
            # If it's a time string like "00:00:26", extract the seconds and convert
            if ':' in hours:
                parts = hours.split(':')
                if len(parts) >= 3:
                    # Convert HH:MM:SS to total hours
                    total_hours = int(parts[0]) + int(parts[1])/60 + int(parts[2])/3600
                else:
                    total_hours = int(hours)
            else:
                total_hours = int(hours)
        else:
            total_hours = int(hours)
        
        days = int(total_hours // 24)
        remaining_hours = int(total_hours % 24)
        
        if days > 0:
            if remaining_hours > 0:
                return f"{days} day{'s' if days > 1 else ''} {remaining_hours} hour{'s' if remaining_hours > 1 else ''}"
            else:
                return f"{days} day{'s' if days > 1 else ''}"
        else:
            return f"{remaining_hours} hour{'s' if remaining_hours > 1 else ''}"
    except Exception as e:
        print(f"Error formatting journey time: {e}, value: {hours}")
        return str(hours)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login route accessed. Method:", request.method)
    if request.method == 'POST':
        print("Login POST triggered")
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT user_id, name, email FROM users WHERE email=%s AND password=%s', (email, password))
        user = cur.fetchone()
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['user_email'] = user[2]
            print("Logged in user email:", user[2])
            if user[2].strip().lower() == 'admin@gmail':
                session['is_admin'] = True
            else:
                session['is_admin'] = False
            flash('Login successful!', 'success')
            cur.close()
            db.close()
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
        cur.close()
        db.close()
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Register route accessed. Method:", request.method)
    if request.method == 'POST':
        print("Register POST triggered")
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        cur = db.cursor()
        try:
            cur.execute('INSERT INTO users(name, email, password) VALUES (%s, %s, %s)', (name, email, password))
            db.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except MySQLdb.IntegrityError:
            flash('Email already exists.', 'danger')
        finally:
            cur.close()
            db.close()
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return render_template('logout.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'warning')
        return redirect(url_for('login'))
    print("Session is_admin:", session.get('is_admin'))
    return render_template(
        'dashboard.html',
        is_admin=session.get('is_admin', False),
        user_name=session.get('user_name', '')
    )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        try:
            msg = Message(subject='Routemate Feedback',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=['arpitamishra2755@gmail.com'],
                          body=f'From: {name} <{email}>\n\n{message}')
            mail.send(msg)
            flash('Thank you for your feedback!', 'success')
        except Exception as e:
            flash('Failed to send feedback. Please try again later.', 'danger')
    return render_template('feedback.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        try:
            msg = Message(subject='Routemate Contact',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=['arpitamishra2755@gmail.com'],
                          body=f'From: {name} <{email}>\n\n{message}')
            mail.send(msg)
            flash('Your message has been sent!', 'success')
        except Exception as e:
            flash('Failed to send message. Please try again later.', 'danger')
    return render_template('contact.html')

@app.route('/admin/buses')
def admin_buses():
    if not session.get('is_admin'):
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard'))
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM buses')
    buses = cur.fetchall()
    
    # Format journey_time for display
    formatted_buses = []
    for bus in buses:
        bus_list = list(bus)
        print(f"Original journey_time: {bus[4]}, type: {type(bus[4])}")
        bus_list[4] = format_journey_time(bus[4])  # journey_time is at index 4
        print(f"Formatted journey_time: {bus_list[4]}")
        formatted_buses.append(bus_list)
    
    cur.close()
    db.close()
    return render_template('admin_buses.html', buses=formatted_buses)

@app.route('/admin/bookings', methods=['GET', 'POST'])
def admin_bookings():
    if not session.get('is_admin'):
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard'))
    bookings = []
    if request.method == 'POST':
        bus_id = request.form.get('bus_id')
        db = get_db()
        cur = db.cursor()
        cur.execute('''SELECT u.user_id, u.name, u.email, b.bus_id, b.journey_date, b.seat FROM bookings b JOIN users u ON b.user_id = u.user_id WHERE b.bus_id=%s''', (bus_id,))
        bookings = cur.fetchall()
        cur.close()
        db.close()
    return render_template('admin_bookings.html', bookings=bookings)

@app.route('/admin/add_bus', methods=['GET', 'POST'])
def admin_add_bus():
    if not session.get('is_admin'):
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        bus_id = request.form['bus_id']
        bus_from = request.form['bus_from']
        bus_to = request.form['bus_to']
        start_time = request.form['start_time']
        journey_time = request.form['journey_time']  # This should be hours (e.g., "26")
        arrival_time = request.form['arrival_time']
        fare = request.form['fare']
        total_seats = request.form['total_seats']
        
        print(f"Adding bus with journey_time: {journey_time} (type: {type(journey_time)})")
        
        db = get_db()
        cur = db.cursor()
        cur.execute('''INSERT INTO buses(bus_id, bus_from, bus_to, start_time, journey_time, arival_time, fare, total_seats) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''', (bus_id, bus_from, bus_to, start_time, journey_time, arrival_time, fare, total_seats))
        db.commit()
        cur.close()
        db.close()
        flash('Bus route added.', 'success')
        return redirect(url_for('admin_buses'))
    return render_template('admin_add_bus.html')

@app.route('/admin/delete_bus', methods=['POST'])
def admin_delete_bus():
    if not session.get('is_admin'):
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard'))
    bus_id = request.form['bus_id']
    db = get_db()
    cur = db.cursor()
    cur.execute('DELETE FROM buses WHERE bus_id=%s', (bus_id,))
    db.commit()
    cur.close()
    db.close()
    flash('Bus route deleted.', 'info')
    return redirect(url_for('admin_buses'))

@app.route('/admin/bookings_by_date', methods=['GET', 'POST'])
def admin_bookings_by_date():
    if not session.get('is_admin'):
        flash('Admin access required.', 'danger')
        return redirect(url_for('dashboard'))
    bookings = []
    if request.method == 'POST':
        date = request.form.get('date')
        db = get_db()
        cur = db.cursor()
        cur.execute('''SELECT u.user_id, u.name, u.email, b.bus_id, b.journey_date, b.seat FROM bookings b JOIN users u ON b.user_id = u.user_id WHERE b.journey_date=%s''', (date,))
        bookings = cur.fetchall()
        cur.close()
        db.close()
    return render_template('admin_bookings_by_date.html', bookings=bookings)

@app.route('/user/book', methods=['GET', 'POST'])
def user_book():
    if 'user_id' not in session or session.get('is_admin'):
        flash('User access required.', 'danger')
        return redirect(url_for('dashboard'))
    buses = []
    if request.method == 'POST':
        bus_from = request.form['bus_from']
        bus_to = request.form['bus_to']
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM buses WHERE bus_from=%s AND bus_to=%s', (bus_from, bus_to))
        buses = cur.fetchall()
        
        # Format journey_time for display
        formatted_buses = []
        for bus in buses:
            bus_list = list(bus)
            bus_list[4] = format_journey_time(bus[4])  # journey_time is at index 4
            formatted_buses.append(bus_list)
        
        cur.close()
        db.close()
        return render_template('user_book.html', buses=formatted_buses)
    return render_template('user_book.html', buses=buses)

@app.route('/user/book/confirm/<int:bus_id>', methods=['GET', 'POST'])
def user_book_confirm(bus_id):
    if 'user_id' not in session or session.get('is_admin'):
        flash('User access required.', 'danger')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        journey_date = request.form['journey_date']
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT total_seats FROM buses WHERE bus_id=%s', (bus_id,))
        total_seats = cur.fetchone()[0]
        cur.execute('SELECT * FROM stats WHERE bus_id=%s AND journey_date=%s', (bus_id, journey_date))
        stat = cur.fetchone()
        if stat is None:
            seat_no = 1
            cur.execute('INSERT INTO bookings(user_id, bus_id, journey_date, seat) VALUES(%s, %s, %s, %s)', (session['user_id'], bus_id, journey_date, seat_no))
            cur.execute('INSERT INTO stats(bus_id, journey_date, availability) VALUES(%s, %s, %s)', (bus_id, journey_date, total_seats - 1))
            db.commit()
            flash(f'Ticket booked. Seat Number is {seat_no}.', 'success')
        else:
            if stat[2] == 0:
                flash('Sorry! The bus is full.', 'danger')
            else:
                seat_no = total_seats - stat[2] + 1
                cur.execute('INSERT INTO bookings(user_id, bus_id, journey_date, seat) VALUES(%s, %s, %s, %s)', (session['user_id'], bus_id, journey_date, seat_no))
                cur.execute('UPDATE stats SET availability=availability-1 WHERE bus_id=%s AND journey_date=%s', (bus_id, journey_date))
                db.commit()
                flash(f'Ticket booked. Seat Number is {seat_no}.', 'success')
        cur.close()
        db.close()
        return redirect(url_for('user_bookings'))
    return render_template('user_book_confirm.html', bus_id=bus_id)

@app.route('/user/bookings')
def user_bookings():
    if 'user_id' not in session or session.get('is_admin'):
        flash('User access required.', 'danger')
        return redirect(url_for('dashboard'))
    db = get_db()
    cur = db.cursor()
    cur.execute('''SELECT booking_id, b1.bus_id, journey_date, seat, bus_from, bus_to, start_time, journey_time, arival_time, fare FROM bookings b1 JOIN buses b2 ON b1.bus_id = b2.bus_id WHERE user_id = %s''', (session['user_id'],))
    bookings = cur.fetchall()
    
    # Format journey_time for display
    formatted_bookings = []
    for booking in bookings:
        booking_list = list(booking)
        booking_list[7] = format_journey_time(booking[7])  # journey_time is at index 7
        formatted_bookings.append(booking_list)
    
    cur.close()
    db.close()
    return render_template('user_bookings.html', bookings=formatted_bookings)

@app.route('/user/cancel/<int:booking_id>', methods=['POST'])
def user_cancel(booking_id):
    if 'user_id' not in session or session.get('is_admin'):
        flash('User access required.', 'danger')
        return redirect(url_for('dashboard'))
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT bus_id, journey_date FROM bookings WHERE booking_id=%s', (booking_id,))
    result = cur.fetchone()
    if result:
        bus_id, journey_date = result
        cur.execute('UPDATE stats SET availability=availability+1 WHERE bus_id=%s AND journey_date=%s', (bus_id, journey_date))
        cur.execute('DELETE FROM bookings WHERE booking_id=%s', (booking_id,))
        db.commit()
        flash('Your booking has been cancelled. Refund will be issued.', 'info')
    cur.close()
    db.close()
    return redirect(url_for('user_bookings'))

if __name__ == '__main__':
    app.run(debug=True) 