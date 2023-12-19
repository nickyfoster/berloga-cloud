import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import servers from './modules/servers';
import users from './modules/users';
import alerts from './modules/alerts';

export default createStore({
  plugins: [createPersistedState()],
  modules: {
    servers,
    users,
    alerts,
  }
});
