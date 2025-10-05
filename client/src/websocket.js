let socket = null;
const listeners = new Set();

export function connectWebSocket() {
  if (socket) return;

  socket = new WebSocket("ws://localhost:8000/ws");

  socket.onopen = () => {
    console.log("WebSocket подключен");
  };

  socket.onmessage = (event) => {
    console.log("Сообщение:", event.data);
    if (event.data === "balance_done") {
      // уведомляем всех подписчиков
      listeners.forEach((cb) => cb());
    }
  };

  socket.onclose = () => {
    socket = null;
    console.log("WebSocket закрыт");
    // можно попытаться переподключиться через 5 сек
    setTimeout(connectWebSocket, 5000);
  };
}

export function onBalanceDone(callback) {
  listeners.add(callback);
  // Возвращаем функцию для отписки
  return () => listeners.delete(callback);
}
