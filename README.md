# 🔧 Sistem Inventori R&D & Teknisi
### PT Interskala Mandiri Indonesia

Aplikasi manajemen inventori toolbox, peminjaman, service teknisi, dan laporan harian berbasis web.

---

## 🛠️ Tech Stack

| Layer      | Teknologi                  |
|------------|---------------------------|
| Frontend   | Vue.js 3, Pinia, Vue Router |
| Backend    | Python Flask, SQLAlchemy   |
| Database   | PostgreSQL                 |
| Auth       | JWT (Flask-JWT-Extended)   |
| Export     | openpyxl (Excel), reportlab (PDF) |

---

## 📁 Struktur Project

```
rnd-inventory/
├── backend/
│   ├── app.py                 # Flask entry point
│   ├── app_instance.py        # SQLAlchemy instance
│   ├── config.py              # Konfigurasi
│   ├── models.py              # Database models
│   ├── requirements.txt       # Python dependencies
│   └── routes/
│       ├── auth.py            # Login & auth
│       ├── dashboard.py       # Stats dashboard
│       ├── toolbox.py         # CRUD toolbox & items
│       ├── peminjaman.py      # Catat peminjaman
│       ├── pengembalian.py    # Catat pengembalian
│       ├── riwayat.py         # Riwayat + export
│       ├── service_teknisi.py # Service teknisi + export
│       ├── laporan_harian.py  # Laporan harian + export
│       ├── user_management.py # Kelola user
│       └── upload.py          # Upload foto
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.js
        ├── App.vue
        ├── router/index.js
        ├── stores/auth.js
        ├── assets/styles/main.css
        ├── components/layout/
        │   ├── AppLayout.vue  # Layout wrapper
        │   ├── Sidebar.vue    # Sidebar navigasi
        │   └── Navbar.vue     # Header navbar
        └── views/
            ├── Landing.vue        # Halaman utama / profil divisi
            ├── Login.vue          # Halaman login
            ├── Dashboard.vue      # Dashboard statistik
            ├── Toolbox.vue        # Kelola toolbox
            ├── Peminjaman.vue     # Form peminjaman + kamera
            ├── Pengembalian.vue   # Form pengembalian + kamera
            ├── Riwayat.vue        # Riwayat + filter + export
            ├── ServiceTeknisi.vue # Service teknisi
            ├── LaporanHarian.vue  # Laporan harian teknisi
            └── UserManagement.vue # Kelola user
```

---

## ⚙️ Setup & Instalasi

### 1. PostgreSQL — Buat Database

```sql
CREATE DATABASE rnd_inventory;
CREATE USER rnd_user WITH PASSWORD 'password123';
GRANT ALL PRIVILEGES ON DATABASE rnd_inventory TO rnd_user;
```

---

### 2. Backend (Flask)

```bash
cd backend

# Buat virtual environment
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Konfigurasi environment (opsional, buat file .env)
# DATABASE_URL=postgresql://rnd_user:password123@localhost:5432/rnd_inventory
# SECRET_KEY=your-secret-key
# JWT_SECRET_KEY=your-jwt-secret

# Jalankan backend
python app.py
```

Backend berjalan di: `http://localhost:5000`

---

### 3. Frontend (Vue.js)

```bash
cd frontend

# Install dependencies
npm install

# Jalankan development server
npm run dev
```

Frontend berjalan di: `http://localhost:3000`

---

## 🔐 Akun Default

Setelah backend pertama kali dijalankan, akun berikut otomatis dibuat:

| Username  | Password  | Role     | Akses                         |
|-----------|-----------|----------|-------------------------------|
| admin     | admin123  | Admin    | Semua fitur + user management |
| rnd1      | rnd123    | R&D      | Toolbox, peminjaman, riwayat  |
| teknisi1  | tek123    | Teknisi  | Semua + service + laporan     |

---

## 📋 Fitur Lengkap

### 🏠 Landing Page
- Profil Divisi R&D dan Teknisi
- Tampilan supervisor dan anggota tim
- Produk R&D dengan spesifikasi
- Fitur-fitur sistem

### 📊 Dashboard
- Total barang, dipinjam, tersedia, belum kembali
- Tabel aktivitas terbaru (peminjaman & pengembalian)
- Quick action buttons

### 🧰 Toolbox
- CRUD toolbox (nama pemilik, deskripsi)
- CRUD barang per toolbox (nama, foto, qty, kondisi, status)
- Upload foto barang

### 📤 Peminjaman
- Form: nama peminjam, divisi, pilih barang
- Catatan kondisi (opsional)
- **Foto realtime via kamera** sebagai bukti
- Daftar barang sedang dipinjam

### 📥 Pengembalian
- Form: nama yang mengembalikan, divisi, pilih barang
- Catatan kondisi (opsional)
- **Foto realtime via kamera** sebagai bukti

### 📚 Riwayat
- Filter: Semua / Peminjaman / Pengembalian
- Filter tanggal: Hari ini / 7 hari / Sebulan / Custom
- **Export Excel** & **Export PDF** formal
- Preview foto bukti

### 🔧 Servis Teknisi
- No, Tgl Pengajuan, Teknisi, Sales, Customer, Produk, Lokasi
- Tipe Service, Tgl Service, Tgl Selesai, Status, Keterangan
- Filter tanggal + Export Excel & PDF
- Auto-generate nomor service (SRV/YYYYMM/XXXX)

### 📝 Laporan Harian Teknisi
- Tanggal & Hari (otomatis), Pekerjaan, Produk
- Info tambahan, Status Garansi
- Jam Mulai & Selesai
- **Foto hasil service via kamera**
- Filter tanggal + Export Excel & PDF

### 👥 User Management (Admin only)
- Tambah, edit, hapus user
- Kelola nama lengkap, username, password
- Role: Admin / R&D / Teknisi
- Aktifkan / nonaktifkan akun

---

## 🔒 Hak Akses (Role-based)

| Halaman         | Admin | R&D | Teknisi |
|-----------------|:-----:|:---:|:-------:|
| Dashboard       | ✅   | ✅  | ✅     |
| Toolbox         | ✅   | ✅  | ✅     |
| Peminjaman      | ✅   | ✅  | ✅     |
| Pengembalian    | ✅   | ✅  | ✅     |
| Riwayat         | ✅   | ✅  | ✅     |
| Service Teknisi | ✅   | ❌  | ✅     |
| Laporan Harian  | ✅   | ❌  | ✅     |
| User Management | ✅   | ❌  | ❌     |

---

## 🌐 API Endpoints

| Method | Endpoint                        | Deskripsi                  |
|--------|---------------------------------|----------------------------|
| POST   | /api/auth/login                 | Login                      |
| GET    | /api/dashboard/stats            | Statistik dashboard        |
| GET    | /api/toolbox                    | List toolbox               |
| POST   | /api/toolbox                    | Tambah toolbox             |
| POST   | /api/toolbox/:id/items          | Tambah item                |
| GET    | /api/toolbox/items              | Item tersedia              |
| POST   | /api/peminjaman                 | Catat peminjaman           |
| POST   | /api/pengembalian               | Catat pengembalian         |
| GET    | /api/riwayat                    | Riwayat + filter           |
| GET    | /api/riwayat/export/excel       | Export Excel               |
| GET    | /api/riwayat/export/pdf         | Export PDF                 |
| GET    | /api/service                    | List service               |
| POST   | /api/service                    | Tambah service             |
| GET    | /api/service/export/excel       | Export Excel               |
| GET    | /api/laporan                    | List laporan harian        |
| POST   | /api/laporan                    | Tambah laporan             |
| GET    | /api/users                      | List user (admin)          |
| POST   | /api/upload/:folder             | Upload foto                |

---

## 🚀 Build Production

```bash
# Frontend
cd frontend
npm run build
# Output: frontend/dist/

# Backend: deploy dengan gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

---

*© 2024 PT Interskala Mandiri Indonesia — Created by R&D and Technician*
# rnd_inventory-internal
