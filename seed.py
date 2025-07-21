from app import create_app, db
from app.models import Role

app = create_app()

def seed_roles():
    roles = ['Driver', 'Approver', 'Loader', 'Administrator']

    for role_name in roles:
        # Corrected: check by 'name', not 'username'
        existing_role = Role.query.filter_by(name=role_name).first()
        if not existing_role:
            new_role = Role(name=role_name)
            db.session.add(new_role)

    db.session.commit()
    print("✅ Role seeding complete.")

# Run inside app context
with app.app_context():
    seed_roles()

