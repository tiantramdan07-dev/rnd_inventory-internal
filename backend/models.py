from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app_instance import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='teknisi')  # admin, rnd, teknisi
    division = db.Column(db.String(50))  # RnD, Teknisi
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'role': self.role,
            'division': self.division,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Toolbox(db.Model):
    __tablename__ = 'toolboxes'
    id = db.Column(db.Integer, primary_key=True)
    owner_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    items = db.relationship('ToolboxItem', backref='toolbox', lazy=True, cascade='all, delete-orphan')

    def to_dict(self, include_items=True):
        data = {
            'id': self.id,
            'owner_name': self.owner_name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'item_count': len(self.items)
        }
        if include_items:
            data['items'] = [item.to_dict() for item in self.items]
        return data


class ToolboxItem(db.Model):
    __tablename__ = 'toolbox_items'
    id = db.Column(db.Integer, primary_key=True)
    toolbox_id = db.Column(db.Integer, db.ForeignKey('toolboxes.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    photo_url = db.Column(db.String(500))
    quantity = db.Column(db.Integer, default=1)
    condition = db.Column(db.String(50), default='Baik')  # Baik, Rusak, Perlu Perbaikan
    status = db.Column(db.String(20), default='Tersedia')  # Tersedia, Dipinjam
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'toolbox_id': self.toolbox_id,
            'name': self.name,
            'description': self.description,
            'photo_url': self.photo_url,
            'quantity': self.quantity,
            'condition': self.condition,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Peminjaman(db.Model):
    __tablename__ = 'peminjaman'
    id = db.Column(db.Integer, primary_key=True)
    borrower_name = db.Column(db.String(150), nullable=False)
    division = db.Column(db.String(100), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('toolbox_items.id'), nullable=False)
    condition_note = db.Column(db.Text)
    photo_url = db.Column(db.String(500))
    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Dipinjam')  # Dipinjam, Dikembalikan
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    item = db.relationship('ToolboxItem', backref='peminjaman_records', lazy=True)
    creator = db.relationship('User', backref='peminjaman_created', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'borrower_name': self.borrower_name,
            'division': self.division,
            'item_id': self.item_id,
            'item_name': self.item.name if self.item else None,
            'toolbox_owner': self.item.toolbox.owner_name if self.item and self.item.toolbox else None,
            'condition_note': self.condition_note,
            'photo_url': self.photo_url,
            'borrowed_at': self.borrowed_at.isoformat() if self.borrowed_at else None,
            'status': self.status,
            'created_by': self.creator.full_name if self.creator else None
        }


class Pengembalian(db.Model):
    __tablename__ = 'pengembalian'
    id = db.Column(db.Integer, primary_key=True)
    returner_name = db.Column(db.String(150), nullable=False)
    division = db.Column(db.String(100), nullable=False)
    peminjaman_id = db.Column(db.Integer, db.ForeignKey('peminjaman.id'), nullable=False)
    condition_note = db.Column(db.Text)
    photo_url = db.Column(db.String(500))
    returned_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    peminjaman = db.relationship('Peminjaman', backref='pengembalian_record', lazy=True)
    creator = db.relationship('User', backref='pengembalian_created', lazy=True)

    def to_dict(self):
        pinjam = self.peminjaman
        return {
            'id': self.id,
            'returner_name': self.returner_name,
            'division': self.division,
            'peminjaman_id': self.peminjaman_id,
            'item_name': pinjam.item.name if pinjam and pinjam.item else None,
            'borrower_name': pinjam.borrower_name if pinjam else None,
            'condition_note': self.condition_note,
            'photo_url': self.photo_url,
            'returned_at': self.returned_at.isoformat() if self.returned_at else None,
            'created_by': self.creator.full_name if self.creator else None
        }


class ServiceTeknisi(db.Model):
    __tablename__ = 'service_teknisi'
    id = db.Column(db.Integer, primary_key=True)
    nomor = db.Column(db.String(50), unique=True, nullable=False)
    tanggal_pengajuan = db.Column(db.Date, nullable=False)
    nama_teknisi = db.Column(db.String(150), nullable=False)
    nama_sales = db.Column(db.String(150))
    customer = db.Column(db.String(200), nullable=False)
    produk = db.Column(db.String(200), nullable=False)
    lokasi = db.Column(db.String(300))
    tipe_service = db.Column(db.String(50))  # Servis, Demo
    tanggal_service = db.Column(db.Date)
    tanggal_selesai = db.Column(db.Date)
    status = db.Column(db.String(50), default='Pending')  # Pending, Proses, Selesai, Batal
    keterangan = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    creator = db.relationship('User', backref='services_created', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nomor': self.nomor,
            'tanggal_pengajuan': self.tanggal_pengajuan.isoformat() if self.tanggal_pengajuan else None,
            'nama_teknisi': self.nama_teknisi,
            'nama_sales': self.nama_sales,
            'customer': self.customer,
            'produk': self.produk,
            'lokasi': self.lokasi,
            'tipe_service': self.tipe_service,
            'tanggal_service': self.tanggal_service.isoformat() if self.tanggal_service else None,
            'tanggal_selesai': self.tanggal_selesai.isoformat() if self.tanggal_selesai else None,
            'status': self.status,
            'keterangan': self.keterangan,
            'created_by': self.creator.full_name if self.creator else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class LaporanHarian(db.Model):
    __tablename__ = 'laporan_harian'
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date, nullable=False)
    hari = db.Column(db.String(20))
    pekerjaan = db.Column(db.Text, nullable=False)
    produk = db.Column(db.String(200))
    informasi_tambahan = db.Column(db.Text)
    status_garansi = db.Column(db.Boolean, default=False)
    jam_start = db.Column(db.Time)
    jam_end = db.Column(db.Time)
    foto_url = db.Column(db.String(500))
    teknisi_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    teknisi = db.relationship('User', backref='laporan_harian', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'tanggal': self.tanggal.isoformat() if self.tanggal else None,
            'hari': self.hari,
            'pekerjaan': self.pekerjaan,
            'produk': self.produk,
            'informasi_tambahan': self.informasi_tambahan,
            'status_garansi': self.status_garansi,
            'jam_start': str(self.jam_start) if self.jam_start else None,
            'jam_end': str(self.jam_end) if self.jam_end else None,
            'foto_url': self.foto_url,
            'teknisi_id': self.teknisi_id,
            'teknisi_name': self.teknisi.full_name if self.teknisi else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
