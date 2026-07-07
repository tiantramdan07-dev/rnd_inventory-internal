from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Pengembalian, Peminjaman, ToolboxItem
from app_instance import db

pengembalian_bp = Blueprint('pengembalian', __name__)


@pengembalian_bp.route('/active-loans', methods=['GET'])
@jwt_required()
def get_active_loans():
    """Get list of active borrowings for return selection."""
    loans = Peminjaman.query.filter_by(status='Dipinjam').all()
    return jsonify([l.to_dict() for l in loans]), 200


@pengembalian_bp.route('', methods=['POST'])
@jwt_required()
def create_pengembalian():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    peminjaman_id = data.get('peminjaman_id')
    pinjam = Peminjaman.query.get(peminjaman_id)
    if not pinjam:
        return jsonify({'message': 'Data peminjaman tidak ditemukan'}), 404
    if pinjam.status == 'Dikembalikan':
        return jsonify({'message': 'Barang sudah dikembalikan'}), 400

    r = Pengembalian(
        returner_name=data['returner_name'],
        division=data['division'],
        peminjaman_id=peminjaman_id,
        condition_note=data.get('condition_note'),
        photo_url=data.get('photo_url'),
        created_by=user_id
    )

    pinjam.status = 'Dikembalikan'
    if pinjam.item:
        pinjam.item.status = 'Tersedia'

    db.session.add(r)
    db.session.commit()
    return jsonify(r.to_dict()), 201
