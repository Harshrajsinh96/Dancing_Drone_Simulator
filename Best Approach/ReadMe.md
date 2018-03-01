# How to Run 

* Run Proto file:

> python3 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. drone.proto
<hr>

* Run Server:
> python3 server.py 0,0,0 5,0,0
```
Server Started at 3000
```
<hr>

* Run Client:
> python3 client.py 3000
```
Drone [random_id] connected to the server.
Cords received, moving to [first_cords]
Drone [random_id] connected to the server.
Cords received, moving to [calculated_cords]