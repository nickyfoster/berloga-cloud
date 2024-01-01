import axios from 'axios';

const state = {
  servers: [],
  server: null,
  isServerUpdating: false,
  serverTypes: [],
  serverImages: [],
};

const getters = {
  stateServers: state => state.servers,
  stateServer: state => state.server,
  isServerUpdating: state => state.isServerUpdating,
  serverTypes: state => state.serverTypes,
  serverImages: state => state.serverImages,
};

const actions = {
  async createServer({ commit, dispatch }, server) {
    commit('setServerUpdating', true);
    console.log(111, server)
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
      commit('setServerUpdating', false);
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
  async deleteServer({ commit }, id) {
    commit('setServerUpdating', true);
    await axios.delete(`server/${id}`);
    commit('setServerUpdating', false);
  },
  async logOut({ commit }) {
    commit('setServer', null);
    commit('setServers', []);
  },
  async fetchServerTypes({ commit }) {
    try {
      let response = await axios.get('server-types');
      if (response.data && response.data.server_types) {
        commit('setServerTypes', response.data.server_types);

      } else {
        throw new Error('Invalid server types format');
      }
    } catch (error) {
      console.error('Error fetching server types:', error);
    }
  },
  async fetchServerImages({ commit }) {
    try {
      let response = await axios.get('server-images');
      if (response.data && response.data.server_images) {
        commit('setServerImages', response.data.server_images);

      } else {
        throw new Error('Invalid server images format');
      }
    } catch (error) {
      console.error('Error fetching server images:', error);
    }
  },
};

const mutations = {
  setServers(state, servers) {
    state.servers = servers;
  },
  setServer(state, server) {
    state.server = server;
  },
  setServerUpdating(state, isUpdating) {
    state.isServerUpdating = isUpdating;
  },
  setServerTypes(state, types) {
    state.serverTypes = types;
  },
  setServerImages(state, images) {
    state.serverImages = images;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};
