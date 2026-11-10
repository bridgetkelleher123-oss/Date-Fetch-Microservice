from datetime import datetime
import zmq
import json

context = zmq.Context()

socket = context.socket(zmq.REP)

socket.bind("tcp://*:5555")

while True:
        try:
            req = socket.recv_json()
        except json.JSONDecodeError as error:
            #handles JSONs with inccorect syntax
            res = {
                "success": False,
                "error": f"Malformed JSON input: {error}"
            }
            socket.send_json(res)
            continue
        else:
            try:
                date_string = req["date"]
                input_format = req["input_format"]
                output_format = req["output_format"]

                date_object = datetime.strptime(date_string, input_format)
                new_formatted_date = date_object.strftime(output_format)
                
                res = {
                    "success": True,
                    "output_date" : new_formatted_date
                    } 
            
            except( KeyError, ValueError, TypeError) as error:
                #KeyError: catches JSON with key name that does not match what date_fetch microservice expects
                #ValueError: catches incorrect dates (i.e. Novemeber 35th, 2027) 
                #TypeError: catches incorrect values associated with each key in received JSON
                res = {
                    "success": False,
                    "error": f"{type(error).__name__}: {error}"
                }     
            socket.send_json(res)