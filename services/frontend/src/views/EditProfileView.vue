<template>
  <section>
    <h1>Edit profile</h1>
    <hr /><br />
    <form @submit.prevent="submit">
      <div class="mb-3">
        <label for="full_name" class="form-label">Full Name:</label>
        <input type="text" name="full_name" v-model="form.full_name" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password:</label>
        <input type="password" name="password" v-model="form.password" class="form-control" />
      </div>
      <div class="mb-3">
        <label for="ssh_key" class="form-label">SSH Key:</label>
        <input type="text" name="ssh_key" v-model="form.ssh_key" class="form-control" />
      </div>
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </section>
</template>

<script>
import { defineComponent } from 'vue';
import { mapGetters, mapActions } from 'vuex';

export default defineComponent({
  name: 'EditUser',
  props: ['id'],
  data() {
    return {
      form: {
        full_name: null,
        password: null,
        ssh_key: null
      }
    };
  },
  created: function () {
    this.GetUser();
  },
  computed: {
    ...mapGetters({ user: 'stateUser' }),
  },
  methods: {
    ...mapActions(['updateUser', 'viewMe']),
    async submit() {
      try {
        let user = {
          form: this.form,
          id: this.id
        };
        await this.updateUser(user);
        this.$router.push('/profile');
      } catch (error) {
        console.log(error);
      }
    },
    async GetUser() {
      try {
        await this.viewMe(); // TODO: change to viewUser in order to enable editing other users
        console.log(this.id);
        this.form.full_name = this.user.full_name;
        this.form.ssh_key = this.user.ssh_key;
      } catch (error) {
        console.error(error);
        this.$router.push('/dashboard');
      }
    }
  },
});
</script>
