# core/socketio_app.py
import socketio

# Create an Async SocketIO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def join_order(sid, data):
    # Both Driver and Customer join a room specific to their order ID
    order_id = data.get('order_id')
    if order_id:
        sio.enter_room(sid, str(order_id))
        print(f"Client {sid} joined room for Order: {order_id}")

# 1. ADDED THIS: Listen for the driver's live GPS updates and broadcast to the customer
@sio.event
async def driver_location_update(sid, data):
    order_id = data.get('order_id')
    if order_id:
        await sio.emit('driver_location_update', data, room=str(order_id))

# 2. FIXED NAME: Listen for exactly what React emits ('ride_accepted_event')
@sio.event
async def ride_accepted_event(sid, data):
    order_id = data.get('order_id')
    if order_id:
        await sio.emit('ride_accepted_event', data, room=str(order_id))

# 3. FIXED NAME: Listen for exactly what React emits ('ride_completed_event')
@sio.event
async def ride_completed_event(sid, data):
    order_id = data.get('order_id')
    if order_id:
        await sio.emit('ride_completed_event', data, room=str(order_id))

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")