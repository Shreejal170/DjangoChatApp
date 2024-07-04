document.addEventListener("DOMContentLoaded", function () {
  const chatForm = document.getElementById("chat_message_form");
  const inputField = chatForm.querySelector("input[name=body]");

  const chatSocket = new WebSocket(
    "ws://" + window.location.host + "/ws/chatroom/public-chat/"
  );

  chatSocket.onopen = function (e) {
    console.log("WebSocket connection established");
  };

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log("Message received: ", data);
    // Handle received message, e.g., append to chat
  };

  chatSocket.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
  };

  chatForm.addEventListener("submit", function (event) {
    event.preventDefault();
    const message = inputField.value;

    chatSocket.send(
      JSON.stringify({
        body: message,
      })
    );
    console.log("Message sent: ", message);
    inputField.value = "";
  });
});
