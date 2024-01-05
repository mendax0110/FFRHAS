from flask import Flask, render_template
import socket

app = Flask(__name__)

received_data = ""

def receive_data_from_microcontroller():
    try:
        pi_ip = '192.168.178.66'
        pi_port = 80

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((pi_ip, pi_port))
            s.listen(1)
            print("Waiting for connection from microcontroller...")
            conn, addr = s.accept()

            global received_data
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024).decode()
                    if not data:
                        break
                    print(f"Received data from microcontroller: {data}")
                    received_data = data
    except Exception as e:
        print(f"Error: {str(e)}")

@app.route('/')
def home():
    try:
        global received_data
        ip_address = socket.gethostbyname(socket.gethostname())
        return render_template('index.html', received_data=received_data, ip_address=ip_address)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    receive_data_from_microcontroller()
    app.run(host='0.0.0.0', port=80, debug=True)
