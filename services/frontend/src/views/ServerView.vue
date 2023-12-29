<template>
  <div v-if="server">
    <p><strong>Name:</strong> {{ server.name }}</p>
    <p><strong>Type:</strong> {{ server.type }}</p>
    <p><strong>Creator:</strong> {{ server.creator.username }}</p>

    <div v-if="user.id === server.creator.id">
      <p><router-link :to="{ name: 'EditServer', params: { id: server.id } }" class="btn btn-primary">Edit</router-link>
      </p>

      <button type="button" class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteConfirmationModal">
        Delete
      </button>

      <div class="modal fade" id="deleteConfirmationModal" tabindex="-1" role="dialog"
        aria-labelledby="deleteConfirmationModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
          <div class="modal-content">

            <div class="modal-header">
              <h5 class="modal-title" id="deleteConfirmationModalLabel">Delete server</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              Are you sure you want to delete server?
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="button" @click="removeServer()" class="btn btn-danger" data-bs-dismiss="modal">Delete</button>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>


<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'ServerView',
  props: ['id'],
  async created() {
    try {
      await this.viewServer(this.id);
    } catch (error) {
      console.error(error);
      this.$router.push('/dashboard');
    }
  },
  computed: {
    ...mapGetters({ server: 'stateServer', user: 'stateUser' }),
  },
  methods: {
    ...mapActions(['viewServer', 'deleteServer']),
    async removeServer() {
      try {
        await this.deleteServer(this.id);
        this.$router.push('/dashboard');
      } catch (error) {
        console.error(error);
      }
    }
  },
});
</script>
