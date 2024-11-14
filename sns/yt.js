const fetch = require('node-fetch');
const readline = require('readline');

const API_KEY = 'AIzaSyA5xnptR7sDNMoyjXiqmZ-h5M4olcKd048';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Please enter a value: ', (answer) => {
  const CHANNEL_ID = answer;
  // console.log(`You entered: ${CHANNEL_ID}`);
  
  const url = `https://www.googleapis.com/youtube/v3/channels?part=statistics&id=${CHANNEL_ID}&key=${API_KEY}`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      if (data.items && data.items.length > 0) {
        const subscriberCount = data.items[0].statistics.subscriberCount;
        console.log(`Subscriber count: ${subscriberCount}`);
      } else {
        console.log('Channel not found or invalid API key');
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });

  rl.close(); // Close the interface after getting the input
});
