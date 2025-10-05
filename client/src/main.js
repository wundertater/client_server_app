import { createApp } from 'vue'
import App from './App.vue'
import { connectWebSocket } from "@/websocket";

createApp(App).mount('#app')

connectWebSocket();