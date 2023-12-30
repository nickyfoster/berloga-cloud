import 'bootstrap/dist/css/bootstrap.css';
import "bootstrap"

import { createApp } from "vue";
import axios from 'axios';

import App from './App.vue';
import router from './router';
import store from './store';

const app = createApp(App);

axios.defaults.withCredentials = true;
axios.defaults.baseURL = process.env.VUE_APP_BACKEND_URL;

axios.interceptors.response.use(response => {
  return response;
}, function (error) {
  if (error) {
    if (!error.response) {
      console.error('Network error or no response from server');
      store.dispatch('triggerAlert', {
        message: "Network error or server unresponsive",
        type: 'error'
      });
    } else {
      const originalRequest = error.config;
      if (error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;
        store.dispatch('logOut');
        router.push('/login');
        // TODO: prompt user to log in again with popup
        return Promise.reject('Unauthorized');
      } else if (error.response.status >= 500) {
        store.dispatch('triggerAlert', {
          message: "Server error",
          type: 'error'
        });
      }
    }
  }
  return Promise.reject(error);
});

app.use(router);
app.use(store);
app.mount("#app");
