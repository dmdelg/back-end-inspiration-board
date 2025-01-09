# seed_card.py
from app import create_app, db
from app.models.card import Card
from dotenv import load_dotenv

load_dotenv ()



my_app = create_app()
with my_app.app_context():
    # Team 1: Team Tiger (Board ID 1)
    db.session.add(Card(board_id=1, message="Optimize database queries for better performance."))
    db.session.add(Card(board_id=1, message="Implement user authentication and authorization."))
    db.session.add(Card(board_id=1, message="Develop new REST API for order processing."))

    # Team 2: Rainbow team (Board ID 2)
    db.session.add(Card(board_id=2, message="Refactor the dashboard for better responsiveness."))
    db.session.add(Card(board_id=2, message="Integrate the payment gateway UI."))
    db.session.add(Card(board_id=2, message="Fix layout issues on the mobile view."))

    # Team 3: Blue Ocean team (Board ID 3)
    db.session.add(Card(board_id=3, message="Develop a real-time chat feature."))
    db.session.add(Card(board_id=3, message="Ensure the application is compliant with security standards."))
    db.session.add(Card(board_id=3, message="Set up CI/CD pipelines for automated deployment."))

    # Team 4: My team (Board ID 4)
    db.session.add(Card(board_id=4, message="Set up monitoring and alerting for critical services."))
    db.session.add(Card(board_id=4, message="Migrate the application to Kubernetes."))
    db.session.add(Card(board_id=4, message="Automate server backups to cloud storage."))

    db.session.commit()

