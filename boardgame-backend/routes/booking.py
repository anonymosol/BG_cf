from flask import Blueprint, request, jsonify
from utils.db import get_db

booking_bp = Blueprint('booking', __name__, url_prefix='/api/bookings')

@booking_bp.route('', methods=['GET'])
def get_bookings():
    date = request.args.get('date')
    room_type = request.args.get('room_type')

    db = get_db()
    query = 'SELECT * FROM bookings WHERE 1=1'
    params = []

    if date:
        query += ' AND date = ?'
        params.append(date)

    if room_type:
        query += ' AND room_type = ?'
        params.append(room_type)

    query += ' ORDER BY date, start_time'

    bookings = db.execute(query, params).fetchall()
    return jsonify([dict(b) for b in bookings])


@booking_bp.route('', methods=['POST'])
def create_booking():
    data = request.get_json()

    # Đồng bộ tên trường với React BookingForm
    name = data.get('customer_name')
    phone = data.get('phone')
    room_type = data.get('room_type')
    date = data.get('date')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    number_of_people = data.get('number_of_people')
    note = data.get('note')

    if not name or not phone or not room_type or not date or not start_time:
        return jsonify({'error': 'Missing required fields'}), 400

    db = get_db()

    # Kiểm tra trùng lịch
    conflict_query = '''
        SELECT * FROM bookings
        WHERE room_type = ? AND date = ? AND start_time = ?
    '''
    conflict = db.execute(conflict_query, (room_type, date, start_time)).fetchone()
    if conflict:
        return jsonify({'error': 'Time slot already booked for this room type'}), 409

    cursor = db.execute(
        '''
        INSERT INTO bookings 
        (name, phone, room_type, date, start_time, end_time, number_of_people, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (name, phone, room_type, date, start_time, end_time, number_of_people, note)
    )
    db.commit()

    return jsonify({'message': 'Booking created successfully', 'id': cursor.lastrowid}), 201


@booking_bp.route('/<int:id>', methods=['DELETE'])
def delete_booking(id):
    db = get_db()
    db.execute('DELETE FROM bookings WHERE id = ?', (id,))
    db.commit()
    return jsonify({'message': 'Booking deleted'}), 200
