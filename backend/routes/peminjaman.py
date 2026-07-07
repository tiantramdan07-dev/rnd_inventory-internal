from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Peminjaman, ToolboxItem
from app_instance import db

peminjaman_bp = Blueprint('peminjaman', __name__)


@peminjaman_bp.route('', methods=['GET'])
@jwt_required()
def get_peminjaman():
    records = Peminjaman.query.filter_by(status='Dipinjam').order_by(
        Peminjaman.borrowed_at.desc()
    ).all()
    return jsonify([r.to_dict() for r in records]), 200


@peminjaman_bp.route('', methods=['POST'])
@jwt_required()
def create_peminjaman():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    item_id = data.get('item_id')
    item = ToolboxItem.query.get(item_id)
    if not item:
        return jsonify({'message': 'Barang tidak ditemukan'}), 404
    if item.status == 'Dipinjam':
        return jsonify({'message': 'Barang sedang dipinjam'}), 400

    p = Peminjaman(
        borrower_name=data['borrower_name'],
        division=data['division'],
        item_id=item_id,
        condition_note=data.get('condition_note'),
        photo_url=data.get('photo_url'),
        created_by=user_id
    )
    item.status = 'Dipinjam'
    db.session.add(p)
    db.session.commit()
    return jsonify(p.to_dict()), 201
