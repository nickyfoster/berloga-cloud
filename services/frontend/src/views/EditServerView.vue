<template>
  <section>
    <h1>Edit server</h1>
    <hr /><br />

    <form @submit.prevent="submit">
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
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </section>
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'EditServer',
  props: ['id'],
  data() {
    return {
      form: {
        type: null,
        image: null,
      },
    };
  },
  created: async function () {
    await this.fetchServerTypes();
    await this.fetchServerImages();
    this.GetServer();
  },
  computed: {
    ...mapGetters({
      server: 'stateServer',
      types: 'serverTypes',
      images: 'serverImages',
    }),
  },
  methods: {
    ...mapActions([
      'updateServer',
      'viewServer',
      'fetchServerTypes',
      'fetchServerImages'
    ]),
    async submit() {
      try {
        let server = {
          id: this.id,
          form: this.form,
        };
        await this.updateServer(server);
        this.$router.push({ name: 'Server', params: { id: this.server.id } });
      } catch (error) {
        console.log(error);
      }
    },
    async GetServer() {
      try {
        await this.viewServer(this.id);
        this.form.type = this.server.type;
        this.form.image = this.server.image;
      } catch (error) {
        console.error(error);
        this.$router.push('/dashboard');
      }
    },
  },
});
</script>
