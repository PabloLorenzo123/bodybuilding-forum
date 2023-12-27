from project import create_app, db
from project.muscle.models import Muscle
from project.auth.models import User, Role, Permission

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User, Role=Role, Permission=Permission, Muscle=Muscle)
    
  