const BASE_URL = "http://localhost:5000"

const genres = document.querySelectorAll('.box.genre');

genres.forEach(genre => {
  const boxClass = sessionStorage.getItem(genre.id);
  if (boxClass !== null) {
    genre.className = boxClass;
  }
  genre.onclick = function() {
    sessionStorage.setItem(genre.id, 'box genre completed');
  }
  if ($('.box.genre').length === $('.box.genre.completed').length) {
    let score = localStorage.getItem("score");
    const url = "/game-over";
    //alert(`You scored: ${score} points!!`);
    /*async function getScore() {
      const endGameRes = axios.post(`${BASE_URL}/game-over`, {
        score
      });
      let myScore = endGameRes
      console.log(myScore);
    }
    getScore();*/
    $.ajax({
        url: url,
        type : "POST",
        data : {"score":score},
        success: function(data) {
          console.log(score); // this shows the localStorage score!!
            if (data.redirect) {
              console.log(score) // this shows the localStorage score!!
              score = data.score
              window.location.href = data.redirect;
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
  }
});

// **********************This works just uncomment these lines!!**********************
let lyrics = document.getElementById('line3').innerText // string of text
let blank = lyrics.replace(/[A-z]/gi, '_'); // blank string '___ _ __'
let words = lyrics.split(/\s*\b\s*/); // aray of words ['word', 'word', 'word'], split punctuation
let sauce = blank.split(/\s*\b\s*/); // blank array ['___', '__', '___']
let genresBtn = document.getElementById('genres');
// regex v.2 = .replace(/[^\w\s]|_/g, "").replace(/\s+/g, " ")
// regex v.3 = .split(/\s*\b\s*/)
document.getElementById('guess').focus();
document.getElementById('guess').select();

// compare without punctuation for guess

genresBtn.style.visibility = 'hidden';
console.log(words);
document.addEventListener('keydown', event => {
  if (event.code === 'Space') {
    event.preventDefault();

    let userInput = $('#guess').val();
  
    const matchIdx = [];

    if (words.join(' ').toLowerCase().includes(userInput)) {
      document.getElementById('guess').style.borderBottom = '2px solid green';
    } else {
      document.getElementById('guess').style.borderBottom = '2px solid red';
    }

    words.forEach((word, idx) => {
        if (userInput === word.toLowerCase()) { // check punct list word
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
let count = 20;
let score = localStorage.getItem('score') || 10000;

if (score !== null) {
  localStorage.setItem('score', '50000');
}
// let points = document.getElementById('score').innerHTML;

function timer() {

  count --;
  score -= 50;

  if (!blank.includes("_")) {
    clearInterval(counter);
    localStorage.setItem('score', $('#score').html());
    setTimeout(function () {
      genresBtn.style.visibility = 'visible';
      alert("WINNER WINNER CHICKEN DINNER!");
    }, 200);
  };

  if (count <= 0) {
    clearInterval(counter);
    localStorage.setItem('score', $('#score').html());
    setTimeout(function() {
      genresBtn.style.visibility = 'visible';
      alert("Times UP BUCKO!");
    }, 500);
  };

  document.getElementById('timer').innerHTML = count;
  document.getElementById('score').innerHTML = score;
}