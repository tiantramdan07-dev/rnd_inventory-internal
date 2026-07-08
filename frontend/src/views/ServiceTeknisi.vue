<template>
  <div>
    <div class="page-header">
      <div><h1 class="page-title">Servis Teknisi</h1><p class="page-subtitle">Manajemen data servis teknisi keluar</p></div>
      <button class="btn btn-primary" @click="openModal()"><i class="fas fa-plus"></i> Tambah Service</button>
    </div>

    <!-- Filter -->
    <div class="card mb-16">
      <div class="filter-bar">
        <select v-model="filters.filter" class="form-control" style="width:160px" @change="onFilterChange">
          <option value="all">Semua</option>
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
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input v-model="search" class="form-control" placeholder="Cari customer, teknisi..." />
        </div>
        <div style="margin-left:auto;display:flex;gap:8px">
          <button class="btn btn-success btn-sm" @click="exportExcel"><i class="fas fa-file-excel"></i> Excel</button>
          <button class="btn btn-danger btn-sm" @click="exportPdf"><i class="fas fa-file-pdf"></i> PDF</button>
        </div>
      </div>

      <div class="card-body" style="padding:0">
        <div v-if="loading" style="text-align:center;padding:40px">
          <div class="spinner spinner-dark" style="width:32px;height:32px;margin:0 auto 10px"></div>
        </div>
        <div class="table-container" v-else>
          <table v-if="filteredRecords.length">
            <thead>
              <tr>
                <th>No</th><th>Nomor</th><th>Tgl Pengajuan</th><th>Teknisi</th>
                <th>Sales</th><th>Customer</th><th>Produk</th><th>Lokasi</th>
                <th>Tipe</th><th>Tgl Service</th><th>Tgl Selesai</th><th>Status</th><th v-if="auth.isAdmin">Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(s, i) in filteredRecords" :key="s.id">
                <td>{{ i+1 }}</td>
                <td class="fw-semibold text-primary" style="white-space:nowrap">{{ s.nomor }}</td>
                <td>{{ formatDate(s.tanggal_pengajuan) }}</td>
                <td>{{ s.nama_teknisi }}</td>
                <td>{{ s.nama_sales || '-' }}</td>
                <td class="fw-semibold">{{ s.customer }}</td>
                <td>{{ s.produk }}</td>
                <td>{{ s.lokasi || '-' }}</td>
                <td><span class="badge badge-primary">{{ s.tipe_service || '-' }}</span></td>
                <td>{{ formatDate(s.tanggal_service) }}</td>
                <td>{{ formatDate(s.tanggal_selesai) }}</td>
                <td><span class="badge" :class="statusClass(s.status)">{{ s.status }}</span></td>
                <td v-if="auth.isAdmin">
                  <div class="d-flex gap-8">
                    <button class="btn btn-ghost btn-icon btn-sm" @click="openModal(s)"><i class="fas fa-edit text-primary"></i></button>
                    <button class="btn btn-ghost btn-icon btn-sm" @click="deleteRecord(s)"><i class="fas fa-trash text-danger"></i></button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="empty-state" v-else><i class="fas fa-wrench"></i><p>Tidak ada data service</p></div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal-overlay" v-if="showModal" @click.self="closeModal">
      <div class="modal modal-lg">
        <div class="modal-header">
          <h3 class="modal-title">{{ editing ? 'Edit Service' : 'Tambah Service' }}</h3>
          <button class="btn btn-ghost btn-icon" @click="closeModal"><i class="fas fa-times"></i></button>
        </div>
        <div class="modal-body">
          <div class="grid grid-2" style="gap:12px">
            <div class="form-group">
              <label class="form-label">Tgl Pengajuan <span style="color:red">*</span></label>
              <input v-model="form.tanggal_pengajuan" type="date" class="form-control" />
            </div>
            <div class="form-group">
              <label class="form-label">Nama Teknisi <span style="color:red">*</span></label>
              <input v-model="form.nama_teknisi" class="form-control" placeholder="Nama teknisi" readonly :disabled="!editing" style="background:var(--bg-secondary, #f3f4f6);cursor:not-allowed" />
            </div>
            <div class="form-group">
              <label class="form-label">Nama Sales</label>
              <input v-model="form.nama_sales" class="form-control" placeholder="Nama sales" />
            </div>
            <div class="form-group">
              <label class="form-label">Customer <span style="color:red">*</span></label>
              <input v-model="form.customer" class="form-control" placeholder="Nama customer" />
            </div>
            <div class="form-group">
              <label class="form-label">Produk <span style="color:red">*</span></label>
              <input v-model="form.produk" class="form-control" placeholder="Nama produk" />
            </div>
            <div class="form-group">
              <label class="form-label">Lokasi / User</label>
              <input v-model="form.lokasi" class="form-control" placeholder="Lokasi / nama user" />
            </div>
            <div class="form-group">
              <label class="form-label">Tipe</label>
              <select v-model="form.tipe_service" class="form-control">
                <option value="">-- Pilih --</option>
                <option>Servis</option><option>Demo</option><option>Instalasi</option><option>Training</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Status</label>
              <select v-model="form.status" class="form-control">
                <option>Pending</option><option>Proses</option><option>Selesai</option><option>Batal</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Tanggal Service</label>
              <input v-model="form.tanggal_service" type="date" class="form-control" />
            </div>
            <div class="form-group">
              <label class="form-label">Tanggal Selesai</label>
              <input v-model="form.tanggal_selesai" type="date" class="form-control" />
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Keterangan</label>
            <textarea v-model="form.keterangan" class="form-control" rows="3" placeholder="Keterangan tambahan..."></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-ghost" @click="closeModal">Batal</button>
          <button class="btn btn-primary" @click="save" :disabled="saving">
            <span class="spinner" v-if="saving"></span>
            <i class="fas fa-save" v-else></i> Simpan
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const records = ref([])
const loading = ref(true)
const saving = ref(false)
const showModal = ref(false)
const editing = ref(null)
const search = ref('')
const filters = ref({ filter: 'all', date_from: '', date_to: '' })

const emptyForm = () => ({
  tanggal_pengajuan: new Date().toISOString().split('T')[0],
  nama_teknisi: auth.user?.full_name || '', nama_sales: '', customer: '', produk: '',
  lokasi: '', tipe_service: '', status: 'Pending',
  tanggal_service: '', tanggal_selesai: '', keterangan: ''
})
const form = ref(emptyForm())

const filteredRecords = computed(() => {
  if (!search.value) return records.value
  const q = search.value.toLowerCase()
  return records.value.filter(r =>
    r.customer?.toLowerCase().includes(q) || r.nama_teknisi?.toLowerCase().includes(q) ||
    r.produk?.toLowerCase().includes(q) || r.nomor?.toLowerCase().includes(q)
  )
})

function statusClass(s) {
  const m = { Pending: 'badge-warning', Proses: 'badge-primary', Selesai: 'badge-success', Batal: 'badge-danger' }
  return m[s] || 'badge-gray'
}

function formatDate(d) { if (!d) return '-'; try { return d.split('-').reverse().join('/') } catch { return d } }

function onFilterChange() { if (filters.value.filter !== 'custom') fetchData() }

async function fetchData() {
  loading.value = true
  try {
    const { data } = await axios.get('/service', { params: filters.value })
    records.value = data
  } finally { loading.value = false }
}

function openModal(s = null) {
  if (s && !auth.isAdmin) return
  editing.value = s
  form.value = s ? { ...s, tanggal_pengajuan: s.tanggal_pengajuan || '', tanggal_service: s.tanggal_service || '', tanggal_selesai: s.tanggal_selesai || '' } : emptyForm()
  showModal.value = true
}
function closeModal() { showModal.value = false; editing.value = null }

async function save() {
  if (!form.value.tanggal_pengajuan || !form.value.nama_teknisi || !form.value.customer || !form.value.produk) return
  saving.value = true
  try {
    if (editing.value) await axios.put(`/service/${editing.value.id}`, form.value)
    else await axios.post('/service', form.value)
    await fetchData(); closeModal()
  } finally { saving.value = false }
}

async function deleteRecord(s) {
  if (!auth.isAdmin) return
  if (!confirm(`Hapus data service ${s.nomor}?`)) return
  await axios.delete(`/service/${s.id}`)
  await fetchData()
}

async function exportExcel() {
  const res = await axios.get('/service/export/excel', { params: filters.value, responseType: 'blob' })
  const url = URL.createObjectURL(new Blob([res.data]))
  Object.assign(document.createElement('a'), { href: url, download: 'service_teknisi.xlsx' }).click()
}

async function exportPdf() {
  const res = await axios.get('/service/export/pdf', { params: filters.value, responseType: 'blob' })
  const url = URL.createObjectURL(new Blob([res.data]))
  Object.assign(document.createElement('a'), { href: url, download: 'service_teknisi.pdf' }).click()
}

onMounted(fetchData)
</script>