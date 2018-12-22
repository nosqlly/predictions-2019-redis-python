from flask import Flask,request,jsonify
import redis

application = Flask(__name__)

redis_obj = redis.Redis(host = '127.0.0.1', port = 6379, db = 0)
redis_obj_db1 = redis.Redis(host = '127.0.0.1', port = 6379, db = 1)
limit = 5
time_limit = 60

no_of_predictions = len(redis_obj.keys())

def name_prediction_value(name):
    result=0
    for cnt,alpha in enumerate(name.lower()):
        result+=(cnt+1)*ord(alpha)
    return result

def check_ip(ip):
    check = True
    if redis_obj_db1.get(ip): # check if the ip is present. Returns True if ip is present else False
        print type(redis_obj_db1.get(ip)),limit
        if int(redis_obj_db1.get(ip)) < limit: # Checks if the limit is within threshold
            redis_obj_db1.incr(ip)
        else:
            check = False
    else:
        redis_obj_db1.incr(ip)
        redis_obj_db1.expire(ip,time_limit) # Set the time limit for the key to expire
    return (check, redis_obj_db1.ttl(ip))

@application.route('/predict/<name>')
def func(name):
    check_value, time_remaining=check_ip(request.remote_addr)
    print check_value, time_remaining
    if check_value:
        index = name_prediction_value(name)%no_of_predictions # Find the index for the name
        return jsonify({ 'prediction' : redis_obj.get(index) }),200
    else:
        return jsonify({ 'Error' : 'Your limit for this session has reached. Try after {} mins {} secs'.format(time_remaining/60, time_remaining%60) }),401

if __name__ == '__main__':
    application.run(host = '0.0.0.0', port = 80)