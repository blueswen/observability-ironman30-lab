<!-- src/components/TodoItem.vue -->

<template>
  <BCard :title="todo.title">

    <BCardText>
      <h6>
        <BBadge :variant="todo.completed ? 'success' : 'warning'">{{ todo.completed ? 'Completed' : 'Pending' }}</BBadge>
      </h6>
      {{ todo.description }}
    </BCardText>

    <div class="text-center">
      <BButton class="mx-2" @click="$emit('complete', todo.id)" variant="success" v-if="!todo.completed">Complete
      </BButton>
      <BButton class="mx-2" @click="$emit('undoComplete', todo.id)" variant="warning" v-if="todo.completed">
        Pending</BButton>
      <BButton class="mx-2" @click="$emit('delete', todo.id)" variant="danger">Delete</BButton>
    </div>
  </BCard>
</template>

<script>
import { BCard, BCardText, BButton, BBadge } from 'bootstrap-vue-next';
export default {
  components: {
    BCard,
    BCardText,
    BButton,
    BBadge
  },
  props: {
    todo: Object
  }
};
</script>
