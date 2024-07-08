import { createApp } from 'vue'
import { createBootstrap } from 'bootstrap-vue-next'
import App from './App.vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

import {
  initializeFaro,
  getWebInstrumentations,
} from '@grafana/faro-web-sdk';

import { TracingInstrumentation } from '@grafana/faro-web-tracing';

initializeFaro({
  url: 'http://localhost:12347/collect',
  instrumentations: [
    ...getWebInstrumentations({ captureConsole: true }),
    new TracingInstrumentation({ instrumentationOptions: { propagateTraceHeaderCorsUrls: [new RegExp('.*')] } })
  ],
  app: {
    name: 'vue-app',
    version: '1.0.0',
  },
});

const app = createApp(App)
app.use(createBootstrap())
app.mount('#app')
