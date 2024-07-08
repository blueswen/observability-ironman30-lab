<!-- src/components/TodoForm.vue -->

<template>
  <BForm>
    <BFormGroup id="input-title-group" label="Title" label-for="input-title">
      <BFormInput id="input-title" v-model="todo.title" placeholder="Title" required />
    </BFormGroup>
    <BFormGroup id="input-description-group" label="Description" label-for="input-description">
      <BFormInput id="input-description" v-model="todo.description" placeholder="Description" required />
    </BFormGroup>
    <div class="text-center mt-3">
      <BButton class="mx-2" @click="summit" variant="primary">Add Todo</BButton>
      <BButton class="mx-2" @click="triggerBackendError" variant="danger">Trigger Backend Error</BButton>
      <BButton class="mx-2" @click="triggerFrontendError" variant="warning">Trigger Frontend Error</BButton>
      <BButton class="mx-2" @click="consoleLog" variant="info">Console Log</BButton>
    </div>
  </BForm>
</template>

<script>
import { BForm, BFormGroup, BFormInput, BButton } from 'bootstrap-vue-next';
import api from '../services/api';

export default {
  components: {
    BForm,
    BFormGroup,
    BFormInput,
    BButton
  },
  props: {
    initialTodo: {
      type: Object,
      default: () => ({ title: '', description: '', completed: false })
    },
  },
  data() {
    return {
      todo: { ...this.initialTodo }
    };
  },
  methods: {
    summit() {
      this.$emit('submit', this.todo);
      this.todo = { ...this.initialTodo };
    },
    triggerBackendError() {
      api.backendError().catch(error => {
        console.error('Backend Error:', error);
        window.alert('Backend Error');
      });
    },
    triggerFrontendError() {
      throw new Error('Triggered Error');
    },
    consoleLog() {
      const timestamp = new Date().toISOString();
      console.log(`Console Log: ${timestamp}`);
      console.error(`Console Error: ${timestamp}`);
    }
  }
};
</script>
