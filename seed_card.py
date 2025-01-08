from app import create_app, db
from app.models.card import Card

my_app = create_app()
with my_app.app_context():
    # Team 1: Team Tiger
    db.session.add(Card(board_id=16, message="Optimize database queries for better performance."))
    db.session.add(Card(board_id=16, message="Implement user authentication and authorization."))
    db.session.add(Card(board_id=16, message="Develop new REST API for order processing."))

    # Team 2: Rainbow team
    db.session.add(Card(board_id=17, message="Refactor the dashboard for better responsiveness."))
    db.session.add(Card(board_id=17, message="Integrate the payment gateway UI."))
    db.session.add(Card(board_id=17, message="Fix layout issues on the mobile view."))

    # Team 3: Blue Ocean team
    db.session.add(Card(board_id=18, message="Develop a real-time chat feature."))
    db.session.add(Card(board_id=18, message="Ensure the application is compliant with security standards."))
    db.session.add(Card(board_id=18, message="Set up CI/CD pipelines for automated deployment."))

    # Team 4: My team
    db.session.add(Card(board_id=19, message="Set up monitoring and alerting for critical services."))
    db.session.add(Card(board_id=19, message="Migrate the application to Kubernetes."))
    db.session.add(Card(board_id=19, message="Automate server backups to cloud storage."))

    db.session.commit()
