<template>
  <div class="dashboard">
    <div class="page-header">
      <div>
        <h1 class="page-title">Dashboard</h1>
        <p class="page-subtitle">Selamat datang, {{ auth.user?.full_name }} — {{ today }}</p>
      </div>
    </div>

    <!-- Stats -->
    <div class="grid grid-4 mb-20" v-if="stats">
      <div class="stat-card">
        <div class="stat-icon purple"><i class="fas fa-toolbox"></i></div>
        <div>
          <div class="stat-value">{{ stats.total_items }}</div>
          <div class="stat-label">Total Barang</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon orange"><i class="fas fa-hand-holding"></i></div>
        <div>
          <div class="stat-value">{{ stats.dipinjam }}</div>
          <div class="stat-label">Sedang Dipinjam</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green"><i class="fas fa-check-circle"></i></div>
        <div>
          <div class="stat-value">{{ stats.tersedia }}</div>
          <div class="stat-label">Tersedia</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon red"><i class="fas fa-exclamation-circle"></i></div>
        <div>
          <div class="stat-value">{{ stats.belum_kembali }}</div>
          <div class="stat-label">Belum Dikembalikan</div>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" style="text-align:center;padding:40px">
      <div class="spinner spinner-dark" style="width:36px;height:36px;margin:0 auto"></div>
      <p style="margin-top:12px;color:var(--text-secondary)">Memuat data...</p>
    </div>

    <!-- Recent Activity -->
    <div class="card" v-if="stats && !loading">
      <div class="card-header">
        <div>
          <h3 style="font-size:15px;font-weight:700">Aktivitas Terbaru</h3>
          <p style="font-size:12px;color:var(--text-secondary)">Peminjaman & pengembalian terkini</p>
        </div>
        <RouterLink to="/app/riwayat" class="btn btn-outline btn-sm">Lihat Semua</RouterLink>
      </div>
      <div class="card-body" style="padding:0">
        <div class="table-container">
          <table v-if="stats.recent_activity?.length">
            <thead>
              <tr>
                <th>Tipe</th>
                <th>Nama</th>
                <th>Divisi</th>
                <th>Barang</th>
                <th>Waktu</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="a in stats.recent_activity" :key="a.time + a.name">
                <td>
                  <span class="badge" :class="a.type === 'Peminjaman' ? 'badge-warning' : 'badge-success'">
                    <i :class="a.type === 'Peminjaman' ? 'fas fa-arrow-right' : 'fas fa-arrow-left'"></i>
                    {{ a.type }}
                  </span>
                </td>
                <td class="fw-semibold">{{ a.name }}</td>
                <td>{{ a.division }}</td>
                <td>{{ a.item }}</td>
                <td style="color:var(--text-secondary);font-size:12px">{{ formatTime(a.time) }}</td>
              </tr>
            </tbody>
          </table>
          <div class="empty-state" v-else>
            <i class="fas fa-inbox"></i>
            <p>Belum ada aktivitas</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-3 mt-16">
      <RouterLink to="/app/peminjaman" class="quick-action purple">
        <i class="fas fa-hand-holding"></i>
        <span>Catat Peminjaman</span>
      </RouterLink>
      <RouterLink to="/app/pengembalian" class="quick-action blue">
        <i class="fas fa-undo-alt"></i>
        <span>Catat Pengembalian</span>
      </RouterLink>
      <RouterLink to="/app/toolbox" class="quick-action green">
        <i class="fas fa-toolbox"></i>
        <span>Kelola Toolbox</span>
      </RouterLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'
import axios from 'axios'
import { format } from 'date-fns'
import { id } from 'date-fns/locale'

const auth = useAuthStore()
const stats = ref(null)
const loading = ref(true)

const today = computed(() => format(new Date(), 'EEEE, dd MMMM yyyy', { locale: id }))

function formatTime(t) {
  if (!t) return '-'
  try { return format(new Date(t), 'dd/MM/yyyy HH:mm') } catch { return t }
}

async function fetchStats() {
  try {
    const { data } = await axios.get('/dashboard/stats')
    stats.value = data
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

onMounted(fetchStats)
</script>

<style scoped>
.quick-action {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px 22px;
  border-radius: var(--radius-md);
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: var(--shadow-sm);
}

.quick-action:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
.quick-action i { font-size: 22px; }

.quick-action.purple { background: var(--primary-gradient); color: #fff; }
.quick-action.blue { background: linear-gradient(135deg, #2196F3, #1565C0); color: #fff; }
.quick-action.green { background: linear-gradient(135deg, #4CAF50, #2E7D32); color: #fff; }
</style>
