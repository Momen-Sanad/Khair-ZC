from __init__ import create_app
from dbSchema import User,db
app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created successfully!")
    # Insert a new user directly into the database
    new_user = User(
        fname="Abdullah", 
        lname="Ayman", 
        email="abdullah@example.com", 
        password="password123",
        points=200
    )
       

    db.session.add(new_user)  # Add the new user to the session
    db.session.commit()  # Commit the transaction to the database
    
    print("New user added successfully!")

if __name__ == '__main__':
    app.run(debug=False)
