<template>
  <aside class="sidebar" :class="{ collapsed: !isOpen }">
    <div class="sidebar-logo">
      <img src="/logo.png" alt="Logo" class="logo-img" @error="logoError = true" v-if="!logoError" />
      <div class="logo-fallback" v-else><i class="fas fa-flask"></i></div>
      <div class="logo-text" v-show="isOpen">
        <span class="logo-company">PT Interskala</span>
        <span class="logo-company">Mandiri Indonesia</span>
      </div>
    </div>

    <nav class="sidebar-nav">
      <div class="nav-section">
        <span class="nav-section-title" v-show="isOpen">Dashboard</span>
        <RouterLink to="/app/dashboard" class="nav-item" active-class="active">
          <span class="nav-icon"><i class="fas fa-th-large"></i></span>
          <span class="nav-label" v-show="isOpen">Dashboard</span>
        </RouterLink>
      </div>

      <div class="nav-section">
        <span class="nav-section-title" v-show="isOpen">Master Data</span>
        <RouterLink to="/app/toolbox" class="nav-item" active-class="active">
          <span class="nav-icon"><i class="fas fa-toolbox"></i></span>
          <span class="nav-label" v-show="isOpen">Toolbox</span>
        </RouterLink>
        <RouterLink to="/app/peminjaman" class="nav-item" active-class="active">
          <span class="nav-icon"><i class="fas fa-hand-holding"></i></span>
          <span class="nav-label" v-show="isOpen">Peminjaman</span>
        </RouterLink>
        <RouterLink to="/app/pengembalian" class="nav-item" active-class="active">
          <span class="nav-icon"><i class="fas fa-undo-alt"></i></span>
          <span class="nav-label" v-show="isOpen">Pengembalian</span>
        </RouterLink>
        <RouterLink to="/app/riwayat" class="nav-item" active-class="active">
          <span class="nav-icon"><i class="fas fa-history"></i></span>
          <span class="nav-label" v-show="isOpen">Riwayat</span>
        </RouterLink>
      </div>

      <div class="nav-section" v-if="auth.isTeknisi">
        <span class="nav-section-title" v-show="isOpen">Teknisi</span>
        <RouterLink to="/app/service" class="nav-item" active-class="active">
          <span class="nav-icon"><i class="fas fa-wrench"></i></span>
          <span class="nav-label" v-show="isOpen">Servis Teknisi</span>
        </RouterLink>
        <RouterLink to="/app/laporan" class="nav-item" active-class="active">
          <span class="nav-icon"><i class="fas fa-clipboard-list"></i></span>
          <span class="nav-label" v-show="isOpen">Laporan Harian</span>
        </RouterLink>
      </div>

      <div class="nav-section" v-if="auth.isAdmin">
        <span class="nav-section-title" v-show="isOpen">Sistem</span>
        <RouterLink to="/app/users" class="nav-item" active-class="active">
          <span class="nav-icon"><i class="fas fa-users-cog"></i></span>
          <span class="nav-label" v-show="isOpen">User Management</span>
        </RouterLink>
      </div>
    </nav>

    <div class="sidebar-footer" v-show="isOpen">
      <span>Created by R&D and Technician</span>
      <span>PT Interskala Mandiri Indonesia</span>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

defineProps({ isOpen: { type: Boolean, default: true } })
const auth = useAuthStore()
const logoError = ref(false)
</script>

<style scoped>
.sidebar {
  width: var(--sidebar-width);
  min-height: 100vh;
  background: var(--sidebar-bg);
  box-shadow: 2px 0 8px rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  transition: width 0.25s ease;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
}

.sidebar.collapsed { width: 64px; }

.sidebar-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 18px 16px;
  border-bottom: 1px solid var(--border);
  min-height: var(--navbar-height);
}

.logo-img { width: 36px; height: 36px; object-fit: contain; flex-shrink: 0; }
.logo-fallback {
  width: 36px; height: 36px;
  background: var(--primary-gradient);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 16px;
  flex-shrink: 0;
}

.logo-text { display: flex; flex-direction: column; overflow: hidden; }
.logo-company { font-size: 13px; font-weight: 800; color: var(--primary); white-space: nowrap; }
.logo-sub { font-size: 10px; color: var(--text-secondary); white-space: nowrap; }

.sidebar-nav { flex: 1; padding: 12px 8px; overflow-y: auto; }

.nav-section { margin-bottom: 8px; }

.nav-section-title {
  display: block;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--text-secondary);
  padding: 10px 12px 6px;
  white-space: nowrap;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 9px 12px;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 13.5px;
  font-weight: 500;
  transition: all 0.18s ease;
  margin-bottom: 2px;
  white-space: nowrap;
  overflow: hidden;
}

.nav-item:hover {
  background: var(--primary-light);
  color: var(--primary);
}

.nav-item.active {
  background: var(--primary-gradient);
  color: #fff;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(123,94,167,0.3);
}

.nav-icon {
  width: 20px;
  text-align: center;
  font-size: 14px;
  flex-shrink: 0;
}

.nav-label { flex: 1; }

.sidebar-footer {
  padding: 14px 16px;
  border-top: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  font-size: 10px;
  color: var(--text-secondary);
  line-height: 1.5;
}
</style>
