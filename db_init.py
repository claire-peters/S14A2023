from models import db, app, User, Order

with app.app_context():
    db.create_all()

    # Query the whole table
    users = db.session.execute(
        db.select(User).order_by(User.username)).scalars()
    for u in users:
        print(u.as_dict())
    print("==========After Select All 1===============")

    # Insert a new object
    user1 = User(
        username="username1",
        email="email1@example.com",
    )
    db.session.add(user1)
    db.session.commit()
    print("==========After Commit===============")
    # Query the whole table
    userList = db.session.execute(
        db.select(User).order_by(User.username)).scalars()
    for s in userList:
        print(s.as_dict())
    print("==========After Select All 2===============")
    # Query by id, a specific record
    user = db.get_or_404(User, 1)
    print(user.as_dict())
