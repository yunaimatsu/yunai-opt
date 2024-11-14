const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.question('Please enter a value: ', (answer) => {
  const userInput = answer;
  console.log(`You entered: ${userInput}`);
  rl.close(); // Close the interface after getting the input
});

