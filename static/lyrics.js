// keep track of past correct guesses
const genres = document.querySelectorAll('.box');

genres.forEach(genre => {
  genre.onclick = function() {
    console.log(genre.innerText);
    genre.style.backgroundColor = 'orange';
  }
})

// **********************This works just uncomment these lines!!**********************
let lyrics = document.getElementById('line3').innerText // string of text
let blank = lyrics.replace(/[A-z]/gi, '_'); // blank string '___ _ __'
let words = lyrics.split(/\s*\b\s*/); // aray of words ['word', 'word', 'word'], split punctuation
let sauce = blank.split(/\s*\b\s*/) // blank array ['___', '__', '___']
let count = 20;
//let score = 0;
// regex v.2 = .replace(/[^\w\s]|_/g, "").replace(/\s+/g, " ")

console.log(words);
document.addEventListener('keydown', event => {
  if (event.code === 'Space') {
    event.preventDefault();

    let userInput = $('#guess').val();
  
    const matchIdx = [];

    if (words.join(' ').includes(userInput)) {
      document.getElementById('guess').style.borderBottom = '2px solid green';
    } else {
      document.getElementById('guess').style.borderBottom = '2px solid red';
    }

    words.forEach((word, idx) => {
        if (userInput === word.toLowerCase()) {
          matchIdx.push(idx);
        }
    });

    matchIdx.forEach(idx => {
      sauce[idx] = words[idx];
    });

    blank = sauce.join(' ');
    document.getElementById('ghost').innerText = blank;
    console.log(blank)
    document.getElementById('word-form').reset();
  };
});


document.addEventListener('keydown', event => {
  if (event.code === 'Enter') {
    event.preventDefault();
  }
});

// -------------Code for Timer/Score--------------------->>>>>>>>

let counter = setInterval(timer, 1000);

let ghost = document.getElementById('ghost').innerText

let score = 1000;

function timer() {

  count --;
  score -= 50;

  if (!blank.includes("_")) {
    clearInterval(counter);
    setTimeout(function () {
      alert("WINNER WINNER CHICKEN DINNER!");
    }, 200);
  };

  if (count <= 0) {
    clearInterval(counter);
    setTimeout(function() {
      alert("Times UP BUCKO!");
    }, 500);
  };
  
  document.getElementById("timer").innerHTML = count;
  document.getElementById("score").innerHTML = score;
}

// ----------Code for Score-------------------->>>>

