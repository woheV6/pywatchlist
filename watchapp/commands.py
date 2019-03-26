from watchapp import app,db
import click
@app.cli.command() # 注册为命令
@click.option('--drop',is_flag=True,help='Create after drop.')
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database')

@app.cli.command()
@click.option('--username',prompt=True,help='The username used to login')
@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True, help='The password used to login')
def admin(username,password):
    from watchapp.models import User
    """create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updtating user...')
        user.username=username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username,name='admin')
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo("Done")


@app.cli.command()
def forge():
    from watchapp.models import Movie,User
    """Generate fake data"""
    db.create_all()
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done!')