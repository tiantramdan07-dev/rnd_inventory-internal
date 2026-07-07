import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const Landing = () => import('@/views/Landing.vue')
const Login = () => import('@/views/Login.vue')
const Dashboard = () => import('@/views/Dashboard.vue')
const Toolbox = () => import('@/views/Toolbox.vue')
const Peminjaman = () => import('@/views/Peminjaman.vue')
const Pengembalian = () => import('@/views/Pengembalian.vue')
const Riwayat = () => import('@/views/Riwayat.vue')
const ServiceTeknisi = () => import('@/views/ServiceTeknisi.vue')
const LaporanHarian = () => import('@/views/LaporanHarian.vue')
const UserManagement = () => import('@/views/UserManagement.vue')
const AppLayout = () => import('@/components/layout/AppLayout.vue')

const routes = [
  { path: '/', name: 'Landing', component: Landing },
  { path: '/login', name: 'Login', component: Login },
  {
    path: '/app',
    component: AppLayout,
    meta: { requiresAuth: true },
    children: [
      { path: '', redirect: '/app/dashboard' },
      { path: 'dashboard', name: 'Dashboard', component: Dashboard },
      { path: 'toolbox', name: 'Toolbox', component: Toolbox },
      { path: 'peminjaman', name: 'Peminjaman', component: Peminjaman },
      { path: 'pengembalian', name: 'Pengembalian', component: Pengembalian },
      { path: 'riwayat', name: 'Riwayat', component: Riwayat },
      {
        path: 'service',
        name: 'ServiceTeknisi',
        component: ServiceTeknisi,
        meta: { roles: ['admin', 'teknisi'] }
      },
      {
        path: 'laporan',
        name: 'LaporanHarian',
        component: LaporanHarian,
        meta: { roles: ['admin', 'teknisi'] }
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: UserManagement,
        meta: { roles: ['admin'] }
      }
    ]
  },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return next('/login')
  }

  if (to.meta.roles && !to.meta.roles.includes(auth.user?.role)) {
    return next('/app/dashboard')
  }

  if (to.name === 'Login' && auth.isLoggedIn) {
    return next('/app/dashboard')
  }

  next()
})

export default router
