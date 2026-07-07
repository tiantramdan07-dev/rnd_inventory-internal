<template>
  <div class="landing">
    <!-- Hero Navbar -->
    <nav class="lnav">
      <div class="lnav-inner">
        <div class="lnav-brand">
          <div class="brand-icon"><i class="fas fa-flask"></i></div>
          <div>
            <div class="brand-name">PT Interskala Mandiri Indonesia</div>
            <div class="brand-sub">R&D & Teknisi Division</div>
          </div>
        </div>
        <RouterLink to="/login" class="btn btn-primary">
          <i class="fas fa-sign-in-alt"></i> Login
        </RouterLink>
      </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
      <div class="hero-bg"></div>
      <div class="container">
        <div class="hero-content">
          <div class="hero-badge"><i class="fas fa-star"></i> Sistem Inventori Digital</div>
          <h1 class="hero-title">Divisi R&D & Teknisi<br /><span>PT Interskala Mandiri Indonesia</span></h1>
          <p class="hero-desc">Kelola inventori toolbox, peminjaman, service teknisi, dan laporan harian dalam satu platform terintegrasi.</p>
          <RouterLink to="/login" class="btn btn-primary btn-lg">
            <i class="fas fa-rocket"></i> Masuk ke Dashboard
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Divisi Cards -->
    <section class="section">
      <div class="container">
        <div class="section-header">
          <h2>Profil Divisi</h2>
          <p>Tim profesional kami siap melayani dengan sepenuh hati</p>
        </div>

        <div class="grid grid-2" style="gap:28px">
          <!-- RnD -->
          <div class="division-card">
            <div class="division-header purple">
              <div class="division-icon"><i class="fas fa-flask"></i></div>
              <div>
                <h3>Divisi Research & Development</h3>
                <p>Inovasi & Pengembangan Produk</p>
              </div>
            </div>
            <div class="division-body">
              <div class="team-grid">
                <div class="member-card" v-for="m in rndTeam" :key="m.name">
                  <div class="member-avatar" :style="m.color">
                    <i :class="m.icon"></i>
                  </div>
                  <div class="member-info">
                    <strong>{{ m.name }}</strong>
                    <span>{{ m.title }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Teknisi -->
          <div class="division-card">
            <div class="division-header blue">
              <div class="division-icon"><i class="fas fa-tools"></i></div>
              <div>
                <h3>Divisi Teknisi</h3>
                <p>Service & Maintenance Expert</p>
              </div>
            </div>
            <div class="division-body">
              <div class="team-grid">
                <div class="member-card" v-for="m in tekTeam" :key="m.name">
                  <div class="member-avatar" :style="m.color">
                    <i :class="m.icon"></i>
                  </div>
                  <div class="member-info">
                    <strong>{{ m.name }}</strong>
                    <span>{{ m.title }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Produk RnD -->
    <section class="section bg-light">
      <div class="container">
        <div class="section-header">
          <h2>Produk R&D</h2>
          <p>Inovasi produk unggulan hasil riset dan pengembangan</p>
        </div>
        <div class="grid grid-3" style="gap:20px">
          <div class="product-card" v-for="p in products" :key="p.name">
            <div class="product-icon" :style="p.color">
              <i :class="p.icon"></i>
            </div>
            <h4>{{ p.name }}</h4>
            <p>{{ p.desc }}</p>
            <div class="product-specs">
              <span v-for="s in p.specs" :key="s" class="spec-tag">{{ s }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="section">
      <div class="container">
        <div class="section-header">
          <h2>Fitur Sistem</h2>
          <p>Semua yang Anda butuhkan untuk manajemen inventori</p>
        </div>
        <div class="grid grid-4" style="gap:16px">
          <div class="feature-card" v-for="f in features" :key="f.title">
            <div class="feature-icon" :style="f.color"><i :class="f.icon"></i></div>
            <h4>{{ f.title }}</h4>
            <p>{{ f.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <footer class="footer">
      <div class="container">
        <p>&copy; {{ new Date().getFullYear() }} PT Interskala Mandiri Indonesia. Created by R&D and Technician.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const rndTeam = [
  { name: 'Supervisor R&D', title: 'Aep Saepuloh', icon: 'fas fa-user-tie', color: 'background:linear-gradient(135deg,#7B5EA7,#5C3D96)' },
  { name: 'Staff R&D 1', title: 'Research Engineer', icon: 'fas fa-microscope', color: 'background:linear-gradient(135deg,#9C6FD4,#7B5EA7)' },
  { name: 'Staff R&D 2', title: 'Product Developer', icon: 'fas fa-flask', color: 'background:linear-gradient(135deg,#B39DDB,#9575CD)' },
]

const tekTeam = [
  { name: 'Supervisor Teknisi', title: 'Aep Saepuloh', icon: 'fas fa-user-cog', color: 'background:linear-gradient(135deg,#2196F3,#1565C0)' },
  { name: 'Teknisi Senior 1', title: 'Senior Technician', icon: 'fas fa-tools', color: 'background:linear-gradient(135deg,#42A5F5,#1E88E5)' },
  { name: 'Teknisi Senior 2', title: 'Field Technician', icon: 'fas fa-wrench', color: 'background:linear-gradient(135deg,#64B5F6,#42A5F5)' },
]

const products = [
  { name: 'Produk Alpha', icon: 'fas fa-microchip', desc: 'Solusi elektronik inovatif untuk industri modern.', specs: ['Industrial Grade', 'IoT Ready', 'IP67'], color: 'background:var(--primary-light);color:var(--primary)' },
  { name: 'Produk Beta', icon: 'fas fa-cogs', desc: 'Sistem otomasi presisi tinggi untuk efisiensi operasional.', specs: ['Automation', 'High Precision', 'CE Certified'], color: 'background:var(--secondary-light);color:var(--secondary)' },
  { name: 'Produk Gamma', icon: 'fas fa-satellite-dish', desc: 'Perangkat monitoring & kontrol jarak jauh secara real-time.', specs: ['Remote Control', 'Real-time', '4G/WiFi'], color: 'background:#E8F5E9;color:#2E7D32' },
]

const features = [
  { title: 'Toolbox Management', desc: 'Kelola inventori toolbox lengkap dengan foto & detail.', icon: 'fas fa-toolbox', color: 'background:var(--primary-light);color:var(--primary)' },
  { title: 'Peminjaman', desc: 'Catat peminjaman dengan foto bukti realtime.', icon: 'fas fa-hand-holding', color: 'background:var(--secondary-light);color:var(--secondary)' },
  { title: 'Service Tracking', desc: 'Pantau status servis teknisi dari pengajuan hingga selesai.', icon: 'fas fa-wrench', color: 'background:#E8F5E9;color:#2E7D32' },
  { title: 'Export Laporan', desc: 'Download laporan formal dalam format Excel & PDF.', icon: 'fas fa-file-export', color: 'background:#FFF3E0;color:#E65100' },
]
</script>

<style scoped>
.landing { min-height: 100vh; background: #fff; }

/* Nav */
.lnav { background: rgba(255,255,255,0.95); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(0,0,0,0.06); position: sticky; top: 0; z-index: 100; }
.lnav-inner { max-width: 1200px; margin: 0 auto; padding: 0 24px; height: 68px; display: flex; align-items: center; justify-content: space-between; }
.lnav-brand { display: flex; align-items: center; gap: 12px; }
.brand-icon { width: 40px; height: 40px; background: var(--primary-gradient); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 18px; }
.brand-name { font-size: 14px; font-weight: 800; color: var(--text-primary); }
.brand-sub { font-size: 11px; color: var(--text-secondary); }

/* Hero */
.hero { position: relative; padding: 100px 0 80px; overflow: hidden; background: linear-gradient(135deg, #1a0533 0%, #2d1b69 50%, #1a237e 100%); }
.hero-bg { position: absolute; inset: 0; background: url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Ccircle cx='30' cy='30' r='1.5' fill='rgba(255,255,255,0.1)'/%3E%3C/svg%3E"); }
.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; position: relative; }
.hero-content { max-width: 640px; }
.hero-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.12); color: #E8D5FF; padding: 6px 16px; border-radius: 99px; font-size: 12px; font-weight: 600; border: 1px solid rgba(255,255,255,0.15); margin-bottom: 24px; }
.hero-title { font-size: 48px; font-weight: 900; color: #fff; line-height: 1.15; margin-bottom: 20px; }
.hero-title span { color: #C5A3FF; }
.hero-desc { font-size: 16px; color: rgba(255,255,255,0.75); margin-bottom: 32px; line-height: 1.7; }

/* Section */
.section { padding: 72px 0; }
.section.bg-light { background: var(--bg); }
.section-header { text-align: center; margin-bottom: 48px; }
.section-header h2 { font-size: 32px; font-weight: 800; color: var(--text-primary); margin-bottom: 8px; }
.section-header p { color: var(--text-secondary); font-size: 15px; }

/* Division cards */
.division-card { background: #fff; border-radius: var(--radius-lg); box-shadow: var(--shadow-md); overflow: hidden; border: 1px solid rgba(0,0,0,0.04); }
.division-header { display: flex; align-items: center; gap: 16px; padding: 22px 24px; }
.division-header.purple { background: linear-gradient(135deg, #7B5EA7, #5C3D96); color: #fff; }
.division-header.blue { background: linear-gradient(135deg, #2196F3, #1565C0); color: #fff; }
.division-header h3 { font-size: 16px; font-weight: 700; margin-bottom: 2px; }
.division-header p { font-size: 12px; opacity: 0.8; }
.division-icon { width: 48px; height: 48px; background: rgba(255,255,255,0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 22px; flex-shrink: 0; }
.division-body { padding: 20px 24px; }
.team-grid { display: flex; flex-direction: column; gap: 12px; }
.member-card { display: flex; align-items: center; gap: 14px; padding: 12px; background: var(--bg); border-radius: var(--radius-sm); }
.member-avatar { width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 16px; flex-shrink: 0; }
.member-info strong { display: block; font-size: 13px; font-weight: 700; }
.member-info span { font-size: 11px; color: var(--text-secondary); }

/* Products */
.product-card { background: #fff; border-radius: var(--radius-md); padding: 24px; box-shadow: var(--shadow-sm); border: 1px solid rgba(0,0,0,0.04); transition: transform 0.2s, box-shadow 0.2s; }
.product-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
.product-icon { width: 52px; height: 52px; border-radius: var(--radius-md); display: flex; align-items: center; justify-content: center; font-size: 22px; margin-bottom: 14px; }
.product-card h4 { font-size: 15px; font-weight: 700; margin-bottom: 6px; }
.product-card p { font-size: 13px; color: var(--text-secondary); margin-bottom: 14px; line-height: 1.6; }
.product-specs { display: flex; flex-wrap: wrap; gap: 6px; }
.spec-tag { background: var(--bg); color: var(--text-secondary); padding: 3px 10px; border-radius: 99px; font-size: 11px; font-weight: 600; }

/* Features */
.feature-card { background: #fff; border-radius: var(--radius-md); padding: 22px; box-shadow: var(--shadow-sm); border: 1px solid rgba(0,0,0,0.04); transition: transform 0.2s; }
.feature-card:hover { transform: translateY(-2px); }
.feature-icon { width: 46px; height: 46px; border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 14px; }
.feature-card h4 { font-size: 14px; font-weight: 700; margin-bottom: 6px; }
.feature-card p { font-size: 12px; color: var(--text-secondary); line-height: 1.6; }

/* Footer */
.footer { background: #1a0533; color: rgba(255,255,255,0.6); text-align: center; padding: 24px; font-size: 13px; }

@media (max-width: 768px) {
  .hero-title { font-size: 32px; }
  .grid-2 { grid-template-columns: 1fr !important; }
}
</style>
