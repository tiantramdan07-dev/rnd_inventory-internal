<template>
  <div>
    <div class="page-header">
      <div><h1 class="page-title">User Management</h1><p class="page-subtitle">Kelola akun pengguna sistem</p></div>
      <button class="btn btn-primary" @click="openModal()"><i class="fas fa-user-plus"></i> Tambah User</button>
    </div>

    <div class="card">
      <div class="filter-bar">
        <div class="search-box">
          <i class="fas fa-search"></i>
          <input v-model="search" class="form-control" placeholder="Cari nama atau username..." />
        </div>
        <select v-model="filterRole" class="form-control" style="width:140px">
          <option value="">Semua Role</option>
          <option value="admin">Admin</option>
          <option value="rnd">R&D</option>
          <option value="teknisi">Teknisi</option>
        </select>
      </div>

      <div class="card-body" style="padding:0">
        <div v-if="loading" style="text-align:center;padding:40px">
          <div class="spinner spinner-dark" style="width:32px;height:32px;margin:0 auto 10px"></div>
        </div>
        <div class="table-container" v-else>
          <table v-if="filteredUsers.length">
            <thead>
              <tr><th>No</th><th>Nama Lengkap</th><th>Username</th><th>Divisi</th><th>Role</th><th>Status</th><th>Aksi</th></tr>
            </thead>
            <tbody>
              <tr v-for="(u, i) in filteredUsers" :key="u.id">
                <td>{{ i+1 }}</td>
                <td>
                  <div class="d-flex align-center gap-12">
                    <div class="user-avatar">{{ initials(u.full_name) }}</div>
                    <span class="fw-semibold">{{ u.full_name }}</span>
                  </div>
                </td>
                <td style="font-family:monospace;color:var(--primary)">{{ u.username }}</td>
                <td>{{ u.division || '-' }}</td>
                <td><span class="badge" :class="roleClass(u.role)">{{ roleLabel(u.role) }}</span></td>
                <td>
                  <span class="badge" :class="u.is_active ? 'badge-success' : 'badge-danger'">
                    {{ u.is_active ? 'Aktif' : 'Nonaktif' }}
                  </span>
                </td>
                <td>
                  <div class="d-flex gap-8">
                    <button class="btn btn-ghost btn-icon btn-sm" @click="openModal(u)" title="Edit"><i class="fas fa-edit text-primary"></i></button>
                    <button class="btn btn-ghost btn-icon btn-sm" @click="deleteUser(u)" title="Hapus" :disabled="u.id === authStore.user?.id"><i class="fas fa-trash text-danger"></i></button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="empty-state" v-else><i class="fas fa-users"></i><p>Tidak ada user</p></div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal-overlay" v-if="showModal" @click.self="closeModal">
      <div class="modal">
        <div class="modal-header">
          <h3 class="modal-title">{{ editing ? 'Edit User' : 'Tambah User' }}</h3>
          <button class="btn btn-ghost btn-icon" @click="closeModal"><i class="fas fa-times"></i></button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">Nama Lengkap <span style="color:red">*</span></label>
            <input v-model="form.full_name" class="form-control" placeholder="Nama lengkap" />
          </div>
          <div class="form-group">
            <label class="form-label">Username <span style="color:red">*</span></label>
            <input v-model="form.username" class="form-control" placeholder="Username unik" />
          </div>
          <div class="form-group">
            <label class="form-label">Password {{ editing ? '(kosongkan jika tidak diubah)' : '' }} <span v-if="!editing" style="color:red">*</span></label>
            <div style="position:relative">
              <input v-model="form.password" :type="showPw ? 'text' : 'password'" class="form-control" placeholder="Password" />
              <button type="button" style="position:absolute;right:12px;top:50%;transform:translateY(-50%);background:none;border:none;color:#aaa;cursor:pointer" @click="showPw=!showPw">
                <i :class="showPw ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
          </div>
          <div class="grid grid-2" style="gap:12px">
            <div class="form-group">
              <label class="form-label">Role</label>
              <select v-model="form.role" class="form-control">
                <option value="admin">Admin</option>
                <option value="rnd">R&D</option>
                <option value="teknisi">Teknisi</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Divisi</label>
              <select v-model="form.division" class="form-control">
                <option value="">-- Pilih --</option>
                <option>RnD</option><option>Teknisi</option><option>Admin</option><option>Sales</option>
              </select>
            </div>
          </div>
          <div class="form-group" v-if="editing">
            <label class="form-label" style="display:flex;align-items:center;gap:10px;cursor:pointer">
              <input type="checkbox" v-model="form.is_active" style="width:16px;height:16px" />
              Akun Aktif
            </label>
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
import { useAuthStore } from '@/stores/auth.js'

const authStore = useAuthStore()
const users = ref([])
const loading = ref(true)
const saving = ref(false)
const showModal = ref(false)
const editing = ref(null)
const search = ref('')
const filterRole = ref('')
const showPw = ref(false)

const emptyForm = () => ({ full_name: '', username: '', password: '', role: 'teknisi', division: '', is_active: true })
const form = ref(emptyForm())

const filteredUsers = computed(() => {
  return users.value.filter(u => {
    const matchSearch = !search.value || u.full_name.toLowerCase().includes(search.value.toLowerCase()) || u.username.toLowerCase().includes(search.value.toLowerCase())
    const matchRole = !filterRole.value || u.role === filterRole.value
    return matchSearch && matchRole
  })
})

function initials(name) { return (name || 'U').split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase() }

function roleLabel(r) { return { admin: 'Admin', rnd: 'R&D', teknisi: 'Teknisi' }[r] || r }

function roleClass(r) { return { admin: 'badge-danger', rnd: 'badge-primary', teknisi: 'badge-secondary' }[r] || 'badge-gray' }

async function fetchUsers() {
  loading.value = true
  try { const { data } = await axios.get('/users'); users.value = data }
  finally { loading.value = false }
}

function openModal(u = null) {
  editing.value = u
  showPw.value = false
  form.value = u ? { full_name: u.full_name, username: u.username, password: '', role: u.role, division: u.division || '', is_active: u.is_active } : emptyForm()
  showModal.value = true
}
function closeModal() { showModal.value = false; editing.value = null }

async function save() {
  if (!form.value.full_name || !form.value.username) return
  if (!editing.value && !form.value.password) return
  saving.value = true
  try {
    if (editing.value) await axios.put(`/users/${editing.value.id}`, form.value)
    else await axios.post('/users', form.value)
    await fetchUsers(); closeModal()
  } finally { saving.value = false }
}

async function deleteUser(u) {
  if (u.id === authStore.user?.id) return
  if (!confirm(`Hapus user "${u.full_name}"?`)) return
  await axios.delete(`/users/${u.id}`)
  await fetchUsers()
}

onMounted(fetchUsers)
</script>

<style scoped>
.user-avatar {
  width: 34px; height: 34px;
  background: var(--primary-gradient);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 12px; font-weight: 700;
  flex-shrink: 0;
}
</style>
