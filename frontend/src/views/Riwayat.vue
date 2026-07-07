<template>
  <div>
    <div class="page-header">
      <div><h1 class="page-title">Riwayat</h1><p class="page-subtitle">Riwayat peminjaman dan pengembalian</p></div>
    </div>

    <div class="card mb-16">
      <div class="filter-bar">
        <!-- Type filter -->
        <select v-model="filters.type" class="form-control" style="width:160px" @change="fetchData">
          <option value="all">Semua</option>
          <option value="peminjaman">Peminjaman</option>
          <option value="pengembalian">Pengembalian</option>
        </select>

        <!-- Date filter -->
        <select v-model="filters.filter" class="form-control" style="width:160px" @change="onFilterChange">
          <option value="today">Hari Ini</option>
          <option value="7days">7 Hari Lalu</option>
          <option value="30days">Sebulan Lalu</option>
          <option value="custom">Custom</option>
        </select>

        <template v-if="filters.filter === 'custom'">
          <input v-model="filters.date_from" type="date" class="form-control" style="width:150px" @change="fetchData" />
          <span style="color:var(--text-secondary)">s/d</span>
          <input v-model="filters.date_to" type="date" class="form-control" style="width:150px" @change="fetchData" />
        </template>

        <div style="margin-left:auto;display:flex;gap:8px">
          <button class="btn btn-success btn-sm" @click="exportExcel" :disabled="exporting">
            <i class="fas fa-file-excel"></i> Excel
          </button>
          <button class="btn btn-danger btn-sm" @click="exportPdf" :disabled="exporting">
            <i class="fas fa-file-pdf"></i> PDF
          </button>
        </div>
      </div>

      <div class="card-body" style="padding:0">
        <div v-if="loading" style="text-align:center;padding:40px">
          <div class="spinner spinner-dark" style="width:32px;height:32px;margin:0 auto 10px"></div>
          <p style="color:var(--text-secondary)">Memuat...</p>
        </div>
        <div class="table-container" v-else>
          <table v-if="records.length">
            <thead>
              <tr>
                <th>No</th><th>Tipe</th><th>Nama</th><th>Divisi</th>
                <th>Barang</th><th>Catatan Kondisi</th><th>Foto</th><th>Waktu</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(r, i) in records" :key="r.id + r.record_type">
                <td style="color:var(--text-secondary)">{{ i + 1 }}</td>
                <td>
                  <span class="badge" :class="r.record_type === 'Peminjaman' ? 'badge-warning' : 'badge-success'">
                    {{ r.record_type }}
                  </span>
                </td>
                <td class="fw-semibold">{{ r.borrower_name || r.returner_name }}</td>
                <td>{{ r.division }}</td>
                <td>{{ r.item_name }}</td>
                <td style="max-width:150px;color:var(--text-secondary)">{{ r.condition_note || '-' }}</td>
                <td>
                  <img v-if="r.photo_url" :src="r.photo_url" style="width:40px;height:40px;object-fit:cover;border-radius:6px;cursor:pointer" @click="viewPhoto(r.photo_url)" />
                  <span v-else style="color:#ccc;font-size:12px">—</span>
                </td>
                <td style="font-size:12px;color:var(--text-secondary);white-space:nowrap">{{ formatTime(r.waktu) }}</td>
              </tr>
            </tbody>
          </table>
          <div class="empty-state" v-else>
            <i class="fas fa-history"></i>
            <p>Tidak ada data pada periode ini</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Photo Modal -->
    <div class="modal-overlay" v-if="photoModal" @click="photoModal = null">
      <div style="max-width:600px;width:100%">
        <img :src="photoModal" style="width:100%;border-radius:var(--radius-lg);box-shadow:var(--shadow-lg)" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { format } from 'date-fns'

const records = ref([])
const loading = ref(false)
const exporting = ref(false)
const photoModal = ref(null)

const filters = ref({
  type: 'all',
  filter: 'today',
  date_from: '',
  date_to: ''
})

function onFilterChange() {
  if (filters.value.filter !== 'custom') fetchData()
}

async function fetchData() {
  loading.value = true
  try {
    const { data } = await axios.get('/riwayat', { params: {
      type: filters.value.type,
      filter: filters.value.filter,
      date_from: filters.value.date_from,
      date_to: filters.value.date_to
    }})
    records.value = data
  } finally { loading.value = false }
}

async function exportExcel() {
  exporting.value = true
  try {
    const res = await axios.get('/riwayat/export/excel', {
      params: filters.value, responseType: 'blob'
    })
    downloadBlob(res.data, 'riwayat_inventori.xlsx')
  } finally { exporting.value = false }
}

async function exportPdf() {
  exporting.value = true
  try {
    const res = await axios.get('/riwayat/export/pdf', {
      params: filters.value, responseType: 'blob'
    })
    downloadBlob(res.data, 'riwayat_inventori.pdf')
  } finally { exporting.value = false }
}

function downloadBlob(data, filename) {
  const url = URL.createObjectURL(new Blob([data]))
  const a = document.createElement('a')
  a.href = url; a.download = filename; a.click()
  URL.revokeObjectURL(url)
}

function viewPhoto(url) { photoModal.value = url }

function formatTime(t) {
  if (!t) return '-'
  try { return format(new Date(t), 'dd/MM/yyyy HH:mm') } catch { return t }
}

onMounted(fetchData)
</script>
