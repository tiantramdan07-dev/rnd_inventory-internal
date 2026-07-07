<template>
  <header class="navbar">
    <div class="navbar-left">
      <button class="btn btn-ghost btn-icon" @click="$emit('toggle-sidebar')">
        <i class="fas fa-bars"></i>
      </button>
      <div class="breadcrumb">
        <span class="breadcrumb-page">{{ pageTitle }}</span>
      </div>
    </div>

    <div class="navbar-right">
      <div class="user-menu" @click="showDropdown = !showDropdown" ref="menuRef">
        <div class="avatar">
          {{ initials }}
        </div>
        <div class="user-info" v-if="!isMobile">
          <span class="user-name">{{ auth.user?.full_name }}</span>
          <span class="user-role">{{ roleLabel }}</span>
        </div>
        <i class="fas fa-chevron-down" style="font-size:11px;color:#aaa;"></i>

        <div class="dropdown" v-if="showDropdown">
          <div class="dropdown-header">
            <strong>{{ auth.user?.full_name }}</strong>
            <span>{{ auth.user?.division }}</span>
          </div>
          <div class="dropdown-divider"></div>
          <button class="dropdown-item" @click="logout">
            <i class="fas fa-sign-out-alt"></i> Keluar
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

emit: ['toggle-sidebar']
defineEmits(['toggle-sidebar'])

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const showDropdown = ref(false)
const menuRef = ref(null)
const isMobile = ref(window.innerWidth < 768)

const initials = computed(() => {
  const name = auth.user?.full_name || 'U'
  return name.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase()
})

const roleLabel = computed(() => {
  const map = { admin: 'Administrator', rnd: 'R&D', teknisi: 'Teknisi' }
  return map[auth.user?.role] || auth.user?.role
})

const pageTitle = computed(() => {
  const map = {
    Dashboard: 'Dashboard', Toolbox: 'Toolbox', Peminjaman: 'Peminjaman',
    Pengembalian: 'Pengembalian', Riwayat: 'Riwayat', ServiceTeknisi: 'Servis Teknisi',
    LaporanHarian: 'Laporan Harian Teknisi', UserManagement: 'User Management'
  }
  return map[route.name] || 'Dashboard'
})

function logout() {
  auth.logout()
  router.push('/login')
}

function handleClickOutside(e) {
  if (menuRef.value && !menuRef.value.contains(e.target)) {
    showDropdown.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
.navbar {
  height: var(--navbar-height);
  background: #fff;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-left { display: flex; align-items: center; gap: 12px; }

.breadcrumb-page {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
}

.navbar-right { display: flex; align-items: center; gap: 10px; }

.user-menu {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 12px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background 0.15s;
  position: relative;
}

.user-menu:hover { background: var(--bg); }

.avatar {
  width: 36px; height: 36px;
  background: var(--primary-gradient);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}

.user-info { display: flex; flex-direction: column; }
.user-name { font-size: 13px; font-weight: 600; color: var(--text-primary); }
.user-role { font-size: 11px; color: var(--text-secondary); }

.dropdown {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: #fff;
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-lg);
  border: 1px solid var(--border);
  min-width: 200px;
  z-index: 200;
  animation: slideUp 0.15s ease;
  overflow: hidden;
}

.dropdown-header {
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  background: var(--primary-light);
}

.dropdown-header strong { font-size: 13px; color: var(--primary); }
.dropdown-header span { font-size: 11px; color: var(--text-secondary); }

.dropdown-divider { height: 1px; background: var(--border); }

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 11px 16px;
  background: none;
  border: none;
  font-family: var(--font);
  font-size: 13px;
  cursor: pointer;
  color: var(--danger);
  transition: background 0.15s;
}

.dropdown-item:hover { background: #FFEBEE; }
</style>
