import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app_instance import db
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    db.init_app(app)
    JWTManager(app)

    from routes.auth import auth_bp
    from routes.toolbox import toolbox_bp
    from routes.peminjaman import peminjaman_bp
    from routes.pengembalian import pengembalian_bp
    from routes.riwayat import riwayat_bp
    from routes.service_teknisi import service_bp
    from routes.laporan_harian import laporan_bp
    from routes.user_management import user_bp
    from routes.dashboard import dashboard_bp
    from routes.upload import upload_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(toolbox_bp, url_prefix='/api/toolbox')
    app.register_blueprint(peminjaman_bp, url_prefix='/api/peminjaman')
    app.register_blueprint(pengembalian_bp, url_prefix='/api/pengembalian')
    app.register_blueprint(riwayat_bp, url_prefix='/api/riwayat')
    app.register_blueprint(service_bp, url_prefix='/api/service')
    app.register_blueprint(laporan_bp, url_prefix='/api/laporan')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    with app.app_context():
        db.create_all()
        _seed_admin()

    return app


def _seed_admin():
    """Create default admin user if not exists."""
    from models import User
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            full_name='Administrator',
            role='admin',
            division='Admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)

        rnd_user = User(username='rnd1', full_name='Staff R&D', role='rnd', division='RnD')
        rnd_user.set_password('rnd123')
        db.session.add(rnd_user)

        tek_user = User(username='teknisi1', full_name='Teknisi 1', role='teknisi', division='Teknisi')
        tek_user.set_password('tek123')
        db.session.add(tek_user)

        db.session.commit()


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
