const state = {
  alert: {
    visible: false,
    message: '',
    type: 'info'
  }
};

const getters = {
  stateAlert: state => state.alert,
};

const actions = {
  triggerAlert({ commit }, alert) {
    commit('setAlert', alert);
    setTimeout(() => {
      commit('clearAlert');
    }, 3000); // 3 seconds
  },
  clearAlert({ commit }) {
    commit('clearAlert');
  }
};

const mutations = {
  setAlert(state, { message, type = 'info' }) {
    state.alert.message = message;
    state.alert.type = type;
    state.alert.visible = true;
  },
  clearAlert(state) {
    state.alert.visible = false;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
