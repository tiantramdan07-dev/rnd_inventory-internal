<template>
  <div class="login-page">
    <div class="login-left">
      <div class="login-brand">
        <div class="brand-icon"><i class="fa-solid fa-scale-balanced"></i></div>
        <span>PT Interskala Mandiri Indonesia</span>
      </div>
      <div class="login-illustration">
        <div class="ill-circle c1"></div>
        <div class="ill-circle c2"></div>
        <div class="ill-circle c3"></div>
        <div class="ill-icon"><i class="fas fa-toolbox"></i></div>
      </div>
      <h2>Sistem Inventori<br/>R&D & Teknisi</h2>
      <p>Kelola toolbox, peminjaman, service, dan laporan harian.</p>
    </div>

    <div class="login-right">
      <div class="login-card">
        <div class="login-header">
          <h1>Selamat Datang</h1>
          <p>Masuk ke akun Anda untuk melanjutkan</p>
        </div>

        <div class="alert alert-danger" v-if="error">
          <i class="fas fa-exclamation-circle"></i> {{ error }}
        </div>

        <div class="form-group">
          <label class="form-label">Username</label>
          <div class="input-with-icon">
            <i class="fas fa-user"></i>
            <input v-model="form.username" class="form-control" type="text" placeholder="Masukkan username" @keydown.enter="handleLogin" />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label">Password</label>
          <div class="input-with-icon">
            <i class="fas fa-lock"></i>
            <input v-model="form.password" class="form-control" :type="showPw ? 'text' : 'password'" placeholder="Masukkan password" @keydown.enter="handleLogin" />
            <button class="pw-toggle" @click="showPw = !showPw" tabindex="-1">
              <i :class="showPw ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
        </div>

        <button class="btn btn-primary btn-login" @click="handleLogin" :disabled="loading">
          <span class="spinner" v-if="loading"></span>
          <i class="fas fa-sign-in-alt" v-else></i>
          {{ loading ? 'Memproses...' : 'Masuk' }}
        </button>

        <div class="login-hint">
          <i class="fas fa-info-circle"></i>
          Default: admin / admin123
        </div>

        <RouterLink to="/" class="back-link">
          <i class="fas fa-arrow-left"></i> Kembali ke Halaman Utama
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const router = useRouter()
const auth = useAuthStore()
const form = ref({ username: '', password: '' })
const loading = ref(false)
const error = ref('')
const showPw = ref(false)

async function handleLogin() {
  if (!form.value.username || !form.value.password) {
    error.value = 'Username dan password wajib diisi'
    return
  }
  loading.value = true
  error.value = ''
  try {
    await auth.login(form.value.username, form.value.password)
    router.push('/app/dashboard')
  } catch (e) {
    error.value = e.response?.data?.message || 'Login gagal. Periksa kembali username dan password.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
}

.login-left {
  width: 420px;
  flex-shrink: 0;
  background: linear-gradient(160deg, #1a0533 0%, #2d1b69 50%, #1a237e 100%);
  padding: 40px;
  display: flex;
  flex-direction: column;
  color: #fff;
  position: relative;
  overflow: hidden;
}

.login-brand { display: flex; align-items: center; gap: 12px; margin-bottom: 60px; }
.brand-icon { width: 40px; height: 40px; background: rgba(255,255,255,0.15); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; }
.login-brand span { font-size: 13px; font-weight: 700; }

.login-illustration { position: relative; height: 200px; margin-bottom: 40px; }
.ill-circle {
  position: absolute;
  border-radius: 50%;
  border: 2px solid rgba(255,255,255,0.15);
}
.c1 { width: 180px; height: 180px; top: 10px; left: 10px; animation: spin 20s linear infinite; }
.c2 { width: 120px; height: 120px; top: 40px; left: 40px; border-color: rgba(197,163,255,0.3); animation: spin 15s linear infinite reverse; }
.c3 { width: 60px; height: 60px; top: 70px; left: 70px; border-color: rgba(255,255,255,0.4); }
.ill-icon { position: absolute; top: 70px; left: 70px; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-size: 26px; color: #C5A3FF; }

.login-left h2 { font-size: 28px; font-weight: 900; margin-bottom: 12px; line-height: 1.3; }
.login-left p { font-size: 14px; color: rgba(255,255,255,0.7); line-height: 1.7; }

.login-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: var(--bg);
}

.login-card {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: var(--shadow-lg);
}

.login-header { margin-bottom: 28px; }
.login-header h1 { font-size: 24px; font-weight: 800; color: var(--text-primary); margin-bottom: 4px; }
.login-header p { font-size: 13px; color: var(--text-secondary); }

.input-with-icon { position: relative; }
.input-with-icon > i:first-child {
  position: absolute;
  left: 13px;
  top: 50%;
  transform: translateY(-50%);
  color: #aaa;
  font-size: 13px;
  pointer-events: none;
}
.input-with-icon .form-control { padding-left: 38px; }

.pw-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #aaa;
  cursor: pointer;
  padding: 4px;
}
.pw-toggle:hover { color: var(--primary); }

.btn-login {
  width: 100%;
  justify-content: center;
  padding: 12px;
  font-size: 14px;
  margin-top: 8px;
}

.login-hint {
  text-align: center;
  font-size: 11px;
  color: var(--text-secondary);
  margin-top: 14px;
  padding: 8px;
  background: var(--bg);
  border-radius: var(--radius-sm);
}

.back-link {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 20px;
  color: var(--text-secondary);
  font-size: 13px;
  text-decoration: none;
  transition: color 0.15s;
}
.back-link:hover { color: var(--primary); }

@media (max-width: 768px) {
  .login-left { display: none; }
  .login-right { padding: 20px; }
}
</style>
