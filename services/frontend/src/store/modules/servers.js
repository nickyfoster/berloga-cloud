import axios from 'axios';

const state = {
  servers: [],
  server: null
};

const getters = {
  stateServers: state => state.servers,
  stateServer: state => state.server,
};

const actions = {
  async createServer({ dispatch }, server) {
    const response = await axios.post('servers', server);
    if (response) {
      if (response.status === 200) {
        dispatch('triggerAlert', {
          message: 'Server created successfully',
          type: 'success'
        });
      } else {
        dispatch('triggerAlert', {
          message: response.response.data.detail,
          type: 'error'
        });
      }
    }
    await dispatch('getServers');
  },
  async getServers({ commit }) {
    let { data } = await axios.get('servers');
    commit('setServers', data);
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
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
