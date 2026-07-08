<template>
  <div class="landing">
    <!-- Hero Navbar -->
    <nav class="lnav">
      <div class="lnav-inner">
        <div class="lnav-brand">
          <div class="brand-icon"><i class="fa-solid fa-scale-balanced"></i></div>
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
          <div class="hero-badge"><i class=""></i> Sistem Inventori RnD & Teknisi</div>
          <h1 class="hero-title">Divisi RnD & Teknisi<br /><span>PT Interskala Mandiri Indonesia</span></h1>
          <p class="hero-desc">Kelola inventori toolbox, peminjaman, service teknisi, dan laporan harian.</p>
          <RouterLink to="/login" class="btn btn-primary btn-lg">
            <i class="fas fa-rocket"></i> Masuk ke Dashboard
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Produk RnD -->
    <section class="section bg-light">
      <div class="container">
        <div class="section-header">
          <h2>Produk R&D</h2>
          <p>Inovasi produk unggulan hasil riset dan pengembangan - I-CON X Series</p>
        </div>
        <div class="grid grid-3" style="gap:20px">
          <div class="product-card" v-for="p in products" :key="p.name">
            <div class="product-image">
              <img :src="p.image" :alt="p.name" />
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

    <footer class="footer">
      <div class="container">
        <p>&copy; {{ new Date().getFullYear() }} PT Interskala Mandiri Indonesia. Created by R&D and Technician.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

// Ganti path import berikut sesuai lokasi folder assets pada project Anda,
// misalnya: import iconXPlus from '@/assets/products/icon-x-plus.png'
import iconXPlus from '@/assets/products/icon-x-plus.png'
import iconX4 from '@/assets/products/icon-x4.png'
import iconX3 from '@/assets/products/icon-x3.png'
import iconX2 from '@/assets/products/icon-x2.png'
import iconX1 from '@/assets/products/icon-x1.png'
import iconXUsb from '@/assets/products/icon-x-usb.png'

const products = [
  {
    name: 'I-CON X.+',
    image: iconXPlus,
    desc: 'I-CON X.+ merupakan perangkat yang mampu menghubungkan indikator timbangan digital dengan berbagai perangkat dalam satu proses kerja. I-CON X+ merupakan gabungan dari teknologi seri I-CON X sebelumnya. Dengan I-CON X+ kita dapat melakukan penimbangan melalui smartphone yang terhubung dengan printer bluetooth dan display eksternal.',
    specs: ['Bluetooth', 'Smartphone Ready', 'External Display'],
  },
  {
    name: 'I-CON X.4',
    image: iconX4,
    desc: 'I-CON X.4 merupakan pengembangan dari beberapa seri sebelumnya yang merupakan inovasi baru di bidang komunikasi data. Dengan menggunakan I-CON X.4 indikator dapat dihubungkan ke berbagai jenis perangkat seperti display eksternal, printer, secara nirkabel menggunakan Wifi.',
    specs: ['WiFi', 'Wireless', 'Multi-device'],
  },
  {
    name: 'I-CON X.3',
    image: iconX3,
    desc: 'I-CON X.3 merupakan pengembangan dari versi sebelumnya (I-CON X.2) yang merupakan sebuah inovasi dalam komunikasi data. Dengan menggunakan I-CON X.3, indikator yang memiliki serial pin out (RS-232) dapat dihubungkan dengan berbagai jenis perangkat tambahan seperti display eksternal, printer, dan lain-lain melalui frekuensi radio.',
    specs: ['RS-232', '433 MHz', 'Radio Frequency'],
  },
  {
    name: 'I-CON X.2',
    image: iconX2,
    desc: 'I-CON X.2 merupakan pengembangan dari versi sebelumnya (I-CON X.1) yang merupakan produk inovasi baru dalam komunikasi data. Dengan menggunakan I-CON X.2, indikator dapat dihubungkan dengan berbagai jenis perangkat tambahan seperti display eksternal, printer, dan lain-lain tanpa menggunakan kabel.',
    specs: ['Bluetooth', 'Wireless', 'Display & Printer'],
  },
  {
    name: 'I-CON X.1',
    image: iconX1,
    desc: 'I-CON X.1 merupakan produk inovasi baru dalam komunikasi data, yang memungkinkan indikator terhubung dengan berbagai jenis perangkat seperti display eksternal, printer, dan lain sebagainya. Produk ini dibentuk dari sebuah konverter yang dikemas secara ringkas, dengan desain yang sederhana dan kokoh.',
    specs: ['Original', 'Compact Design', 'Durable'],
  },
  {
    name: 'I-CON X.USB',
    image: iconXUsb,
    desc: 'I-CON X.USB merupakan penyempurnaan dari seri I-CON X Series sebelumnya. Dibuat dengan Teknologi USB terbaru untuk mengembangkan fungsi penyimpanan data berat. Output data csv.file terenkripsi dengan baik untuk memenuhi kebutuhan Anda dan kompatibel untuk dibuka di perangkat apa pun.',
    specs: ['USB Storage', 'Encrypted CSV', 'Universal'],
  },
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

/* Products */
.grid { display: grid; }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.product-card { background: #fff; border-radius: var(--radius-md); padding: 24px; box-shadow: var(--shadow-sm); border: 1px solid rgba(0,0,0,0.04); transition: transform 0.2s, box-shadow 0.2s; }
.product-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); }
.product-image { width: 100%; height: 160px; border-radius: var(--radius-md); overflow: hidden; margin-bottom: 14px; background: #f5f5f7; display: flex; align-items: center; justify-content: center; }
.product-image img { width: 100%; height: 100%; object-fit: contain; padding: 8px; }
.product-card h4 { font-size: 15px; font-weight: 700; margin-bottom: 6px; }
.product-card p { font-size: 13px; color: var(--text-secondary); margin-bottom: 14px; line-height: 1.6; }
.product-specs { display: flex; flex-wrap: wrap; gap: 6px; }
.spec-tag { background: var(--bg); color: var(--text-secondary); padding: 3px 10px; border-radius: 99px; font-size: 11px; font-weight: 600; }

/* Footer */
.footer { background: #1a0533; color: rgba(255,255,255,0.6); text-align: center; padding: 24px; font-size: 13px; }

@media (max-width: 768px) {
  .hero-title { font-size: 32px; }
  .grid-3 { grid-template-columns: 1fr !important; }
}

@media (max-width: 1024px) and (min-width: 769px) {
  .grid-3 { grid-template-columns: repeat(2, 1fr); }
}
</style>
