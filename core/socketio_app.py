# core/socketio_app.py
import socketio

# Create an Async SocketIO server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://parceel.netlify.app",
        "https://p-pilot.netlify.app"
    ])

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

@sio.event
async def ride_accepted(sid, data):
    # Driver emits this, backend broadcasts to Customer
    order_id = data.get('order_id')
    await sio.emit('ride_accepted_event', data, room=str(order_id))

@sio.event
async def ride_completed(sid, data):
    # Driver emits this, backend broadcasts to Customer
    order_id = data.get('order_id')
    await sio.emit('ride_completed_event', data, room=str(order_id))

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")