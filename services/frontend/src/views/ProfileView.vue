<template>
  <section>
    <h1>Your Profile</h1>
    <hr /><br />
    <div v-if="user">
      <p><strong>Full Name:</strong> <span>{{ user.full_name }}</span></p>
      <p><strong>Username:</strong> <span>{{ user.username }}</span></p>
      <p><strong>SSH Key:</strong> <span>{{ truncatedSshKey }}</span></p>
      <p><strong>Role:</strong> <span>{{ user.role }}</span></p>
      <p><router-link :to="{ name: 'EditUser', params: { id: this.user.id } }" class="btn btn-primary">Edit
          Account</router-link>
      </p>

      <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteConfirmationModal">
        Delete Account
      </button>

      <div class="modal fade" id="deleteConfirmationModal" tabindex="-1" role="dialog"
        aria-labelledby="deleteConfirmationModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">

            <div class="modal-header">
              <h5 class="modal-title" id="deleteConfirmationModalLabel">Delete user profile</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Are you sure you want to delete your profile?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="button" @click="deleteAccount()" class="btn btn-danger"
                data-bs-dismiss="modal">Delete</button>
            </div>
          </div>
        </div>
      </div>
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
    truncatedSshKey() {
      return this.user.ssh_key ? `${this.user.ssh_key.substring(0, 30)}...` : '';
    }
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
    },
  },
});
</script>
