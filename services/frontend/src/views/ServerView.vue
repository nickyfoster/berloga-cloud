<template>
  <div v-if="server" class="container my-4">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Server Details</h5>
        <ul class="list-group list-group-flush">
          <li class="list-group-item"><strong>Name:</strong> {{ server.name }}</li>
          <li class="list-group-item"><strong>Type:</strong> {{ server.type }}</li>
          <li class="list-group-item"><strong>Public IP:</strong> {{ server.public_ip }}
            <button class="btn btn-outline-secondary btn-sm" @click="copyToClipboard(server.public_ip)">Copy</button>
          </li>
          <li class="list-group-item"><strong>Status:</strong> {{ server.status }}</li>
        </ul>
      </div>
    </div>

    <div v-if="user.id === server.creator.id" class="mt-3">
      <router-link :to="{ name: 'EditServer', params: { id: server.id } }" class="btn btn-primary">Edit</router-link>
      <button type="button" class="btn btn-danger ms-2" data-bs-toggle="modal" data-bs-target="#deleteConfirmationModal">
        Delete
      </button>
    </div>

    <div class="modal fade" id="deleteConfirmationModal" tabindex="-1" aria-labelledby="deleteConfirmationModalLabel"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="deleteConfirmationModalLabel">Delete Server</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to delete this server?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" @click="removeServer" class="btn btn-danger" data-bs-dismiss="modal">Delete</button>
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
    },
    copyToClipboard(ip) {
      if (!navigator.clipboard) {
        const textarea = document.createElement('textarea');
        textarea.value = ip;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
      } else {
        navigator.clipboard.writeText(ip);
      }
    }
  },
});
</script>
