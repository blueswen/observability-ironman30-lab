<!-- src/components/TodoList.vue -->

<template>
  <BContainer>
    <BRow>
      <BCol>
        <h1>Todo List</h1>
      </BCol>
    </BRow>
    <BRow class="m-3">
      <BCol>
        <TodoForm @submit="addTodo" />
      </BCol>
    </BRow>

    <BRow>
      <BCol v-for="todo in todos" :key="todo.id" md="6" lg="3">
        <TodoItem class="my-3" :todo="todo" @complete="completeTodo" @undoComplete="undoCompleteTodo"
          @delete="deleteTodo" />
      </BCol>
    </BRow>
  </BContainer>
</template>

<script>
import { BContainer, BRow, BCol } from 'bootstrap-vue-next';
import TodoForm from './TodoForm.vue';
import TodoItem from './TodoItem.vue';
import api from '../services/api';

export default {
  components: {
    TodoForm,
    TodoItem,
    BContainer,
    BRow,
    BCol
  },
  data() {
    return {
      todos: [],
      editingTodo: null
    };
  },
  methods: {
    fetchTodos() {
      api.listTodos().then(response => {
        this.todos = response.data;
      });
    },
    addTodo(newTodo) {
      api.createTodo(newTodo).then(this.fetchTodos);
    },
    completeTodo(id) {
      api.updateTodo(id, {
        completed: true
      }).then(this.fetchTodos);
      this.editingTodo = null;
    },
    undoCompleteTodo(id) {
      api.updateTodo(id, {
        completed: false
      }).then(this.fetchTodos);
      this.editingTodo = null;
    },
    deleteTodo(id) {
      api.deleteTodo(id).then(this.fetchTodos);
    }
  },
  created() {
    this.fetchTodos();
  }
};
</script>
