<template>
  <section>
    <h1>Your Profile</h1>
    <hr /><br />
    <div v-if="user">
      <p><strong>Full Name:</strong> <span>{{ user.full_name }}</span></p>
      <p><strong>Username:</strong> <span>{{ user.username }}</span></p>
      <p><strong>SSH Key:</strong> <span>{{ user.ssh_key }}</span></p>
      <p><strong>Role:</strong> <span>{{ user.role }}</span></p>
      <p><button @click="deleteAccount()" class="btn btn-primary">Delete Account</button></p>
    </div>
  </section>
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'ProfileView',
  created: function () {
    return this.$store.dispatch('viewMe');
  },
  computed: {
    ...mapGetters({ user: 'stateUser' }),
  },
  methods: {
    ...mapActions(['deleteUser']),
    async deleteAccount() {
      try {
        await this.deleteUser(this.user.id);
        await this.$store.dispatch('logOut');
        this.$router.push('/');
      } catch (error) {
        console.error(error);
      }
    }
  },
});
</script>
