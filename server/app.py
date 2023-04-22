from flask import Flask,render_template,request
import pika
import os


app = Flask(__name__, template_folder='./templates')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the data from the form
        data = request.form['data']
        print("DATAAAAAA: ", data)
        command = f'curl localhost:5000/add-job/{data}'
        # Run the curl command
        try:
            res = os.system(command)
            print("RES: ", res)
            print("EXECUTED command")
        except:
            print("NOT FOUNDDDDDDDDDDDDDD")
        # Return a success message
        
    return render_template("index.html")


@app.route('/add-job/<cmd>')
def add(cmd):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body="hiiiii",
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    return " [x] Sent: %s" % cmd


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
