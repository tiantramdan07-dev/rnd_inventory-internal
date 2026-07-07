from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models import User
from app_instance import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'message': 'Username dan password wajib diisi'}), 400

    user = User.query.filter_by(username=username, is_active=True).first()

    if not user or not user.check_password(password):
        return jsonify({'message': 'Username atau password salah'}), 401

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            'role': user.role,
            'division': user.division,
            'full_name': user.full_name
        }
    )

    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    if not user:
        return jsonify({'message': 'User tidak ditemukan'}), 404
    return jsonify(user.to_dict()), 200


@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = User.query.get(int(user_id))
    data = request.get_json()

    if not user.check_password(data.get('old_password', '')):
        return jsonify({'message': 'Password lama tidak sesuai'}), 400

    user.set_password(data.get('new_password'))
    db.session.commit()
    return jsonify({'message': 'Password berhasil diubah'}), 200
