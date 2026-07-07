from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import User
from app_instance import db

user_bp = Blueprint('users', __name__)


def require_admin(claims):
    if claims.get('role') != 'admin':
        return False
    return True


@user_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    claims = get_jwt()
    if not require_admin(claims):
        return jsonify({'message': 'Akses ditolak. Hanya admin.'}), 403
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([u.to_dict() for u in users]), 200


@user_bp.route('', methods=['POST'])
@jwt_required()
def create_user():
    claims = get_jwt()
    if not require_admin(claims):
        return jsonify({'message': 'Akses ditolak'}), 403

    data = request.get_json()
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username sudah digunakan'}), 409

    user = User(
        username=data['username'],
        full_name=data['full_name'],
        role=data.get('role', 'teknisi'),
        division=data.get('division')
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@user_bp.route('/<int:uid>', methods=['PUT'])
@jwt_required()
def update_user(uid):
    claims = get_jwt()
    current_user_id = int(get_jwt().get('sub', 0)) if hasattr(get_jwt(), 'get') else 0
    # Allow admin OR the user themselves to update
    from flask_jwt_extended import get_jwt_identity
    current_id = int(get_jwt_identity())

    if claims.get('role') != 'admin' and current_id != uid:
        return jsonify({'message': 'Akses ditolak'}), 403

    user = User.query.get_or_404(uid)
    data = request.get_json()

    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username sudah digunakan'}), 409
        user.username = data['username']
    if claims.get('role') == 'admin':
        if 'role' in data:
            user.role = data['role']
        if 'division' in data:
            user.division = data['division']
        if 'is_active' in data:
            user.is_active = data['is_active']
    if 'password' in data and data['password']:
        user.set_password(data['password'])

    db.session.commit()
    return jsonify(user.to_dict()), 200


@user_bp.route('/<int:uid>', methods=['DELETE'])
@jwt_required()
def delete_user(uid):
    claims = get_jwt()
    if not require_admin(claims):
        return jsonify({'message': 'Akses ditolak'}), 403

    from flask_jwt_extended import get_jwt_identity
    if int(get_jwt_identity()) == uid:
        return jsonify({'message': 'Tidak bisa menghapus akun sendiri'}), 400

    user = User.query.get_or_404(uid)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User dihapus'}), 200
