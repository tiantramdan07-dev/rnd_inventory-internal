import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

axios.defaults.baseURL = '/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isRnd = computed(() => user.value?.role === 'rnd' || user.value?.role === 'admin')
  const isTeknisi = computed(() => user.value?.role === 'teknisi' || user.value?.role === 'admin')

  function setAuth(t, u) {
    token.value = t
    user.value = u
    localStorage.setItem('token', t)
    localStorage.setItem('user', JSON.stringify(u))
    axios.defaults.headers.common['Authorization'] = `Bearer ${t}`
  }

  function clearAuth() {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    delete axios.defaults.headers.common['Authorization']
  }

  // Restore token on startup
  if (token.value) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }

  async function login(username, password) {
    const { data } = await axios.post('/auth/login', { username, password })
    setAuth(data.access_token, data.user)
    return data.user
  }

  function logout() {
    clearAuth()
  }

  return { token, user, isLoggedIn, isAdmin, isRnd, isTeknisi, login, logout }
})
