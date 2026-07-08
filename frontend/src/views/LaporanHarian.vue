<template>
  <div>
    <div class="page-header">
      <div><h1 class="page-title">Laporan Harian Teknisi</h1><p class="page-subtitle">Catatan pekerjaan harian teknisi</p></div>
      <button class="btn btn-primary" @click="openModal()"><i class="fas fa-plus"></i> Tambah Laporan</button>
    </div>

    <div class="card mb-16">
      <div class="filter-bar">
        <select v-model="filters.filter" class="form-control" style="width:160px" @change="onFilterChange">
          <option value="today">Hari Ini</option>
          <option value="7days">7 Hari Lalu</option>
          <option value="30days">Sebulan Lalu</option>
          <option value="custom">Custom</option>
        </select>
        <template v-if="filters.filter === 'custom'">
          <input v-model="filters.date_from" type="date" class="form-control" style="width:150px" @change="fetchData" />
          <span>s/d</span>
          <input v-model="filters.date_to" type="date" class="form-control" style="width:150px" @change="fetchData" />
        </template>
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input v-model="search" class="form-control" placeholder="Cari pekerjaan, produk..." />
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
                <th>No</th><th>Tanggal</th><th>Hari</th><th>Teknisi</th>
                <th>Pekerjaan</th><th>Produk</th><th>Info Tambahan</th>
                <th>Garansi</th><th>Jam Mulai</th><th>Jam Selesai</th><th>Foto</th><th>Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(r, i) in filteredRecords" :key="r.id">
                <td>{{ i+1 }}</td>
                <td style="white-space:nowrap">{{ formatDate(r.tanggal) }}</td>
                <td>{{ r.hari }}</td>
                <td class="fw-semibold">{{ r.teknisi_name }}</td>
                <td style="max-width:200px">{{ r.pekerjaan }}</td>
                <td>{{ r.produk || '-' }}</td>
                <td style="max-width:160px;color:var(--text-secondary)">{{ r.informasi_tambahan || '-' }}</td>
                <td>
                  <span class="badge" :class="r.status_garansi ? 'badge-success' : 'badge-gray'">
                    {{ r.status_garansi ? 'Garansi' : 'Non-Garansi' }}
                  </span>
                </td>
                <td>{{ r.jam_start || '-' }}</td>
                <td>{{ r.jam_end || '-' }}</td>
                <td>
                  <img v-if="r.foto_url" :src="r.foto_url" style="width:40px;height:40px;object-fit:cover;border-radius:6px;cursor:pointer" @click="photoModal = r.foto_url" />
                  <span v-else style="color:#ccc;font-size:12px">—</span>
                </td>
                <td>
                  <div class="d-flex gap-8">
                    <button class="btn btn-ghost btn-icon btn-sm" @click="openModal(r)"><i class="fas fa-edit text-primary"></i></button>
                    <button class="btn btn-ghost btn-icon btn-sm" @click="deleteRecord(r)"><i class="fas fa-trash text-danger"></i></button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="empty-state" v-else><i class="fas fa-clipboard-list"></i><p>Belum ada laporan</p></div>
        </div>
      </div>
    </div>

    <!-- Form Modal -->
    <div class="modal-overlay" v-if="showModal" @click.self="closeModal">
      <div class="modal modal-lg">
        <div class="modal-header">
          <h3 class="modal-title">{{ editing ? 'Edit Laporan' : 'Tambah Laporan Harian' }}</h3>
          <button class="btn btn-ghost btn-icon" @click="closeModal"><i class="fas fa-times"></i></button>
        </div>
        <div class="modal-body">
          <div class="grid grid-2" style="gap:12px">
            <div class="form-group">
              <label class="form-label">Tanggal <span style="color:red">*</span></label>
              <input v-model="form.tanggal" type="date" class="form-control" />
            </div>
            <div class="form-group">
              <label class="form-label">Produk</label>
              <input v-model="form.produk" class="form-control" placeholder="Nama produk" />
            </div>
            <div class="form-group">
              <label class="form-label">Jam Mulai</label>
              <input v-model="form.jam_start" type="time" class="form-control" />
            </div>
            <div class="form-group">
              <label class="form-label">Jam Selesai</label>
              <input v-model="form.jam_end" type="time" class="form-control" />
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Pekerjaan <span style="color:red">*</span></label>
            <textarea v-model="form.pekerjaan" class="form-control" rows="3" placeholder="Deskripsi pekerjaan yang dilakukan..."></textarea>
          </div>
          <div class="form-group">
            <label class="form-label">Informasi Tambahan</label>
            <textarea v-model="form.informasi_tambahan" class="form-control" rows="2" placeholder="Informasi tambahan..."></textarea>
          </div>
          <div class="form-group">
            <label class="form-label" style="display:flex;align-items:center;gap:10px;cursor:pointer">
              <input type="checkbox" v-model="form.status_garansi" style="width:16px;height:16px" />
              Dalam Garansi
            </label>
          </div>
          <!-- Camera -->
          <div class="form-group">
            <label class="form-label">Foto Hasil Service</label>
            <div class="camera-section">
              <div class="camera-preview" v-show="!capturedPhoto && !form.foto_url">
                <video ref="videoEl" autoplay playsinline></video>
              </div>
              <div class="camera-preview" v-if="capturedPhoto || form.foto_url">
                <img :src="capturedPhoto || form.foto_url" />
              </div>
              <canvas ref="canvasEl" style="display:none"></canvas>
              <div class="camera-controls">
                <button type="button" class="btn btn-secondary btn-sm" @click="startCamera" v-if="!cameraOn && !capturedPhoto && !form.foto_url"><i class="fas fa-camera"></i> Buka Kamera</button>
                <button type="button" class="btn btn-primary btn-sm" @click="capture" v-if="cameraOn"><i class="fas fa-circle"></i> Ambil Foto</button>
                <button type="button" class="btn btn-danger btn-sm" @click="retake" v-if="capturedPhoto || form.foto_url"><i class="fas fa-redo"></i> Ulangi</button>
              </div>
            </div>
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

    <!-- Photo Modal -->
    <div class="modal-overlay" v-if="photoModal" @click="photoModal = null">
      <img :src="photoModal" style="max-width:90vw;max-height:90vh;border-radius:var(--radius-lg);object-fit:contain" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'

const records = ref([])
const loading = ref(true)
const saving = ref(false)
const showModal = ref(false)
const editing = ref(null)
const search = ref('')
const photoModal = ref(null)
const filters = ref({ filter: 'today', date_from: '', date_to: '' })

const videoEl = ref(null), canvasEl = ref(null)
const cameraOn = ref(false), capturedPhoto = ref('')
let stream = null

const emptyForm = () => ({
  tanggal: new Date().toISOString().split('T')[0], pekerjaan: '',
  produk: '', informasi_tambahan: '', status_garansi: false,
  jam_start: '', jam_end: '', foto_url: ''
})
const form = ref(emptyForm())

const filteredRecords = computed(() => {
  if (!search.value) return records.value
  const q = search.value.toLowerCase()
  return records.value.filter(r => r.pekerjaan?.toLowerCase().includes(q) || r.produk?.toLowerCase().includes(q))
})

function formatDate(d) { if (!d) return '-'; try { return d.split('-').reverse().join('/') } catch { return d } }

function onFilterChange() { if (filters.value.filter !== 'custom') fetchData() }

async function fetchData() {
  loading.value = true
  try {
    const { data } = await axios.get('/laporan', { params: filters.value })
    records.value = data
  } finally { loading.value = false }
}

function openModal(r = null) {
  editing.value = r
  capturedPhoto.value = ''
  form.value = r ? { ...r } : emptyForm()
  showModal.value = true
}
function closeModal() { showModal.value = false; editing.value = null; stopCamera() }

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    videoEl.value.srcObject = stream
    cameraOn.value = true
  } catch { alert('Tidak dapat mengakses kamera') }
}

function capture() {
  const v = videoEl.value, c = canvasEl.value
  c.width = v.videoWidth; c.height = v.videoHeight
  c.getContext('2d').drawImage(v, 0, 0)
  capturedPhoto.value = c.toDataURL('image/jpeg', 0.85)
  form.value.foto_url = ''
  stopCamera()
}

function retake() { capturedPhoto.value = ''; form.value.foto_url = ''; startCamera() }

function stopCamera() {
  if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null }
  cameraOn.value = false
}

async function save() {
  if (!form.value.tanggal || !form.value.pekerjaan) return
  saving.value = true
  try {
    let fotoUrl = form.value.foto_url
    if (capturedPhoto.value) {
      const blob = await (await fetch(capturedPhoto.value)).blob()
      const fd = new FormData()
      fd.append('file', blob, 'laporan.jpg')
      const { data } = await axios.post('/upload/laporan', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
      fotoUrl = data.url
    }
    const payload = { ...form.value, foto_url: fotoUrl }
    if (editing.value) await axios.put(`/laporan/${editing.value.id}`, payload)
    else await axios.post('/laporan', payload)
    await fetchData(); closeModal()
  } catch (err) {
    alert(err.response?.data?.message || 'Gagal menyimpan laporan. Silakan coba lagi.')
  } finally { saving.value = false }
}

async function deleteRecord(r) {
  if (!confirm('Hapus laporan ini?')) return
  await axios.delete(`/laporan/${r.id}`)
  await fetchData()
}

async function exportExcel() {
  const res = await axios.get('/laporan/export/excel', { params: filters.value, responseType: 'blob' })
  Object.assign(document.createElement('a'), { href: URL.createObjectURL(new Blob([res.data])), download: 'laporan_harian.xlsx' }).click()
}

async function exportPdf() {
  const res = await axios.get('/laporan/export/pdf', { params: filters.value, responseType: 'blob' })
  Object.assign(document.createElement('a'), { href: URL.createObjectURL(new Blob([res.data])), download: 'laporan_harian.pdf' }).click()
}

onMounted(fetchData)
onUnmounted(stopCamera)
</script>

<style scoped>
.camera-section { display: flex; flex-direction: column; gap: 10px; }
.camera-preview { width: 100%; border-radius: var(--radius-md); overflow: hidden; background: #111; aspect-ratio: 4/3; }
.camera-preview video, .camera-preview img { width: 100%; height: 100%; object-fit: cover; }
.camera-controls { display: flex; align-items: center; gap: 10px; }
</style>