from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from models import Toolbox, ToolboxItem
from app_instance import db

toolbox_bp = Blueprint('toolbox', __name__)


@toolbox_bp.route('', methods=['GET'])
@jwt_required()
def get_toolboxes():
    toolboxes = Toolbox.query.order_by(Toolbox.created_at.desc()).all()
    return jsonify([t.to_dict() for t in toolboxes]), 200


@toolbox_bp.route('/<int:tid>', methods=['GET'])
@jwt_required()
def get_toolbox(tid):
    t = Toolbox.query.get_or_404(tid)
    return jsonify(t.to_dict()), 200


@toolbox_bp.route('', methods=['POST'])
@jwt_required()
def create_toolbox():
    data = request.get_json()
    t = Toolbox(owner_name=data['owner_name'], description=data.get('description'))
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201


@toolbox_bp.route('/<int:tid>', methods=['PUT'])
@jwt_required()
def update_toolbox(tid):
    t = Toolbox.query.get_or_404(tid)
    data = request.get_json()
    t.owner_name = data.get('owner_name', t.owner_name)
    t.description = data.get('description', t.description)
    db.session.commit()
    return jsonify(t.to_dict()), 200


@toolbox_bp.route('/<int:tid>', methods=['DELETE'])
@jwt_required()
def delete_toolbox(tid):
    claims = get_jwt()
    if claims.get('role') not in ['admin', 'rnd']:
        return jsonify({'message': 'Akses ditolak'}), 403
    t = Toolbox.query.get_or_404(tid)
    db.session.delete(t)
    db.session.commit()
    return jsonify({'message': 'Toolbox dihapus'}), 200


# ---- Items ----

@toolbox_bp.route('/<int:tid>/items', methods=['POST'])
@jwt_required()
def add_item(tid):
    Toolbox.query.get_or_404(tid)
    data = request.get_json()
    item = ToolboxItem(
        toolbox_id=tid,
        name=data['name'],
        description=data.get('description'),
        photo_url=data.get('photo_url'),
        quantity=data.get('quantity', 1),
        condition=data.get('condition', 'Baik')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@toolbox_bp.route('/items/<int:iid>', methods=['PUT'])
@jwt_required()
def update_item(iid):
    item = ToolboxItem.query.get_or_404(iid)
    data = request.get_json()
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    item.photo_url = data.get('photo_url', item.photo_url)
    item.quantity = data.get('quantity', item.quantity)
    item.condition = data.get('condition', item.condition)
    db.session.commit()
    return jsonify(item.to_dict()), 200


@toolbox_bp.route('/items/<int:iid>', methods=['DELETE'])
@jwt_required()
def delete_item(iid):
    item = ToolboxItem.query.get_or_404(iid)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item dihapus'}), 200


@toolbox_bp.route('/items', methods=['GET'])
@jwt_required()
def get_all_items():
    """Get all available items for borrowing selection."""
    items = ToolboxItem.query.filter_by(status='Tersedia').all()
    result = []
    for item in items:
        d = item.to_dict()
        d['toolbox_owner'] = item.toolbox.owner_name if item.toolbox else None
        result.append(d)
    return jsonify(result), 200
