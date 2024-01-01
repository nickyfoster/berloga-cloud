<template>
  <div>
    <section>
      <h1>Create server</h1>
      <hr /><br />

      <form @submit.prevent="submit">
        <div class="mb-3">
          <label for="name" class="form-label">Name:</label>
          <input type="text" name="name" v-model="form.name" class="form-control" />
        </div>
        <div class="mb-3">
          <label for="type" class="form-label">Type:</label>
          <select name="type" v-model="form.type" class="form-control">
            <option v-for="type in types" :value="type" :key="type">{{ type }}</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="image" class="form-label">Image:</label>
          <select name="image" v-model="form.image" class="form-control">
            <option v-for="image in images" :value="image" :key="image">{{ image }}</option>
          </select>
        </div>
        <div v-if="!isServerUpdating">
          <button type="submit" class="btn btn-primary">Submit</button>
        </div>
        <div v-else>
          <button class="btn btn-primary" type="button" disabled>
            <span class="spinner-border spinner-border-sm" aria-hidden="true"></span>
            <span class="visually-hidden">Submit</span>
          </button>

        </div>
      </form>
    </section>

    <br /><br />

    <section>
      <h1>Servers</h1>
      <hr /><br />

      <div v-if="servers.length">
        <div v-for="server in servers" :key="server.id" class="mb-3">
          <div class="card" style="width: 18rem;">
            <div class="card-header">
              <h5 class="card-title">{{ server.name }}</h5>
            </div>
            <ul class="list-group list-group-flush">
              <li class="list-group-item"><strong>Type:</strong> {{ server.type }}</li>
              <li class="list-group-item"><strong>Image:</strong> {{ server.image }}</li>
            </ul>
            <div class="card-body">
              <router-link :to="{ name: 'Server', params: { id: server.id } }" class="btn btn-primary">View
                Server</router-link>
            </div>
          </div>
        </div>
      </div>


      <div v-else>
        <p>Nothing to see.</p>
      </div>
    </section>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'DashboardView',
  data() {
    return {
      form: {
        name: '',
        type: null,
        image: null,
      },
    };
  },
  created: async function () {
    await this.fetchServerTypes();
    await this.fetchServerImages();
    this.setDefaultValues();
    return this.$store.dispatch('getServers');
  },
  computed: {
    ...mapGetters({
      servers: 'stateServers',
      isServerUpdating: 'isServerUpdating',
      types: 'serverTypes',
      images: 'serverImages',
    }),
  },
  methods: {
    ...mapActions([
      'createServer',
      'fetchServerTypes',
      'fetchServerImages'
    ]),
    async submit() {
      await this.createServer(this.form);
    },
    setDefaultValues() {
      if (this.types.length > 0) {
        this.form.type = this.types[0];
      }
      if (this.images.length > 0) {
        this.form.image = this.images[0];
      }
    }
  },
});
</script>
