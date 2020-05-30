// Load initial web page
window.onload = () => {

    // Toggle modal if there is no username in localStorage
    if (!localStorage.getItem('username')) {
        console.log("No username in local storage!");
        $('#nicknameModal').modal('toggle');
    };

    if (!localStorage.getItem('active_channel')) {

      // Load placeholder for chat
      console.log("No active channel is selected!")
      const div = document.createElement('div');
      div.className = 'empty';
      div.innerHTML = "No active channel is selected";
      document.querySelector('#content-area').append(div);
    }

    else {

      // Activate last channel from localStorage
      const active = localStorage.getItem('active_channel');
      console.log(active);

      document.querySelectorAll('.channel').forEach(channel => {

        if (channel.innerHTML === active) {
          activateChannel(channel);
        };
      });
    };


};

// Store username in localStorage
document.addEventListener('DOMContentLoaded', () => {
    document.querySelector('#nicknameForm').onsubmit = () => {
        const username = document.querySelector('#usernameInput').value;
        localStorage.setItem('username', username);
    };

// Initialize navigation for left menu
document.addEventListener('DOMContentLoaded', navigation());
});

// Push username from localStorage to header
document.querySelector('#usernameHeader').innerHTML = localStorage.getItem('username');

// Channels list navigation function
function navigation() {

    document.querySelectorAll('.channel').forEach(channel => {
        channel.onclick = () => {
          document.querySelectorAll('.channel.active').forEach(channel => {
            channel.classList.remove('active');
          });
          activateChannel(channel);
        };
    });
};

// Get messages for the channel
function fetchMessages(channel) {

    // Initialize new ajax request
    const request = new XMLHttpRequest();
    const name = document.querySelector('.channel.active').value;
    request.open('POST', '/get_messages');

    // Callback function for when request completes
    request.onload = () => {

        const data = JSON.parse(request.responseText);
        if (data.success) {

          const template = Handlebars.compile(document.querySelector('#messages').innerHTML);
          const content = template({'messages': data.messages});

          document.querySelector('#content-area').innerHTML = content;
        }
        else {
             document.querySelector('#content-area').innerHTML = data.error;
        }
    }

    // Add data to send with request
    const data = new FormData();
    data.append('channel', channel);

    // Send request
    request.send(data);
};

// Websockets
document.addEventListener('DOMContentLoaded', () => {

      // Connect to websocket
      var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

      // When connected
      socket.on('connect', () => {

          // Announce that user joined
          const user = localStorage.getItem('username');
          const greeting = document.createElement('div');
          greeting.innerHTML = `${user} is online!`;
          console.log(greeting.innerHTML);
          greeting.classList.add('system-announcement');
          // writeInChannel(greeting, handlebars=false);

          document.querySelector('#sendMessage').onsubmit = () => {

              // Prepare message data for sending
              const message = document.querySelector('#sendMessageText').value;
              const channel = document.querySelector('.channel.active').innerHTML;

              // Send data to socket
              socket.emit('send message', {'message': message, 'user': user, 'channel': channel});
              document.querySelector('#sendMessageText').value = '';
              return false;
          };

          document.querySelector('#channelCreation').onsubmit = () => {

            const channel = document.querySelector('#newChannel').value;
            socket.emit('create channel', {'channel': channel});
            document.querySelector('#newChannel').value = '';
            return false;
          };
      });

      socket.on('announce message', data => {

          // Check if message is for active channel
          if (document.querySelector('.channel.active').innerHTML === `#${data.message.channel}`) {

            // Compile Handlebars message template
            const template = Handlebars.compile(document.querySelector('#messages').innerHTML);
            const content = template({'messages': data});

            // Add new message to the channel
            writeInChannel(content);
          };
      });

      socket.on('announce channel', data => {

          // Modify channels list
          const div = document.createElement('div');
          div.className = 'channel';
          div.innerHTML = `#${data.channel}`;
          document.querySelector('#channelsList').append(div);

          // Empty the input field
          document.querySelector('#newChannel').value = '';

          // Reinitialize navigation for left menu
          document.querySelector('DOMContentLoaded', navigation());
      });

      socket.on('channel creation error', data => {

          console.error(data);
      });

      socket.on('disconnect', () => {

        // Announce that user left
        const user = localStorage.getItem('username');
        const goodbye = document.createElement('div');
        goodbye.innerHTML = `${user} gone offline!`;
        console.log(goodbye.innerHTML);
        goodbye.classList.add('system-announcement');
        // writeInChannel(goodbye, handlebars=false);
      });
});

// Submit messages on enter (textarea doesn't support by default)
function submitOnEnter(event){
    if(event.which === 13 && !event.shiftKey) {
        event.target.form.dispatchEvent(new Event("submit", {cancelable: true}));
        event.preventDefault();
    }
}

document.querySelector("#sendMessageText").addEventListener("keypress", submitOnEnter);

// Activate channel on click
function activateChannel(channel) {

    channel.classList.add('active');
    // document.querySelector('.empty').remove();
    fetchMessages(channel.innerHTML);
    document.querySelector('#sendPanel').classList.remove('hidden');
    localStorage.setItem('active_channel', channel.innerHTML);
};

function writeInChannel(content, handlebars=true) {

  // Add new message to the channel
  let empty = 'No messages in this channel';

  if (document.querySelector('#content-area').innerHTML === empty) {
    document.querySelector('#content-area').innerHTML = content;
  }
  else {
      if (handlebars) {
          document.querySelector('#content-area').innerHTML += content;
      }
      else {
          document.querySelector('#content-area').append(content);
      };
  };
};
