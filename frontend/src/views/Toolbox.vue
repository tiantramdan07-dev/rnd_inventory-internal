<template>
  <div>
    <div class="page-header">
      <div>
        <h1 class="page-title">Toolbox</h1>
        <p class="page-subtitle">Kelola inventori toolbox dan barang</p>
      </div>
      <button class="btn btn-primary" @click="openToolboxModal()">
        <i class="fas fa-plus"></i> Tambah Toolbox
      </button>
    </div>

    <!-- Toolbox List -->
    <div v-if="loading" style="text-align:center;padding:60px">
      <div class="spinner spinner-dark" style="width:36px;height:36px;margin:0 auto 12px"></div>
      <p style="color:var(--text-secondary)">Memuat data...</p>
    </div>

    <div v-else>
      <div v-if="!toolboxes.length" class="card">
        <div class="empty-state"><i class="fas fa-toolbox"></i><p>Belum ada toolbox. Tambah toolbox baru.</p></div>
      </div>

      <div class="grid grid-2" style="gap:20px" v-else>
        <div class="card" v-for="tb in toolboxes" :key="tb.id">
          <div class="card-header">
            <div class="d-flex align-center gap-12">
              <div class="tb-icon"><i class="fas fa-toolbox"></i></div>
              <div>
                <h3 style="font-size:15px;font-weight:700">{{ tb.owner_name }}</h3>
                <p style="font-size:12px;color:var(--text-secondary)">{{ tb.item_count }} barang</p>
              </div>
            </div>
            <div class="d-flex gap-8">
              <button class="btn btn-ghost btn-icon" @click="openToolboxModal(tb)" title="Edit"><i class="fas fa-edit text-primary"></i></button>
              <button class="btn btn-ghost btn-icon" @click="addItem(tb)" title="Tambah Barang"><i class="fas fa-plus text-success"></i></button>
              <button class="btn btn-ghost btn-icon" @click="deleteToolbox(tb)" title="Hapus"><i class="fas fa-trash text-danger"></i></button>
            </div>
          </div>
          <div class="card-body" style="padding:0">
            <div v-if="tb.items && tb.items.length">
              <div class="item-row" v-for="item in tb.items" :key="item.id">
                <div class="item-photo">
                  <img v-if="item.photo_url" :src="item.photo_url" :alt="item.name" />
                  <div v-else class="photo-placeholder"><i class="fas fa-image"></i></div>
                </div>
                <div class="item-info">
                  <strong>{{ item.name }}</strong>
                  <span>{{ item.description || 'Tidak ada deskripsi' }}</span>
                  <div class="d-flex gap-8 mt-4">
                    <span class="badge badge-gray">Qty: {{ item.quantity }}</span>
                    <span class="badge" :class="item.status === 'Tersedia' ? 'badge-success' : 'badge-warning'">{{ item.status }}</span>
                    <span class="badge badge-gray">{{ item.condition }}</span>
                  </div>
                </div>
                <div class="item-actions">
                  <button class="btn btn-ghost btn-icon btn-sm" @click="openItemModal(item, tb.id)" title="Edit"><i class="fas fa-edit text-primary"></i></button>
                  <button class="btn btn-ghost btn-icon btn-sm" @click="deleteItem(item)" title="Hapus"><i class="fas fa-trash text-danger"></i></button>
                </div>
              </div>
            </div>
            <div class="empty-state" style="padding:32px" v-else>
              <i class="fas fa-box-open" style="font-size:32px"></i>
              <p>Belum ada barang. Klik + untuk menambah.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Toolbox Modal -->
    <div class="modal-overlay" v-if="showToolboxModal" @click.self="closeToolboxModal">
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">{{ editingToolbox ? 'Edit Toolbox' : 'Tambah Toolbox' }}</h3>
          <button class="btn btn-ghost btn-icon" @click="closeToolboxModal"><i class="fas fa-times"></i></button>
        </div>
        <div class="modal-body">
          <div class="form-group" v-if="canChooseOwner">
            <label class="form-label">Nama Pemilik <span style="color:red">*</span></label>
            <input v-model="toolboxForm.owner_name" class="form-control" placeholder="Nama pemilik toolbox" />
          </div>
          <div class="form-group" v-else>
            <label class="form-label">Nama Pemilik</label>
            <input :value="authStore.user?.full_name" class="form-control" disabled />
          </div>
          <div class="form-group">
            <label class="form-label">Deskripsi</label>
            <textarea v-model="toolboxForm.description" class="form-control" placeholder="Deskripsi toolbox (opsional)"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-ghost" @click="closeToolboxModal">Batal</button>
          <button class="btn btn-primary" @click="saveToolbox" :disabled="saving">
            <span class="spinner" v-if="saving"></span>
            <i class="fas fa-save" v-else></i> Simpan
          </button>
        </div>
      </div>
    </div>

    <!-- Item Modal -->
    <div class="modal-overlay" v-if="showItemModal" @click.self="closeItemModal">
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">{{ editingItem ? 'Edit Barang' : 'Tambah Barang' }}</h3>
          <button class="btn btn-ghost btn-icon" @click="closeItemModal"><i class="fas fa-times"></i></button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Nama Barang <span style="color:red">*</span></label>
            <input v-model="itemForm.name" class="form-control" placeholder="Nama barang" />
          </div>
          <div class="form-group">
            <label class="form-label">Deskripsi</label>
            <textarea v-model="itemForm.description" class="form-control" placeholder="Detail barang"></textarea>
          </div>
          <div class="grid grid-2 gap-12">
            <div class="form-group">
              <label class="form-label">Jumlah</label>
              <input v-model.number="itemForm.quantity" class="form-control" type="number" min="1" />
            </div>
            <div class="form-group">
              <label class="form-label">Kondisi</label>
              <select v-model="itemForm.condition" class="form-control">
                <option>Baik</option>
                <option>Rusak</option>
                <option>Perlu Perbaikan</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label class="form-label">Foto Barang</label>
            <div class="photo-upload-box" @click="$refs.fileInput.click()">
              <img v-if="itemForm.photo_url" :src="itemForm.photo_url" class="uploaded-preview" />
              <div v-else class="upload-placeholder">
                <i class="fas fa-camera"></i>
                <span>Klik untuk unggah foto</span>
              </div>
              <input ref="fileInput" type="file" accept="image/*" @change="handleFileUpload" style="display:none" />
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-ghost" @click="closeItemModal">Batal</button>
          <button class="btn btn-primary" @click="saveItem" :disabled="saving">
            <span class="spinner" v-if="saving"></span>
            <i class="fas fa-save" v-else></i> Simpan
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const canChooseOwner = computed(() => authStore.isAdmin || authStore.isRnd)

const toolboxes = ref([])
const loading = ref(true)
const saving = ref(false)

const showToolboxModal = ref(false)
const showItemModal = ref(false)
const editingToolbox = ref(null)
const editingItem = ref(null)
const currentToolboxId = ref(null)

const toolboxForm = ref({ owner_name: '', description: '' })
const itemForm = ref({ name: '', description: '', quantity: 1, condition: 'Baik', photo_url: '' })

async function fetchToolboxes() {
  loading.value = true
  try {
    const { data } = await axios.get('/toolbox')
    toolboxes.value = data
  } finally { loading.value = false }
}

function openToolboxModal(tb = null) {
  editingToolbox.value = tb
  toolboxForm.value = tb ? { owner_name: tb.owner_name, description: tb.description || '' } : { owner_name: canChooseOwner.value ? '' : (authStore.user?.full_name || ''), description: '' }
  showToolboxModal.value = true
}

function closeToolboxModal() { showToolboxModal.value = false; editingToolbox.value = null }

async function saveToolbox() {
  if (canChooseOwner.value && !toolboxForm.value.owner_name.trim()) return
  saving.value = true
  try {
    if (editingToolbox.value) {
      await axios.put(`/toolbox/${editingToolbox.value.id}`, toolboxForm.value)
    } else {
      await axios.post('/toolbox', toolboxForm.value)
    }
    await fetchToolboxes()
    closeToolboxModal()
  } finally { saving.value = false }
}

async function deleteToolbox(tb) {
  if (!confirm(`Hapus toolbox "${tb.owner_name}"? Semua barang di dalamnya juga akan dihapus.`)) return
  await axios.delete(`/toolbox/${tb.id}`)
  await fetchToolboxes()
}

function addItem(tb) { openItemModal(null, tb.id) }

function openItemModal(item = null, toolboxId = null) {
  editingItem.value = item
  currentToolboxId.value = toolboxId || item?.toolbox_id
  itemForm.value = item ? { name: item.name, description: item.description || '', quantity: item.quantity, condition: item.condition, photo_url: item.photo_url || '' } : { name: '', description: '', quantity: 1, condition: 'Baik', photo_url: '' }
  showItemModal.value = true
}

function closeItemModal() { showItemModal.value = false; editingItem.value = null }

async function handleFileUpload(e) {
  const file = e.target.files[0]
  if (!file) return
  const fd = new FormData()
  fd.append('file', file)
  const { data } = await axios.post('/upload/toolbox', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
  itemForm.value.photo_url = data.url
}

async function saveItem() {
  if (!itemForm.value.name.trim()) return
  saving.value = true
  try {
    if (editingItem.value) {
      await axios.put(`/toolbox/items/${editingItem.value.id}`, itemForm.value)
    } else {
      await axios.post(`/toolbox/${currentToolboxId.value}/items`, itemForm.value)
    }
    await fetchToolboxes()
    closeItemModal()
  } finally { saving.value = false }
}

async function deleteItem(item) {
  if (!confirm(`Hapus barang "${item.name}"?`)) return
  await axios.delete(`/toolbox/items/${item.id}`)
  await fetchToolboxes()
}

onMounted(fetchToolboxes)
</script>

<style scoped>
.tb-icon { width: 42px; height: 42px; background: var(--primary-light); border-radius: var(--radius-sm); display: flex; align-items: center; justify-content: center; color: var(--primary); font-size: 18px; }

.item-row { display: flex; align-items: center; gap: 14px; padding: 12px 16px; border-bottom: 1px solid var(--border); }
.item-row:last-child { border-bottom: none; }

.item-photo { width: 52px; height: 52px; border-radius: var(--radius-sm); overflow: hidden; flex-shrink: 0; background: var(--bg); }
.item-photo img { width: 100%; height: 100%; object-fit: cover; }
.photo-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: #ccc; font-size: 20px; }

.item-info { flex: 1; min-width: 0; }
.item-info strong { display: block; font-size: 13px; font-weight: 700; }
.item-info span { font-size: 11px; color: var(--text-secondary); display: block; }

.item-actions { display: flex; gap: 4px; }

.photo-upload-box {
  border: 2px dashed var(--border);
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: border-color 0.2s;
  min-height: 120px;
  display: flex; align-items: center; justify-content: center;
}
.photo-upload-box:hover { border-color: var(--primary); }
.uploaded-preview { width: 100%; max-height: 200px; object-fit: contain; }
.upload-placeholder { display: flex; flex-direction: column; align-items: center; gap: 8px; color: #aaa; font-size: 13px; padding: 20px; }
.upload-placeholder i { font-size: 28px; }
.gap-12 { gap: 12px; }
</style>