// MAIN.FNT - JavaScript - Cluster h0land - Canonical Main File
// Purpose: Adds interactivity. One main.js = One Truth.

const output = document.getElementById('jsOutput');
const btn = document.getElementById('cssBtn');

let clicks = 0; // let = reassignable
const appName = 'MAIN.FNT'; // const = constant

function handleClick() {
  clicks++;
  const types = ['Number', 'String', 'Boolean', 'Object', 'Array', 'Undefined', 'Null'];
  if (clicks === 1) {
    output.textContent = `Hello World from ${appName} - Clicks: ${clicks}`;
  } else if (clicks > 1) {
    output.textContent = `Still working - Clicks: ${clicks} - Types: ${types.join(', ')}`;
  }
  console.log('Hello World', clicks);
}

btn.addEventListener('click', handleClick);
