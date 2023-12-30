import axios from 'axios';

const state = {
  user: null
};

const getters = {
  isAuthenticated: state => !!state.user,
  isAdmin: state => state.user && state.user.role === 'admin',
  stateUser: state => state.user,
};

const actions = {
  async register({ dispatch }, form) {
    await axios.post('register', form);
    let UserForm = new FormData();
    UserForm.append('username', form.username);
    UserForm.append('password', form.password);
    await dispatch('logIn', UserForm);
  },
  async logIn({ dispatch }, user) {
    try {
      let response = await axios.post('login', user, {
        validateStatus: () => true,
      });
      if (response) {
        if (response.status === 200) {
          await dispatch('viewMe');
        } else {
          dispatch('triggerAlert', {
            message: "Invalid credentials",
            type: 'error'
          });
        }
      } else {
        dispatch('triggerAlert', {
          message: "Auth error",
          type: 'error'
        });
      }
    } catch (error) {
      console.error(error);
    }
  },
  async viewMe({ commit }) {
    try {
      let { data } = await axios.get('users/whoami');
      await commit('setUser', data);
    } catch (error) {
      console.log(error)
    }
  },
  // eslint-disable-next-line no-empty-pattern
  async deleteUser({ }, id) {
    await axios.delete(`user/${id}`);
  },
  async logOut({ commit }) {
    commit('logout', null);
  },
  // eslint-disable-next-line no-empty-pattern
  async updateUser({ }, user) {
    await axios.patch(`user/${user.id}`, user.form);
  }
};

const mutations = {
  setUser(state, username) {
    state.user = username;
  },
  logout(state, user) {
    state.user = user;
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};
