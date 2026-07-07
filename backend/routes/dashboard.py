from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from models import ToolboxItem, Peminjaman, Pengembalian
from app_instance import db
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    total_items = ToolboxItem.query.count()
    dipinjam = ToolboxItem.query.filter_by(status='Dipinjam').count()
    tersedia = ToolboxItem.query.filter_by(status='Tersedia').count()
    belum_kembali = Peminjaman.query.filter_by(status='Dipinjam').count()

    # Latest activity
    latest_peminjaman = db.session.query(Peminjaman).order_by(
        Peminjaman.borrowed_at.desc()
    ).limit(5).all()

    latest_pengembalian = db.session.query(Pengembalian).order_by(
        Pengembalian.returned_at.desc()
    ).limit(5).all()

    recent_activity = []
    for p in latest_peminjaman:
        recent_activity.append({
            'type': 'Peminjaman',
            'name': p.borrower_name,
            'item': p.item.name if p.item else '-',
            'time': p.borrowed_at.isoformat() if p.borrowed_at else None,
            'division': p.division
        })
    for r in latest_pengembalian:
        recent_activity.append({
            'type': 'Pengembalian',
            'name': r.returner_name,
            'item': r.peminjaman.item.name if r.peminjaman and r.peminjaman.item else '-',
            'time': r.returned_at.isoformat() if r.returned_at else None,
            'division': r.division
        })

    recent_activity.sort(key=lambda x: x['time'] or '', reverse=True)

    return jsonify({
        'total_items': total_items,
        'dipinjam': dipinjam,
        'tersedia': tersedia,
        'belum_kembali': belum_kembali,
        'recent_activity': recent_activity[:8]
    }), 200
