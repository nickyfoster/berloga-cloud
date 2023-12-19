<template>
  <div v-if="server">
    <p><strong>Name:</strong> {{ server.name }}</p>
    <p><strong>Type:</strong> {{ server.type }}</p>
    <p><strong>Creator:</strong> {{ server.creator.username }}</p>

    <div v-if="user.id === server.creator.id">
      <p><router-link :to="{ name: 'EditServer', params: { id: server.id } }" class="btn btn-primary">Edit</router-link>
      </p>
      <p><button @click="removeServer()" class="btn btn-secondary">Delete</button></p>
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
