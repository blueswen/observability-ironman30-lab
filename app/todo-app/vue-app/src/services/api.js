// src/services/api.js

import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  listTodos(skip = 0, limit = 10) {
    return apiClient.get('/todos/', { params: { skip, limit } });
  },
  createTodo(todo) {
    console.log('Creating todo', todo);
    return apiClient.post('/todos/', todo);
  },
  readTodo(id) {
    return apiClient.get(`/todos/${id}`);
  },
  updateTodo(id, todo) {
    return apiClient.put(`/todos/${id}`, todo);
  },
  deleteTodo(id) {
    return apiClient.delete(`/todos/${id}`);
  },
  backendError() {
    return apiClient.get('/error');
  }
};
