from main import app, db
from flask.cli import FlaskGroup
# from flask_migrate import Migrate, MigrateCommand
# from flask_script import Manager

# migrate = Migrate(app, db)

# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

cli = FlaskGroup(app)

# @cli.add_command('db', MigrateCommand)
# @cli.command('db')
# def db():
#     print('Migration')


if __name__ == '__main__':
    cli()
    # manager.run()
