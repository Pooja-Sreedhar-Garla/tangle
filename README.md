# tangle
Tangle Simulator

## requirements
* <code>python3</code>
* <code>sqlite3</code>

## instructions
*  install and create a virtual environment (optional): <br> 
   <code>$pip3 install virtualenv</code> <br>
   <code>$virtualenv -p python3 venv</code> <br>
   <code>$source venv/bin/activate</code> <br>

*  install dependencies: <br>
   <code>$pip3 install -r requirements.txt</code>

*  create and initialize the database (can be used to reset the database as well): <br>
   <code>$python3 run.py createdb</code>
   
*  run the server: <br>
   <code>$python3 run.py</code>
   
* the server can be accessed at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)