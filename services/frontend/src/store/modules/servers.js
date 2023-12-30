import axios from 'axios';

const state = {
  servers: [],
  server: null,
  isServerCreating: false,
};

const getters = {
  stateServers: state => state.servers,
  stateServer: state => state.server,
  isServerCreating: state => state.isServerCreating
};

const actions = {
  async createServer({ commit, dispatch }, server) {
    commit('setServerCreating');
    try {
      const response = await axios.post('servers', server);
      console.log(response);
      dispatch('triggerAlert', {
        message: 'Server created! Status: ' + response.data.status,
        type: 'success'
      });
    } catch (error) {
      dispatch('triggerAlert', {
        message: 'Error creating server: ' + (error.response?.data?.detail || error.message),
        type: 'error'
      });
    } finally {
      commit('setServerNotCreating');
    }
    await dispatch('getServers');
  },
  async getServers({ commit }) {
    try {
      let { data } = await axios.get('servers');
      commit('setServers', data);
    } catch (error) {
      console.log(error);
    }
  },
  async viewServer({ commit }, id) {
    let { data } = await axios.get(`server/${id}`);
    commit('setServer', data);
  },
  // eslint-disable-next-line no-empty-pattern
  async updateServer({ }, server) {
    await axios.patch(`server/${server.id}`, server.form);
  },
  // eslint-disable-next-line no-empty-pattern
  async deleteServer({ }, id) {
    await axios.delete(`server/${id}`);
  },
  async logOut({ commit }) {
    commit('setServer', null);
    commit('setServers', []);
  }
};

const mutations = {
  setServers(state, servers) {
    state.servers = servers;
  },
  setServer(state, server) {
    state.server = server;
  },
  setServerCreating(state) {
    state.isServerCreating = true;
  },
  setServerNotCreating(state) {
    state.isServerCreating = false;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
