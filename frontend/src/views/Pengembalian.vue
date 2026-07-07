<template>
  <div>
    <div class="page-header">
      <div>
        <h1 class="page-title">Pengembalian</h1>
        <p class="page-subtitle">Catat pengembalian barang yang dipinjam</p>
      </div>
    </div>

    <div class="grid grid-2" style="gap:24px;align-items:start">
      <div class="card">
        <div class="card-header">
          <h3 style="font-size:15px;font-weight:700"><i class="fas fa-undo-alt text-success"></i> Form Pengembalian</h3>
        </div>
        <div class="card-body">
          <div class="alert alert-success" v-if="successMsg"><i class="fas fa-check-circle"></i> {{ successMsg }}</div>
          <div class="alert alert-danger" v-if="errorMsg"><i class="fas fa-exclamation-circle"></i> {{ errorMsg }}</div>

          <div class="form-group">
            <label class="form-label">Nama yang Mengembalikan <span style="color:red">*</span></label>
            <input v-model="form.returner_name" class="form-control" placeholder="Nama lengkap" />
          </div>

          <div class="form-group">
            <label class="form-label">Divisi <span style="color:red">*</span></label>
            <select v-model="form.division" class="form-control">
              <option value="">-- Pilih Divisi --</option>
              <option>R&D</option>
              <option>Teknisi</option>
              <option>Sales</option>
              <option>Marketing</option>
              <option>Operasional</option><option>Admin</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Pilih Barang yang Dikembalikan <span style="color:red">*</span></label>
            <select v-model="form.peminjaman_id" class="form-control">
              <option value="">-- Pilih Barang --</option>
              <option v-for="loan in activeLoans" :key="loan.id" :value="loan.id">
                {{ loan.item_name }} — dipinjam oleh {{ loan.borrower_name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label">Catatan Kondisi <span style="color:var(--text-secondary);font-weight:400">(opsional)</span></label>
            <textarea v-model="form.condition_note" class="form-control" placeholder="Kondisi barang saat dikembalikan..."></textarea>
          </div>

          <div class="form-group">
            <label class="form-label">Foto Bukti <span style="color:red">*</span></label>
            <div class="camera-section">
              <div class="camera-preview" v-show="!capturedPhoto">
                <video ref="videoEl" autoplay playsinline></video>
              </div>
              <div class="camera-preview" v-show="capturedPhoto">
                <img :src="capturedPhoto" alt="Foto" />
              </div>
              <canvas ref="canvasEl" style="display:none"></canvas>
              <div class="camera-controls">
                <button class="btn btn-secondary btn-sm" @click="startCamera" v-if="!cameraOn && !capturedPhoto">
                  <i class="fas fa-camera"></i> Buka Kamera
                </button>
                <button class="btn btn-primary btn-sm" @click="capture" v-if="cameraOn && !capturedPhoto">
                  <i class="fas fa-circle"></i> Ambil Foto
                </button>
                <button class="btn btn-danger btn-sm" @click="retake" v-if="capturedPhoto">
                  <i class="fas fa-redo"></i> Ulangi
                </button>
                <span v-if="capturedPhoto" class="badge badge-success"><i class="fas fa-check"></i> Foto diambil</span>
              </div>
            </div>
          </div>

          <button class="btn btn-success" style="width:100%;justify-content:center" @click="submit" :disabled="saving">
            <span class="spinner" v-if="saving"></span>
            <i class="fas fa-check-circle" v-else></i>
            {{ saving ? 'Menyimpan...' : 'Konfirmasi Pengembalian' }}
          </button>
        </div>
      </div>

      <!-- Active Loans list -->
      <div class="card">
        <div class="card-header">
          <h3 style="font-size:15px;font-weight:700">Daftar Barang Dipinjam</h3>
          <span class="badge badge-warning">{{ activeLoans.length }}</span>
        </div>
        <div class="card-body" style="padding:0">
          <div v-if="activeLoans.length">
            <div class="loan-item" v-for="loan in activeLoans" :key="loan.id">
              <div class="loan-dot orange"></div>
              <div class="loan-info">
                <strong>{{ loan.item_name }}</strong>
                <span>Peminjam: {{ loan.borrower_name }}</span>
                <span>{{ loan.division }}</span>
                <span style="font-size:10px;color:#aaa">{{ formatTime(loan.borrowed_at) }}</span>
              </div>
            </div>
          </div>
          <div class="empty-state" v-else>
            <i class="fas fa-box-open"></i>
            <p>Tidak ada barang yang dipinjam</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import { format } from 'date-fns'

const form = ref({ returner_name: '', division: '', peminjaman_id: '', condition_note: '' })
const activeLoans = ref([])
const saving = ref(false)
const successMsg = ref('')
const errorMsg = ref('')

const videoEl = ref(null)
const canvasEl = ref(null)
const cameraOn = ref(false)
const capturedPhoto = ref('')
let stream = null

async function fetchLoans() {
  const { data } = await axios.get('/pengembalian/active-loans')
  activeLoans.value = data
}

async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
    videoEl.value.srcObject = stream
    cameraOn.value = true
  } catch { errorMsg.value = 'Tidak dapat mengakses kamera.' }
}

function capture() {
  const v = videoEl.value, c = canvasEl.value
  c.width = v.videoWidth; c.height = v.videoHeight
  c.getContext('2d').drawImage(v, 0, 0)
  capturedPhoto.value = c.toDataURL('image/jpeg', 0.85)
  stopCamera()
}

function retake() { capturedPhoto.value = ''; startCamera() }

function stopCamera() {
  if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null }
  cameraOn.value = false
}

async function submit() {
  if (!form.value.returner_name || !form.value.division || !form.value.peminjaman_id) {
    errorMsg.value = 'Semua field wajib diisi'; return
  }
  if (!capturedPhoto.value) { errorMsg.value = 'Foto bukti wajib diambil'; return }
  saving.value = true; errorMsg.value = ''
  try {
    let photoUrl = null
    const blob = await (await fetch(capturedPhoto.value)).blob()
    const fd = new FormData()
    fd.append('file', blob, 'pengembalian.jpg')
    const { data: uploadData } = await axios.post('/upload/pengembalian', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    photoUrl = uploadData.url
    await axios.post('/pengembalian', { ...form.value, photo_url: photoUrl })
    successMsg.value = 'Pengembalian berhasil dicatat!'
    form.value = { returner_name: '', division: '', peminjaman_id: '', condition_note: '' }
    capturedPhoto.value = ''
    await fetchLoans()
    setTimeout(() => successMsg.value = '', 3000)
  } catch (e) {
    errorMsg.value = e.response?.data?.message || 'Gagal menyimpan'
  } finally { saving.value = false }
}

function formatTime(t) {
  if (!t) return '-'
  try { return format(new Date(t), 'dd/MM/yyyy HH:mm') } catch { return t }
}

onMounted(fetchLoans)
onUnmounted(stopCamera)
</script>

<style scoped>
.camera-section { display: flex; flex-direction: column; gap: 10px; }
.camera-preview { width: 100%; border-radius: var(--radius-md); overflow: hidden; background: #111; aspect-ratio: 4/3; }
.camera-preview video, .camera-preview img { width: 100%; height: 100%; object-fit: cover; }
.camera-controls { display: flex; align-items: center; gap: 10px; }
.loan-item { display: flex; align-items: flex-start; gap: 12px; padding: 12px 16px; border-bottom: 1px solid var(--border); }
.loan-item:last-child { border-bottom: none; }
.loan-dot { width: 10px; height: 10px; border-radius: 50%; margin-top: 4px; flex-shrink: 0; }
.loan-dot.orange { background: var(--warning); }
.loan-info { display: flex; flex-direction: column; gap: 2px; }
.loan-info strong { font-size: 13px; font-weight: 700; }
.loan-info span { font-size: 12px; color: var(--text-secondary); }
</style>
