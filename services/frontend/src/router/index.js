import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue';
import RegisterView from '@/views/RegisterView.vue';
import LoginView from '@/views/LoginView.vue';
import DashboardView from '@/views/DashboardView.vue';
import ProfileView from '@/views/ProfileView.vue';
import ServerView from '@/views/ServerView.vue';
import EditServerView from '@/views/EditServerView.vue';
import store from '@/store';


const routes = [
  {
    path: '/',
    name: "Home",
    component: HomeView,
  },
  {
    path: '/register',
    name: 'Register',
    meta: { requiresAuth: true, requiresAdmin: true },
    component: RegisterView,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true },
  },
  {
    path: '/server/:id',
    name: 'Server',
    component: ServerView,
    meta: { requiresAuth: true },
    props: true,
  },
  {
    path: '/editserver/:id',
    name: 'EditServer',
    component: EditServerView,
    meta: { requiresAuth: true },
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, _, next) => {
  const isAuthenticated = store.getters.isAuthenticated;
  const isAdmin = store.getters.isAdmin;

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next('/login');
      return;
    }

    if (to.matched.some(record => record.meta.requiresAdmin) && !isAdmin) {
      next('/');
      return;
    }

    next();
  } else {
    next();
  }
});

export default router;
